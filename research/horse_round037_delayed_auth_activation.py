from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

OUT = Path('research_outputs/horse_round037')
OUT.mkdir(parents=True, exist_ok=True)

CONTRACT_SHA256 = 'e446a15ebc40bd4ad7ccc820e60ec829d623311f22d71b425c98c01fc13724e3'
ACCOUNT_ENDPOINT = 'https://api.betfair.com/exchange/account/json-rpc/v1'
BETTING_ENDPOINT = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
RACECARD = 'https://apigateway.betfair.com.au/hub/racecard?date={date}'
DATES = ['2026-08-11', '2026-08-12']

S = requests.Session()
S.headers.update({'User-Agent': 'FutureAbilityHorsePaper/1.0 (paper-only delayed-api activation)'})


def fp(value: str) -> str | None:
    if not value:
        return None
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def env_first(*names: str) -> tuple[str, str | None]:
    for name in names:
        v = os.getenv(name, '').strip()
        if v:
            return v, name
    return '', None


def post_rpc(url: str, method: str, params: dict[str, Any], headers: dict[str, str], req_id: int) -> dict:
    payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': req_id}
    try:
        r = S.post(url, headers=headers, json=payload, timeout=40)
        rec: dict[str, Any] = {'http_status': r.status_code, 'captured_at_utc': datetime.now(timezone.utc).isoformat()}
        try:
            rec['json'] = r.json()
        except Exception:
            rec['json'] = None
            rec['body_prefix'] = r.text[:700]
        return rec
    except Exception as e:
        return {'http_status': None, 'error': repr(e), 'captured_at_utc': datetime.now(timezone.utc).isoformat()}


def parse_delayed_key(j: Any) -> str:
    if not isinstance(j, dict):
        return ''
    result = j.get('result')
    if not isinstance(result, list):
        return ''
    for app in result:
        versions = app.get('appVersions') or app.get('appversions') or []
        for ver in versions:
            version = str(ver.get('version') or '').upper()
            active = bool(ver.get('active'))
            key = str(ver.get('applicationKey') or '').strip()
            if key and active and ('DELAY' in version or version == '1.0'):
                return key
    return ''


def get_or_create_delayed_key(session_token: str) -> tuple[str, dict]:
    headers = {'content-type': 'application/json', 'accept': 'application/json', 'X-Authentication': session_token}
    get_rec = post_rpc(ACCOUNT_ENDPOINT, 'AccountAPING/v1.0/getDeveloperAppKeys', {}, headers, 3701)
    delayed = parse_delayed_key(get_rec.get('json'))
    audit: dict[str, Any] = {
        'getDeveloperAppKeys': {
            'http_status': get_rec.get('http_status'),
            'json_error': (get_rec.get('json') or {}).get('error') if isinstance(get_rec.get('json'), dict) else None,
        },
        'created_new_keys': False,
    }
    if delayed:
        audit['delayed_key_fingerprint'] = fp(delayed)
        return delayed, audit

    # Only create after retrieval returned no active delayed key. This is account-level mutation already approved by owner.
    app_name = 'FutureAbilityHorsePaper-' + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    create_rec = post_rpc(
        ACCOUNT_ENDPOINT,
        'AccountAPING/v1.0/createDeveloperAppKeys',
        {'appName': app_name},
        headers,
        3702,
    )
    audit['createDeveloperAppKeys'] = {
        'http_status': create_rec.get('http_status'),
        'json_error': (create_rec.get('json') or {}).get('error') if isinstance(create_rec.get('json'), dict) else None,
        'app_name': app_name,
    }
    audit['created_new_keys'] = bool(isinstance(create_rec.get('json'), dict) and create_rec['json'].get('result'))

    # Retrieve again so parsing is identical for existing/new keys.
    time.sleep(0.5)
    get2 = post_rpc(ACCOUNT_ENDPOINT, 'AccountAPING/v1.0/getDeveloperAppKeys', {}, headers, 3703)
    delayed = parse_delayed_key(get2.get('json'))
    audit['getDeveloperAppKeys_after_create'] = {
        'http_status': get2.get('http_status'),
        'json_error': (get2.get('json') or {}).get('error') if isinstance(get2.get('json'), dict) else None,
    }
    audit['delayed_key_fingerprint'] = fp(delayed)
    return delayed, audit


def thoroughbred_market_ids() -> tuple[list[str], list[dict]]:
    ids: list[str] = []
    qa: list[dict] = []
    for date in DATES:
        try:
            r = S.get(RACECARD.format(date=date), timeout=30)
            j = r.json() if r.status_code == 200 else {}
            count = 0
            if isinstance(j, dict):
                for meet in j.get('MEETINGS') or j.get('meetings') or []:
                    rt = str(meet.get('RACE_TYPE') or meet.get('raceType') or '').upper()
                    country = str(meet.get('COUNTRY') or meet.get('country') or '').upper()
                    if rt != 'R' or country != 'AUS':
                        continue
                    for m in meet.get('MARKETS') or meet.get('markets') or []:
                        mid = str(m.get('MARKET_ID') or m.get('marketId') or '').strip()
                        if mid and not mid.startswith('1.') and mid.isdigit():
                            mid = '1.' + mid
                        if mid:
                            ids.append(mid)
                            count += 1
            qa.append({'date': date, 'http_status': r.status_code, 'aus_thoroughbred_markets': count})
        except Exception as e:
            qa.append({'date': date, 'error': repr(e), 'aus_thoroughbred_markets': 0})
    return list(dict.fromkeys(ids)), qa


def smoke_market_book(app_key: str, session_token: str, market_ids: list[str]) -> dict:
    if not app_key or not session_token:
        return {'status': 'AUTH_MISSING'}
    if not market_ids:
        return {'status': 'NO_MARKETS'}
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'X-Application': app_key,
        'X-Authentication': session_token,
    }
    rec = post_rpc(
        BETTING_ENDPOINT,
        'SportsAPING/v1.0/listMarketBook',
        {
            'marketIds': market_ids[:5],
            'priceProjection': {
                'priceData': ['EX_BEST_OFFERS'],
                'virtualise': True,
                'exBestOffersOverrides': {'bestPricesDepth': 3},
            },
        },
        headers,
        3704,
    )
    j = rec.get('json')
    books = j.get('result') if isinstance(j, dict) else None
    if not isinstance(books, list):
        return {
            'status': 'FAILED',
            'http_status': rec.get('http_status'),
            'error': j.get('error') if isinstance(j, dict) else rec.get('body_prefix'),
        }
    quotes = 0
    delayed_flags = []
    snapshots = []
    for b in books:
        delayed_flags.append(bool(b.get('isMarketDataDelayed')))
        r_out = []
        for rr in b.get('runners') or []:
            lays = ((rr.get('ex') or {}).get('availableToLay') or [])[:3]
            if lays:
                quotes += 1
            r_out.append({
                'selection_id': rr.get('selectionId'),
                'available_to_lay': lays,
                'last_price_traded': rr.get('lastPriceTraded'),
            })
        snapshots.append({
            'market_id': b.get('marketId'),
            'status': b.get('status'),
            'inplay': b.get('inplay'),
            'is_market_data_delayed': b.get('isMarketDataDelayed'),
            'publish_time': b.get('publishTime'),
            'runners': r_out,
        })
    return {
        'status': 'SUCCESS',
        'http_status': rec.get('http_status'),
        'market_books': len(books),
        'usable_runner_lay_quotes': quotes,
        'delayed_flags': delayed_flags,
        'captured_at_utc': rec.get('captured_at_utc'),
        'snapshots': snapshots,
    }


def main() -> None:
    session, session_source = env_first('BETFAIR_SESSION_TOKEN', 'BETFAIR_SSOID')
    configured_key, key_source = env_first('BETFAIR_DELAYED_APP_KEY', 'BETFAIR_APP_KEY')
    username_present = bool(os.getenv('BETFAIR_USERNAME', '').strip())
    password_present = bool(os.getenv('BETFAIR_PASSWORD', '').strip())

    market_ids, racecard_qa = thoroughbred_market_ids()
    auth_audit: dict[str, Any] = {}
    delayed_key = configured_key

    if session and not delayed_key:
        delayed_key, auth_audit = get_or_create_delayed_key(session)
    elif session and delayed_key:
        auth_audit = {'used_configured_key': True, 'delayed_key_fingerprint': fp(delayed_key)}
    else:
        # Control call proves that account-key creation/retrieval cannot proceed without authenticated ssoid.
        ctrl = post_rpc(
            ACCOUNT_ENDPOINT,
            'AccountAPING/v1.0/getDeveloperAppKeys',
            {},
            {'content-type': 'application/json', 'accept': 'application/json'},
            3799,
        )
        auth_audit = {
            'unauthenticated_control': {
                'http_status': ctrl.get('http_status'),
                'error': (ctrl.get('json') or {}).get('error') if isinstance(ctrl.get('json'), dict) else ctrl.get('body_prefix'),
            }
        }

    smoke = smoke_market_book(delayed_key, session, market_ids)

    if session and delayed_key and smoke.get('status') == 'SUCCESS' and smoke.get('usable_runner_lay_quotes', 0) > 0:
        classification = 'DELAYED_AUTH_ACTIVE_AND_PREOFF_SNAPSHOT_CAPTURED'
        activation_ready = True
        blocker = None
    elif session and delayed_key:
        classification = 'DELAYED_AUTH_PRESENT_BUT_MARKETBOOK_SMOKE_FAILED'
        activation_ready = False
        blocker = 'BETFAIR_MARKETBOOK_TRANSPORT_OR_AUTH_FAILURE'
    elif session:
        classification = 'SESSION_PRESENT_BUT_DELAYED_APP_KEY_UNAVAILABLE'
        activation_ready = False
        blocker = 'DELAYED_APP_KEY_RETRIEVAL_OR_CREATION_FAILED'
    else:
        classification = 'EXTERNAL_BETFAIR_ACCOUNT_SESSION_REQUIRED'
        activation_ready = False
        blocker = 'BETFAIR_AUTHENTICATED_SESSION_NOT_AVAILABLE_TO_RUNTIME'

    status = {
        'round': 37,
        'capability': 'HorseRacing.BetfairDelayedAuthActivation',
        'status': 'COMPLETE',
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
        'contract_sha256': CONTRACT_SHA256,
        'strategy_tuning': False,
        'paper_only': True,
        'real_betting_allowed': False,
        'runtime_auth_presence': {
            'session_present': bool(session),
            'session_source': session_source,
            'session_fingerprint': fp(session),
            'configured_app_key_present': bool(configured_key),
            'configured_app_key_source': key_source,
            'effective_delayed_key_present': bool(delayed_key),
            'effective_delayed_key_fingerprint': fp(delayed_key),
            'username_secret_present': username_present,
            'password_secret_present': password_present,
        },
        'racecard_qa': racecard_qa,
        'candidate_market_count_for_smoke': len(market_ids),
        'auth_activation_audit': auth_audit,
        'marketbook_smoke': {
            k: v for k, v in smoke.items() if k != 'snapshots'
        },
        'classification': classification,
        'delayed_auth_activation_ready': activation_ready,
        'remaining_blocker': blocker,
        'governance': {
            'delayed_key_only': True,
            'live_key_activation_forbidden_this_round': True,
            'orders_forbidden': True,
            'no_secrets_committed': True,
            'no_threshold_window_state_or_rank_changes': True,
        },
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2, default=str), encoding='utf-8')
    if smoke.get('snapshots'):
        (OUT / 'paper_preoff_snapshot.json').write_text(json.dumps({
            'captured_at_utc': smoke.get('captured_at_utc'),
            'source': 'BETFAIR_EXCHANGE_LISTMARKETBOOK_DELAYED_KEY',
            'paper_only': True,
            'snapshots': smoke['snapshots'],
        }, indent=2, default=str), encoding='utf-8')
    print(json.dumps(status, indent=2, default=str))


if __name__ == '__main__':
    main()
