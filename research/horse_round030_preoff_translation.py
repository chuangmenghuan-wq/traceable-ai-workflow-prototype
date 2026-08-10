from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from horse_round025_runtime import BASE, PERIODS, PERIOD_ORDER, load_period
from horse_round027_source_reconcile import verify_source_vintage

OUT = Path('research_outputs/horse_round030')
CACHE = Path('.cache/horse_round030')
OUT.mkdir(parents=True, exist_ok=True)
CACHE.mkdir(parents=True, exist_ok=True)

ANZ_PERIODS = {
    '2023': [f'{BASE}/ANZ_Thoroughbreds_2023.csv'],
    '2024': [f'{BASE}/ANZ_Thoroughbreds_2024.csv'],
    '2025': [f'{BASE}/ANZ_Thoroughbreds_2025.csv'],
    '2026_JAN_JUL': [f'{BASE}/ANZ_Thoroughbreds_2026_{m:02d}.csv' for m in range(1, 8)],
}
PAST_WINDOW = 50
PRIMARY_COMMISSION = 0.07
RNG_SEED = 300826
BOOT_DRAWS = 10000


def download(url: str) -> Path:
    p = CACHE / url.rsplit('/', 1)[-1]
    if p.exists() and p.stat().st_size > 1024:
        return p
    with requests.get(url, stream=True, timeout=(20, 300)) as r:
        r.raise_for_status()
        with p.open('wb') as fh:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return p


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def norm_market(s: pd.Series) -> pd.Series:
    x = s.astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    # Kash market ids may carry Betfair's conventional leading "1." prefix.
    x = x.str.replace(r'^1\.(\d+)$', r'\1', regex=True)
    return x


def norm_selection(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.replace(r'\.0$', '', regex=True)


def load_anz_file(url: str, period: str) -> tuple[pd.DataFrame, dict]:
    p = download(url)
    needed = [
        'LOCAL_MEETING_DATE','TRACK','STATE_CODE','WIN_MARKET_ID','SELECTION_ID','WIN_RESULT','WIN_BSP',
        'BEST_AVAIL_LAY_AT_SCHEDULED_OFF','WIN_PREPLAY_LAST_PRICE_TAKEN','WIN_PREPLAY_WEIGHTED_AVERAGE_PRICE_TAKEN',
        'SCHEDULED_RACE_TIME','ACTUAL_OFF_TIME'
    ]
    d = pd.read_csv(p, usecols=lambda c: c in needed, low_memory=False)
    missing = sorted(set(needed) - set(d.columns))
    if missing:
        raise RuntimeError(f'ANZ_SCHEMA_MISSING {p.name}: {missing}')
    d['date'] = pd.to_datetime(d.LOCAL_MEETING_DATE.astype(str).str.strip(), format='%Y-%m-%d', errors='coerce')
    d['track_anz'] = d.TRACK.astype(str).str.strip()
    d['state_code'] = d.STATE_CODE.astype(str).str.strip().str.upper()
    d['market_key'] = norm_market(d.WIN_MARKET_ID)
    d['selection_key'] = norm_selection(d.SELECTION_ID)
    d['win'] = d.WIN_RESULT.astype(str).str.upper().map({'WINNER':1.0,'LOSER':0.0})
    d['bsp_anz'] = pd.to_numeric(d.WIN_BSP, errors='coerce')
    d['preoff_lay'] = pd.to_numeric(d.BEST_AVAIL_LAY_AT_SCHEDULED_OFF, errors='coerce')
    d['preoff_lpt'] = pd.to_numeric(d.WIN_PREPLAY_LAST_PRICE_TAKEN, errors='coerce')
    d['preoff_wap'] = pd.to_numeric(d.WIN_PREPLAY_WEIGHTED_AVERAGE_PRICE_TAKEN, errors='coerce')
    d['period'] = period
    d['source_file_anz'] = p.name
    d = d.replace([np.inf,-np.inf], np.nan).dropna(subset=['date','market_key','selection_key','bsp_anz','win'])
    d = d[(d.bsp_anz > 1) & d.win.isin([0,1])].copy()
    dup = int(d.duplicated(['date','market_key','selection_key'], keep=False).sum())
    d = d.sort_values(['date','market_key','selection_key']).drop_duplicates(['date','market_key','selection_key'], keep='last')
    info = {
        'period':period,'file':p.name,'sha256':sha256_file(p),'rows':int(len(d)),'duplicate_rows':dup,
        'date_min':str(d.date.min().date()),'date_max':str(d.date.max().date()),
        'preoff_lay_coverage':float(d.preoff_lay.notna().mean()),
    }
    return d, info


def load_anz_period(period: str) -> tuple[pd.DataFrame, list[dict]]:
    parts, infos = [], []
    for u in ANZ_PERIODS[period]:
        d, info = load_anz_file(u, period)
        parts.append(d); infos.append(info)
    z = pd.concat(parts, ignore_index=True)
    z = z.sort_values(['date','market_key','selection_key']).drop_duplicates(['date','market_key','selection_key'], keep='last')
    return z, infos


def build_joined() -> tuple[pd.DataFrame, list[dict], list[dict]]:
    joined_parts, join_qa, anz_fps = [], [], []
    for period in PERIOD_ORDER:
        k, kinfo = load_period(period, PERIODS[period])
        k = k.copy()
        k['market_key'] = norm_market(k.market_id)
        k['selection_key'] = norm_selection(k.selection_id)
        k['track_kash'] = k.track.astype(str).str.strip()
        a, infos = load_anz_period(period)
        anz_fps.extend(infos)
        m = k.merge(
            a[['date','market_key','selection_key','track_anz','state_code','win','bsp_anz','preoff_lay','preoff_lpt','preoff_wap']],
            on=['date','market_key','selection_key'], how='left', validate='one_to_one', indicator=True
        )
        # Validate settlement consistency where joined.
        hit = m._merge.eq('both')
        bsp_abs = (m.loc[hit,'bsp'] - m.loc[hit,'bsp_anz']).abs()
        win_match = (m.loc[hit,'win_x'] == m.loc[hit,'win_y']) if 'win_x' in m.columns else pd.Series([], dtype=bool)
        # normalize duplicated merge names
        if 'win_x' in m.columns:
            m['win'] = m['win_x']
            m = m.drop(columns=['win_x','win_y'])
        qa = {
            'period':period,
            'kash_rows':int(len(k)),
            'joined_rows':int(hit.sum()),
            'join_rate':float(hit.mean()),
            'joined_preoff_lay_rows':int((hit & m.preoff_lay.notna() & m.preoff_lay.gt(1)).sum()),
            'joined_preoff_lay_rate':float((hit & m.preoff_lay.notna() & m.preoff_lay.gt(1)).mean()),
            'bsp_max_abs_diff':float(bsp_abs.max()) if len(bsp_abs) else None,
            'bsp_mean_abs_diff':float(bsp_abs.mean()) if len(bsp_abs) else None,
            'win_match_rate':float(win_match.mean()) if len(win_match) else None,
            'kash_integrity':kinfo,
        }
        join_qa.append(qa)
        m['period'] = period
        joined_parts.append(m.drop(columns=['_merge']))
    x = pd.concat(joined_parts, ignore_index=True)
    return x, join_qa, anz_fps


def market_net_pnl(x: pd.DataFrame, price_col: str, commission: float) -> pd.DataFrame:
    if x.empty:
        return pd.DataFrame(columns=['date','market_key','gross','liability','net'])
    gross = np.where(x.win.eq(1), -(x[price_col]-1.0), 1.0)
    z = pd.DataFrame({'date':x.date.to_numpy(),'market_key':x.market_key.to_numpy(),'gross':gross,'liability':(x[price_col]-1.0).to_numpy()})
    z = z.groupby(['date','market_key'],as_index=False).agg(gross=('gross','sum'),liability=('liability','sum'))
    z['net'] = z.gross - np.where(z.gross>0, commission*z.gross, 0.0)
    return z.sort_values(['date','market_key']).reset_index(drop=True)


def maxdd(z: pd.DataFrame) -> float:
    if z.empty: return 0.0
    eq = z.net.cumsum().to_numpy(float)
    peak = np.maximum.accumulate(np.r_[0.0,eq])[:-1]
    return float(np.max(peak-eq)) if len(eq) else 0.0


def metrics(x: pd.DataFrame, price_col: str, commission: float) -> dict:
    if x.empty:
        return {'n':0,'net_pl':0.0,'pot':None,'rol':None,'maxdd':0.0,'horse_win_rate':None}
    z = market_net_pnl(x, price_col, commission)
    return {
        'n':int(len(x)),'net_pl':float(z.net.sum()),'pot':float(z.net.sum()/len(x)),
        'rol':float(z.net.sum()/z.liability.sum()),'maxdd':maxdd(z),'horse_win_rate':float(x.win.mean())
    }


def apply_preoff_gate(cand: pd.DataFrame) -> pd.DataFrame:
    y = cand.sort_values(['date','market_key','selection_key']).copy()
    y['model_prob'] = 1.0/y.model_odds
    y['preoff_market_prob'] = 1.0/y.preoff_lay
    y['model_sqerr'] = (y.win-y.model_prob)**2
    y['preoff_market_sqerr'] = (y.win-y.preoff_market_prob)**2
    y['gate_on'] = False
    y['hist_n'] = 0
    y['hist_brier_adv'] = np.nan
    hist_idx=[]
    for _, idx in y.groupby('date',sort=True).groups.items():
        idx=list(idx)
        prior=y.loc[hist_idx].tail(PAST_WINDOW) if hist_idx else y.iloc[0:0]
        if len(prior)>=PAST_WINDOW:
            mb=float(prior.preoff_market_sqerr.mean()); rb=float(prior.model_sqerr.mean()); adv=mb-rb
            gate=bool(adv>0)
        else:
            adv=np.nan; gate=False
        y.loc[idx,'gate_on']=gate
        y.loc[idx,'hist_n']=int(len(prior))
        y.loc[idx,'hist_brier_adv']=adv
        hist_idx.extend(idx)
    y['gate_on']=y.gate_on.astype(bool)
    return y


def overlap_row(g: pd.DataFrame, label: str) -> dict:
    f=g.final_candidate; p=g.preoff_candidate
    inter=int((f&p).sum()); fn=int(f.sum()); pn=int(p.sum()); union=int((f|p).sum())
    return {
        'period':label,'eligible_r2':int(len(g)),'final_candidate_n':fn,'preoff_candidate_n':pn,'intersection_n':inter,
        'recall_vs_final':inter/fn if fn else None,'precision_vs_final':inter/pn if pn else None,'jaccard':inter/union if union else None,
        'preoff_lay_mean':float(g.preoff_lay.mean()) if len(g) else None,
    }


def month_bootstrap_pot(x: pd.DataFrame, price_col: str, commission: float, draws: int=BOOT_DRAWS) -> dict:
    if x.empty: return {'ci95':[None,None],'p_nonpositive':None,'months':0}
    y=x.copy(); y['month']=y.date.dt.to_period('M').astype(str)
    rows=[]
    for month,g in y.groupby('month'):
        z=market_net_pnl(g,price_col,commission)
        rows.append((month,float(z.net.sum()),int(len(g))))
    if len(rows)<2: return {'ci95':[None,None],'p_nonpositive':None,'months':len(rows)}
    pl=np.array([r[1] for r in rows]); n=np.array([r[2] for r in rows]); rng=np.random.default_rng(RNG_SEED)
    vals=np.empty(draws)
    for i in range(draws):
        idx=rng.integers(0,len(rows),size=len(rows))
        vals[i]=pl[idx].sum()/n[idx].sum()
    q=np.quantile(vals,[.025,.975])
    return {'ci95':[float(q[0]),float(q[1])],'p_nonpositive':float((vals<=0).mean()),'months':len(rows)}


def main() -> None:
    # Protect the already-frozen Kash source vintage.
    kash_fps=verify_source_vintage()
    x, join_qa, anz_fps = build_joined()
    # Only rows that can be evaluated at scheduled off are deployable candidates.
    r2=x[(x.state_code.eq('SA')) & x.model_rank.eq(2)].copy()
    r2=r2[r2.preoff_lay.notna() & r2.preoff_lay.gt(1) & r2.bsp_anz.gt(1)].copy()
    r2['final_value']=1.0/r2.model_odds - 1.0/r2.bsp_anz
    r2['preoff_value']=1.0/r2.model_odds - 1.0/r2.preoff_lay
    r2['final_candidate']=r2.final_value.lt(-0.07)
    r2['preoff_candidate']=r2.preoff_value.lt(-0.07)

    overlaps=[overlap_row(r2[r2.period.eq(p)],p) for p in PERIOD_ORDER]
    overlaps.append(overlap_row(r2,'ALL'))

    pre=r2[r2.preoff_candidate].copy()
    pre=apply_preoff_gate(pre)
    rows=[]
    for p in PERIOD_ORDER:
        g=pre[pre.period.eq(p)]
        on=g[g.gate_on]; off=g[~g.gate_on]
        rows.append({
            'period':p,'candidate_n':int(len(g)),'gate_on_n':int(len(on)),'gate_off_n':int(len(off)),
            'all_5pct':metrics(g,'preoff_lay',.05),'all_7pct':metrics(g,'preoff_lay',.07),
            'gate_on_5pct':metrics(on,'preoff_lay',.05),'gate_on_7pct':metrics(on,'preoff_lay',.07),
            'gate_off_7pct':metrics(off,'preoff_lay',.07),
        })
    on_all=pre[pre.gate_on]
    off_all=pre[~pre.gate_on]
    aggregate={
        'all_candidates_7pct':metrics(pre,'preoff_lay',.07),
        'gate_on_7pct':metrics(on_all,'preoff_lay',.07),
        'gate_off_7pct':metrics(off_all,'preoff_lay',.07),
        'gate_on_month_bootstrap_7pct':month_bootstrap_pot(on_all,'preoff_lay',.07),
    }
    s=pd.DataFrame([{
        'period':r['period'],'candidate_n':r['candidate_n'],'gate_on_n':r['gate_on_n'],
        'all_pot_7pct':r['all_7pct']['pot'],'gate_on_pot_7pct':r['gate_on_7pct']['pot'],'gate_off_pot_7pct':r['gate_off_7pct']['pot']
    } for r in rows]).set_index('period')
    tests={
        'kash_hashes_match_round026':bool(all(r['match_round026_vintage'] for r in kash_fps)),
        'overall_gate_on_pot_7pct_positive':bool(aggregate['gate_on_7pct']['pot'] is not None and aggregate['gate_on_7pct']['pot']>0),
        'overall_gate_on_bootstrap_ci_low_positive':bool(aggregate['gate_on_month_bootstrap_7pct']['ci95'][0] is not None and aggregate['gate_on_month_bootstrap_7pct']['ci95'][0]>0),
        '2025_gate_on_positive':bool(pd.notna(s.loc['2025','gate_on_pot_7pct']) and s.loc['2025','gate_on_pot_7pct']>0),
        '2026_gate_on_positive':bool(pd.notna(s.loc['2026_JAN_JUL','gate_on_pot_7pct']) and s.loc['2026_JAN_JUL','gate_on_pot_7pct']>0),
        'at_least_50_gate_on_bets':bool(aggregate['gate_on_7pct']['n']>=50),
    }
    classification='PREOFF_ECONOMIC_TRANSLATION_SUPPORTED' if all(tests.values()) else 'PREOFF_TRANSLATION_NOT_PROVEN'
    status={
        'round':30,'capability':'HorseRacing.PreOffSignalTranslation','status':'COMPLETE',
        'source_vintage':'ROUND026_SHA256_FROZEN_VINTAGE for Kash + Round030 ANZ fingerprints',
        'frozen_final_signal':'SA × model rank 2 × (1/RP - 1/final BSP) < -7% × LAY',
        'translated_preoff_signal':'SA × model rank 2 × (1/RP - 1/BEST_AVAIL_LAY_AT_SCHEDULED_OFF) < -7% × LAY',
        'entry_price':'BEST_AVAIL_LAY_AT_SCHEDULED_OFF',
        'gate':'past 50 translated preoff candidates, date-safe; MODEL_TRUSTED iff RP Brier < preoff market Brier',
        'threshold_tuning':False,'primary_commission':PRIMARY_COMMISSION,
        'join_qa':join_qa,'anz_source_fingerprints':anz_fps,'overlap':overlaps,
        'period_economics':rows,'aggregate_economics':aggregate,
        'decision':{'classification':classification,'tests':tests},
        'governance':{
            'betting_ready':False,
            'reason':'Translation audit is retrospective on previously inspected years; live/paper forward confirmation still required. Scheduled-off snapshot is observable pre-race, but execution latency/slippage remains untested.',
            'no_parameter_tuning_this_round':True,
        },
    }
    (OUT/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
    pd.DataFrame(overlaps).to_csv(OUT/'candidate_overlap.csv',index=False)
    pd.DataFrame([{
        'date':str(r.date.date()),'period':r.period,'track':r.track_anz,'market_id':r.market_key,'selection_id':r.selection_key,
        'model_odds':r.model_odds,'preoff_lay':r.preoff_lay,'bsp':r.bsp_anz,'win':r.win,'preoff_value':r.preoff_value,
        'gate_on':r.gate_on,'hist_n':r.hist_n,'hist_brier_adv':r.hist_brier_adv,
    } for _,r in pre.iterrows()]).to_csv(OUT/'translated_candidates.csv',index=False)
    print(json.dumps(status,indent=2))

if __name__=='__main__':
    main()
