# FII/PRO Option Strategy Backtester

Backtest NIFTY option strategies (Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, Strangle) against 6 years of historical data, segmented by FII View x PRO View combinations.

The system uses the proven insight that **FII and PRO positioning data from T-1 predicts next-day NIFTY movement patterns** — and maps each combination to the option strategy that would have generated the most profit.

## Background

This project builds on analysis of 1,488 trading days (Aug 2020 - Sep 2026) showing that specific FII/PRO view combinations reliably predict next-day directional moves:

| Signal | Days | Green% | Best Strategy |
|---|---|---|---|
| Mildly Bearish + Mildly Bearish | 11 | 100% | Bull Call Spread |
| Bullish + Strong Bullish | 134 | 36.5% | Straddle (high intraday range) |
| Neutral + Neutral | 179 | ~47% | Straddle |
| Bearish + Strong Bearish | 95 | ~47% | Bear Put Spread |
| Mildly Bearish + Strong Bearish | 49 | ~53% | Straddle |

Full analysis: [`FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md`](FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Run backtest on historical data
python -m option_backtester backtest

# Step 2: Generate profitability report
python -m option_backtester report

# Step 3: Get today's recommendation
python -m option_backtester recommend \
  --fii-view "Mildly Bearish" \
  --pro-view "Mildly Bearish" \
  --vix 18 \
  --nifty-spot 22000
```

## Commands

### `backtest` — Run historical simulation

Simulates all 6 option strategies across every trading day. Entry at market open, exit at market close. Premiums estimated via Black-Scholes using VIX as implied volatility.

```bash
python -m option_backtester backtest [OPTIONS]

Options:
  --csv PATH              Input CSV file (default: vix_fii_t1_intraday_daily_results.csv)
  --output PATH           Output results CSV (default: backtest_results.csv)
  --stop-loss {on,off}    Enable/disable stop loss (default: on)
```

Output: `backtest_results.csv` with 8,928 rows (1,488 days x 6 strategies), containing daily P&L, intraday max loss, and whether stop loss was triggered for each strategy.

### `report` — Generate profitability report

Produces a full analysis report with:
- **7x7 Summary Matrix** — best strategy per FII/PRO combination at a glance
- **Strategy Rankings** — all 6 strategies ranked by total P&L for each of the 48 combinations
- **Expiry vs Non-Expiry Divergence** — combinations where the optimal strategy differs on expiry days
- **VIX Regime Analysis** — how the best strategy changes across Low/Normal/Elevated/High VIX for high-frequency combinations

```bash
python -m option_backtester report [OPTIONS]

Options:
  --output-format {md,html,csv}  Report format (default: md)
  --output-dir PATH              Output directory (default: current dir)
  --backtest-results PATH        Input results CSV (default: backtest_results.csv)
```

Output formats:
- **md** — GitHub-flavored Markdown (`strategy_report.md`)
- **html** — Styled HTML with embedded heatmap charts (`strategy_report.html`)
- **csv** — Three separate CSV files (`strategy_rankings.csv`, `summary_matrix.csv`, `expiry_comparison.csv`)

### `recommend` — Daily strategy recommendation

Given today's FII View, PRO View, and VIX level, returns the historically best option strategy with confidence rating.

```bash
python -m option_backtester recommend [OPTIONS]

Required:
  --fii-view TEXT    Current FII view (e.g., "Neutral", "Bullish", "Mildly Bearish")
  --pro-view TEXT    Current PRO view
  --vix FLOAT        Current VIX level

Optional:
  --nifty-spot FLOAT     Current NIFTY price (for strike calculation)
  --backtest-results PATH  Input results CSV (default: backtest_results.csv)
```

Example output:
```
============================================================
  DAILY STRATEGY RECOMMENDATION
============================================================
  FII View:   Mildly Bearish
  PRO View:   Mildly Bearish
  VIX:        18.0
------------------------------------------------------------
  Strategy:   Bull Call Spread
  Confidence: Medium (11 historical days)
  Win Rate:   63.6%
  Avg P&L:    1.69 pts/day
  Expected:   -13.49 to 16.88 pts
  Total P&L:  18.63 pts (across 11 days)
------------------------------------------------------------
  NIFTY Spot: 22000
  Strikes:    Buy 22000 CE / Sell 22100 CE
------------------------------------------------------------
  Live premiums: Upstox not configured (backtest-only mode)
============================================================
```

Confidence levels:
- **High** — 30+ historical days for this combination
- **Medium** — 10-29 historical days
- **Low** — fewer than 10 historical days

## Strategies Tested

| Strategy | Type | Legs | Profits When |
|---|---|---|---|
| **Iron Condor** | Premium selling | 4 | Market stays in a narrow range |
| **Iron Butterfly** | Premium selling | 4 | Market stays near the open price |
| **Bull Call Spread** | Directional bullish | 2 | Market moves up |
| **Bear Put Spread** | Directional bearish | 2 | Market moves down |
| **Straddle** | Long volatility | 2 | Market makes a large move in either direction |
| **Strangle** | Long volatility | 2 | Market makes a very large move in either direction |

Default strike configuration (configurable in `config.py`):
- Iron Condor: short legs at ATM +/- 100pts, wings at +/- 200pts
- Iron Butterfly: sell ATM, buy wings at +/- 200pts
- Spreads: ATM to ATM + 100pts
- Strangle: OTM at +/- 200pts from ATM
- Strike interval: 50 points (NIFTY standard)

## How Premiums Are Estimated

Since historical option chain data is not available for the full 6-year period, premiums are estimated using the **Black-Scholes model** with:

- **Implied Volatility**: VIX value at market open (entry) and close (exit), divided by 100
- **Skew Adjustment**: OTM puts use 1.10x VIX (higher IV due to skew), OTM calls use 0.95x VIX
- **Time to Expiry**: Calculated from each day's position relative to the next weekly NIFTY expiry
- **Risk-Free Rate**: 6.5% (Indian 10Y government bond)
- **Slippage**: 2 NIFTY points per leg deducted from each trade

These are approximations. The absolute P&L numbers should be treated as estimates — **the relative ranking of strategies across FII/PRO combinations is the primary insight**.

## Key Findings from the Backtest

### Straddle dominates most combinations

Long Straddle is the best strategy for the majority of FII/PRO combinations. This is because NIFTY has significant intraday ranges (avg ~1%) that exceed the directional close-to-close moves (avg ~0.1-0.3%). Buying volatility captures these swings.

### When directional strategies win

- **Bull Call Spread** is best for strongly bullish signals: Mildly Bearish x Mildly Bearish (100% Green historically), and when FII is Bearish but PRO is Bullish (contrarian reversal)
- **Bear Put Spread** is best for high-conviction bearish signals: Bearish x Strong Bearish, and Strong Bearish x Bearish

### Premium selling strategies (Iron Condor, Iron Butterfly) underperform

Iron Condor and Iron Butterfly consistently rank 5th-6th across most combinations. NIFTY's daily ranges are large enough to breach the sold strikes on most days, making these strategies unprofitable in a daily entry/exit model.

### Expiry days diverge

Several combinations show different optimal strategies on expiry vs non-expiry days, driven by theta decay acceleration and gamma risk on expiry days.

## Stop Loss

The backtester includes **percentage-based stop loss** per strategy. The SL threshold is expressed as a percentage of the day's NIFTY spot price, so it automatically scales across the dataset (NIFTY ranged from ~11,000 in 2020 to ~25,000+ in 2026).

For example, a 0.25% SL = 28 pts when NIFTY was at 11,000, but 63 pts when NIFTY was at 25,000. This keeps risk proportional to the underlying price.

**Default stop loss thresholds:**

| Strategy | SL (% of spot) | SL Range (pts) | Rationale | SL Hit Rate |
|---|---|---|---|---|
| Iron Condor | 0.25% | 28–105 | ~50% of wing width | 7.3% |
| Iron Butterfly | 0.40% | 44–168 | ~40% of wing width | 5.7% |
| Bull Call Spread | 0.25% | 28–105 | ~50% of spread width | 3.6% |
| Bear Put Spread | 0.25% | 28–105 | ~50% of spread width | 0.1% |
| Straddle | 0.30% | 33–126 | ~35% of premium paid | 0.0% |
| Strangle | 0.20% | 22–84 | ~45% of premium paid | 0.0% |

Overall SL trigger rate: **2.8%** of all trades (248 out of 8,928). Average loss saved per SL event: **14.0 pts**.

Premium selling strategies (Iron Condor, Iron Butterfly) trigger SL most often because large intraday moves breach their short strikes. Long volatility strategies (Straddle, Strangle) rarely hit SL because their downside is limited to theta decay on flat days, which is gradual.

**How intraday max loss is calculated:**

The backtester evaluates the full strategy's P&L at two spot levels — the day's high and the day's low — and takes the worse result. This correctly handles hedged strategies where legs offset each other (e.g., in a Straddle, if spot rises the call gains while the put loses — the net effect is evaluated together, not per-leg independently).

**To disable stop loss:**
```bash
python -m option_backtester backtest --stop-loss off
```

**To customize thresholds**, edit `STOP_LOSS_PCT` in `option_backtester/config.py`.

## Upstox API Integration (Optional)

The `recommend` command can optionally show live option premiums from Upstox. This requires API credentials.

### Setup

Set environment variables:
```bash
export UPSTOX_API_KEY="your_api_key"
export UPSTOX_API_SECRET="your_api_secret"
export UPSTOX_ACCESS_TOKEN="your_access_token"
```

Or create `~/.upstox/config.json`:
```json
{
  "api_key": "your_api_key",
  "api_secret": "your_api_secret",
  "access_token": "your_access_token"
}
```

Environment variables take precedence over the config file. The access token expires daily and must be refreshed via the Upstox OAuth flow.

Without Upstox credentials, all backtest and report features work normally — only the live premium display in `recommend` is skipped.

## Project Structure

```
OptionDataLearning/
├── option_backtester/
│   ├── __init__.py          # Package init
│   ├── __main__.py          # Entry point for python -m
│   ├── cli.py               # CLI with backtest/report/recommend subcommands
│   ├── config.py            # Default parameters (strikes, slippage, thresholds)
│   ├── pricing.py           # Black-Scholes pricing, VIX-to-premium estimation
│   ├── strategies.py        # 6 strategy definitions, P&L and intraday loss calc
│   ├── backtester.py        # Data loader, DTE computation, simulation loop
│   ├── aggregator.py        # Group-by FII/PRO, expiry/VIX regime segmentation
│   ├── report.py            # Markdown/HTML/CSV report generation with charts
│   ├── upstox_client.py     # Upstox API client (auth, option chain, caching)
│   └── recommender.py       # Daily recommendation engine with confidence levels
├── vix_fii_t1_intraday_daily_results.csv   # 1,488 days of historical data
├── FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md  # Statistical analysis of all combinations
├── backtest_results.csv     # Generated: raw backtest output (8,928 rows, includes sl_hit column)
├── strategy_report.md       # Generated: full profitability report (Markdown)
├── strategy_report.html     # Generated: full profitability report (HTML with charts)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Data Format

The input CSV (`vix_fii_t1_intraday_daily_results.csv`) contains these key columns:

| Column | Description |
|---|---|
| `date` | Trading date |
| `nifty_open/high/low/close` | NIFTY OHLC prices |
| `vix_open/vix_close` | India VIX at open and close |
| `is_nifty_expiry` | 1 if weekly NIFTY expiry day, 0 otherwise |
| `fii_view` | FII positioning classification (Strong Bullish to Strong Bearish) |
| `pro_view` | PRO positioning classification (Strong Bullish to Strong Bearish) |
| `move_direction` | Actual intraday pattern (Down to Up, Top to Down, etc.) |
| `nifty_day` | Green or Red day |

The FII/PRO views are derived from T-1 (previous day) futures and options positioning data: net futures bought/sold, call OI changes, and put OI changes.

## Configuration

All defaults are in `option_backtester/config.py`:

| Parameter | Default | Description |
|---|---|---|
| `STRIKE_INTERVAL` | 50 | NIFTY strike gap in points |
| `RISK_FREE_RATE` | 0.065 | Annual risk-free rate for BS model |
| `SLIPPAGE_PER_LEG` | 2 | Points deducted per leg per trade |
| `CALL_SKEW_FACTOR` | 0.95 | IV multiplier for OTM calls |
| `PUT_SKEW_FACTOR` | 1.10 | IV multiplier for OTM puts |
| `IRON_CONDOR_SHORT_OFFSET` | 100 | Points from ATM for IC short strikes |
| `IRON_CONDOR_WING_WIDTH` | 100 | Width between IC short and long strikes |
| `IRON_BUTTERFLY_WING_WIDTH` | 200 | Wing width for Iron Butterfly |
| `SPREAD_WIDTH` | 100 | Width for Bull Call / Bear Put spreads |
| `STRANGLE_OFFSET` | 200 | Points from ATM for Strangle strikes |
| `STOP_LOSS_ENABLED` | True | Enable stop loss in backtest |
| `STOP_LOSS_PCT` | per-strategy | SL threshold as % of spot price (see Stop Loss section) |

VIX regime thresholds: Low (<15), Normal (15-20), Elevated (20-25), High (25+).

## Dependencies

- Python 3.10+
- pandas
- numpy
- scipy
- requests
- matplotlib
