import io, json
from pathlib import Path
import pandas as pd, requests

OUT=Path('research_outputs/horse_round035'); OUT.mkdir(parents=True,exist_ok=True)
URL='https://betfair-data-supplier-prod.herokuapp.com/api/widgets/kash-ratings-model/datasets?date={date}&presenter=RatingsPresenter&csv=true'
rows=[]
for day in range(1,11):
    date=f'2026-08-{day:02d}'
    r=requests.get(URL.format(date=date),timeout=60); r.raise_for_status()
    d=pd.read_csv(io.BytesIO(r.content),dtype=str,low_memory=False)
    col='meetings.name'
    vals=sorted(d[col].dropna().astype(str).str.strip().unique().tolist()) if col in d.columns else []
    rows.append({'date':date,'meeting_names':vals})
(OUT/'august_meeting_names.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
