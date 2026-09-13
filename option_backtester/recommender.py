"""Daily recommendation engine based on backtest results."""
import logging
import pandas as pd
import numpy as np
from option_backtester.config import (
    CONFIDENCE_HIGH_MIN_DAYS, CONFIDENCE_MEDIUM_MIN_DAYS,
    IRON_CONDOR_SHORT_OFFSET, IRON_CONDOR_WING_WIDTH,
    IRON_BUTTERFLY_WING_WIDTH, SPREAD_WIDTH, STRANGLE_OFFSET,
)

logger = logging.getLogger(__name__)


def _get_confidence(day_count):
    """Determine confidence level based on sample size."""
    if day_count >= CONFIDENCE_HIGH_MIN_DAYS:
        return 'High'
    elif day_count >= CONFIDENCE_MEDIUM_MIN_DAYS:
        return 'Medium'
    else:
        return 'Low'


def get_recommendation(fii_view, pro_view, vix, backtest_results_df):
    """Look up the best strategy for a FII/PRO combination.

    Args:
        fii_view: Current FII view string (e.g., 'Neutral', 'Bullish')
        pro_view: Current PRO view string
        vix: Current VIX level
        backtest_results_df: Raw backtest results DataFrame

    Returns:
        dict with recommendation details
    """
    # Filter results for this combination
    combo = backtest_results_df[
        (backtest_results_df['fii_view'] == fii_view) &
        (backtest_results_df['pro_view'] == pro_view)
    ]

    if combo.empty:
        return {
            'fii_view': fii_view,
            'pro_view': pro_view,
            'vix': vix,
            'strategy': None,
            'message': f'No historical data for {fii_view} × {pro_view}',
            'confidence': 'None',
        }

    # Aggregate P&L by strategy
    strategy_stats = combo.groupby('strategy_name').agg(
        total_pnl=('daily_pnl', 'sum'),
        avg_pnl=('daily_pnl', 'mean'),
        std_pnl=('daily_pnl', 'std'),
        win_rate=('daily_pnl', lambda x: (x > 0).mean() * 100),
        day_count=('daily_pnl', 'count'),
    ).reset_index()

    # Best strategy by total P&L
    best_idx = strategy_stats['total_pnl'].idxmax()
    best = strategy_stats.loc[best_idx]

    day_count = int(best['day_count'])
    avg_pnl = best['avg_pnl']
    std_pnl = best['std_pnl'] if not pd.isna(best['std_pnl']) else 0

    return {
        'fii_view': fii_view,
        'pro_view': pro_view,
        'vix': vix,
        'strategy': best['strategy_name'],
        'total_pnl': best['total_pnl'],
        'avg_daily_pnl': avg_pnl,
        'expected_pnl_low': avg_pnl - std_pnl,
        'expected_pnl_high': avg_pnl + std_pnl,
        'win_rate': best['win_rate'],
        'day_count': day_count,
        'confidence': _get_confidence(day_count),
    }


def _get_strike_description(strategy_name, nifty_spot):
    """Generate strike structure description relative to spot."""
    from option_backtester.pricing import calculate_atm_strike
    atm = calculate_atm_strike(nifty_spot)

    descriptions = {
        'Iron Condor': (
            f'Sell {atm + IRON_CONDOR_SHORT_OFFSET} CE / Buy {atm + IRON_CONDOR_SHORT_OFFSET + IRON_CONDOR_WING_WIDTH} CE / '
            f'Sell {atm - IRON_CONDOR_SHORT_OFFSET} PE / Buy {atm - IRON_CONDOR_SHORT_OFFSET - IRON_CONDOR_WING_WIDTH} PE'
        ),
        'Iron Butterfly': (
            f'Sell {atm} CE / Sell {atm} PE / '
            f'Buy {atm + IRON_BUTTERFLY_WING_WIDTH} CE / Buy {atm - IRON_BUTTERFLY_WING_WIDTH} PE'
        ),
        'Bull Call Spread': f'Buy {atm} CE / Sell {atm + SPREAD_WIDTH} CE',
        'Bear Put Spread': f'Buy {atm} PE / Sell {atm - SPREAD_WIDTH} PE',
        'Straddle': f'Buy {atm} CE / Buy {atm} PE',
        'Strangle': f'Buy {atm + STRANGLE_OFFSET} CE / Buy {atm - STRANGLE_OFFSET} PE',
    }
    return descriptions.get(strategy_name, 'N/A')


def format_recommendation(rec, nifty_spot=None):
    """Format a recommendation as a readable text block.

    Args:
        rec: dict from get_recommendation
        nifty_spot: Optional current NIFTY spot for strike calculation

    Returns:
        Formatted string
    """
    lines = ['=' * 60]
    lines.append('  DAILY STRATEGY RECOMMENDATION')
    lines.append('=' * 60)
    lines.append(f'  FII View:   {rec["fii_view"]}')
    lines.append(f'  PRO View:   {rec["pro_view"]}')
    lines.append(f'  VIX:        {rec["vix"]}')
    lines.append('-' * 60)

    if rec.get('strategy') is None:
        lines.append(f'  {rec.get("message", "No recommendation available")}')
        lines.append('=' * 60)
        return '\n'.join(lines)

    lines.append(f'  Strategy:   {rec["strategy"]}')
    lines.append(f'  Confidence: {rec["confidence"]} ({rec["day_count"]} historical days)')
    lines.append(f'  Win Rate:   {rec["win_rate"]:.1f}%')
    lines.append(f'  Avg P&L:    {rec["avg_daily_pnl"]:.2f} pts/day')
    lines.append(f'  Expected:   {rec["expected_pnl_low"]:.2f} to {rec["expected_pnl_high"]:.2f} pts')
    lines.append(f'  Total P&L:  {rec["total_pnl"]:.2f} pts (across {rec["day_count"]} days)')

    if nifty_spot:
        lines.append('-' * 60)
        lines.append(f'  NIFTY Spot: {nifty_spot}')
        strikes = _get_strike_description(rec['strategy'], nifty_spot)
        lines.append(f'  Strikes:    {strikes}')

    # Live mode info
    lines.append('-' * 60)
    live_info = _try_live_premiums(rec, nifty_spot)
    if live_info:
        lines.append(live_info)
    else:
        lines.append('  Live premiums: Upstox not configured (backtest-only mode)')

    lines.append('=' * 60)
    return '\n'.join(lines)


def _try_live_premiums(rec, nifty_spot):
    """Attempt to fetch live premiums from Upstox. Returns info string or None."""
    if not nifty_spot:
        return None

    try:
        from option_backtester.upstox_client import UpstoxClient
        client = UpstoxClient()
        expiry = UpstoxClient.resolve_nearest_expiry('NIFTY', 'weekly')
        chain = client.fetch_option_chain('NSE_INDEX|Nifty 50', expiry)
        if chain:
            from option_backtester.pricing import calculate_atm_strike
            atm = calculate_atm_strike(nifty_spot)
            atm_data = next((r for r in chain if r.get('strike_price') == atm), None)
            if atm_data:
                return (
                    f'  Live ATM premiums (expiry {expiry}):\n'
                    f'    CE: {atm_data.get("call_ltp", "N/A")} | '
                    f'PE: {atm_data.get("put_ltp", "N/A")}'
                )
        return '  Live premiums: Could not fetch option chain'
    except Exception:
        return None
