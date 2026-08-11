from __future__ import annotations

import hashlib
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path('research_outputs/horse_round035')
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://promo.betfair.com/betfairsp/prices'
DATES = ['31072026'] + [f'{d:02d}082026' for d in range(1, 11)]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    rows = []
    recovered = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            locale='en-AU', timezone_id='Australia/Adelaide', viewport={'width': 1440, 'height': 900},
        )
        page = context.new_page()
        try:
            r = page.goto('https://promo.betfair.com/', wait_until='domcontentloaded', timeout=30000)
            base_status = r.status if r else None
        except Exception as e:
            base_status = None
            rows.append({'kind': 'BASE_NAV', 'error': str(e)[:300]})

        for ds in DATES:
            url = f'{BASE}/dwbfpricesauswin{ds}.csv'
            rec = {'date_token': ds, 'url': url, 'base_status': base_status}
            # Route A: Playwright APIRequestContext sharing browser cookies.
            try:
                rr = context.request.get(url, headers={'Referer': 'https://promo.betfair.com/'}, timeout=30000)
                body = rr.body()
                rec.update({'request_status': rr.status, 'request_bytes': len(body), 'request_ct': rr.headers.get('content-type')})
                if rr.status == 200 and body and b'BSP' in body[:1000].upper():
                    recovered[ds] = body
                    rec['route'] = 'CONTEXT_REQUEST'
            except Exception as e:
                rec['request_error'] = str(e)[:300]

            # Route B: in-page fetch from the same browser origin.
            if ds not in recovered:
                try:
                    result = page.evaluate("""async (url) => {
                        const r = await fetch(url, {credentials:'include', cache:'no-store'});
                        const text = await r.text();
                        return {status:r.status, ct:r.headers.get('content-type'), text};
                    }""", url)
                    b = result['text'].encode('utf-8', errors='replace')
                    rec.update({'fetch_status': result['status'], 'fetch_bytes': len(b), 'fetch_ct': result['ct']})
                    if result['status'] == 200 and b and b'BSP' in b[:1000].upper():
                        recovered[ds] = b
                        rec['route'] = 'PAGE_FETCH'
                except Exception as e:
                    rec['fetch_error'] = str(e)[:300]

            if ds in recovered:
                b = recovered[ds]
                rec['sha256'] = sha(b)
                rec['csv_prefix'] = b[:160].decode('utf-8', errors='replace').replace('\n', ' | ')
            rows.append(rec)
        browser.close()

    for ds, b in recovered.items():
        (OUT / f'dwbfpricesauswin{ds}.csv').write_bytes(b)

    status = {
        'round': 35,
        'capability': 'HorseRacing.SettlementLedgerRecovery',
        'phase': 'OFFICIAL_BROWSER_TRANSPORT_PROBE',
        'status': 'COMPLETE',
        'official_files_requested': len(DATES),
        'official_files_recovered': len(recovered),
        'official_transport_ready': len(recovered) > 0,
        'rows': rows,
        'next': 'PARSE_AND_REBUILD_LEDGER' if len(recovered) >= 10 else 'PROVISIONAL_MIRROR_FALLBACK',
    }
    (OUT / 'browser_probe.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
