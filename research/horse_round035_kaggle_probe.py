from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import quote

import requests

OUT = Path('research_outputs/horse_round035')
OUT.mkdir(parents=True, exist_ok=True)
DATASET = 'eonsky/betfair-sp'
VIEW_URL = f'https://www.kaggle.com/api/v1/datasets/view/{DATASET}'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


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
    out['metadata_keys'] = sorted(meta.keys())
    out['version_number'] = meta.get('currentVersionNumber') or meta.get('versionNumber')
    files = meta.get('files') or meta.get('datasetFiles') or []
    normalized = []
    for f in files:
        name = f.get('name') or f.get('ref') or f.get('fileName')
        if name:
            normalized.append({'name': name, 'size': f.get('totalBytes') or f.get('size'), 'raw': f})
    targets = [x for x in normalized if 'dwbfpricesauswin' in x['name'].lower() and ('2026' in x['name'] or '082026' in x['name'])]
    out['file_count_metadata'] = len(normalized)
    out['target_count_metadata'] = len(targets)
    out['target_examples'] = [{k:v for k,v in x.items() if k != 'raw'} for x in targets[:20]]

    # If the metadata endpoint is paginated/summary-only, also query the file-list endpoint.
    if not targets:
        list_urls = [
            f'https://www.kaggle.com/api/v1/datasets/list/{DATASET}',
            f'https://www.kaggle.com/api/i/datasets.ListFiles?ownerSlug=eonsky&datasetSlug=betfair-sp&pageSize=200',
        ]
        out['list_probes'] = []
        for u in list_urls:
            rr = s.get(u, timeout=60)
            rec = {'url': u, 'status': rr.status_code, 'bytes': len(rr.content), 'ct': rr.headers.get('content-type')}
            if rr.status_code == 200 and 'json' in (rr.headers.get('content-type') or '').lower():
                try:
                    j = rr.json(); rec['keys'] = sorted(j.keys()) if isinstance(j, dict) else None
                except Exception as e:
                    rec['json_error'] = str(e)
            out['list_probes'].append(rec)

    download_results = []
    for x in targets[:5]:
        name = x['name']
        # Official Kaggle API supports a specific file path after owner/dataset.
        url = f'https://www.kaggle.com/api/v1/datasets/download/eonsky/betfair-sp/{quote(name, safe="")}'
        if out.get('version_number'):
            url += f'?datasetVersionNumber={out["version_number"]}'
        rr = s.get(url, timeout=120, allow_redirects=True)
        rec = {'name': name, 'url': url, 'status': rr.status_code, 'bytes': len(rr.content), 'ct': rr.headers.get('content-type')}
        if rr.status_code == 200 and len(rr.content) > 100:
            rec['sha256'] = sha(rr.content)
            rec['prefix'] = rr.content[:120].decode('utf-8', errors='replace').replace('\n',' | ')
            # Save only a small number of targeted source files, never the full 4.6GB dataset.
            safe_name = Path(name).name
            (OUT / f'mirror_{safe_name}').write_bytes(rr.content)
        download_results.append(rec)
    out['download_results'] = download_results
    out['classification'] = 'PROVISIONAL_MIRROR_FILE_READY' if any(x['status']==200 and x['bytes']>100 for x in download_results) else 'PROVISIONAL_MIRROR_NOT_YET_READY'
    (OUT/'kaggle_probe.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
