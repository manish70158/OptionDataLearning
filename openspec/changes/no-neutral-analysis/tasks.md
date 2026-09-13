## 1. Directory Setup

- [x] 1.1 Create the `reports_no_neutral/` directory at the project root. Verify it exists with `ls -d reports_no_neutral/`.

## 2. Directional Combination Analysis Script

- [x] 2.1 Create `reports_no_neutral/generate_directional_reports.py` by forking `reports/generate_neutral_zone_reports.py`. Replace `classify_composite(value, neutral_threshold)` with a no-threshold version that splits at zero: `value >= 0` → "Mildly Bullish", `value < 0` → "Mildly Bearish", NaN → "Mildly Bullish". Remove all neutral-threshold parameters, the `reclassify_views` threshold argument, and the multi-threshold `main()` loop. Update `fii_section_order` to return `["Strong Bullish", "Bullish", "Mildly Bullish", "Mildly Bearish", "Bearish", "Strong Bearish"]`. Update the header, label guide, and conclusion to reflect the no-neutral classification. Output a single report: `FII_PRO_NO_NEUTRAL_DIRECTIONAL_ANALYSIS.md`. Verify by running `python reports_no_neutral/generate_directional_reports.py` and confirming the output file exists and contains the six FII view labels with no "Neutral" label.

## 3. Volatility Whipsaw Analysis Script

- [x] 3.1 Create `reports_no_neutral/generate_volatility_report.py` by forking `reports/generate_volatility_report.py`. Replace `classify_composite` with the no-neutral version (same logic as task 2.1). Remove the `NEUTRAL_THRESHOLD` constant and `TK` suffix. Update `FII_SECTION_ORDER` to use the six no-neutral labels. Update report headers, label guides, and all references to neutral-specific labels. Output `FII_PRO_NO_NEUTRAL_VOLATILITY_WHIPSAW_ANALYSIS.md` (0.5x VIX) and `FII_PRO_NO_NEUTRAL_VOLATILITY_WHIPSAW_0.3VIX_ANALYSIS.md` (0.3x VIX). Verify by running `python reports_no_neutral/generate_volatility_report.py` and confirming both output files exist and contain no "Neutral20" or "MildBull20" labels.

## 4. Reversal Trap Analysis Script

- [x] 4.1 Create `reports_no_neutral/generate_reversal_report.py` by forking `reports/generate_reversal_report.py`. Replace `classify_composite` with the no-neutral version (same logic as task 2.1). Remove the `NEUTRAL_THRESHOLD` constant and `TK` suffix. Update `FII_SECTION_ORDER` to use the six no-neutral labels. Update report headers, label guides, and all references to neutral-specific labels. Output `FII_PRO_NO_NEUTRAL_REVERSAL_TRAP_ANALYSIS.md`. Verify by running `python reports_no_neutral/generate_reversal_report.py` and confirming the output file exists and contains no neutral-tier labels.

## 5. Validation

- [x] 5.1 Run all three scripts in sequence and verify: (a) all four markdown reports are generated in `reports_no_neutral/`, (b) no file in `reports/` was modified (compare timestamps or `git status`), (c) grep across all generated reports confirms zero occurrences of "Neutral" as a standalone label, and (d) "Mildly Bullish" and "Mildly Bearish" appear in all reports without numeric suffixes.
