## 1. Project Setup

- [x] 1.1 Create `option_backtester/` package directory with `__init__.py` and `config.py` containing default parameters (strike interval=50, risk-free rate=0.065, slippage=2 points/leg, skew factors, VIX regime thresholds). Verify by importing the package and accessing config values.
- [x] 1.2 Create `requirements.txt` with `pandas`, `numpy`, `scipy`, `requests`, `matplotlib`. Verify by running `pip install -r requirements.txt` successfully.
- [x] 1.3 Create `cli.py` with argparse skeleton supporting subcommands: `backtest`, `report`, `recommend`. Verify by running `python -m option_backtester --help` and seeing all three subcommands listed.

## 2. Black-Scholes Pricing Engine

- [x] 2.1 Implement `pricing.py` with `black_scholes_call(S, K, T, r, sigma)` and `black_scholes_put(S, K, T, r, sigma)` functions using scipy.stats.norm.cdf. Verify by testing known values: BS call with S=100, K=100, T=1, r=0.05, sigma=0.2 should return ~10.45.
- [x] 2.2 Add `estimate_premium(spot, strike, vix, days_to_expiry, option_type, skew_factor)` function that converts VIX to IV, calculates T from days_to_expiry, and calls the appropriate BS function. Verify with a test: spot=22000, strike=22100, vix=15, dte=3, type=call returns a positive premium less than 200 points.
- [x] 2.3 Add `calculate_atm_strike(spot, interval=50)` function that rounds spot to the nearest strike interval. Verify: 22234→22250, 22225→22250, 22224→22200.

## 3. Strategy Definitions

- [x] 3.1 Implement `strategies.py` with a `StrategyLeg` dataclass (option_type: call/put, strike_offset: int, position: long/short) and a `Strategy` class that holds a list of legs and a name. Verify by constructing an Iron Condor with 4 legs and asserting leg count and types.
- [x] 3.2 Define all 6 strategy factory functions: `iron_condor(short_offset=100, wing_width=100)`, `iron_butterfly(wing_width=200)`, `bull_call_spread(width=100)`, `bear_put_spread(width=100)`, `straddle()`, `strangle(offset=200)`. Each returns a Strategy with correct legs. Verify each factory produces the correct number of legs with correct option types and positions.
- [x] 3.3 Add `calculate_strategy_pnl(strategy, spot_open, spot_close, vix_open, vix_close, days_to_expiry, slippage_per_leg)` function that prices all legs at entry and exit, computes net P&L after slippage. Verify: Iron Condor on a flat day (open=22000, close=22010, vix=15) returns positive P&L; on a big move day (open=22000, close=22500) returns negative P&L.
- [x] 3.4 Add `calculate_intraday_max_loss(strategy, spot_open, spot_high, spot_low, vix_open, days_to_expiry)` that computes worst-case P&L using high for short calls and low for short puts. Verify: returns a worse (more negative) value than close P&L when intraday range exceeds close-to-open move.

## 4. Core Backtester

- [x] 4.1 Implement `backtester.py` with `load_data(csv_path)` that reads `vix_fii_t1_intraday_daily_results.csv` into a pandas DataFrame, parses dates, and validates required columns exist. Verify by loading the CSV and asserting 1,488 rows and presence of `nifty_open`, `fii_view`, `pro_view` columns.
- [x] 4.2 Add `compute_days_to_expiry(df)` that calculates days to the next expiry for each row. Use the `is_nifty_expiry` column: count forward from each row to the next row where `is_nifty_expiry==1`. Verify: an expiry day gets dte=0 (use 0.5 for pricing), the day before expiry gets dte=1.
- [x] 4.3 Implement `run_backtest(df, strategies, config)` that iterates over each row, applies each strategy, computes daily P&L and intraday max loss, and returns a results DataFrame with columns: date, fii_view, pro_view, is_expiry, strategy_name, daily_pnl, intraday_max_loss, vix_open. Verify by running on 10 sample rows and checking output has 60 result rows (10 days × 6 strategies).

## 5. Aggregation Engine

- [x] 5.1 Implement `aggregator.py` with `aggregate_results(results_df)` that groups by (fii_view, pro_view, strategy_name) and computes: total_pnl, avg_daily_pnl, win_rate, max_single_day_loss, max_consecutive_drawdown, sharpe_ratio (avg/std), day_count. Verify by passing a known results set and checking computed metrics match manual calculation.
- [x] 5.2 Add `aggregate_by_expiry(results_df)` that produces three aggregation sets per group: combined, expiry-only (is_expiry==1), non-expiry-only (is_expiry==0). Verify: for Neutral×Bearish, output contains 18 entries (6 strategies × 3 segments).
- [x] 5.3 Add `aggregate_by_vix_regime(results_df, thresholds)` that adds a vix_regime column based on thresholds (Low<15, Normal 15-20, Elevated 20-25, High≥25) and aggregates by (fii_view, pro_view, strategy_name, vix_regime). Verify by checking that a day with vix_open=18 falls in "Normal" regime.
- [x] 5.4 Add `flag_low_sample(aggregated_df, min_days=5)` that adds a `low_sample` boolean column. Verify: a group with 3 days gets True, a group with 30 days gets False.

## 6. Report Generator

- [x] 6.1 Implement `report.py` with `generate_strategy_rankings(aggregated_df)` that for each FII/PRO combination produces a table of 6 strategies sorted by total_pnl descending. Verify by checking the output for Neutral×Neutral has 6 rows in descending P&L order.
- [x] 6.2 Add `generate_summary_matrix(aggregated_df)` that produces a 7×7 matrix (FII view rows × PRO view columns) with the best strategy name, total P&L, and win rate in each cell. Mark cells with <5 days with asterisk. Verify: matrix has 7 rows, 7 columns, unobserved cells show "N/A".
- [x] 6.3 Add `generate_expiry_comparison(expiry_aggregated_df)` that identifies FII/PRO combinations where the best strategy differs between expiry and non-expiry days (both segments ≥3 days). Output a divergence table. Verify by checking output only includes combinations meeting the minimum day threshold.
- [x] 6.4 Add `generate_vix_regime_section(vix_aggregated_df)` that for combinations with ≥30 total days shows optimal strategy per VIX regime. Verify: Neutral×Neutral appears in output, a combination with 10 days does not.
- [x] 6.5 Add `write_markdown_report(sections, output_path)` that composes all sections into a single GFM markdown file. Verify by checking the output file exists and contains expected headers (## Strategy Rankings, ## Summary Matrix, etc.).
- [x] 6.6 Add `write_html_report(sections, charts, output_path)` that generates an HTML file with styled tables and embedded matplotlib charts (bar chart of strategy P&L per combination, heatmap for summary matrix). Verify by checking the HTML file contains `<table>` elements and base64 image tags.
- [x] 6.7 Add `write_csv_export(sections, output_dir)` that writes separate CSV files for strategy rankings, summary matrix, and expiry comparison. Verify by checking 3 CSV files are created with correct headers.

## 7. Upstox API Client

- [x] 7.1 Implement `upstox_client.py` with `UpstoxClient` class that reads credentials from env vars or `~/.upstox/config.json` (env vars take precedence). Raise a clear error with setup instructions if no credentials found. Verify by instantiating with env vars set and checking no error is raised.
- [x] 7.2 Add `fetch_option_chain(underlying, expiry_date)` method that calls the Upstox option chain API endpoint and returns a list of strike-level dicts with LTP, OI, volume, Greeks. Add retry logic for HTTP 429 (up to 3 retries with backoff). Verify with a mock: mock a 429 response followed by 200 and check it retries and returns data.
- [x] 7.3 Add `resolve_nearest_expiry(underlying, expiry_type="weekly")` that calculates the next Thursday (weekly) or last Thursday of month (monthly) from today's date. Verify: on a Monday, weekly resolves to the coming Thursday; on a Friday after expiry, it resolves to next Thursday.
- [x] 7.4 Add TTL-based cache (`_cache` dict with timestamps) that returns cached data if within 5-minute TTL. Verify: two calls within 3 minutes return same object without API call; call after 6 minutes makes a fresh API call.

## 8. Daily Recommendation Engine

- [x] 8.1 Implement `recommender.py` with `get_recommendation(fii_view, pro_view, vix, backtest_results)` that looks up the best strategy for the given combination from backtest results, computes expected P&L range (mean ± 1 std dev), win rate, and confidence level (High ≥30 days, Medium 10-29, Low <10). Verify: Neutral×Neutral returns confidence="High", a 2-day combo returns confidence="Low".
- [x] 8.2 Add `format_recommendation(rec, nifty_spot=None)` that formats the recommendation as a readable text block including strategy name, strike structure (relative to spot if provided), expected P&L, win rate, and confidence. Verify by checking output contains all fields.
- [x] 8.3 Add live mode to recommender: if Upstox client is available and credentials are configured, fetch current option chain and show actual premiums alongside the recommendation. If unavailable, show only historical-based recommendation. Verify: with no Upstox credentials, recommendation still generates without error.

## 9. CLI Integration

- [x] 9.1 Wire `backtest` subcommand: accepts `--csv` path (default: `vix_fii_t1_intraday_daily_results.csv`), runs full backtest, saves raw results to `backtest_results.csv`. Verify by running `python -m option_backtester backtest` and checking `backtest_results.csv` is created with expected columns.
- [x] 9.2 Wire `report` subcommand: accepts `--output-format` (md/html/csv, default md), `--output-dir` (default current dir), loads backtest results, generates report. Verify by running `python -m option_backtester report` and checking a `.md` file is created.
- [x] 9.3 Wire `recommend` subcommand: accepts `--fii-view`, `--pro-view`, `--vix` (required), `--nifty-spot` (optional). Prints recommendation to stdout. Verify by running `python -m option_backtester recommend --fii-view Neutral --pro-view Neutral --vix 18` and checking output contains strategy name and confidence.

## 10. End-to-End Validation

- [x] 10.1 Run full pipeline: backtest → report (markdown) on the complete 1,488-row CSV. Verify: report contains all 47 observed FII/PRO combinations, summary matrix is 7×7, and no Python errors during execution.
- [x] 10.2 Spot-check report accuracy: manually verify that for Mildly Bearish × Mildly Bearish (100% Green, +0.351% avg), Bull Call Spread ranks highest among strategies; and for Bullish × Strong Bullish (36.5% Green, -0.179% avg), Bear Put Spread or Iron Condor ranks highest. Verify by reading the relevant sections in the generated report.
- [x] 10.3 Run `recommend` for 3 known high-confidence combinations and verify output is sensible: correct strategy, reasonable P&L range, confidence=High for ≥30-day combos.
