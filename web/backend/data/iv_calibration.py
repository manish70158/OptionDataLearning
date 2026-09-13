"""Implied-volatility calibration from observed option close prices.

Given the spot at day close, strike, option premium (close), DTE, and option
type, back out the implied volatility that reproduces the premium via
Black-Scholes. Used to persist a per-contract, per-day IV so backtests can
price the same option intraday at a spot-varying but IV-consistent level —
far more accurate than a single VIX-derived guess.
"""
from __future__ import annotations

import math
from typing import Optional

from option_backtester.pricing import black_scholes_call, black_scholes_put
from option_backtester.config import RISK_FREE_RATE


def implied_vol(
    spot: float,
    strike: float,
    market_price: float,
    days_to_expiry: float,
    option_type: str,
    r: float = RISK_FREE_RATE,
) -> Optional[float]:
    """Return implied volatility (as decimal, e.g. 0.18 for 18%) or None if
    the market price is arbitrage-violating or the search fails to converge.
    """
    if market_price <= 0 or spot <= 0 or strike <= 0:
        return None
    T = max(days_to_expiry, 0.5) / 365.0
    # Intrinsic bounds — if market price is below intrinsic (rare, usually stale
    # quote), return None so the caller falls back to a default IV.
    intrinsic = max(spot - strike, 0.0) if option_type == "call" else max(strike - spot, 0.0)
    if market_price < intrinsic * math.exp(-r * T) - 0.01:
        return None

    price_fn = black_scholes_call if option_type == "call" else black_scholes_put

    lo, hi = 0.005, 5.0  # 0.5% – 500% IV bracket
    p_lo = price_fn(spot, strike, T, r, lo)
    p_hi = price_fn(spot, strike, T, r, hi)
    # Ensure the market price is bracketed
    if not (min(p_lo, p_hi) - 1e-6 <= market_price <= max(p_lo, p_hi) + 1e-6):
        # Extrapolation isn't reliable; fail out.
        return None

    for _ in range(60):  # bisection — plenty of precision in 60 iterations
        mid = 0.5 * (lo + hi)
        p_mid = price_fn(spot, strike, T, r, mid)
        if abs(p_mid - market_price) < 1e-4:
            return mid
        if (p_lo - market_price) * (p_mid - market_price) < 0:
            hi, p_hi = mid, p_mid
        else:
            lo, p_lo = mid, p_mid
    return 0.5 * (lo + hi)
