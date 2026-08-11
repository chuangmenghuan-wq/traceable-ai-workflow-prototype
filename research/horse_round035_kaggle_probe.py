from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import quote

import requests

OUT = Path('research_outputs/horse_round035')
OUT.mkdir(parents=True, exist_ok=True)
DATASET = 'eonsky/betfair-sp'
VIEW_URL = f'https://www.kaggle.com/api/v1/datasets/view/{DATASET}'
LIST_URL = f'https://www.kaggle.com/api/v1/datasets/list/{DATASET}'
DATE_TOKENS = ['31072026'] + [f'{d:02d}082026' for d in range(1, 11)]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm_file(f: dict) -> dict | None:
    name = f.get('name') or f.get('ref') or f.get('fileName') or f.get('path')
    if not name:
        return None
    return {
        'name': str(name),
        'size': f.get('totalBytes') or f.get('size') or f.get('bytes'),
        'creationDate': f.get('creationDate') or f.get('dateCreated'),
    }


def main() -> None:
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    r = s.get(VIEW_URL, timeout=60)
    out = {
        'round': 35,
        'phase': 'PROVISIONAL_MIRROR_PROBE',
        'dataset': DATASET,
        'metadata_status': r.status_code,
        'metadata_content_type': r.headers.get('content-type'),
        'metadata_bytes': len(r.content),
    }
    if r.status_code != 200:
        out['classification'] = 'KAGGLE_METADATA_UNAVAILABLE'
        (OUT/'kaggle_probe.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
        print(json.dumps(out, indent=2))
        return

    meta = r.json()
    out['version_number'] = meta.get('currentVersionNumber') or meta.get('versionNumber')
    out['dataset_last_updated'] = meta.get('lastUpdated')
    out['dataset_total_bytes'] = meta.get('totalBytes')

    # Paginate the public file-list endpoint. Kaggle documents max page-size 200.
    all_files: list[dict] = []
    page_token = None
    page_qa = []
    for page_idx in range(1, 31):
        params = {'pageSize': 200}
        if page_token:
            params['pageToken'] = page_token
        rr = s.get(LIST_URL, params=params, timeout=60)
        rec = {'page': page_idx, 'status': rr.status_code, 'bytes': len(rr.content), 'url': rr.url}
        if rr.status_code != 200:
            page_qa.append(rec)
            break
        j = rr.json()
        files = j.get('datasetFiles') or j.get('files') or []
        rec['file_count'] = len(files)
        for f in files:
            z = norm_file(f)
            if z:
                all_files.append(z)
        next_token = j.get('nextPageToken') or j.get('next_page_token')
        rec['has_next'] = bool(next_token)
        rec['next_token_prefix'] = str(next_token)[:24] if next_token else None
        page_qa.append(rec)
        page_token = next_token
        if not page_token:
            break

    out['page_qa'] = page_qa
    out['file_count_listed'] = len(all_files)
    # Exact daily AUS Win targets. Names may include nested folders.
    targets = []
    for f in all_files:
        low = f['name'].lower()
        if 'dwbfpricesauswin' in low and any(tok in low for tok in DATE_TOKENS):
            targets.append(f)
    # De-duplicate by name and retain deterministic order.
    targets = list({x['name']: x for x in targets}.values())
    targets.sort(key=lambda x: x['name'])
    out['target_count'] = len(targets)
    out['targets'] = targets

    download_results = []
    for x in targets:
        name = x['name']
        # First try the public single-file REST path.
        url = f'https://www.kaggle.com/api/v1/datasets/download/eonsky/betfair-sp/{quote(name, safe="")}'
        if out.get('version_number'):
            url += f'?datasetVersionNumber={out["version_number"]}'
        rr = s.get(url, timeout=120, allow_redirects=True)
        rec = {'name': name, 'rest_url': url, 'rest_status': rr.status_code, 'rest_bytes': len(rr.content), 'rest_ct': rr.headers.get('content-type')}
        good = rr.status_code == 200 and len(rr.content) > 100
        if good:
            rec['rest_sha256'] = sha(rr.content)
            rec['rest_prefix'] = rr.content[:120].decode('utf-8', errors='replace').replace('\n',' | ')
            safe_name = Path(name).name
            (OUT / f'mirror_rest_{safe_name}').write_bytes(rr.content)
        else:
            # Official Kaggle CLI documents unauthenticated public dataset file downloads.
            cmd = ['kaggle', 'datasets', 'download', DATASET, '-f', name, '-p', str(OUT), '-o', '-q']
            cp = subprocess.run(cmd, text=True, capture_output=True, timeout=180)
            rec['cli_rc'] = cp.returncode
            rec['cli_stdout'] = cp.stdout[-500:]
            rec['cli_stderr'] = cp.stderr[-500:]
            # Kaggle CLI normally writes <basename>.zip for individual dataset files.
            candidates = [OUT / (Path(name).name + '.zip'), OUT / Path(name).name]
            for p in candidates:
                if p.exists() and p.stat().st_size > 100:
                    b = p.read_bytes()
                    rec['cli_output'] = p.name
                    rec['cli_bytes'] = len(b)
                    rec['cli_sha256'] = sha(b)
                    good = True
                    break
        rec['ready'] = bool(good)
        download_results.append(rec)

    out['download_results'] = download_results
    ready = [x for x in download_results if x.get('ready')]
    out['ready_count'] = len(ready)
    out['classification'] = 'PROVISIONAL_MIRROR_FILES_READY' if len(ready) >= 10 else 'PROVISIONAL_MIRROR_NOT_YET_READY'
    (OUT/'kaggle_probe.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
