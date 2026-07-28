#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

START='2026-03-25'
END='2026-07-27'
TARGETS=(6,7,8)

def get_json(url):
    req=urllib.request.Request(url,headers={'User-Agent':'FAU-MLB-HSI-2026/1.0'})
    with urllib.request.urlopen(req,timeout=120) as r:
        return json.loads(r.read().decode('utf-8'))

def wilson(h,n,z=1.959963984540054):
    if n==0:return [0.0,0.0]
    p=h/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    m=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
    return [max(0,c-m),min(1,c+m)]

def stat(h,n):
    p=h/n if n else 0.0
    return {'n':n,'hits':h,'rate':p,'wilson95':wilson(h,n),'fair_odds':(1/p if p else None),'roi_8x':p*8-1}

def main(outdir):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    params={'sportId':1,'gameTypes':'R','startDate':START,'endDate':END,'hydrate':'linescore'}
    url='https://statsapi.mlb.com/api/v1/schedule?'+urllib.parse.urlencode(params)
    data=get_json(url)
    games=[]
    per_target=defaultdict(lambda:[0,0])
    team_target=defaultdict(lambda:[0,0])
    tie_count=0
    for date in data.get('dates',[]):
        for g in date.get('games',[]):
            status=g.get('status',{})
            if status.get('abstractGameState')!='Final':
                continue
            if g.get('gameType')!='R':
                continue
            innings=[0]*9
            for inn in g.get('linescore',{}).get('innings',[]):
                num=inn.get('num')
                if isinstance(num,int) and 1<=num<=9:
                    a=inn.get('away',{}).get('runs') or 0
                    h=inn.get('home',{}).get('runs') or 0
                    innings[num-1]=int(a)+int(h)
            if not any(True for _ in innings):
                # zero-score game still valid, but schedule linescore should have inning records
                if not g.get('linescore',{}).get('innings'):
                    continue
            mx=max(innings); leaders=[i+1 for i,v in enumerate(innings) if v==mx]
            winner=leaders[0] if len(leaders)==1 else None
            if winner is None: tie_count+=1
            away=g['teams']['away']['team']['name']; home=g['teams']['home']['team']['name']
            games.append({'gamePk':g['gamePk'],'date':g['gameDate'][:10],'away':away,'home':home,'innings':innings,'winner':winner})
            for t in TARGETS:
                per_target[t][1]+=1
                if winner==t: per_target[t][0]+=1
                for team in (away,home):
                    team_target[(team,t)][1]+=1
                    if winner==t: team_target[(team,t)][0]+=1
    per={str(t):stat(*per_target[t]) for t in TARGETS}
    team_rows=[]
    for (team,t),(h,n) in team_target.items():
        row={'team':team,'target':t,**stat(h,n)}
        team_rows.append(row)
    team_rows.sort(key=lambda r:(r['rate'],r['n']),reverse=True)
    eligible60=[r for r in team_rows if r['n']>=60]
    eligible80=[r for r in team_rows if r['n']>=80]
    result={
      'cutoff':END,'start':START,'games':len(games),'tie_count':tie_count,
      'tie_rate':tie_count/len(games) if games else 0,
      'per_target':per,
      'top_team_target_min60':eligible60[:15],
      'top_team_target_min80':eligible80[:15],
      'best_target':max(per.items(),key=lambda kv:kv[1]['rate']),
      'best_team_target_min80':eligible80[0] if eligible80 else None,
      'notes':['regular season only','completed games only','innings 1-9','tie for highest counts as loss']
    }
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'games.json').write_text(json.dumps(games,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'artifacts/mlb_hsi_2026_current')
