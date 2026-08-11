from __future__ import annotations
import json, os, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import pandas as pd
import requests

OUT=Path('research_outputs/horse_round036'); OUT.mkdir(parents=True,exist_ok=True)
RACECARD='https://apigateway.betfair.com.au/hub/racecard?date={date}'
RACEEVENT='https://apigateway.betfair.com.au/hub/raceevent/{market_id}'
EXCHANGE='https://api.betfair.com/exchange/betting/json-rpc/v1'
DATES=['2026-08-11','2026-08-12']
SA={'BALAKLAVA','BORDERTOWN','CLARE','GAWLER','HALIDON','KANGAROO ISLAND','MORPHETTVILLE','MORPHETTVILLE PARKS','MOUNT GAMBIER','MURRAY BRIDGE','NARACOORTE','OAKBANK','PENOLA','PORT AUGUSTA','PORT LINCOLN','STRATHALBYN'}
S=requests.Session(); S.headers.update({'User-Agent':'FutureAbilityResearch/1.0 (paper-only read-only probe)'})

def jget(url:str):
    try:
        r=S.get(url,timeout=40); qa={'url':url,'http_status':r.status_code,'content_type':r.headers.get('content-type')}
        if r.status_code!=200:
            qa['body_prefix']=r.text[:500]; return None,qa
        try: return r.json(),qa
        except Exception as e:
            qa['json_error']=repr(e); qa['body_prefix']=r.text[:500]; return None,qa
    except Exception as e: return None,{'url':url,'error':repr(e)}

def mid(v:Any)->str:
    s=str(v or '').strip()
    if s.startswith('1.'): return s
    if re.fullmatch(r'\d+',s): return '1.'+s
    return s

def racecard(date:str):
    j,qa=jget(RACECARD.format(date=date)); rows=[]
    if isinstance(j,dict):
        for meet in (j.get('MEETINGS') or j.get('meetings') or []):
            venue=str(meet.get('VENUE_NAME') or meet.get('venueName') or '').strip().upper()
            country=str(meet.get('COUNTRY') or meet.get('country') or '').strip().upper()
            rtype=str(meet.get('RACE_TYPE') or meet.get('raceType') or '').strip().upper()
            for m in (meet.get('MARKETS') or meet.get('markets') or []):
                market_id=mid(m.get('MARKET_ID') or m.get('marketId'))
                if market_id:
                    rows.append({'date':date,'venue':venue,'country':country,'race_type':rtype,'market_id':market_id,'race_no':m.get('RACE_NO') or m.get('raceNo'),'start_time':m.get('START_TIME') or m.get('startTime'),'market_status':m.get('MARKET_STATUS') or m.get('marketStatus'),'event_name':m.get('EVENT_NAME') or m.get('eventName')})
    d=pd.DataFrame(rows)
    qa.update({'parsed_markets':len(d),'au_markets':int(d.country.eq('AUS').sum()) if len(d) else 0,'sa_markets':int(d.venue.isin(SA).sum()) if len(d) else 0})
    return d,qa

def flat(x:Any,p=''):
    out=[]
    if isinstance(x,dict):
        for k,v in x.items():
            q=f'{p}.{k}' if p else str(k); out.append((q,v)); out.extend(flat(v,q))
    elif isinstance(x,list):
        for i,v in enumerate(x[:20]): out.extend(flat(v,f'{p}[{i}]'))
    return out

def hub_probe(markets:pd.DataFrame):
    if markets.empty: return {'tested':0,'accepted_as_exchange_price_source':False,'reason':'NO_MARKETS'}
    c=markets.copy(); c['is_sa']=c.venue.isin(SA); c['status_u']=c.market_status.astype(str).str.upper(); c['rank']=c.status_u.map({'OPEN':0,'ACTIVE':0,'SUSPENDED':1,'CLOSED':2}).fillna(1)
    c=c.sort_values(['date','is_sa','rank'],ascending=[False,False,True])
    probes=[]; explicit=[]; price_paths=[]
    for r in c.head(8).itertuples(index=False):
        j,qa=jget(RACEEVENT.format(market_id=r.market_id)); rec={'market_id':r.market_id,'venue':r.venue,'date':r.date,**qa}
        if isinstance(j,dict):
            pls=[]; expl=[]
            for path,val in flat(j):
                low=path.lower()
                if any(t in low for t in ['price','odds','back','lay','bsp','tote']) and not isinstance(val,(dict,list)):
                    pls.append({'path':path,'value':val})
                if 'availabletoback' in low or 'availabletolay' in low or ('exchange' in low and ('back' in low or 'lay' in low)):
                    expl.append(path)
            explicit+=expl; price_paths += [x['path'] for x in pls]
            rec['top_level_keys']=sorted(j.keys()); rec['price_like_samples']=pls[:40]; rec['explicit_exchange_price_paths']=sorted(set(expl))
        probes.append(rec)
    return {'tested':len(probes),'accepted_as_exchange_price_source':bool(explicit),'explicit_exchange_price_paths':sorted(set(explicit)),'price_like_paths':sorted(set(price_paths))[:100],'probes':probes,'governance_note':'Accept only explicit Betfair Exchange back/lay ladder fields; tote/bestPrice/generic odds are rejected.'}

def exchange_call(ids,app,token):
    if not ids: return {'status':'NO_MARKETS'}
    body={'jsonrpc':'2.0','method':'SportsAPING/v1.0/listMarketBook','params':{'marketIds':ids[:5],'priceProjection':{'priceData':['EX_BEST_OFFERS'],'virtualise':True,'exBestOffersOverrides':{'bestPricesDepth':3}}},'id':36}
    h={'content-type':'application/json','accept':'application/json'}
    if app: h['X-Application']=app
    if token: h['X-Authentication']=token
    try:
        r=S.post(EXCHANGE,headers=h,json=body,timeout=40); rec={'endpoint':EXCHANGE,'http_status':r.status_code,'captured_at_utc':datetime.now(timezone.utc).isoformat()}
        try: j=r.json()
        except Exception: j=None; rec['body_prefix']=r.text[:1000]
        rec['json']=j
        if r.status_code==200 and isinstance(j,dict) and 'result' in j:
            books=[]
            for b in (j.get('result') or []):
                runners=[]
                for rr in (b.get('runners') or []):
                    ex=rr.get('ex') or {}; runners.append({'selection_id':rr.get('selectionId'),'last_price_traded':rr.get('lastPriceTraded'),'available_to_back':(ex.get('availableToBack') or [])[:3],'available_to_lay':(ex.get('availableToLay') or [])[:3]})
                books.append({'market_id':b.get('marketId'),'status':b.get('status'),'inplay':b.get('inplay'),'is_market_data_delayed':b.get('isMarketDataDelayed'),'publish_time':b.get('publishTime'),'runners':runners})
            return {'status':'SUCCESS','attempt':rec,'books':books}
        return {'status':'FAILED','attempt':rec}
    except Exception as e: return {'status':'EXCEPTION','error':repr(e)}

def main():
    cards=[]; qas=[]
    for dte in DATES:
        d,qa=racecard(dte); cards.append(d); qas.append(qa)
    markets=pd.concat(cards,ignore_index=True) if cards else pd.DataFrame()
    if len(markets): markets.to_csv(OUT/'racecard_markets.csv',index=False)
    hp=hub_probe(markets); (OUT/'hub_raceevent_probe.json').write_text(json.dumps(hp,indent=2,default=str),encoding='utf-8')
    app=os.getenv('BETFAIR_APP_KEY','').strip(); tok=os.getenv('BETFAIR_SESSION_TOKEN','').strip(); presence={'BETFAIR_APP_KEY':bool(app),'BETFAIR_SESSION_TOKEN':bool(tok)}
    (OUT/'secret_presence.json').write_text(json.dumps(presence,indent=2),encoding='utf-8')
    ids=[]
    if len(markets):
        au=markets[markets.country.eq('AUS')].copy(); active=au[~au.market_status.astype(str).str.upper().eq('CLOSED')]; use=active if len(active) else au
        ids=use.sort_values(['date','start_time'],ascending=[False,True]).market_id.astype(str).drop_duplicates().head(5).tolist()
    unauth=exchange_call(ids,'',''); auth=exchange_call(ids,app,tok) if app and tok else {'status':'NOT_ATTEMPTED_MISSING_SECRETS'}
    (OUT/'exchange_api_probe.json').write_text(json.dumps({'unauthenticated_control':unauth,'authenticated':auth},indent=2,default=str),encoding='utf-8')
    books=(auth.get('books') or []) if isinstance(auth,dict) else []; layq=sum(1 for b in books for rr in (b.get('runners') or []) if rr.get('available_to_lay')); flags=[bool(b.get('is_market_data_delayed')) for b in books]
    if auth.get('status')=='SUCCESS' and layq:
        if flags and all(flags): cls='OFFICIAL_DELAYED_PREOFF_ADAPTER_READY_FOR_SIMULATION'; ready=True; real=False; blocker='REALTIME_LIVE_APP_KEY_NOT_CONFIRMED'
        else: cls='OFFICIAL_PREOFF_ADAPTER_READY'; ready=True; real=True; blocker=None
    elif hp.get('accepted_as_exchange_price_source'):
        cls='PUBLIC_HUB_EXCHANGE_PRICE_PATH_DISCOVERED_REQUIRES_VALIDATION'; ready=False; real=False; blocker='PUBLIC_HUB_PRICE_SEMANTICS_NOT_YET_VALIDATED'
    elif not (app and tok):
        cls='OFFICIAL_EXCHANGE_AUTH_REQUIRED'; ready=False; real=False; blocker='BETFAIR_APP_KEY_AND_SESSION_TOKEN_NOT_PRESENT_IN_RUNTIME'
    else:
        cls='OFFICIAL_EXCHANGE_AUTH_PRESENT_BUT_PRICE_PROBE_FAILED'; ready=False; real=False; blocker='AUTH_OR_MARKETBOOK_CALL_FAILED'
    st={'round':36,'capability':'HorseRacing.LivePreOffPriceAdapterReadiness','status':'COMPLETE','strategy_tuning':False,'real_betting_allowed':False,'paper_only':True,'captured_at_utc':datetime.now(timezone.utc).isoformat(),'racecard_qa':qas,'target_market_ids':ids,'runtime_secret_presence':presence,'public_hub_raceevent':{'tested':hp.get('tested'),'accepted_as_exchange_price_source':hp.get('accepted_as_exchange_price_source'),'explicit_exchange_price_paths':hp.get('explicit_exchange_price_paths')},'exchange_api':{'unauthenticated_status':unauth.get('status'),'authenticated_status':auth.get('status'),'market_books':len(books),'usable_runner_lay_quotes':layq,'is_market_data_delayed_flags':flags},'classification':cls,'preoff_adapter_ready':ready,'realtime_preoff_ready':real,'remaining_blocker':blocker,'frozen_execution_contract':{'observable_price_required':True,'final_bsp_for_signal_forbidden':True,'signal':'SA × Model Rank 2 × preoff_value < -7% → LAY','gate':'Past 50 settled candidates; strict date < race date; Trusted iff RP Brier < market Brier','no_threshold_window_state_or_rank_changes':True}}
    (OUT/'status.json').write_text(json.dumps(st,indent=2,default=str),encoding='utf-8'); print(json.dumps(st,indent=2,default=str))
if __name__=='__main__': main()
