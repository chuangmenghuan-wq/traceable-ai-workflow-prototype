from __future__ import annotations
import os
from datetime import datetime, timezone
import requests

ENDPOINT='https://api.betfair.com/exchange/betting/json-rpc/v1'

class BetfairPreOffAdapter:
    """Read-only Exchange price adapter. Never places/cancels orders."""
    def __init__(self, app_key: str | None=None, session_token: str | None=None, session: requests.Session | None=None):
        self.app_key=(app_key if app_key is not None else os.getenv('BETFAIR_APP_KEY','')).strip()
        self.session_token=(session_token if session_token is not None else os.getenv('BETFAIR_SESSION_TOKEN','')).strip()
        self.http=session or requests.Session()
        self.http.headers.update({'User-Agent':'FutureAbilityResearch/1.0 (paper-only read-only adapter)'})

    def readiness(self) -> dict:
        return {'app_key_present':bool(self.app_key),'session_token_present':bool(self.session_token),'ready':bool(self.app_key and self.session_token)}

    def snapshot(self, market_ids: list[str], depth: int=3) -> dict:
        if not self.app_key or not self.session_token:
            return {'status':'AUTH_MISSING','captured_at_utc':datetime.now(timezone.utc).isoformat(),'markets':[]}
        ids=[str(x) for x in market_ids if str(x).strip()][:5]
        if not ids:
            return {'status':'NO_MARKETS','captured_at_utc':datetime.now(timezone.utc).isoformat(),'markets':[]}
        body={'jsonrpc':'2.0','method':'SportsAPING/v1.0/listMarketBook','params':{'marketIds':ids,'priceProjection':{'priceData':['EX_BEST_OFFERS'],'virtualise':True,'exBestOffersOverrides':{'bestPricesDepth':max(1,min(int(depth),10))}}},'id':1}
        headers={'X-Application':self.app_key,'X-Authentication':self.session_token,'content-type':'application/json','accept':'application/json'}
        captured=datetime.now(timezone.utc).isoformat()
        try:
            r=self.http.post(ENDPOINT,headers=headers,json=body,timeout=40)
        except Exception as e:
            return {'status':'TRANSPORT_ERROR','captured_at_utc':captured,'error':repr(e),'markets':[]}
        try: j=r.json()
        except Exception:
            return {'status':'NON_JSON_RESPONSE','captured_at_utc':captured,'http_status':r.status_code,'body_prefix':r.text[:500],'markets':[]}
        if r.status_code!=200 or not isinstance(j,dict) or 'result' not in j:
            return {'status':'API_ERROR','captured_at_utc':captured,'http_status':r.status_code,'error':j.get('error') if isinstance(j,dict) else None,'markets':[]}
        markets=[]
        for b in j.get('result') or []:
            runners=[]
            for rr in b.get('runners') or []:
                ex=rr.get('ex') or {}; backs=ex.get('availableToBack') or []; lays=ex.get('availableToLay') or []
                runners.append({'selection_id':rr.get('selectionId'),'last_price_traded':rr.get('lastPriceTraded'),'best_back':backs[0] if backs else None,'best_lay':lays[0] if lays else None,'back_ladder':backs[:depth],'lay_ladder':lays[:depth]})
            markets.append({'market_id':b.get('marketId'),'status':b.get('status'),'inplay':b.get('inplay'),'is_market_data_delayed':b.get('isMarketDataDelayed'),'publish_time':b.get('publishTime'),'runners':runners})
        return {'status':'SUCCESS','captured_at_utc':captured,'markets':markets}
