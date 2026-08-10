from __future__ import annotations

import zipfile
import numpy as np
import pandas as pd

import horse_round030_preoff_translation as r

r.ANZ_PERIODS = {
    '2023': [f'{r.BASE}/ANZ_Thoroughbreds_2023.zip'],
    '2024': [f'{r.BASE}/ANZ_Thoroughbreds_2024.zip'],
    '2025': [f'{r.BASE}/ANZ_Thoroughbreds_2025.zip'],
    '2026_JAN_JUL': [f'{r.BASE}/ANZ_Thoroughbreds_2026_{m:02d}.csv' for m in range(1, 8)],
}

ESSENTIAL = [
    'LOCAL_MEETING_DATE','TRACK','STATE_CODE','WIN_MARKET_ID','SELECTION_ID','WIN_RESULT','WIN_BSP',
    'BEST_AVAIL_LAY_AT_SCHEDULED_OFF'
]
OPTIONAL = [
    'WIN_PREPLAY_LAST_PRICE_TAKEN','WIN_PREPLAY_WEIGHTED_AVERAGE_PRICE_TAKEN',
    'SCHEDULED_RACE_TIME','ACTUAL_OFF_TIME'
]


def parse_anz_dates_fail_closed(s: pd.Series, source_label: str) -> tuple[pd.Series, dict]:
    raw=s.astype(str).str.strip()
    iso=raw.str.match(r'^\d{4}-\d{2}-\d{2}$')
    dmy=raw.str.match(r'^\d{1,2}/\d{2}/\d{4}$')
    unknown=~(iso|dmy)
    if unknown.any():
        vals=raw[unknown].drop_duplicates().head(10).tolist()
        raise RuntimeError(f'ANZ_DATE_FORMAT_UNKNOWN {source_label}: {vals}')
    out=pd.Series(pd.NaT,index=raw.index,dtype='datetime64[ns]')
    if iso.any(): out.loc[iso]=pd.to_datetime(raw.loc[iso],format='%Y-%m-%d',errors='raise')
    if dmy.any(): out.loc[dmy]=pd.to_datetime(raw.loc[dmy],format='%d/%m/%Y',errors='raise')
    if out.isna().any():
        raise RuntimeError(f'ANZ_DATE_PARSE_NAT {source_label}: n={int(out.isna().sum())}')
    return out, {'ISO_YMD':int(iso.sum()),'DMY_SLASH':int(dmy.sum())}


def patched_load_anz_file(url: str, period: str):
    p = r.download(url)
    if p.suffix.lower() == '.zip':
        with zipfile.ZipFile(p) as zf:
            names = [n for n in zf.namelist() if n.lower().endswith('.csv')]
            if not names:
                raise RuntimeError(f'ANZ_ZIP_NO_CSV {p.name}')
            parts=[]
            for name in names:
                with zf.open(name) as fh:
                    part=pd.read_csv(fh,usecols=lambda c:c in ESSENTIAL+OPTIONAL,low_memory=False)
                    part['_anz_member']=name
                    parts.append(part)
            d=pd.concat(parts,ignore_index=True)
            source_label=f'{p.name}:{"|".join(names)}'
    else:
        d=pd.read_csv(p,usecols=lambda c:c in ESSENTIAL+OPTIONAL,low_memory=False)
        d['_anz_member']=p.name
        source_label=p.name

    missing=sorted(set(ESSENTIAL)-set(d.columns))
    if missing:
        raise RuntimeError(f'ANZ_SCHEMA_MISSING {source_label}: {missing}')
    for c in OPTIONAL:
        if c not in d.columns:
            d[c]=np.nan

    d['date'],date_formats=parse_anz_dates_fail_closed(d.LOCAL_MEETING_DATE,source_label)
    d['track_anz']=d.TRACK.astype(str).str.strip()
    d['state_code']=d.STATE_CODE.astype(str).str.strip().str.upper()
    d['market_key']=r.norm_market(d.WIN_MARKET_ID)
    d['selection_key']=r.norm_selection(d.SELECTION_ID)
    d['win']=d.WIN_RESULT.astype(str).str.upper().map({'WINNER':1.0,'LOSER':0.0})
    d['bsp_anz']=pd.to_numeric(d.WIN_BSP,errors='coerce')
    d['preoff_lay']=pd.to_numeric(d.BEST_AVAIL_LAY_AT_SCHEDULED_OFF,errors='coerce')
    d['preoff_lpt']=pd.to_numeric(d.WIN_PREPLAY_LAST_PRICE_TAKEN,errors='coerce')
    d['preoff_wap']=pd.to_numeric(d.WIN_PREPLAY_WEIGHTED_AVERAGE_PRICE_TAKEN,errors='coerce')
    d['period']=period
    d['source_file_anz']=d['_anz_member']
    d=d.replace([np.inf,-np.inf],np.nan).dropna(subset=['date','market_key','selection_key','bsp_anz','win'])
    d=d[(d.bsp_anz>1)&d.win.isin([0,1])].copy()
    dup=int(d.duplicated(['date','market_key','selection_key'],keep=False).sum())
    d=d.sort_values(['date','market_key','selection_key']).drop_duplicates(['date','market_key','selection_key'],keep='last')
    info={
        'period':period,'file':source_label,'archive_sha256':r.sha256_file(p),'rows':int(len(d)),'duplicate_rows':dup,
        'date_min':str(d.date.min().date()),'date_max':str(d.date.max().date()),'date_formats':date_formats,
        'preoff_lay_coverage':float((d.preoff_lay.notna()&d.preoff_lay.gt(1)).mean()),
    }
    return d,info

r.load_anz_file = patched_load_anz_file

if __name__ == '__main__':
    r.main()
