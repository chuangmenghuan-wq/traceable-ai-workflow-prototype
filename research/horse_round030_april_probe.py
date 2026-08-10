import hashlib, json, requests, zipfile
from pathlib import Path

BASE='https://betfair-datascientists.github.io/data/assets'
URLS=[
 f'{BASE}/ANZ_Thoroughbreds_2025_04.csv',
 f'{BASE}/ANZ_Thoroughbreds_2025_04.zip',
 f'{BASE}/ANZ_Thoroughbreds_2025_April.csv',
]
rows=[]
headers={'User-Agent':'Mozilla/5.0','Accept':'text/csv,application/zip,*/*'}
for u in URLS:
 r=requests.get(u,headers=headers,timeout=(20,120))
 rows.append({'url':u,'status':r.status_code,'content_type':r.headers.get('content-type'),'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest() if r.status_code==200 else None,'prefix':r.content[:80].decode('utf-8',errors='replace') if r.status_code!=200 else None})
# also inspect annual zip member sizes to confirm April member presence/content
annual=requests.get(f'{BASE}/ANZ_Thoroughbreds_2025.zip',headers=headers,timeout=(20,180))
annual.raise_for_status()
p=Path('/tmp/anz2025.zip'); p.write_bytes(annual.content)
with zipfile.ZipFile(p) as z:
 members=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size} for i in z.infolist() if '2025_04' in i.filename or i.filename.lower().endswith('.csv')]
out={'probes':rows,'annual_zip_sha256':hashlib.sha256(annual.content).hexdigest(),'annual_members':members}
Path('research_outputs/horse_round030').mkdir(parents=True,exist_ok=True)
Path('research_outputs/horse_round030/april_2025_asset_probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))