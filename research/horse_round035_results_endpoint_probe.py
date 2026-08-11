from __future__ import annotations

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path('research_outputs/horse_round035')
OUT.mkdir(parents=True, exist_ok=True)
URL = 'https://www.betfair.com.au/hub/racing/horse-racing/racing-results/'


def main():
    events=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        ctx=browser.new_context(locale='en-AU', timezone_id='Australia/Adelaide')
        page=ctx.new_page()
        def on_response(resp):
            u=resp.url
            low=u.lower()
            if any(k in low for k in ['result','racing','race','api','json','graphql','hub']):
                rec={'url':u,'status':resp.status,'ct':resp.headers.get('content-type')}
                ct=(resp.headers.get('content-type') or '').lower()
                if ('json' in ct or 'text' in ct) and resp.status==200:
                    try:
                        txt=resp.text()
                        if len(txt)<200000:
                            rec['body_prefix']=txt[:2000]
                    except Exception as e:
                        rec['body_error']=str(e)[:200]
                events.append(rec)
        page.on('response', on_response)
        nav=None
        try:
            r=page.goto(URL, wait_until='domcontentloaded', timeout=60000)
            nav=r.status if r else None
            page.wait_for_timeout(12000)
        except Exception as e:
            nav_error=str(e)
        else:
            nav_error=None
        title=page.title()
        body=page.locator('body').inner_text(timeout=10000)[:20000]
        scripts=page.locator('script').evaluate_all("els => els.map(e => e.src || e.textContent.slice(0,500)).filter(Boolean)")
        browser.close()
    # de-dup responses by URL/status
    uniq=[]; seen=set()
    for e in events:
        k=(e['url'],e['status'])
        if k not in seen:
            seen.add(k); uniq.append(e)
    out={'round':35,'phase':'BETFAIR_RESULTS_ENDPOINT_DISCOVERY','page_status':nav,'page_error':nav_error,'title':title,'response_count':len(uniq),'responses':uniq,'body_prefix':body,'scripts':scripts[:100]}
    (OUT/'results_endpoint_probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'page_status':nav,'response_count':len(uniq),'interesting_urls':[e['url'] for e in uniq if any(k in e['url'].lower() for k in ['api','result','json','graphql'])][:30]},indent=2))

if __name__=='__main__': main()
