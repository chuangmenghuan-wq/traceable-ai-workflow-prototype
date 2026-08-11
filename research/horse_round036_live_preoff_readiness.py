from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests

OUT = Path('research_outputs/horse_round036')
OUT.mkdir(parents=True, exist_ok=True)

RACECARD = 'https://apigateway.betfair.com.au/hub/racecard?date={date}'
RACEEVENT = 'https://apigateway.betfair.com.au/hub/raceevent/{market_id}'
EXCHANGE_ENDPOINTS = [
    'https://api.betfair.com/exchange/betting/json-rpc/v1',
    'https://api.betfair.com/exchange/betting/json-rpc/v1/',
]
DATES = ['2026-08-11', '2026-08-12']
SA_TRACKS = {
    'BALAKLAVA','BORDERTOWN','CLARE','GAWLER','HALIDON','KANGAROO ISLAND',
    'MORPHETTVILLE','MORPHETTVILLE PARKS','MOUNT GAMBIER','MURRAY BRIDGE',
    'NARACOORTE','OAKBANK','PENOLA','PORT AUGUSTA','PORT LINCOLN','STRATHALBYN',
}
S = requests.Session()
S.headers.update({'User-Agent': 'FutureAbilityResearch/1.0 (paper-only read-only probe)'})


def get_json(url: str, *, timeout: int = 40) -> tuple[Any | None, dict]:
    try:
        r = S.get(url, timeout=timeout)
        qa = {'url': url, 'http_status': r.status_code, 'content_type': r.headers.get('content-type')}
        if r.status_code != 200:
            qa['body_prefix'] = r.text[:500]
            return None, qa
        try:
            return r.json(), qa
        except Exception as e:
            qa.update({'json_error': str(e), 'body_prefix': r.text[:500]})
            return None, qa
    except Exception as e:
        return None, {'url': url, 'error': repr(e)}


def canonical_market_id(v: Any) -> str:
    s = str(v or '').strip()
    if not s:
        return ''
    if s.startswith('1.'):
        return s
    if re.fullmatch(r'\d+', s):
        return '1.' + s
    return s


def parse_racecard(date: str) -> tuple[pd.DataFrame, dict]:
    j, qa = get_json(RACECARD.format(date=date))
    rows = []
    if isinstance(j, dict):
        meetings = j.get('MEETINGS') or j.get('meetings') or []
        for meet in meetings:
            venue = str(meet.get('VENUE_NAME') or meet.get('venueName') or '').strip().upper()
            country = str(meet.get('COUNTRY') or meet.get('country') or '').strip().upper()
            race_type = str(meet.get('RACE_TYPE') or meet.get('raceType') or '').strip().upper()
            markets = meet.get('MARKETS') or meet.get('markets') or []
            for m in markets:
                mid = canonical_market_id(m.get('MARKET_ID') or m.get('marketId'))
                if not mid:
                    continue
                rows.append({
                    'date': date,
                    'venue': venue,
                    'country': country,
                    'race_type': race_type,
                    'market_id': mid,
                    'race_no': m.get('RACE_NO') or m.get('raceNo'),
                    'start_time': m.get('START_TIME') or m.get('startTime'),
                    'market_status': m.get('MARKET_STATUS') or m.get('marketStatus'),
                    'event_name': m.get('EVENT_NAME') or m.get('eventName'),
                })
    d = pd.DataFrame(rows)
    qa.update({
        'parsed_markets': int(len(d)),
        'au_markets': int((d.country.eq('AUS')).sum()) if not d.empty else 0,
        'sa_markets': int((d.venue.isin(SA_TRACKS)).sum()) if not d.empty else 0,
    })
    return d, qa


def flatten_keys(x: Any, prefix: str = '') -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(x, dict):
        for k, v in x.items():
            p = f'{prefix}.{k}' if prefix else str(k)
            out.append((p, v))
            out.extend(flatten_keys(v, p))
    elif isinstance(x, list):
        for i, v in enumerate(x[:20]):
            p = f'{prefix}[{i}]'
            out.extend(flatten_keys(v, p))
    return out


def probe_raceevent(markets: pd.DataFrame) -> dict:
    # Prefer future/active SA markets, then any AU market from the latest date.
    if markets.empty:
        return {'tested': 0, 'accepted_as_exchange_price_source': False, 'reason': 'NO_RACECARD_MARKETS'}
    cand = markets.copy()
    cand['is_sa'] = cand.venue.isin(SA_TRACKS)
    cand['status_u'] = cand.market_status.astype(str).str.upper()
    cand['status_rank'] = cand.status_u.map({'OPEN': 0, 'ACTIVE': 0, 'SUSPENDED': 1, 'CLOSED': 2}).fillna(1)
    cand = cand.sort_values(['date','is_sa','status_rank'], ascending=[False,False,True])
    probes = []
    explicit_exchange_price_paths = []
    price_like_paths = []
    for row in cand.head(8).itertuples(index=False):
        j, qa = get_json(RACEEVENT.format(market_id=row.market_id))
        rec = {'market_id': row.market_id, 'venue': row.venue, 'date': row.date, **qa}
        if isinstance(j, dict):
            flat = flatten_keys(j)
            pl = []
            expl = []
            for path, value in flat:
                low = path.lower()
                if any(tok in low for tok in ['price','odds','back','lay','bsp','tote']):
                    if not isinstance(value, (dict, list)):
                        pl.append({'path': path, 'value': value})
                if ('availabletoback' in low or 'availabletolay' in low or ('exchange' in low and ('back' in low or 'lay' in low))):
                    expl.append(path)
            price_like_paths.extend(x['path'] for x in pl)
            explicit_exchange_price_paths.extend(expl)
            rec['top_level_keys'] = sorted(j.keys())
            rec['price_like_samples'] = pl[:40]
            rec['explicit_exchange_price_paths'] = sorted(set(expl))
        probes.append(rec)
    accepted = bool(explicit_exchange_price_paths)
    return {
        'tested': len(probes),
        'accepted_as_exchange_price_source': accepted,
        'explicit_exchange_price_paths': sorted(set(explicit_exchange_price_paths)),
        'price_like_paths': sorted(set(price_like_paths))[:100],
        'probes': probes,
        'governance_note': 'Raceevent is accepted only if response exposes explicit exchange back/lay ladders; generic bestPrice/tote/odds fields are not accepted as Betfair Exchange executable price.',
    }


def exchange_call(market_ids: list[str], app_key: str, session_token: str) -> dict:
    if not market_ids:
        return {'status': 'NO_MARKETS'}
    payload = {
        'jsonrpc': '2.0',
        'method': 'SportsAPING/v1.0/listMarketBook',
        'params': {
            'marketIds': market_ids[:5],
            'priceProjection': {'priceData': ['EX_BEST_OFFERS'], 'virtualise': True, 'exBestOffersOverrides': {'bestPricesDepth': 3}},
        },
        'id': 36,
    }
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    if app_key:
        headers['X-Application'] = app_key
    if session_token:
        headers['X-Authentication'] = session_token
    attempts = []
    for endpoint in EXCHANGE_ENDPOINTS:
        try:
            r = S.post(endpoint, headers=headers, json=payload, timeout=40)
            rec = {'endpoint': endpoint, 'http_status': r.status_code, 'captured_at_utc': datetime.now(timezone.utc).isoformat()}
            try:
                j = r.json()
            except Exception:
                j = None
                rec['body_prefix'] = r.text[:1000]
            rec['json'] = j
            attempts.append(rec)
            if r.status_code == 200 and isinstance(j, dict) and 'result' in j:
                result = j.get('result') or []
                books = []
                for b in result:
                    runners = []
                    for rr in b.get('runners') or []:
                        ex = rr.get('ex') or {}
                        runners.append({
                            'selection_id': rr.get('selectionId'),
                            'last_price_traded': rr.get('lastPriceTraded'),
                            'available_to_back': (ex.get('availableToBack') or [])[:3],
                            'available_to_lay': (ex.get('availableToLay') or [])[:3],
                        })
                    books.append({
                        'market_id': b.get('marketId'),
                        'status': b.get('status'),
                        'inplay': b.get('inplay'),
                        'is_market_data_delayed': b.get('isMarketDataDelayed'),
                        'publish_time': b.get('publishTime'),
                        'runners': runners,
                    })
                return {'status': 'SUCCESS', 'attempts': attempts, 'books': books}
    return {'status': 'FAILED', 'attempts': attempts}


def main() -> None:
    cards, card_qa = [], []
    for date in DATES:
        d, qa = parse_racecard(date)
        cards.append(d)
        card_qa.append(qa)
    markets = pd.concat(cards, ignore_index=True) if cards else pd.DataFrame()
    if not markets.empty:
        markets.to_csv(OUT / 'racecard_markets.csv', index=False)

    hub_probe = probe_raceevent(markets)
    (OUT / 'hub_raceevent_probe.json').write_text(json.dumps(hub_probe, indent=2, default=str), encoding='utf-8')

    app_key = os.getenv('BETFAIR_APP_KEY', '').strip()
    session = os.getenv('BETFAIR_SESSION_TOKEN', '').strip()
    secret_presence = {'BETFAIR_APP_KEY': bool(app_key), 'BETFAIR_SESSION_TOKEN': bool(session)}
    (OUT / 'secret_presence.json').write_text(json.dumps(secret_presence, indent=2), encoding='utf-8')

    # Prefer AU markets not closed; if none, use latest AU markets simply to test authenticated market-book access.
    target_ids: list[str] = []
    if not markets.empty:
        au = markets[markets.country.eq('AUS')].copy()
        active = au[~au.market_status.astype(str).str.upper().eq('CLOSED')]
        use = active if len(active) else au
        target_ids = use.sort_values(['date','start_time'], ascending=[False,True]).market_id.dropna().astype(str).drop_duplicates().head(5).tolist()

    # Always perform an unauthenticated control request; authenticated path only if secrets already exist.
    unauth = exchange_call(target_ids, '', '')
    auth = exchange_call(target_ids, app_key, session) if app_key and session else {'status': 'NOT_ATTEMPTED_MISSING_SECRETS'}
    (OUT / 'exchange_api_probe.json').write_text(json.dumps({'unauthenticated_control': unauth, 'authenticated': auth}, indent=2, default=str), encoding='utf-8')

    live_books = auth.get('books') or [] if isinstance(auth, dict) else []
    usable_lay_quotes = 0
    delayed_flags = []
    for b in live_books:
        delayed_flags.append(bool(b.get('is_market_data_delayed')))
        for rr in b.get('runners') or []:
            if rr.get('available_to_lay'):
                usable_lay_quotes += 1

    if auth.get('status') == 'SUCCESS' and usable_lay_quotes > 0:
        if delayed_flags and all(delayed_flags):
            classification = 'OFFICIAL_DELAYED_PREOFF_ADAPTER_READY_FOR_SIMULATION'
            adapter_ready = True
            realtime_ready = False
            blocker = 'REALTIME_LIVE_APP_KEY_NOT_CONFIRMED'
        else:
            classification = 'OFFICIAL_PREOFF_ADAPTER_READY'
            adapter_ready = True
            realtime_ready = True
            blocker = None
    elif hub_probe.get('accepted_as_exchange_price_source'):
        classification = 'PUBLIC_HUB_EXCHANGE_PRICE_PATH_DISCOVERED_REQUIRES_VALIDATION'
        adapter_ready = False
        realtime_ready = False
        blocker = 'PUBLIC_HUB_PRICE_SEMANTICS_NOT_YET_VALIDATED'
    elif not (app_key and session):
        classification = 'OFFICIAL_EXCHANGE_AUTH_REQUIRED'
        adapter_ready = False
        realtime_ready = False
        blocker = 'BETFAIR_APP_KEY_AND_SESSION_TOKEN_NOT_PRESENT_IN_RUNTIME'
    else:
        classification = 'OFFICIAL_EXCHANGE_AUTH_PRESENT_BUT_PRICE_PROBE_FAILED'
        adapter_ready = False
        realtime_ready = False
        blocker = 'AUTH_OR_MARKETBOOK_CALL_FAILED'

    status = {
        'round': 36,
        'capability': 'HorseRacing.LivePreOffPriceAdapterReadiness',
        'status': 'COMPLETE',
        'strategy_tuning': False,
        'real_betting_allowed': False,
        'paper_only': True,
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
        'racecard_qa': card_qa,
        'target_market_ids': target_ids,
        'runtime_secret_presence': secret_presence,
        'public_hub_raceevent': {
            'tested': hub_probe.get('tested'),
            'accepted_as_exchange_price_source': hub_probe.get('accepted_as_exchange_price_source'),
            'explicit_exchange_price_paths': hub_probe.get('explicit_exchange_price_paths'),
        },
        'exchange_api': {
            'authenticated_status': auth.get('status'),
            'market_books': len(live_books),
            'usable_runner_lay_quotes': usable_lay_quotes,
            'is_market_data_delayed_flags': delayed_flags,
        },
        'classification': classification,
        'preoff_adapter_ready': adapter_ready,
        'realtime_preoff_ready': realtime_ready,
        'remaining_blocker': blocker,
        'frozen_execution_contract': {
            'observable_price_required': True,
            'final_bsp_for_signal_forbidden': True,
            'signal': 'SA × Model Rank 2 × preoff_value < -7% → LAY',
            'gate': 'Past 50 settled candidates; strict date < race date; Trusted iff RP Brier < market Brier',
            'no_threshold_window_state_or_rank_changes': True,
        },
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2, default=str), encoding='utf-8')
    print(json.dumps(status, indent=2, default=str))


if __name__ == '__main__':
    main()
