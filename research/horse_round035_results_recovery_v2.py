from __future__ import annotations

import re

import horse_round035_results_recovery as base

_original_get_market_result = base.get_market_result


def api_market_id(market_id: str) -> str:
    s = str(market_id).strip()
    # Kash historical CSV stores Betfair market 1.259574031 as 259574031.
    # Daily ratings may already retain the canonical `1.` prefix.
    if s.startswith('1.'):
        return s
    if re.fullmatch(r'\d+', s):
        return '1.' + s
    return s


def fixed_get_market_result(market_id: str):
    result, qa = _original_get_market_result(api_market_id(market_id))
    qa['source_market_id'] = str(market_id)
    qa['api_market_id'] = api_market_id(market_id)
    return result, qa


base.get_market_result = fixed_get_market_result

if __name__ == '__main__':
    base.main()
