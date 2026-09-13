## 1. Project Setup

- [x] 1.1 Create `vix_fii_pro_analysis/` directory at project root. Verify the directory exists with `ls -d vix_fii_pro_analysis/`.

## 2. Core Analysis Script

- [x] 2.1 Create `vix_fii_pro_analysis/analyze_vix_fii_pro.py` with data loading: read `vix_fii_t1_intraday_daily_results.csv` from the parent directory, validate required columns (`vix_accuracy`, `fii_view`, `pro_view`, `nifty_day`) exist, print row count. Verify by running the script and confirming it prints "Loaded X rows" without errors.
- [x] 2.2 Add VIX accuracy partitioning: filter into `overestimated_df` and `underestimated_df` DataFrames. Print counts for each. Verify by running the script and confirming Overestimated=1210, Underestimated=278.
- [x] 2.3 Implement cross-tabulation and combination ranking function: for a given DataFrame, compute `pd.crosstab(fii_view, pro_view)`, then flatten into a ranked list of (fii_view, pro_view, count, pct) sorted by count descending. Apply this to both Overestimated and Underestimated DataFrames. Verify by running and confirming ranked output is printed for both categories.
- [x] 2.4 Add market direction breakdown: split each VIX accuracy group by `nifty_day` (Green/Red) and compute ranked combinations for each of the 4 subgroups (Overestimated+Green, Overestimated+Red, Underestimated+Green, Underestimated+Red). Verify by running and confirming 4 breakdown sections appear in output.

## 3. Output Generation

- [x] 3.1 Add CSV export: write `overestimated_combinations.csv`, `underestimated_combinations.csv`, and `market_direction_breakdown.csv` to the `vix_fii_pro_analysis/` folder. Each CSV includes columns: rank, fii_view, pro_view, count, percentage. The market direction CSV adds vix_accuracy and nifty_day columns. Verify all 3 CSV files exist and contain valid data by checking with `head -5` on each.
- [x] 3.2 Add console summary report: print a formatted report showing top 5 combinations for Overestimated, top 5 for Underestimated, and a comparison section highlighting combinations unique to each category's top 10. Verify by running the script end-to-end and confirming the summary report prints with all sections.

## 4. Validation

- [x] 4.1 Run the complete script end-to-end (`python3 vix_fii_pro_analysis/analyze_vix_fii_pro.py`) and verify: (a) no errors, (b) 3 CSV files created in `vix_fii_pro_analysis/`, (c) console summary shows top 5 combinations per category, (d) percentage values sum reasonably within each group.
