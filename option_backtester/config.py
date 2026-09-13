"""Default configuration for the option backtester."""

# Strike selection
STRIKE_INTERVAL = 50  # NIFTY strike interval in points
RISK_FREE_RATE = 0.065  # Annual risk-free rate (Indian 10Y govt bond ~6.5%)

# Slippage
SLIPPAGE_PER_LEG = 2  # Points deducted per leg per trade

# IV skew adjustments applied to VIX for OTM options
CALL_SKEW_FACTOR = 0.95  # OTM calls typically have lower IV than ATM
PUT_SKEW_FACTOR = 1.10   # OTM puts typically have higher IV (skew)

# Default strike offsets (points from ATM)
IRON_CONDOR_SHORT_OFFSET = 100
IRON_CONDOR_WING_WIDTH = 100
IRON_BUTTERFLY_WING_WIDTH = 200
SPREAD_WIDTH = 100
STRANGLE_OFFSET = 200

# VIX regime thresholds
VIX_REGIME_THRESHOLDS = {
    'Low': (0, 15),
    'Normal': (15, 20),
    'Elevated': (20, 25),
    'High': (25, float('inf')),
}

# Confidence thresholds based on sample size (number of days)
CONFIDENCE_HIGH_MIN_DAYS = 30
CONFIDENCE_MEDIUM_MIN_DAYS = 10

# Low sample size flag threshold
LOW_SAMPLE_THRESHOLD = 5

# Stop loss settings (percentage of spot price)
# If intraday loss exceeds (spot × SL%), position is closed at SL level
# Percentage-based SL scales automatically with NIFTY level across the dataset
STOP_LOSS_ENABLED = True
STOP_LOSS_PCT = {
    'Iron Condor': 0.25,       # 0.25% of spot (~50pts at NIFTY 20000)
    'Iron Butterfly': 0.40,    # 0.40% of spot (~80pts at NIFTY 20000)
    'Bull Call Spread': 0.25,  # 0.25% of spot
    'Bear Put Spread': 0.25,   # 0.25% of spot
    'Straddle': 0.30,          # 0.30% of spot (~60pts at NIFTY 20000)
    'Strangle': 0.20,          # 0.20% of spot (~40pts at NIFTY 20000)
    'Short Straddle': 0.50,    # 0.50% of spot — naked selling needs wider SL
    'Short Strangle': 0.40,    # 0.40% of spot — OTM gives some buffer
}

# Move-based exit: exit when NIFTY moves X% from open (either direction)
# This captures profits from the intraday swing before reversal
# Only applies when --move-exit is passed via CLI
MOVE_EXIT_PCT = 0.50  # Exit when NIFTY moves 0.50% from open (~100 pts at NIFTY 20000)

# Upstox cache TTL in seconds
UPSTOX_CACHE_TTL = 300  # 5 minutes

# FII and PRO view categories (ordered for matrix display)
FII_VIEWS = [
    'Strong Bullish', 'Bullish', 'Mildly Bullish', 'Neutral',
    'Mildly Bearish', 'Bearish', 'Strong Bearish',
]
PRO_VIEWS = [
    'Strong Bullish', 'Bullish', 'Mildly Bullish', 'Neutral',
    'Mildly Bearish', 'Bearish', 'Strong Bearish',
]
