## Context

See proposal.md for motivation. The project has two key data sources:
1. `vix_fii_t1_intraday_daily_results.csv` — 1,488 rows (2020-08-06 to 2026-09-09) with pre-computed `fii_composite`, `pro_composite`, VIX predictions, and intraday high/low percentages from open
2. `NIFTY_50_2021-09-13_2026-09-11.csv` — 16,075 rows of 30-minute candles (1,242 trading days) for intraday swing timing analysis

The existing `FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md` was generated using ±30K neutral thresholds. The current classification maps composite ranges to 7 views (Strong Bearish through Strong Bullish) and the view assignment is deterministic based on composite value boundaries.

Key data characteristics observed:
- FII composite range: -444,137 to +328,658
- PRO composite range: -769,958 to +804,728
- FII Neutral day counts per threshold: ±30K=625, ±25K=537, ±20K=443, ±10K=220
- Bullish/Bearish (±50-100K) and Strong (±100K+) categories are threshold-invariant at 220/177/94/120 days respectively
- Average Up Ratio (from open to high / half-VIX): 1.08; Average Down Ratio: 1.39 — the market has a downside bias intraday
- 157 extreme whipsaw days (10.6%) where both up and down moves exceeded half the VIX-predicted range

## Goals / Non-Goals

**Goals:**
- Single Python script in `reports/` that generates all 4 per-threshold reports in one run
- Exact structural match with the existing analysis report format for per-threshold reports
- Configurable thresholds via a function parameter (not hardcoded per-report)
- Cross-threshold comparison report identifying threshold-proof signals, threshold-sensitive signals, and actionable rules
- Separate volatility/whipsaw report analyzing intraday swing intensity using VIX as benchmark, with intraday timing from 30-min candles
- All output files and scripts in `reports/` directory

**Non-Goals:**
- Modifying the existing `FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md`
- Building a general-purpose CLI tool or web interface
- Real-time or streaming volatility monitoring

## Decisions

### 1. Single Python script with parameterized generation (threshold reports)

**Decision**: One script `reports/generate_neutral_zone_reports.py` with a `generate_report(neutral_threshold, output_path)` function called four times (±30K, ±25K, ±20K, ±10K).

**Why over alternatives**:
- Alternative: Separate scripts per threshold → duplication, maintenance burden
- Alternative: Jupyter notebook → harder to run headlessly, state issues
- A single parameterized function ensures all reports use identical logic

### 2. Reclassify from raw composite values, not existing view columns

**Decision**: Ignore the existing `fii_view` and `pro_view` columns entirely. Reclassify from `fii_composite` and `pro_composite` using the new thresholds.

**Why**: The existing view columns encode the ±30K thresholds. Reclassifying from composites ensures the new thresholds are applied consistently.

### 3. Report structure as formatted string templates

**Decision**: Build each report section as a Python function that returns a markdown string. Combine sections in order. No external templating library.

**Why**: The report structure is fixed and well-defined. String formatting with f-strings is sufficient and avoids adding dependencies.

### 4. Statistics computation via pandas

**Decision**: Use pandas for data loading, groupby operations, and aggregation.

**Why over alternatives**:
- Alternative: Pure csv + manual aggregation → error-prone, verbose for group-by stats
- pandas groupby + agg covers all required metrics cleanly

### 5. Dominant move determination

**Decision**: For each (FII_view, PRO_view) group, compute `value_counts()` on `move_direction` column and take the most frequent. Report as "Pattern (X%)" where X is the percentage of that most frequent pattern.

**Why**: Matches the existing report format exactly (e.g., "Down to Up (59%)").

### 6. Comparison report as a manually authored markdown file

**Decision**: The comparison report (`FII_PRO_NEUTRAL_ZONE_COMPARISON.md`) is generated separately by running all 4 threshold analyses and cross-referencing their stats to identify threshold-proof and threshold-sensitive combinations.

**Why over alternatives**:
- Alternative: Auto-generate from the script → the comparison report requires qualitative analysis (key findings, interpretive insights) that benefits from human/AI authoring rather than templated output
- The per-threshold reports are fully automated; the comparison report combines automated data extraction with authored interpretation

### 7. Script location in reports/ directory

**Decision**: Both generation scripts live in `reports/` alongside their output files, referencing CSVs in the parent directory via `SCRIPT_DIR.parent`.

**Why**: Keeps all analysis artifacts together. Scripts are tightly coupled to their output — co-locating them makes the `reports/` folder self-contained.

### 8. Dedicated script for volatility/whipsaw analysis

**Decision**: A separate script `reports/generate_volatility_report.py` produces the whipsaw report, independent from the threshold reports script.

**Why over alternatives**:
- Alternative: Add to `generate_neutral_zone_reports.py` → the volatility report has fundamentally different concerns (VIX benchmarking, intraday candle parsing, swing timing) and uses a second data source. Coupling them increases complexity for no benefit.
- The volatility script uses ±20K as a fixed neutral threshold for FII/PRO classification (matching the middle-ground threshold from the threshold analysis).

### 9. Half-VIX as whipsaw benchmark

**Decision**: Use `vix_predicted_move_pct / 2` as the benchmark for a "significant" one-directional move. A whipsaw extreme day requires BOTH up and down moves to exceed this half-VIX threshold.

**Why**: VIX predicts total daily range. If the market uses more than half that range going up AND more than half going down, it has covered more ground than VIX predicted — a genuine whipsaw. This is more meaningful than fixed percentage thresholds because it adapts to volatility regime.

### 10. Intraday timing via running high/low tracking

**Decision**: For each whipsaw day with intraday data, iterate through 30-min candles chronologically and track when the running high and running low are set. Classify the time of each into Morning (<12:15) or Afternoon (≥12:15).

**Why over alternatives**:
- Alternative: Use only the candle that contains the daily high/low → multiple candles may touch near the high; the first occurrence matters for timing
- Running high/low gives the true first time each extreme was reached
- Morning/Afternoon split at 12:15 aligns with the lunch transition and divides the trading day roughly in half (9:15-12:15 = 3h, 12:15-15:30 = 3h15m)

## Risks / Trade-offs

- **[Small sample combinations]** → Narrowing neutral (especially ±10K) creates new combinations with very few days. The minimum-5-day filter for Top/Worst tables handles this, but per-section tables will show all combinations.
- **[Distribution shift]** → The ±10K report will have a very large Mildly Bullish/Bearish category. The comparison report explicitly flags these threshold-sensitive patterns.
- **[Pandas dependency]** → Standard library for this use case. No other external dependencies needed.
- **[Comparison report staleness]** → The comparison report is authored separately. If thresholds or data change, both the script and the comparison report need updating.
- **[Intraday data coverage gap]** → The intraday CSV covers 2021-09-13 onward but the daily CSV starts 2020-08-06. Swing timing analysis is limited to the 1,242 overlapping days (out of 1,488 total). This covers ~84% of the dataset and is noted in the report header.
- **[Whipsaw correlation ≠ causation]** → The whipsaw report shows correlation between FII×PRO combos and volatility patterns, but FII/PRO positions are T+1 data and reflect the previous day's activity. The report documents this limitation in its methodology section.
