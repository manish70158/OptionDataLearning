"""Option strategy definitions and P&L calculation."""
from dataclasses import dataclass, field
from typing import List
from option_backtester.pricing import estimate_premium, calculate_atm_strike
from option_backtester.config import (
    IRON_CONDOR_SHORT_OFFSET, IRON_CONDOR_WING_WIDTH,
    IRON_BUTTERFLY_WING_WIDTH, SPREAD_WIDTH, STRANGLE_OFFSET,
    SLIPPAGE_PER_LEG, CALL_SKEW_FACTOR, PUT_SKEW_FACTOR,
)


@dataclass
class StrategyLeg:
    """A single leg of an option strategy."""
    option_type: str      # 'call' or 'put'
    strike_offset: int    # Points from ATM (positive = OTM call / ITM put, negative = opposite)
    position: str         # 'long' or 'short'


@dataclass
class Strategy:
    """A multi-leg option strategy."""
    name: str
    legs: List[StrategyLeg] = field(default_factory=list)


def iron_condor(short_offset=IRON_CONDOR_SHORT_OFFSET, wing_width=IRON_CONDOR_WING_WIDTH):
    """Create an Iron Condor strategy.

    Sell OTM call + sell OTM put, buy further OTM call + buy further OTM put.
    """
    return Strategy(
        name='Iron Condor',
        legs=[
            StrategyLeg('call', short_offset, 'short'),
            StrategyLeg('call', short_offset + wing_width, 'long'),
            StrategyLeg('put', -short_offset, 'short'),
            StrategyLeg('put', -(short_offset + wing_width), 'long'),
        ],
    )


def iron_butterfly(wing_width=IRON_BUTTERFLY_WING_WIDTH):
    """Create an Iron Butterfly strategy.

    Sell ATM call + sell ATM put, buy OTM call + buy OTM put.
    """
    return Strategy(
        name='Iron Butterfly',
        legs=[
            StrategyLeg('call', 0, 'short'),
            StrategyLeg('put', 0, 'short'),
            StrategyLeg('call', wing_width, 'long'),
            StrategyLeg('put', -wing_width, 'long'),
        ],
    )


def bull_call_spread(width=SPREAD_WIDTH):
    """Create a Bull Call Spread strategy.

    Buy ATM call, sell OTM call.
    """
    return Strategy(
        name='Bull Call Spread',
        legs=[
            StrategyLeg('call', 0, 'long'),
            StrategyLeg('call', width, 'short'),
        ],
    )


def bear_put_spread(width=SPREAD_WIDTH):
    """Create a Bear Put Spread strategy.

    Buy ATM put, sell OTM put.
    """
    return Strategy(
        name='Bear Put Spread',
        legs=[
            StrategyLeg('put', 0, 'long'),
            StrategyLeg('put', -width, 'short'),
        ],
    )


def straddle():
    """Create a Long Straddle strategy.

    Buy ATM call + buy ATM put.
    """
    return Strategy(
        name='Straddle',
        legs=[
            StrategyLeg('call', 0, 'long'),
            StrategyLeg('put', 0, 'long'),
        ],
    )


def strangle(offset=STRANGLE_OFFSET):
    """Create a Long Strangle strategy.

    Buy OTM call + buy OTM put.
    """
    return Strategy(
        name='Strangle',
        legs=[
            StrategyLeg('call', offset, 'long'),
            StrategyLeg('put', -offset, 'long'),
        ],
    )


def short_straddle():
    """Create a Short Straddle strategy.

    Sell ATM call + sell ATM put. Naked premium selling — profits on flat days.
    """
    return Strategy(
        name='Short Straddle',
        legs=[
            StrategyLeg('call', 0, 'short'),
            StrategyLeg('put', 0, 'short'),
        ],
    )


def short_strangle(offset=STRANGLE_OFFSET):
    """Create a Short Strangle strategy.

    Sell OTM call + sell OTM put. Naked premium selling with wider range.
    """
    return Strategy(
        name='Short Strangle',
        legs=[
            StrategyLeg('call', offset, 'short'),
            StrategyLeg('put', -offset, 'short'),
        ],
    )


def get_all_strategies():
    """Return a list of all 8 strategy instances with default parameters."""
    return [
        iron_condor(),
        iron_butterfly(),
        bull_call_spread(),
        bear_put_spread(),
        straddle(),
        strangle(),
        short_straddle(),
        short_strangle(),
    ]


def _get_skew_factor(leg):
    """Determine skew factor based on leg moneyness."""
    if leg.strike_offset > 0 and leg.option_type == 'call':
        return CALL_SKEW_FACTOR  # OTM call
    elif leg.strike_offset < 0 and leg.option_type == 'put':
        return PUT_SKEW_FACTOR  # OTM put
    return 1.0  # ATM


def _price_leg(leg, spot, atm_strike, vix, days_to_expiry):
    """Price a single leg given market conditions."""
    strike = atm_strike + leg.strike_offset
    skew = _get_skew_factor(leg)
    premium = estimate_premium(spot, strike, vix, days_to_expiry, leg.option_type, skew)
    return premium


def calculate_strategy_pnl(strategy, spot_open, spot_close, vix_open, vix_close,
                           days_to_expiry, slippage_per_leg=SLIPPAGE_PER_LEG):
    """Calculate daily P&L for a strategy.

    Entry at open (using spot_open, vix_open), exit at close (using spot_close, vix_close).
    """
    atm_strike = calculate_atm_strike(spot_open)

    # For exit pricing, DTE is reduced by ~1 day (intraday fraction)
    exit_dte = max(days_to_expiry - 0.7, 0.1)

    total_pnl = 0.0
    num_legs = len(strategy.legs)

    for leg in strategy.legs:
        entry_premium = _price_leg(leg, spot_open, atm_strike, vix_open, days_to_expiry)
        exit_premium = _price_leg(leg, spot_close, atm_strike, vix_close, exit_dte)

        if leg.position == 'long':
            # Long: pay premium at entry, receive premium at exit
            leg_pnl = exit_premium - entry_premium
        else:
            # Short: receive premium at entry, pay premium at exit
            leg_pnl = entry_premium - exit_premium

        total_pnl += leg_pnl

    # Deduct slippage for all legs (entry + exit = 2 transactions per leg)
    total_pnl -= slippage_per_leg * num_legs

    return total_pnl


def calculate_intraday_max_loss(strategy, spot_open, spot_high, spot_low,
                                vix_open, days_to_expiry):
    """Calculate worst-case intraday P&L.

    Evaluates the entire strategy's P&L at spot_high and spot_low separately,
    then returns the worse of the two. This correctly handles hedged strategies
    where legs offset each other (e.g., straddle: if spot rises, call gains
    but put loses — the net effect is evaluated together).
    """
    atm_strike = calculate_atm_strike(spot_open)

    worst_pnl = 0.0

    # Evaluate strategy P&L at each extreme spot level
    for extreme_spot in [spot_high, spot_low]:
        total_pnl = 0.0
        for leg in strategy.legs:
            entry_premium = _price_leg(leg, spot_open, atm_strike, vix_open, days_to_expiry)
            extreme_premium = _price_leg(leg, extreme_spot, atm_strike, vix_open, days_to_expiry)

            if leg.position == 'long':
                total_pnl += extreme_premium - entry_premium
            else:
                total_pnl += entry_premium - extreme_premium

        total_pnl -= SLIPPAGE_PER_LEG * len(strategy.legs)
        worst_pnl = min(worst_pnl, total_pnl)

    return worst_pnl


def calculate_intraday_max_profit(strategy, spot_open, spot_high, spot_low,
                                  vix_open, days_to_expiry):
    """Calculate best-case intraday P&L.

    Evaluates the entire strategy's P&L at spot_high and spot_low separately,
    then returns the better of the two.
    """
    atm_strike = calculate_atm_strike(spot_open)

    best_pnl = 0.0

    for extreme_spot in [spot_high, spot_low]:
        total_pnl = 0.0
        for leg in strategy.legs:
            entry_premium = _price_leg(leg, spot_open, atm_strike, vix_open, days_to_expiry)
            extreme_premium = _price_leg(leg, extreme_spot, atm_strike, vix_open, days_to_expiry)

            if leg.position == 'long':
                total_pnl += extreme_premium - entry_premium
            else:
                total_pnl += entry_premium - extreme_premium

        total_pnl -= SLIPPAGE_PER_LEG * len(strategy.legs)
        best_pnl = max(best_pnl, total_pnl)

    return best_pnl


def calculate_pnl_at_spot(strategy, spot_open, spot_exit, vix_open, days_to_expiry):
    """Calculate strategy P&L if exited at a specific spot level.

    Used for move-based exit: when NIFTY hits a threshold level, compute
    what the strategy P&L would be at that moment.
    """
    atm_strike = calculate_atm_strike(spot_open)
    total_pnl = 0.0

    for leg in strategy.legs:
        entry_premium = _price_leg(leg, spot_open, atm_strike, vix_open, days_to_expiry)
        exit_premium = _price_leg(leg, spot_exit, atm_strike, vix_open, days_to_expiry)

        if leg.position == 'long':
            total_pnl += exit_premium - entry_premium
        else:
            total_pnl += entry_premium - exit_premium

    total_pnl -= SLIPPAGE_PER_LEG * len(strategy.legs)
    return total_pnl
