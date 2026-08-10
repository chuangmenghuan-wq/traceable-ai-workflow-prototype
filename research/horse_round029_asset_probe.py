import hashlib, json
from pathlib import Path
import requests

OUT=Path('research_outputs/horse_round029')
OUT.mkdir(parents=True,exist_ok=True)
urls={
 'anz_thoroughbreds_aug':'https://betfair-datascientists.github.io/data/assets/ANZ_Thoroughbreds_2026_08.csv',
 'kash_model_aug':'https://betfair-datascientists.github.io/data/assets/Kash_Model_Results_2026_08.csv',
}
rows=[]
for name,url in urls.items():
    r=requests.get(url,timeout=(20,120))
    rows.append({
      'name':name,'url':url,'status':r.status_code,
      'content_type':r.headers.get('content-type',''),'bytes':len(r.content),
      'sha256':hashlib.sha256(r.content).hexdigest() if r.status_code==200 else None,
      'prefix':r.text[:120] if r.status_code!=200 else None,
    })
(OUT/'august_asset_probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
