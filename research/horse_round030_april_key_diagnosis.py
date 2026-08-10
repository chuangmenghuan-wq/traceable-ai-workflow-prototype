import io, json, requests
import pandas as pd
import horse_round030_preoff_translation as r
from horse_round025_runtime import load_period, PERIODS, SA_TRACKS

k,_=load_period('2025',PERIODS['2025'])
k=k[(k.date.dt.year==2025)&(k.date.dt.month==4)].copy()
k['market_key']=r.norm_market(k.market_id); k['selection_key']=r.norm_selection(k.selection_id)
k=k[k.track.isin(SA_TRACKS)&k.model_rank.eq(2)].copy()

u=f'{r.BASE}/ANZ_Thoroughbreds_2025_04.csv'
raw=requests.get(u,timeout=(20,180)); raw.raise_for_status()
a=pd.read_csv(io.BytesIO(raw.content),low_memory=False)
a['date']=pd.to_datetime(a.LOCAL_MEETING_DATE.astype(str).str.strip(),format='%Y-%m-%d',errors='coerce')
a['market_key']=r.norm_market(a.WIN_MARKET_ID); a['selection_key']=r.norm_selection(a.SELECTION_ID)
a['track_anz']=a.TRACK.astype(str).str.strip(); a['state_code']=a.STATE_CODE.astype(str).str.strip().str.upper()
asa=a[a.state_code.eq('SA')].copy()

# hierarchical key overlap diagnostics
km=set(zip(k.market_key,k.selection_key)); am=set(zip(asa.market_key,asa.selection_key))
kd=set(zip(k.date.astype(str),k.market_key,k.selection_key)); ad=set(zip(asa.date.astype(str),asa.market_key,asa.selection_key))
sel_k=set(k.selection_key); sel_a=set(asa.selection_key)
market_k=set(k.market_key); market_a=set(asa.market_key)

# For each Kash SA R2 show possible ANZ matches by selection id, so format/date/market differences are visible.
sample=[]
for _,q in k.head(30).iterrows():
    m=asa[asa.selection_key.eq(q.selection_key)]
    sample.append({
        'k_date':str(q.date.date()),'k_track':q.track,'k_market_raw':str(q.market_id),'k_market_key':q.market_key,
        'selection_key':q.selection_key,'anz_match_count_by_selection':int(len(m)),
        'anz_dates':sorted(set(str(d.date()) for d in m.date.dropna()))[:5],
        'anz_tracks':sorted(set(m.track_anz))[:5],
        'anz_market_keys':sorted(set(m.market_key))[:5],
    })

# identify raw id examples
out={
 'kash_sa_r2':len(k),'anz_sa_rows':len(asa),
 'selection_overlap_count':len(sel_k&sel_a),'kash_unique_selections':len(sel_k),
 'market_overlap_count':len(market_k&market_a),'kash_unique_markets':len(market_k),
 'market_selection_overlap':len(km&am),
 'date_market_selection_overlap':len(kd&ad),
 'kash_market_raw_examples':k[['market_id','market_key']].drop_duplicates().head(10).astype(str).to_dict(orient='records'),
 'anz_market_raw_examples':asa[['WIN_MARKET_ID','market_key']].drop_duplicates().head(10).astype(str).to_dict(orient='records'),
 'sample_by_selection':sample,
}
from pathlib import Path
Path('research_outputs/horse_round030/april_key_diagnosis.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))