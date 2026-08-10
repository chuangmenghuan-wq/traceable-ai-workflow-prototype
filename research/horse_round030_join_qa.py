import json
import pandas as pd
import horse_round030_preoff_translation_v2 as v2
import horse_round030_preoff_translation as r
from horse_round025_runtime import SA_TRACKS

x, join_qa, _ = r.build_joined()
rows=[]
for period in r.PERIOD_ORDER:
    p=x[x.period.eq(period)].copy()
    sa=p[p.track_kash.isin(SA_TRACKS) & p.model_rank.eq(2)].copy()
    sa['month']=sa.date.dt.to_period('M').astype(str)
    sa['joined']=sa.state_code.notna()
    sa['preoff_ok']=sa.preoff_lay.notna() & sa.preoff_lay.gt(1)
    sa['final_candidate_kash']=(1/sa.model_odds - 1/sa.bsp).lt(-0.07)
    for month,g in sa.groupby('month',sort=True):
        rows.append({
            'period':period,'month':month,'sa_r2':len(g),'joined':int(g.joined.sum()),'join_rate':float(g.joined.mean()),
            'preoff_ok':int((g.joined & g.preoff_ok).sum()),
            'final_candidates':int(g.final_candidate_kash.sum()),
            'final_candidates_joined':int((g.final_candidate_kash & g.joined).sum()),
            'final_candidates_preoff_ok':int((g.final_candidate_kash & g.joined & g.preoff_ok).sum()),
        })

p=x[x.period.eq('2025')].copy()
sa=p[p.track_kash.isin(SA_TRACKS)&p.model_rank.eq(2)].copy()
sa['joined']=sa.state_code.notna(); sa['preoff_ok']=sa.preoff_lay.notna()&sa.preoff_lay.gt(1)
sa['final_candidate_kash']=(1/sa.model_odds - 1/sa.bsp).lt(-0.07)
track=(sa.groupby('track_kash').agg(sa_r2=('market_key','size'),joined=('joined','sum'),preoff_ok=('preoff_ok','sum'),final_candidates=('final_candidate_kash','sum')).reset_index())
track['join_rate']=track.joined/track.sa_r2
missing=sa[~sa.joined][['date','track_kash','market_key','selection_key','model_odds','bsp','final_candidate_kash']].copy()

# 2023 BSP outliers between sources.
p23=x[x.period.eq('2023') & x.bsp_anz.notna()].copy(); p23['bsp_abs_diff']=(p23.bsp-p23.bsp_anz).abs()
outliers=p23.nlargest(20,'bsp_abs_diff')[['date','track_kash','market_key','selection_key','bsp','bsp_anz','bsp_abs_diff']]

outdir=r.OUT
pd.DataFrame(rows).to_csv(outdir/'join_qa_by_month.csv',index=False)
track.to_csv(outdir/'join_qa_2025_by_track.csv',index=False)
missing.to_csv(outdir/'join_qa_2025_missing_sa_r2.csv',index=False)
outliers.to_csv(outdir/'join_qa_2023_bsp_outliers.csv',index=False)
summary={
    '2025_sa_r2':int(len(sa)),'2025_joined_sa_r2':int(sa.joined.sum()),'2025_join_rate_sa_r2':float(sa.joined.mean()),
    '2025_final_candidates':int(sa.final_candidate_kash.sum()),
    '2025_final_candidates_joined':int((sa.final_candidate_kash&sa.joined).sum()),
    '2025_final_candidates_preoff_ok':int((sa.final_candidate_kash&sa.joined&sa.preoff_ok).sum()),
    'missing_month_counts':missing.assign(month=missing.date.dt.to_period('M').astype(str)).groupby('month').size().to_dict(),
    'missing_track_counts':missing.groupby('track_kash').size().sort_values(ascending=False).to_dict(),
    'largest_2023_bsp_diff':float(outliers.bsp_abs_diff.max()) if len(outliers) else None,
}
(outdir/'join_qa_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))