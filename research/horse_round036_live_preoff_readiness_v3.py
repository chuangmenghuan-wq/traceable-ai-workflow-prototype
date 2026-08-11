from __future__ import annotations
import json, os, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import pandas as pd
import requests
from horse_round036_preoff_adapter import BetfairPreOffAdapter

OUT=Path('research_outputs/horse_round036'); OUT.mkdir(parents=True,exist_ok=True)
RACECARD='https://apigateway.betfair.com.au/hub/racecard?date={date}'
RACEEVENT='https://apigateway.betfair.com.au/hub/raceevent/{market_id}'
DATES=['2026-08-11','2026-08-12']
SA={'BALAKLAVA','BORDERTOWN','CLARE','GAWLER','HALIDON','KANGAROO ISLAND','MORPHETTVILLE','MORPHETTVILLE PARKS','MOUNT GAMBIER','MURRAY BRIDGE','NARACOORTE','OAKBANK','PENOLA','PORT AUGUSTA','PORT LINCOLN','STRATHALBYN'}
S=requests.Session(); S.headers.update({'User-Agent':'FutureAbilityResearch/1.0 (paper-only read-only probe)'})

def jget(url):
    try:
        r=S.get(url,timeout=40); qa={'url':url,'http_status':r.status_code,'content_type':r.headers.get('content-type')}
        if r.status_code!=200: qa['body_prefix']=r.text[:500]; return None,qa
        try:return r.json(),qa
        except Exception as e: qa['json_error']=repr(e); return None,qa
    except Exception as e:return None,{'url':url,'error':repr(e)}

def mid(v:Any):
    s=str(v or '').strip()
    return s if s.startswith('1.') else ('1.'+s if re.fullmatch(r'\d+',s) else s)

def racecard(date):
    j,qa=jget(RACECARD.format(date=date)); rows=[]
    if isinstance(j,dict):
        for meet in (j.get('MEETINGS') or j.get('meetings') or []):
            venue=str(meet.get('VENUE_NAME') or meet.get('venueName') or '').strip().upper(); country=str(meet.get('COUNTRY') or meet.get('country') or '').strip().upper(); rtype=str(meet.get('RACE_TYPE') or meet.get('raceType') or '').strip().upper()
            for m in (meet.get('MARKETS') or meet.get('markets') or []):
                mkt=mid(m.get('MARKET_ID') or m.get('marketId'))
                if mkt: rows.append({'date':date,'venue':venue,'country':country,'race_type':rtype,'market_id':mkt,'race_no':m.get('RACE_NO') or m.get('raceNo'),'start_time':m.get('START_TIME') or m.get('startTime'),'market_status':m.get('MARKET_STATUS') or m.get('marketStatus'),'event_name':m.get('EVENT_NAME') or m.get('eventName')})
    d=pd.DataFrame(rows); gallops=d[d.race_type.eq('R')].copy() if len(d) else d
    qa.update({'parsed_markets':len(d),'au_markets':int(d.country.eq('AUS').sum()) if len(d) else 0,'aus_thoroughbred_markets':int((d.country.eq('AUS') & d.race_type.eq('R')).sum()) if len(d) else 0,'sa_thoroughbred_markets':int((d.country.eq('AUS') & d.race_type.eq('R') & d.venue.isin(SA)).sum()) if len(d) else 0})
    return d,qa

def flatten(x,p=''):
    out=[]
    if isinstance(x,dict):
        for k,v in x.items(): q=f'{p}.{k}' if p else str(k); out.append((q,v)); out.extend(flatten(v,q))
    elif isinstance(x,list):
        for i,v in enumerate(x[:20]): out.extend(flatten(v,f'{p}[{i}]'))
    return out

def hub_probe(markets):
    g=markets[(markets.country.eq('AUS')) & (markets.race_type.eq('R'))].copy() if len(markets) else pd.DataFrame()
    if g.empty:return {'tested':0,'accepted_as_exchange_price_source':False,'reason':'NO_AUS_THOROUGHBRED_MARKETS'}
    g['is_sa']=g.venue.isin(SA); g['rank']=g.market_status.astype(str).str.upper().map({'OPEN':0,'ACTIVE':0,'SUSPENDED':1,'CLOSED':2}).fillna(1); g=g.sort_values(['date','is_sa','rank'],ascending=[False,False,True])
    probes=[]; explicit=[]; paths=[]
    for r in g.head(8).itertuples(index=False):
        j,qa=jget(RACEEVENT.format(market_id=r.market_id)); rec={'market_id':r.market_id,'venue':r.venue,'date':r.date,**qa}
        if isinstance(j,dict):
            pls=[]; expl=[]
            for path,val in flatten(j):
                low=path.lower()
                if any(t in low for t in ['price','odds','back','lay','bsp','tote']) and not isinstance(val,(dict,list)): pls.append({'path':path,'value':val})
                if 'availabletoback' in low or 'availabletolay' in low or ('exchange' in low and ('back' in low or 'lay' in low)): expl.append(path)
            rec['race_type']=j.get('raceType'); rec['price_like_samples']=pls[:40]; rec['explicit_exchange_price_paths']=sorted(set(expl)); explicit+=expl; paths += [x['path'] for x in pls]
        probes.append(rec)
    return {'tested':len(probes),'accepted_as_exchange_price_source':bool(explicit),'explicit_exchange_price_paths':sorted(set(explicit)),'price_like_paths':sorted(set(paths))[:100],'probes':probes,'governance_note':'Only explicit Exchange back/lay ladders qualify. Generic runner market price/tote/BSP fields do not.'}

def main():
    cards=[]; qas=[]
    for dte in DATES:
        d,qa=racecard(dte); cards.append(d); qas.append(qa)
    markets=pd.concat(cards,ignore_index=True) if cards else pd.DataFrame()
    if len(markets): markets.to_csv(OUT/'racecard_markets.csv',index=False)
    hp=hub_probe(markets); (OUT/'hub_raceevent_probe.json').write_text(json.dumps(hp,indent=2,default=str),encoding='utf-8')
    gallops=markets[(markets.country.eq('AUS')) & (markets.race_type.eq('R'))].copy() if len(markets) else pd.DataFrame(); ids=[]
    if len(gallops):
        active=gallops[~gallops.market_status.astype(str).str.upper().eq('CLOSED')]; use=active if len(active) else gallops; ids=use.sort_values(['date','start_time'],ascending=[False,True]).market_id.astype(str).drop_duplicates().head(5).tolist()
    adapter=BetfairPreOffAdapter(); presence=adapter.readiness(); unauth=BetfairPreOffAdapter(app_key='',session_token='').snapshot(ids); auth=adapter.snapshot(ids)
    (OUT/'secret_presence.json').write_text(json.dumps(presence,indent=2),encoding='utf-8'); (OUT/'exchange_api_probe.json').write_text(json.dumps({'unauthenticated_control':unauth,'runtime_adapter':auth},indent=2,default=str),encoding='utf-8')
    books=auth.get('markets') or []; layq=sum(1 for b in books for rr in (b.get('runners') or []) if rr.get('best_lay')); flags=[bool(b.get('is_market_data_delayed')) for b in books]
    if auth.get('status')=='SUCCESS' and layq:
        if flags and all(flags): cls='OFFICIAL_DELAYED_PREOFF_ADAPTER_READY_FOR_SIMULATION'; ready=True; realtime=False; blocker='REALTIME_LIVE_APP_KEY_NOT_CONFIRMED'
        else: cls='OFFICIAL_PREOFF_ADAPTER_READY'; ready=True; realtime=True; blocker=None
    elif hp.get('accepted_as_exchange_price_source'):
        cls='PUBLIC_HUB_EXCHANGE_PRICE_PATH_DISCOVERED_REQUIRES_VALIDATION'; ready=False; realtime=False; blocker='PUBLIC_HUB_PRICE_SEMANTICS_NOT_YET_VALIDATED'
    elif auth.get('status')=='AUTH_MISSING':
        cls='OFFICIAL_EXCHANGE_AUTH_REQUIRED'; ready=False; realtime=False; blocker='BETFAIR_APP_KEY_AND_SESSION_TOKEN_NOT_PRESENT_IN_RUNTIME'
    else:
        cls='OFFICIAL_EXCHANGE_PRICE_PROBE_FAILED'; ready=False; realtime=False; blocker=auth.get('status')
    st={'round':36,'capability':'HorseRacing.LivePreOffPriceAdapterReadiness','status':'COMPLETE','run_scope':'AUS_THOROUGHBRED_ONLY','strategy_tuning':False,'paper_only':True,'real_betting_allowed':False,'captured_at_utc':datetime.now(timezone.utc).isoformat(),'racecard_qa':qas,'target_market_ids':ids,'runtime_auth':presence,'public_hub_raceevent':{'tested':hp.get('tested'),'accepted_as_exchange_price_source':hp.get('accepted_as_exchange_price_source'),'explicit_exchange_price_paths':hp.get('explicit_exchange_price_paths')},'exchange_adapter':{'status':auth.get('status'),'market_books':len(books),'usable_runner_lay_quotes':layq,'is_market_data_delayed_flags':flags},'classification':cls,'preoff_adapter_ready':ready,'realtime_preoff_ready':realtime,'remaining_blocker':blocker,'reusable_adapter':'research/horse_round036_preoff_adapter.py','frozen_execution_contract':{'observable_price_required':True,'final_bsp_for_signal_forbidden':True,'signal':'SA × Model Rank 2 × preoff_value < -7% → LAY','gate':'Past 50 settled candidates; strict date < race date; Trusted iff RP Brier < market Brier','no_threshold_window_state_or_rank_changes':True}}
    (OUT/'status.json').write_text(json.dumps(st,indent=2,default=str),encoding='utf-8'); print(json.dumps(st,indent=2,default=str))
if __name__=='__main__':main()
