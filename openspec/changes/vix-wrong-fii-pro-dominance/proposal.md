## Why

The dataset `vix_fii_t1_intraday_daily_results.csv` (1,488 trading days from Aug 2020 onwards) tracks VIX prediction accuracy alongside FII and Pro trader positioning. When VIX accuracy is wrong (both Overestimated and Underestimated cases), understanding which FII+Pro view combinations dominate reveals which institutional positioning patterns coincide with VIX mispredictions — useful for building better trading filters.

## What Changes

- Create a new `vix_fii_pro_analysis/` folder in the project root to house all analysis files
- Build a Python analysis script that:
  - Loads the CSV and filters rows where VIX accuracy is wrong (Overestimated and Underestimated separately)
  - Cross-tabulates `fii_view` x `pro_view` combinations for each VIX accuracy category
  - Computes frequency counts, percentages, and dominance rankings for each combination
  - Compares combination distributions between Overestimated vs Underestimated scenarios
  - Breaks down further by `nifty_day` (Green/Red) to see if the dominant combination shifts with market direction
- Generate summary CSV outputs with the combination analysis results
- Produce a final analysis report (printed to console) with key findings

## Capabilities

### New Capabilities
- `vix-fii-pro-dominance-analysis`: Analyze which FII+Pro view combinations dominate when VIX accuracy is wrong (Overestimated/Underestimated), with breakdowns by market direction

### Modified Capabilities
(none)

## Impact

- **New folder**: `vix_fii_pro_analysis/` created at project root
- **New files**: Python analysis script, output CSVs with cross-tabulation results
- **Data dependency**: Reads from existing `vix_fii_t1_intraday_daily_results.csv` (read-only)
- **No external dependencies**: Uses only Python standard library + pandas
