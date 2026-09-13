## Why

The existing `FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md` uses a fixed ±30K neutral zone for classifying FII and PRO composite values. Different neutral zone thresholds can reveal hidden patterns — a tighter ±10K neutral captures only the most indecisive days, while ±20K and ±25K provide middle grounds. Generating separate reports for each threshold, plus a side-by-side comparison, allows identification of which FII×PRO signals are robust across all definitions ("threshold-proof") versus which are artifacts of a specific neutral boundary. Additionally, understanding which combinations produce the most intraday volatility (whipsaw — large swings in both directions relative to VIX predictions) enables options strategy selection (straddles vs iron condors) and intraday risk management.

## What Changes

- Create a `reports/` folder in the project root containing all generated reports and generation scripts
- Generate **4 per-threshold analysis reports**, each following the exact structure of `FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md`:
  - `FII_PRO_NEUTRAL_30K_ANALYSIS.md` — ±30K neutral (matches original classification)
  - `FII_PRO_NEUTRAL_25K_ANALYSIS.md` — ±25K neutral
  - `FII_PRO_NEUTRAL_20K_ANALYSIS.md` — ±20K neutral
  - `FII_PRO_NEUTRAL_10K_ANALYSIS.md` — ±10K neutral
- Generate **1 comparison report** (`FII_PRO_NEUTRAL_ZONE_COMPARISON.md`) that compares all 4 threshold reports side by side: distribution impact, top/worst combos across thresholds, threshold-proof good/bad signals, threshold-sensitive combos, and actionable rules based only on robust signals
- Generate **1 volatility/whipsaw report** (`FII_PRO_VOLATILITY_WHIPSAW_ANALYSIS.md`) that analyzes which FII×PRO combinations produce the most intraday volatility using VIX as a benchmark — identifying whipsaw days where the market swings significantly in both directions from open, swing asymmetry (up-biased vs down-biased), intraday timing of whipsaws using 30-min candle data, and range vs VIX prediction accuracy
- `generate_neutral_zone_reports.py` produces the 4 threshold reports; `generate_volatility_report.py` produces the whipsaw analysis

### Classification Thresholds

| Category | ±30K | ±25K | ±20K | ±10K |
|---|---|---|---|---|
| Neutral | -30K to +30K | -25K to +25K | -20K to +20K | -10K to +10K |
| Mildly Bullish | +30K to +50K | +25K to +50K | +20K to +50K | +10K to +50K |
| Mildly Bearish | -30K to -50K | -25K to -50K | -20K to -50K | -10K to -50K |
| Bullish | +50K to +100K | +50K to +100K | +50K to +100K | +50K to +100K |
| Bearish | -50K to -100K | -50K to -100K | -50K to -100K | -50K to -100K |
| Strong Bullish | > +100K | > +100K | > +100K | > +100K |
| Strong Bearish | < -100K | < -100K | < -100K | < -100K |

## Capabilities

### New Capabilities
- `fii-pro-custom-neutral-analysis`: Python-based report generation that reclassifies FII/PRO composite values using configurable neutral zone thresholds and produces markdown analysis reports matching the structure of the existing 6-year analysis, plus a cross-threshold comparison report identifying threshold-proof and threshold-sensitive signals.
- `fii-pro-volatility-whipsaw-analysis`: VIX-benchmarked intraday volatility analysis that identifies which FII×PRO combinations produce the most whipsaw (large swings in both directions), using half-VIX as the significance threshold, with intraday swing timing from 30-min candle data and options strategy recommendations.

### Modified Capabilities
<!-- None — this is a new standalone analysis capability -->

## Impact

- **New files (6 reports + 2 scripts)**:
  - `reports/FII_PRO_NEUTRAL_30K_ANALYSIS.md`, `reports/FII_PRO_NEUTRAL_25K_ANALYSIS.md`, `reports/FII_PRO_NEUTRAL_20K_ANALYSIS.md`, `reports/FII_PRO_NEUTRAL_10K_ANALYSIS.md` — per-threshold analysis
  - `reports/FII_PRO_NEUTRAL_ZONE_COMPARISON.md` — cross-threshold comparison
  - `reports/FII_PRO_VOLATILITY_WHIPSAW_ANALYSIS.md` — volatility/whipsaw analysis
  - `reports/generate_neutral_zone_reports.py` — generates the 4 threshold reports
  - `reports/generate_volatility_report.py` — generates the whipsaw report
- **Data sources**: `vix_fii_t1_intraday_daily_results.csv` (1,488 rows, 2020-08-06 to 2026-09-09) for all reports; `NIFTY_50_2021-09-13_2026-09-11.csv` (16,075 rows, 30-min candles) for intraday swing timing in the volatility report
- **No breaking changes**: Existing files are not modified
