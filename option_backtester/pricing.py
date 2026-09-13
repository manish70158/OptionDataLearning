"""Black-Scholes pricing and premium estimation from VIX."""
import math
from scipy.stats import norm
from option_backtester.config import RISK_FREE_RATE, STRIKE_INTERVAL


def black_scholes_call(S, K, T, r, sigma):
    """Calculate Black-Scholes call option price.

    Args:
        S: Spot price
        K: Strike price
        T: Time to expiry in years
        r: Risk-free rate (annual)
        sigma: Implied volatility (annual, as decimal e.g. 0.20 for 20%)

    Returns:
        Call option premium
    """
    if T <= 0:
        return max(S - K, 0.0)
    if sigma <= 0:
        return max(S * math.exp(-r * T) - K * math.exp(-r * T), 0.0)

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(S, K, T, r, sigma):
    """Calculate Black-Scholes put option price.

    Args:
        S: Spot price
        K: Strike price
        T: Time to expiry in years
        r: Risk-free rate (annual)
        sigma: Implied volatility (annual, as decimal e.g. 0.20 for 20%)

    Returns:
        Put option premium
    """
    if T <= 0:
        return max(K - S, 0.0)
    if sigma <= 0:
        return max(K * math.exp(-r * T) - S * math.exp(-r * T), 0.0)

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def estimate_premium(spot, strike, vix, days_to_expiry, option_type, skew_factor=1.0):
    """Estimate option premium using VIX as implied volatility proxy.

    Args:
        spot: Current underlying price
        strike: Option strike price
        vix: VIX value (e.g. 15.0 for VIX at 15)
        days_to_expiry: Calendar days to expiry (use 0.5 for expiry day)
        option_type: 'call' or 'put'
        skew_factor: Multiplier for IV adjustment (>1 for puts, <1 for calls typically)

    Returns:
        Estimated option premium in points
    """
    sigma = (vix / 100.0) * skew_factor
    T = max(days_to_expiry, 0.5) / 365.0
    r = RISK_FREE_RATE

    if option_type == 'call':
        return black_scholes_call(spot, strike, T, r, sigma)
    elif option_type == 'put':
        return black_scholes_put(spot, strike, T, r, sigma)
    else:
        raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")


def calculate_atm_strike(spot, interval=None):
    """Round spot price to the nearest strike interval.

    Args:
        spot: Current underlying price
        interval: Strike interval (default: from config)

    Returns:
        Nearest strike price
    """
    if interval is None:
        interval = STRIKE_INTERVAL
    return int(math.floor(spot / interval + 0.5)) * interval
