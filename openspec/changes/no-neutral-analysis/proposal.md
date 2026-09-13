## Why

The current FII/PRO analysis in `reports/` uses a neutral zone (±10K to ±30K) that absorbs a significant portion of trading days (15-42%) into a "no signal" bucket. This makes the analysis less actionable on days where composite scores are small but still directional. A separate analysis folder that eliminates the neutral zone entirely — treating every day as either bullish or bearish — will reveal whether low-conviction days still carry exploitable directional bias and provide a cleaner binary signal framework.

## What Changes

- Create a new `reports_no_neutral/` folder at the project root, parallel to the existing `reports/` folder
- New Python scripts that mirror the existing analysis pipeline but with a modified 6-tier classification system:
  - **Strong Bullish**: composite > +100,000
  - **Bullish**: +50,001 to +100,000
  - **Mildly Bullish**: 0 to +50,000 (replaces the old neutral-to-+50K range)
  - **Mildly Bearish**: -50,000 to 0 (replaces the old -50K-to-neutral range)
  - **Bearish**: -100,000 to -50,001
  - **Strong Bearish**: < -100,000
- No neutral threshold parameter — a single classification applies to all reports
- Generate the same report types: neutral-zone-equivalent analysis (now "directional zone"), volatility whipsaw, and reversal trap
- Same data sources: `vix_fii_t1_intraday_daily_results.csv` and NIFTY 50 intraday CSV
- The existing `reports/` folder remains completely untouched

## Capabilities

### New Capabilities
- `no-neutral-classification`: Binary directional classification system (0-50K = mildly bullish/bearish, no neutral tier) with report generation scripts that produce FII x PRO combination analysis, volatility whipsaw analysis, and reversal trap analysis

### Modified Capabilities
(none)

## Impact

- **New files**: `reports_no_neutral/` directory with 3 Python generator scripts and their output markdown reports
- **Data dependencies**: Same CSV files already in the project (`vix_fii_t1_intraday_daily_results.csv`, NIFTY 50 intraday CSV)
- **No changes** to existing `reports/`, `option_backtester/`, or any other project code
