from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

OUT = Path('research_outputs/horse_round039')
SNAP = OUT / 'snapshots'
OUT.mkdir(parents=True, exist_ok=True)
SNAP.mkdir(parents=True, exist_ok=True)

CONTRACT_SHA256 = 'e446a15ebc40bd4ad7ccc820e60ec829d623311f22d71b425c98c01fc13724e3'
CERTLOGIN = 'https://identitysso-cert.betfair.com/api/certlogin'
KEEPALIVE = 'https://identitysso.betfair.com/api/keepAlive'
BETTING = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
RACECARD = 'https://apigateway.betfair.com.au/hub/racecard?date={date}'
SA_TRACKS = {
    'BALAKLAVA','BORDERTOWN','CLARE','GAWLER','HALIDON','KANGAROO ISLAND',
    'MORPHETTVILLE','MORPHETTVILLE PARKS','MOUNT GAMBIER','MURRAY BRIDGE',
    'NARACOORTE','OAKBANK','PENOLA','PORT AUGUSTA','PORT LINCOLN','STRATHALBYN',
}
S = requests.Session()
S.headers.update({'User-Agent': 'FutureAbilityHorsePaper/1.0 (paper-only certificate runtime)'})


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fp(s: str) -> str | None:
    return hashlib.sha256(s.encode()).hexdigest()[:16] if s else None


def safe_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False, default=str)


def write_private_temp(content: str, suffix: str) -> str:
    f = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False, encoding='utf-8')
    try:
        f.write(content)
        f.flush()
        os.fchmod(f.fileno(), stat.S_IRUSR | stat.S_IWUSR)
        return f.name
    finally:
        f.close()


def cert_login(username: str, password: str, app_key: str, cert_pem: str, key_pem: str) -> dict:
    cert_path = key_path = ''
    try:
        cert_path = write_private_temp(cert_pem, '.crt')
        key_path = write_private_temp(key_pem, '.key')
        r = S.post(
            CERTLOGIN,
            headers={'X-Application': app_key, 'Accept': 'application/json'},
            data={'username': username, 'password': password},
            cert=(cert_path, key_path),
            timeout=40,
        )
        try:
            j = r.json()
        except Exception:
            j = None
        token = str((j or {}).get('sessionToken') or '') if isinstance(j, dict) else ''
        return {
            'ok': r.status_code == 200 and isinstance(j, dict) and j.get('loginStatus') == 'SUCCESS' and bool(token),
            'http_status': r.status_code,
            'login_status': (j or {}).get('loginStatus') if isinstance(j, dict) else None,
            'session_token': token,
            'session_fingerprint': fp(token),
            'captured_at_utc': now(),
            'body_prefix': None if isinstance(j, dict) else r.text[:500],
        }
    except Exception as e:
        return {'ok': False, 'error': repr(e), 'captured_at_utc': now(), 'session_token': ''}
    finally:
        for p in (cert_path, key_path):
            if p:
                try: os.remove(p)
                except OSError: pass


def keep_alive(app_key: str, token: str) -> dict:
    if not app_key or not token:
        return {'ok': False, 'status': 'AUTH_MISSING'}
    try:
        r = S.post(KEEPALIVE, headers={
            'X-Application': app_key,
            'X-Authentication': token,
            'Accept': 'application/json',
        }, timeout=30)
        try: j = r.json()
        except Exception: j = None
        new_token = str((j or {}).get('token') or token) if isinstance(j, dict) else token
        return {
            'ok': r.status_code == 200 and isinstance(j, dict) and str(j.get('status')).upper() == 'SUCCESS',
            'http_status': r.status_code,
            'status': (j or {}).get('status') if isinstance(j, dict) else None,
            'token': new_token,
            'token_fingerprint': fp(new_token),
            'captured_at_utc': now(),
        }
    except Exception as e:
        return {'ok': False, 'error': repr(e), 'captured_at_utc': now()}


def racecard(date: str) -> tuple[list[dict], dict]:
    try:
        r = S.get(RACECARD.format(date=date), timeout=30)
        j = r.json() if r.status_code == 200 else {}
    except Exception as e:
        return [], {'date': date, 'error': repr(e)}
    rows = []
    if isinstance(j, dict):
        for meet in j.get('MEETINGS') or j.get('meetings') or []:
            rt = str(meet.get('RACE_TYPE') or meet.get('raceType') or '').upper()
            country = str(meet.get('COUNTRY') or meet.get('country') or '').upper()
            venue = str(meet.get('VENUE_NAME') or meet.get('venueName') or '').strip().upper()
            if rt != 'R' or country != 'AUS':
                continue
            for m in meet.get('MARKETS') or meet.get('markets') or []:
                mid = str(m.get('MARKET_ID') or m.get('marketId') or '').strip()
                if mid and not mid.startswith('1.') and mid.isdigit(): mid = '1.' + mid
                if not mid: continue
                rows.append({
                    'date': date, 'venue': venue, 'market_id': mid,
                    'race_no': m.get('RACE_NO') or m.get('raceNo'),
                    'start_time': m.get('START_TIME') or m.get('startTime'),
                    'market_status': str(m.get('MARKET_STATUS') or m.get('marketStatus') or '').upper(),
                    'is_sa': venue in SA_TRACKS,
                })
    return rows, {
        'date': date, 'http_status': r.status_code,
        'aus_thoroughbred_markets': len(rows),
        'sa_thoroughbred_markets': sum(1 for x in rows if x['is_sa']),
    }


def list_market_book(app_key: str, token: str, market_ids: list[str]) -> dict:
    if not app_key or not token: return {'ok': False, 'status': 'AUTH_MISSING', 'books': []}
    if not market_ids: return {'ok': True, 'status': 'NO_TARGET_MARKETS', 'books': []}
    payload = {
        'jsonrpc':'2.0','method':'SportsAPING/v1.0/listMarketBook','id':3901,
        'params':{
            'marketIds':market_ids[:40],
            'priceProjection':{'priceData':['EX_BEST_OFFERS'],'virtualise':True,'exBestOffersOverrides':{'bestPricesDepth':3}},
        },
    }
    try:
        r = S.post(BETTING, headers={
            'content-type':'application/json','accept':'application/json',
            'X-Application':app_key,'X-Authentication':token,
        }, json=payload, timeout=40)
        try: j = r.json()
        except Exception: j = None
        books = j.get('result') if isinstance(j, dict) else None
        if not isinstance(books, list):
            return {'ok':False,'status':'FAILED','http_status':r.status_code,'error':(j or {}).get('error') if isinstance(j,dict) else r.text[:500],'books':[]}
        clean=[]; quotes=0; delayed=[]
        for b in books:
            delayed.append(bool(b.get('isMarketDataDelayed')))
            runners=[]
            for rr in b.get('runners') or []:
                ex=rr.get('ex') or {}; lays=(ex.get('availableToLay') or [])[:3]; backs=(ex.get('availableToBack') or [])[:3]
                if lays: quotes += 1
                runners.append({'selection_id':rr.get('selectionId'),'status':rr.get('status'),'last_price_traded':rr.get('lastPriceTraded'),'available_to_lay':lays,'available_to_back':backs})
            clean.append({'market_id':b.get('marketId'),'status':b.get('status'),'inplay':b.get('inplay'),'is_market_data_delayed':b.get('isMarketDataDelayed'),'publish_time':b.get('publishTime'),'runners':runners})
        return {'ok':True,'status':'SUCCESS','http_status':r.status_code,'books':clean,'usable_runner_lay_quotes':quotes,'delayed_flags':delayed,'captured_at_utc':now()}
    except Exception as e:
        return {'ok':False,'status':'FAILED','error':repr(e),'books':[],'captured_at_utc':now()}


def main() -> None:
    username=os.getenv('BETFAIR_USERNAME','').strip(); password=os.getenv('BETFAIR_PASSWORD','').strip()
    app_key=(os.getenv('BETFAIR_DELAYED_APP_KEY','').strip() or os.getenv('BETFAIR_APP_KEY','').strip())
    cert_pem=os.getenv('BETFAIR_CERT_PEM','').strip(); key_pem=os.getenv('BETFAIR_CERT_KEY_PEM','').strip()
    existing=(os.getenv('BETFAIR_SESSION_TOKEN','').strip() or os.getenv('BETFAIR_SSOID','').strip())
    secrets={'username':bool(username),'password':bool(password),'app_key':bool(app_key),'cert':bool(cert_pem),'cert_key':bool(key_pem),'existing_session':bool(existing)}

    auth_mode='NONE'; token=''; keepalive_result=None; login_result=None
    if existing and app_key:
        keepalive_result=keep_alive(app_key,existing)
        if keepalive_result.get('ok'):
            token=str(keepalive_result.get('token') or existing); auth_mode='KEEPALIVE'
    if not token and all([username,password,app_key,cert_pem,key_pem]):
        login_result=cert_login(username,password,app_key,cert_pem,key_pem)
        if login_result.get('ok'):
            token=str(login_result.get('session_token') or ''); auth_mode='CERTLOGIN'

    today=datetime.now(timezone.utc).date().isoformat()
    cards, qa = racecard(today)
    open_au=[x for x in cards if x['market_status'] not in {'CLOSED'}]
    open_sa=[x for x in open_au if x['is_sa']]
    # Infrastructure smoke uses up to five AU thoroughbreds if no SA market is available.
    target=open_sa if open_sa else open_au[:5]
    books=list_market_book(app_key,token,[x['market_id'] for x in target]) if token else {'ok':False,'status':'AUTH_MISSING','books':[]}

    snapshot_receipt=None
    if books.get('ok') and books.get('books'):
        snapshot={
            'schema':'HorseRacing.ImmutablePreOffSnapshot.v1',
            'contract_sha256':CONTRACT_SHA256,
            'captured_at_utc':books.get('captured_at_utc') or now(),
            'paper_only':True,'orders_allowed':False,
            'auth_mode':auth_mode,
            'scope':'SA_THOROUGHBRED' if open_sa else 'AU_THOROUGHBRED_INFRA_SMOKE',
            'target_markets':target,
            'market_books':books['books'],
        }
        digest=hashlib.sha256(safe_json(snapshot).encode()).hexdigest()
        snapshot['snapshot_sha256']=digest
        filename=f"snapshot_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{digest[:12]}.json"
        path=SNAP/filename; path.write_text(json.dumps(snapshot,indent=2,ensure_ascii=False),encoding='utf-8')
        snapshot_receipt={'file':str(path),'sha256':digest,'market_books':len(books['books']),'usable_runner_lay_quotes':books.get('usable_runner_lay_quotes',0),'scope':snapshot['scope']}

    missing=[k for k,v in secrets.items() if k in {'username','password','app_key','cert','cert_key'} and not v]
    if token and snapshot_receipt:
        classification='CERTIFICATE_RUNTIME_ACTIVE_SNAPSHOT_CAPTURED'
        blocker=None
    elif missing:
        classification='CERTIFICATE_RUNTIME_ARMED_AWAITING_IDENTITY_MATERIAL'
        blocker='MISSING_RUNTIME_SECRETS:' + ','.join(missing)
    elif not token:
        classification='CERTIFICATE_RUNTIME_AUTH_FAILED'
        blocker='CERTLOGIN_OR_KEEPALIVE_FAILED'
    else:
        classification='CERTIFICATE_RUNTIME_AUTH_OK_NO_MARKET_SNAPSHOT'
        blocker='NO_TARGET_MARKET_OR_MARKETBOOK_FAILURE'

    status={
        'round':39,'capability':'HorseRacing.BetfairCertificateRuntime','status':'COMPLETE',
        'captured_at_utc':now(),'contract_sha256':CONTRACT_SHA256,
        'strategy_tuning':False,'paper_only':True,'real_betting_allowed':False,
        'runtime_secret_presence':secrets,'auth_mode':auth_mode,'session_fingerprint':fp(token),
        'keepalive':({k:v for k,v in keepalive_result.items() if k!='token'} if keepalive_result else None),
        'certlogin':({k:v for k,v in login_result.items() if k!='session_token'} if login_result else None),
        'racecard_qa':qa,'open_au_thoroughbred_markets':len(open_au),'open_sa_thoroughbred_markets':len(open_sa),
        'marketbook':{k:v for k,v in books.items() if k!='books'},'immutable_snapshot':snapshot_receipt,
        'classification':classification,'remaining_blocker':blocker,
        'governance':{
            'orders_forbidden':True,'delayed_key_only_for_paper':True,'session_never_written_to_repo':True,
            'private_key_tempfile_mode':'0600_DELETE_AFTER_USE','final_bsp_for_signal_forbidden':True,
            'no_threshold_window_state_or_rank_changes':True,
        },
    }
    (OUT/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(status,indent=2,ensure_ascii=False))


if __name__=='__main__': main()
