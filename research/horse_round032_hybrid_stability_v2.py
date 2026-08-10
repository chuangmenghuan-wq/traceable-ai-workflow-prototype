from __future__ import annotations

import numpy as np
import horse_round032_hybrid_stability as r


def corrected_metrics(z):
    n = int(z.bets.sum()) if len(z) else 0
    net = float(z.net.sum()) if len(z) else 0.0
    liab = float(z.liability.sum()) if len(z) else 0.0
    if len(z):
        eq = z.net.cumsum().to_numpy(float)
        eq0 = np.r_[0.0, eq]
        peaks = np.maximum.accumulate(eq0)
        dd = float(np.max(peaks - eq0))
    else:
        dd = 0.0
    return {
        'n': n,
        'markets': int(len(z)),
        'net_pl': net,
        'pot': net / n if n else None,
        'rol': net / liab if liab else None,
        'maxdd': dd,
    }

r.metrics = corrected_metrics

if __name__ == '__main__':
    r.main()
