from __future__ import annotations

import horse_round035_results_recovery_v2 as v2

base = v2.base
_original_parse_daily_ratings = base.parse_daily_ratings
_original_recover_august = base.recover_august
SA_BY_UPPER = {str(x).strip().upper(): x for x in base.SA_TRACKS}


def fixed_parse_daily_ratings(raw, date):
    x, qa = _original_parse_daily_ratings(raw, date)
    if not x.empty:
        x['track'] = x['track'].map(lambda s: SA_BY_UPPER.get(str(s).strip().upper(), str(s).strip()))
        sa = x[x.track.isin(base.SA_TRACKS)]
        qa['sa_markets'] = int(sa.market_id.nunique())
        qa['sa_r2_rows'] = int(len(sa[sa.model_rank.eq(2)]))
    return x, qa


def fixed_recover_august(validation_ok):
    aug, day_qa, market_qa = _original_recover_august(validation_ok)
    for rec in day_qa:
        if rec.get('ratings_http_status') == 200 and rec.get('sa_r2_rows') == 0:
            rec['status'] = 'RECOVERED'
            rec['recovery_note'] = 'NO_SA_RACES'
    return aug, day_qa, market_qa


base.parse_daily_ratings = fixed_parse_daily_ratings
base.recover_august = fixed_recover_august

if __name__ == '__main__':
    base.main()
