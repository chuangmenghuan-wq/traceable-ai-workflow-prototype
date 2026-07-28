#!/usr/bin/env python3
from __future__ import annotations
import csv, io, json, math, os, sys, urllib.request
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

YEARS = [2021, 2022, 2023, 2024, 2025]
URLS = {
    2021: 'https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/seasons/2021/GL2021.TXT',
    2022: 'https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/seasons/2022/GL2022.TXT',
    2023: 'https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/seasons/2023/GL2023.TXT',
    2024: 'https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/seasons/2024/gl2024.txt',
    2025: 'https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/seasons/2025/GL2025.TXT',
}
TARGETS = (6, 7, 8)
TEAM_ALIAS = {'ATH': 'OAK'}

@dataclass
class Game:
    year:int; date:str; game_no:int; away:str; home:str; park:str; daynight:str
    away_sp:str; home_sp:str; away_runs:List[int]; home_runs:List[int]
    winner:int|None
    @property
    def gid(self): return f'{self.date}-{self.game_no}-{self.away}-{self.home}'


def parse_line_score(s: str) -> List[int]:
    s=(s or '').strip(); out=[]; i=0
    while i < len(s):
        c=s[i]
        if c=='(':
            j=s.find(')',i+1)
            if j<0: break
            out.append(int(s[i+1:j])); i=j+1
        elif c.isdigit(): out.append(int(c)); i+=1
        elif c.lower()=='x': out.append(0); i+=1
        else: i+=1
    return (out+[0]*9)[:9]


def download(url:str)->str:
    req=urllib.request.Request(url,headers={'User-Agent':'FAU-MLB-HSI/1.0'})
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read().decode('utf-8-sig')


def load_games()->List[Game]:
    games=[]
    for y in YEARS:
        text=download(URLS[y])
        n=0
        for row in csv.reader(io.StringIO(text)):
            if len(row)<105: continue
            n+=1
            away=TEAM_ALIAS.get(row[3],row[3]); home=TEAM_ALIAS.get(row[6],row[6])
            ar=parse_line_score(row[19]); hr=parse_line_score(row[20])
            totals=[a+h for a,h in zip(ar,hr)]
            mx=max(totals); leaders=[i+1 for i,v in enumerate(totals) if v==mx]
            winner=leaders[0] if len(leaders)==1 else None
            games.append(Game(y,row[0],int(row[1] or 0),away,home,row[16],row[12],row[101],row[103],ar,hr,winner))
        print(f'loaded {y}: {n}', flush=True)
    games.sort(key=lambda g:(g.date,g.game_no,g.away,g.home))
    return games


def mean_shrunk(total,count,prior,prior_n):
    return (total+prior*prior_n)/(count+prior_n) if count+prior_n else prior

def dqmean(d, default): return float(np.mean(d)) if d else default


def build_features(games:List[Game])->pd.DataFrame:
    league_inn_sum=np.zeros(9); league_games=0
    team_off_sum=defaultdict(lambda:np.zeros(9)); team_off_n=defaultdict(int)
    team_def_sum=defaultdict(lambda:np.zeros(9)); team_def_n=defaultdict(int)
    team_total_for=defaultdict(lambda:deque(maxlen=30)); team_total_against=defaultdict(lambda:deque(maxlen=30))
    team_late_for=defaultdict(lambda:deque(maxlen=20)); team_late_against=defaultdict(lambda:deque(maxlen=20))
    team_hit_sum=defaultdict(int); team_hit_n=defaultdict(int); team_miss=defaultdict(int)
    park_sum=defaultdict(float); park_n=defaultdict(int)
    sp_f5_allowed=defaultdict(lambda:deque(maxlen=20))
    rows=[]
    by_date=defaultdict(list)
    for g in games: by_date[g.date].append(g)
    for date in sorted(by_date):
        batch=sorted(by_date[date],key=lambda g:(g.game_no,g.away,g.home))
        lg_mean=league_inn_sum/max(league_games,1)
        global_game_runs=float(lg_mean.sum()) if league_games else 8.7
        for g in batch:
            exp=[]; raw_feats={}
            for i in range(9):
                prior=float(lg_mean[i]) if league_games else (0.92 if i<5 else 0.98)
                ao=mean_shrunk(team_off_sum[g.away][i],team_off_n[g.away],prior/2,40)
                ho=mean_shrunk(team_off_sum[g.home][i],team_off_n[g.home],prior/2,40)
                ad=mean_shrunk(team_def_sum[g.away][i],team_def_n[g.away],prior/2,40)
                hd=mean_shrunk(team_def_sum[g.home][i],team_def_n[g.home],prior/2,40)
                away_mu=max(0.02, math.sqrt(max(ao,0.01)*max(hd,0.01)))
                home_mu=max(0.02, math.sqrt(max(ho,0.01)*max(ad,0.01)))
                exp.append(away_mu+home_mu)
                raw_feats[f'exp_i{i+1}']=away_mu+home_mu
            park_factor=(park_sum[g.park]/park_n[g.park]/global_game_runs) if park_n[g.park] and global_game_runs>0 else 1.0
            a_rf=dqmean(team_total_for[g.away],global_game_runs/2); h_rf=dqmean(team_total_for[g.home],global_game_runs/2)
            a_ra=dqmean(team_total_against[g.away],global_game_runs/2); h_ra=dqmean(team_total_against[g.home],global_game_runs/2)
            a_lf=dqmean(team_late_for[g.away],sum(lg_mean[5:8])/2 if league_games else 1.5)
            h_lf=dqmean(team_late_for[g.home],sum(lg_mean[5:8])/2 if league_games else 1.5)
            a_la=dqmean(team_late_against[g.away],sum(lg_mean[5:8])/2 if league_games else 1.5)
            h_la=dqmean(team_late_against[g.home],sum(lg_mean[5:8])/2 if league_games else 1.5)
            asp=dqmean(sp_f5_allowed[g.away_sp],sum(lg_mean[:5])/2 if league_games else 2.2)
            hsp=dqmean(sp_f5_allowed[g.home_sp],sum(lg_mean[:5])/2 if league_games else 2.2)
            for target in TARGETS:
                idx=target-1; others=[exp[j] for j in range(9) if j!=idx]
                keya=(g.away,target); keyh=(g.home,target)
                hit_a=mean_shrunk(team_hit_sum[keya],team_hit_n[keya],0.085,80)
                hit_h=mean_shrunk(team_hit_sum[keyh],team_hit_n[keyh],0.085,80)
                row={
                    'year':g.year,'date':g.date,'gid':g.gid,'target':target,
                    'away':g.away,'home':g.home,'park':g.park,'daynight':g.daynight,
                    'label':int(g.winner==target),
                    'target_exp':exp[idx]*park_factor,'max_other_exp':max(others)*park_factor,
                    'mean_other_exp':float(np.mean(others))*park_factor,
                    'exp_gap':(exp[idx]-max(others))*park_factor,
                    'exp_rank':1+sum(v>exp[idx] for v in exp),
                    'park_factor':park_factor,
                    'away_recent_runs':a_rf,'home_recent_runs':h_rf,
                    'away_recent_allowed':a_ra,'home_recent_allowed':h_ra,
                    'away_late_runs':a_lf,'home_late_runs':h_lf,
                    'away_late_allowed':a_la,'home_late_allowed':h_la,
                    'away_sp_f5_allowed':asp,'home_sp_f5_allowed':hsp,
                    'team_hit_prior_mean':(hit_a+hit_h)/2,
                    'team_hit_prior_max':max(hit_a,hit_h),
                    'miss_streak_min':min(team_miss[keya],team_miss[keyh]),
                    'miss_streak_max':max(team_miss[keya],team_miss[keyh]),
                    'games_away':team_off_n[g.away],'games_home':team_off_n[g.home],
                }
                row.update({k:v*park_factor for k,v in raw_feats.items()})
                rows.append(row)
        for g in batch:
            totals=np.array(g.away_runs)+np.array(g.home_runs)
            league_inn_sum += totals; league_games += 1
            for team, own, opp in ((g.away,g.away_runs,g.home_runs),(g.home,g.home_runs,g.away_runs)):
                team_off_sum[team]+=np.array(own); team_off_n[team]+=1
                team_def_sum[team]+=np.array(opp); team_def_n[team]+=1
                team_total_for[team].append(sum(own)); team_total_against[team].append(sum(opp))
                team_late_for[team].append(sum(own[5:8])); team_late_against[team].append(sum(opp[5:8]))
                for t in TARGETS:
                    key=(team,t); hit=int(g.winner==t)
                    team_hit_sum[key]+=hit; team_hit_n[key]+=1
                    team_miss[key]=0 if hit else team_miss[key]+1
            park_sum[g.park]+=sum(totals); park_n[g.park]+=1
            sp_f5_allowed[g.away_sp].append(sum(g.home_runs[:5]))
            sp_f5_allowed[g.home_sp].append(sum(g.away_runs[:5]))
    return pd.DataFrame(rows)


def wilson(h,n,z=1.959963984540054):
    if n==0:return (0.0,0.0)
    p=h/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    m=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
    return max(0,c-m),min(1,c+m)

def stats(sel:pd.DataFrame, score_col='score'):
    n=len(sel); h=int(sel.label.sum()); p=h/n if n else 0; lo,hi=wilson(h,n)
    return {'n':n,'hits':h,'rate':p,'wilson95':[lo,hi],
            'roi_5x':p*5-1,'roi_7x':p*7-1,'roi_8x':p*8-1,
            'avg_score':float(sel[score_col].mean()) if n else None}

def best_per_game(df):
    return df.sort_values(['gid','score'],ascending=[True,False]).groupby('gid',as_index=False).head(1)


def evaluate_rule(df, rule):
    x=df
    if rule['mode']=='best': x=best_per_game(x)
    sel=x[x.score>=rule['threshold']]
    return stats(sel),sel


def main(outdir:str):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    games=load_games(); df=build_features(games)
    df.to_csv(out/'candidate_features.csv.gz',index=False,compression='gzip')
    train=df[df.year<=2023].copy(); val=df[df.year==2024].copy(); test=df[df.year==2025].copy()
    drop={'year','date','gid','label','away','home','park','daynight'}
    features=[c for c in df.columns if c not in drop]
    cat=['target']; num=[c for c in features if c not in cat]
    pre=ColumnTransformer([('num',Pipeline([('imp',SimpleImputer(strategy='median')),('sc',StandardScaler())]),num),
                           ('cat',OneHotEncoder(handle_unknown='ignore'),cat)])
    models={
      'logit':Pipeline([('pre',pre),('m',LogisticRegression(C=0.3,max_iter=2000,class_weight=None))]),
      'extra_trees':Pipeline([('pre',pre),('m',ExtraTreesClassifier(n_estimators=350,min_samples_leaf=25,max_features=0.8,class_weight=None,random_state=20260728,n_jobs=-1))]),
      'hist_gb':Pipeline([('pre',pre),('m',HistGradientBoostingClassifier(max_iter=220,learning_rate=0.035,max_leaf_nodes=12,min_samples_leaf=60,l2_regularization=4.0,random_state=20260728))]),
    }
    val_rows=[]; fitted={}
    qgrid=[0.80,0.85,0.90,0.93,0.95,0.97,0.98]
    modes=['best','all']
    for name,model in models.items():
        model.fit(train[features],train.label); fitted[name]=model
        for split,data in [('train',train),('val',val)]:
            p=model.predict_proba(data[features])[:,1]
            data.loc[:,f'score_{name}']=p
        v=val.copy(); v['score']=v[f'score_{name}']
        auc=roc_auc_score(v.label,v.score); brier=brier_score_loss(v.label,v.score)
        for mode in modes:
            base=best_per_game(v) if mode=='best' else v
            for q in qgrid:
                thr=float(base.score.quantile(q)); sel=base[base.score>=thr]
                s=stats(sel); lo=s['wilson95'][0]
                val_rows.append({'model':name,'mode':mode,'q':q,'threshold':thr,'auc':auc,'brier':brier,**s,'selection_score':lo})
    valtab=pd.DataFrame(val_rows)
    eligible=valtab[valtab.n>=100].copy()
    chosen=eligible.sort_values(['selection_score','rate','n'],ascending=False).iloc[0].to_dict()
    chosen_model=fitted[chosen['model']]
    test['score']=chosen_model.predict_proba(test[features])[:,1]
    rule={'model':chosen['model'],'mode':chosen['mode'],'q':float(chosen['q']),'threshold':float(chosen['threshold'])}
    holdout,hold_sel=evaluate_rule(test,rule)
    benchmarks=[]
    for name in models:
        v=val.copy(); v['score']=v[f'score_{name}']
        t=test.copy(); t['score']=fitted[name].predict_proba(t[features])[:,1]
        sub=valtab[(valtab.model==name)&(valtab.n>=100)].sort_values(['selection_score','rate','n'],ascending=False).iloc[0]
        s,_=evaluate_rule(t,{'mode':sub['mode'],'threshold':float(sub.threshold)})
        benchmarks.append({'method':name,'mode':sub['mode'],'q':float(sub.q),'threshold':float(sub.threshold),**s})
    for col in ['target_exp','exp_gap','team_hit_prior_max']:
        v=val.copy();v['score']=v[col];t=test.copy();t['score']=t[col]
        vb=best_per_game(v); thr=float(vb.score.quantile(.90)); ts=best_per_game(t); s=stats(ts[ts.score>=thr])
        benchmarks.append({'method':f'heuristic_{col}','mode':'best','q':.90,'threshold':thr,**s})
    t=test.copy();t['score']=t.miss_streak_max + t.team_hit_prior_max
    cand=t[t.miss_streak_max>=4]; cand=best_per_game(cand) if len(cand) else cand
    benchmarks.append({'method':'miss_streak_ge4','mode':'best','q':None,'threshold':4,**stats(cand)})
    base=[]
    for y in [2024,2025]:
        d=df[df.year==y]
        for target in TARGETS:
            x=d[d.target==target]; base.append({'year':y,'target':target,**stats(x.assign(score=0))})
        base.append({'year':y,'target':'pooled_678',**stats(d.assign(score=0))})
    per_target=[]
    for t in TARGETS:
        x=hold_sel[hold_sel.target==t]; per_target.append({'target':t,**stats(x)})
    valchosen=val.copy(); valchosen['score']=valchosen[f"score_{chosen['model']}"]
    valstat,_=evaluate_rule(valchosen,rule)
    rng=np.random.default_rng(20260728); bygame=hold_sel.groupby('gid').label.max().to_numpy()
    boots=[]
    if len(bygame):
        for _ in range(5000): boots.append(float(rng.choice(bygame,size=len(bygame),replace=True).mean()))
    boot_ci=[float(np.quantile(boots,.025)),float(np.quantile(boots,.975))] if boots else [0,0]
    rate=holdout['rate']; lo=holdout['wilson95'][0]
    decision={}
    for odds,be in [(5,0.20),(7,1/7),(8,0.125)]:
        if lo>be: state='SUPPORTED'
        elif rate>be: state='POINT_ESTIMATE_ONLY'
        else: state='REJECTED'
        decision[f'{odds}x']={'break_even':be,'state':state,'point_rate':rate,'wilson95_lower':lo}
    overall='CAN_AT_8X_ONLY' if decision['8x']['state']!='REJECTED' else 'NO_VERIFIED_EDGE'
    if decision['7x']['state']!='REJECTED': overall='CAN_AT_7X_PLUS'
    if decision['5x']['state']!='REJECTED': overall='CAN_AT_5X_PLUS'
    result={
      'data':{'games':len(games),'years':YEARS,'candidates':len(df),'holdout_year':2025},
      'selection_rule':rule,'validation_2024':valstat,'holdout_2025':holdout,'bootstrap95_game_cluster':boot_ci,
      'per_target_holdout':per_target,'baselines':base,'benchmarks':benchmarks,
      'decision_by_odds':decision,'overall_decision':overall,
      'notes':['ties counted as losses','one best 6/7/8 candidate per game when mode=best','selection frozen on 2024; 2025 untouched']
    }
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    pd.DataFrame(benchmarks).to_csv(out/'benchmarks.csv',index=False)
    valtab.to_csv(out/'validation_grid.csv',index=False)
    hold_sel[['date','gid','target','score','label','away','home']].to_csv(out/'holdout_selections.csv',index=False)
    summary=f'''# MLB Highest-Scoring Inning Final Holdout Decision\n\n- Games: {len(games)} (2021-2025)\n- Frozen model: {rule}\n- 2024 validation: n={valstat['n']}, hit={valstat['rate']:.4%}, 95% CI={valstat['wilson95']}\n- 2025 untouched holdout: n={holdout['n']}, hit={holdout['rate']:.4%}, 95% CI={holdout['wilson95']}\n- 5x: {decision['5x']['state']}\n- 7x: {decision['7x']['state']}\n- 8x: {decision['8x']['state']}\n- Overall: {overall}\n'''
    (out/'summary.md').write_text(summary,encoding='utf-8')
    print(summary)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'artifacts/mlb_hsi_final')
