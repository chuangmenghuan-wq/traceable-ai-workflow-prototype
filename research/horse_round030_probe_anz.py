import json, requests, pandas as pd, io
from pathlib import Path

URL='https://betfair-datascientists.github.io/data/assets/ANZ_Thoroughbreds_2026_07.csv'
r=requests.get(URL,timeout=(20,120))
out={'url':URL,'status':r.status_code,'content_type':r.headers.get('content-type'),'bytes':len(r.content)}
if r.status_code==200:
    df=pd.read_csv(io.BytesIO(r.content), low_memory=False)
    out['rows']=len(df)
    out['columns']=[str(c) for c in df.columns]
    out['head']=df.head(3).astype(str).to_dict(orient='records')
Path('research_outputs/horse_round030').mkdir(parents=True,exist_ok=True)
Path('research_outputs/horse_round030/anz_schema_probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))