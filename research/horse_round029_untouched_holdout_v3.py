import requests
import horse_round029_untouched_holdout as base


def browser_get_bytes(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150.0 Safari/537.36",
        "Accept": "text/csv,text/plain;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-AU,en;q=0.9",
        "Referer": "https://promo.betfair.com/betfairsp/prices/",
        "Cache-Control": "no-cache",
    }
    r = requests.get(url, headers=headers, timeout=(20, 120), allow_redirects=True)
    return r.status_code, r.content, r.headers.get("content-type", "")


base.get_bytes = browser_get_bytes
base.main()
