## 1. Project Setup

- [x] 1.1 Create `reports/` directory at project root. Verify with `ls -d reports/`.
- [x] 1.2 Create `generate_neutral_zone_reports.py` in `reports/` with imports (pandas, os, pathlib) and main guard. Script references CSV via `SCRIPT_DIR.parent`. Verify the file runs without errors: `python3 reports/generate_neutral_zone_reports.py`.

## 2. Data Loading and Classification (Threshold Reports)

- [x] 2.1 Implement `load_data()` function that reads `vix_fii_t1_intraday_daily_results.csv` into a pandas DataFrame, parsing `fii_composite` and `pro_composite` as floats. Verify by printing `df.shape` and confirming 1,488 rows with all required columns present.
- [x] 2.2 Implement `classify_composite(value, neutral_threshold)` function that maps a composite value to one of 7 view categories using the threshold scheme: Strong Bearish (<-100K), Bearish (-100K to -50K), Mildly Bearish (-50K to -neutral), Neutral (-neutral to +neutral), Mildly Bullish (+neutral to +50K), Bullish (+50K to +100K), Strong Bullish (>+100K). Verify by asserting: `classify_composite(0, 20000) == "Neutral"`, `classify_composite(25000, 20000) == "Mildly Bullish"`, `classify_composite(-15000, 10000) == "Mildly Bearish"`.
- [x] 2.3 Implement `reclassify_views(df, neutral_threshold)` that adds `fii_view_new` and `pro_view_new` columns by applying `classify_composite` to `fii_composite` and `pro_composite`. Verify by printing value counts for each threshold and confirming Neutral shrinks as threshold narrows: ±30K=625, ±25K=537, ±20K=443, ±10K=220.

## 3. Statistics Computation (Threshold Reports)

- [x] 3.1 Implement `compute_combination_stats(df)` that groups by `(fii_view_new, pro_view_new)` and computes: Days (count), Green% (pct where `nifty_day == "Green"`), Avg Chg% (mean of `actual_open_close_pct`), Avg Range% (mean of `actual_range_pct`), Up from Open (mean of `intraday_high_pct` × 100), Down from Open (mean of abs(`intraday_low_pct`) × 100), Dominant Move (mode of `move_direction` with percentage). Verify by comparing a few combinations against the existing report's values for the ±30K case.
- [x] 3.2 Implement `compute_expiry_stats(df)` that splits each combination into expiry (`is_nifty_expiry == 1`) and non-expiry days, computing Green% for each side. Return "-" when a side has zero days. Verify by checking that combinations with no expiry days show "-" for Exp G%.

## 4. Report Section Generators (Threshold Reports)

- [x] 4.1 Implement `generate_header(df, neutral_threshold)` that returns the title line with dataset metadata: day count, date range, and unique combination count. Verify output matches format: `# FII VIEW x PRO VIEW — All Combinations Analysis (±{threshold}K Neutral)`.
- [x] 4.2 Implement `generate_fii_distribution(df, stats)` that produces the FII View Distribution table with Days and % of Total columns, sorted by Days descending. Verify the table renders correctly in markdown.
- [x] 4.3 Implement `generate_master_table(stats, expiry_stats)` that produces the Master Summary Table sorted by Green% descending with columns: FII View, PRO View, Days, Green%, Avg Chg%, Dominant Pattern, Exp G%, Non-Exp G%. Bold rows with ≥5 days. Verify sort order is correct.
- [x] 4.4 Implement `generate_fii_sections(stats, df)` that produces 7 per-FII-view sections (ordered: Strong Bullish, Bullish, Mildly Bullish, Neutral, Mildly Bearish, Bearish, Strong Bearish) each with a PRO breakdown table and a pattern insight paragraph. Verify all 7 sections appear with correct numbering.
- [x] 4.5 Implement `generate_top_bottom_tables(stats)` that produces Top 5 Best Combinations (by Green%, ≥5 days), Top 5 Worst (by Green%, ≥5 days), Top 5 Highest Avg Change (≥5 days), Top 5 Lowest Avg Change (≥5 days). Verify the minimum-5-day filter is applied.
- [x] 4.6 Implement `generate_expiry_divergence(expiry_stats)` that finds combinations where |Exp G% - Non-Exp G%| > 15% with ≥3 days on each side, sorted by divergence descending. Verify output table format matches the existing report.
- [x] 4.7 Implement `generate_conclusion(stats, neutral_threshold, df)` that produces a Conclusion section with key findings and actionable rules, noting the neutral zone threshold used and its impact on category sizes. Verify the section contains numbered findings and bullet-point rules.

## 5. Report Assembly and Output (Threshold Reports)

- [x] 5.1 Implement `generate_report(neutral_threshold, output_path)` that chains all section generators, concatenates their output with `---` separators, and writes to the given output path. Verify by running with threshold=20000 and checking the output file has all sections.
- [x] 5.2 Implement `main()` that calls `generate_report` four times for thresholds ±30K, ±25K, ±20K, ±10K. Verify by running `python3 reports/generate_neutral_zone_reports.py` and checking all four files exist with non-empty content.

## 6. Cross-Threshold Comparison Report

- [x] 6.1 Create `reports/FII_PRO_NEUTRAL_ZONE_COMPARISON.md` containing a distribution impact table showing Neutral/MildlyBullish/MildlyBearish day counts across all 4 thresholds. Verify the table shows Neutral shrinking: 625→537→443→220.
- [x] 6.2 Add Top 5 Best and Top 5 Worst side-by-side tables with one column per threshold. Verify all 4 threshold columns are populated.
- [x] 6.3 Add Threshold-Proof Good Signals section listing combinations with ≥55% Green and ≥5 days across ALL 4 thresholds. Verify at least Bearish+Bullish (83.3%) and Strong Bullish+Bullish (80.0%) appear — these are perfectly threshold-invariant.
- [x] 6.4 Add Threshold-Proof Bad Signals section listing combinations with ≤45% Green across ALL 4 thresholds. Verify Bullish+StrongBullish (40.3%, 134d) appears as the largest reliably bearish setup.
- [x] 6.5 Add Most Threshold-Sensitive Combinations section listing combos with Green% spread >10% across thresholds, sorted by spread descending. Verify MildlyBearish+MildlyBearish (36.9% spread) and MildlyBullish+MildlyBullish (29.6% spread) appear as the most sensitive.
- [x] 6.6 Add Key Findings and Quick Reference Actionable Rules sections summarizing trustworthy vs untrustworthy signals and go-long/avoid-long rules based only on threshold-proof data.

## 7. Volatility/Whipsaw Report — Setup and Data Loading

- [x] 7.1 Create `reports/generate_volatility_report.py` with imports (pandas, numpy, pathlib) and main guard. Script references both CSVs via `SCRIPT_DIR.parent`. Verify import runs without errors.
- [x] 7.2 Implement `load_and_prepare()` that reads `vix_fii_t1_intraday_daily_results.csv`, classifies FII/PRO views using ±20K threshold, and computes volatility columns: `half_vix`, `up_ratio`, `down_ratio`, `both_min_ratio`, `total_swing_pct`, and three boolean whipsaw tier columns (`whipsaw_extreme`, `whipsaw_strong`, `whipsaw_moderate`). Verify 157 extreme whipsaw days out of 1,488 total.
- [x] 7.3 Implement `load_intraday()` that reads `NIFTY_50_2021-09-13_2026-09-11.csv`, parses datetime, extracts date and time columns. Verify 1,242 unique dates with 13 candles per day (30-min intervals).

## 8. Volatility/Whipsaw Report — Statistics and Timing

- [x] 8.1 Implement `compute_combo_volatility(df)` that groups by `(fii_view, pro_view)` and computes per-combination: avg_range_pct, avg_vix_pct, avg_range_vs_vix, avg_up_pct, avg_down_pct, avg_total_swing, avg_up_ratio, avg_down_ratio, whipsaw_extreme_pct, whipsaw_strong_pct, whipsaw_moderate_pct, green_pct, avg_chg. Verify by checking Strong Bullish+Bullish has 40% whipsaw extreme rate.
- [x] 8.2 Implement `compute_intraday_swing_timing(daily_df, intra_df)` that for each whipsaw extreme day with intraday data: tracks running high/low times across 30-min candles, classifies each into Morning (<12:15) or Afternoon (≥12:15), determines swing pattern ("Up Morning → Down Afternoon" etc.) and sequence ("High First" / "Low First"). Verify "Down Morning → Up Afternoon" is the dominant pattern (~53%).

## 9. Volatility/Whipsaw Report — Section Generators

- [x] 9.1 Generate Master Table sorted by Whipsaw Extreme % descending with columns: FII View, PRO View, Days, Whipsaw Extreme %, Whipsaw Strong %, Avg Total Swing, Avg Range%, Range/VIX, Green%, Avg Chg%. Bold rows with whipsaw ≥15%. Verify sort order is correct.
- [x] 9.2 Generate Top 10 Highest Total Swing and Top 10 Lowest Total Swing tables (≥5 days). Verify highest swing combos differ from highest whipsaw combos (swing measures total ground, whipsaw measures both-sides balance).
- [x] 9.3 Generate Swing Asymmetry section with up-biased (bias > +0.15) and down-biased (bias < -0.15) tables showing Avg Up/Down Ratio, Swing Bias, Green%, Avg Chg%. Verify up-biased combos correlate with positive Green% and down-biased with negative.
- [x] 9.4 Generate 7 per-FII-view volatility sections with PRO breakdown showing whipsaw rates, swing metrics, range/VIX, and a volatility insight paragraph. Verify all 7 sections appear.
- [x] 9.5 Generate Intraday Swing Timing section with overall pattern distribution, high-first vs low-first sequence, and pattern breakdown by FII view. Verify only days with intraday data are included (~136 extreme whipsaw days).
- [x] 9.6 Generate Range vs VIX section with Top 10 combos exceeding VIX and Top 10 under VIX. Verify Bearish+Bullish has the highest range/VIX ratio (1.63).
- [x] 9.7 Generate Conclusion with key findings (most/least whipsaw-prone, whipsaw-Green% correlation, dominant swing pattern) and actionable rules (straddle/strangle candidates, iron condor candidates). Verify conclusion references the r=0.37 correlation.

## 10. Volatility/Whipsaw Report — Assembly and Output

- [x] 10.1 Implement `generate_report(df, intra_df)` that chains all volatility section generators, concatenates with `---` separators, and writes to `reports/FII_PRO_VOLATILITY_WHIPSAW_ANALYSIS.md`. Verify output file has all 9 sections.
- [x] 10.2 Implement `main()` that calls `load_and_prepare()`, `load_intraday()`, and `generate_report()`. Verify by running `python3 reports/generate_volatility_report.py` and checking the output file exists with 345 lines.

## 11. Validation

- [x] 11.1 Run `generate_neutral_zone_reports.py` end-to-end and verify all 4 per-threshold reports contain all 8 section types with correct table formatting.
- [x] 11.2 Verify FII Neutral counts decrease monotonically: ±30K (625) > ±25K (537) > ±20K (443) > ±10K (220).
- [x] 11.3 Spot-check 2-3 combinations in threshold reports by manually filtering the CSV and confirming Days count and Green% match.
- [x] 11.4 Verify `reports/FII_PRO_NEUTRAL_ZONE_COMPARISON.md` contains all 7 required sections.
- [x] 11.5 Run `generate_volatility_report.py` and verify `reports/FII_PRO_VOLATILITY_WHIPSAW_ANALYSIS.md` contains all 9 sections: header/methodology, master table, top/bottom swing, swing asymmetry, per-FII sections, intraday timing, range vs VIX, and conclusion.
- [x] 11.6 Verify whipsaw extreme count = 157 days (10.6%) and dominant swing pattern is "Down Morning → Up Afternoon" at ~53%.
