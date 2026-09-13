## Context

See proposal.md for motivation. The source CSV has 1,488 rows with 32 columns. Key columns for this analysis:
- `vix_accuracy`: "Overestimated" (1,210 rows, 81%) or "Underestimated" (278 rows, 19%)
- `fii_view`: 7 categories — Neutral, Bullish, Bearish, Mildly Bearish, Mildly Bullish, Strong Bearish, Strong Bullish
- `pro_view`: 7 categories — Strong Bullish, Strong Bearish, Neutral, Bearish, Bullish, Mildly Bearish, Mildly Bullish
- `nifty_day`: Green (728) or Red (760)

This yields 7x7 = 49 possible FII+Pro combinations per VIX accuracy category.

## Goals / Non-Goals

**Goals:**
- Single Python script that runs end-to-end and produces both CSV outputs and console summary
- All output files in a dedicated `vix_fii_pro_analysis/` folder at project root
- Clear ranking of which FII+Pro combinations dominate when VIX is wrong

**Non-Goals:**
- Predictive modeling or machine learning
- Visualization (charts/plots) — text/CSV output only
- Modifying the source CSV in any way
- Statistical significance testing

## Decisions

### Decision 1: Single script approach
**Choice**: One Python file `vix_fii_pro_analysis/analyze_vix_fii_pro.py` that handles loading, analysis, and output.

**Rationale**: The analysis is linear and self-contained. Splitting into multiple files adds complexity without benefit. A single script is easier to run and understand.

**Alternative considered**: Jupyter notebook — rejected because the user requested a folder with files, and a script is more reproducible.

### Decision 2: Use pandas for data manipulation
**Choice**: pandas for CSV loading, filtering, crosstab, and groupby operations.

**Rationale**: pandas `crosstab` and `value_counts` are purpose-built for this exact analysis pattern. The dataset (1,488 rows) is trivially small for pandas.

**Alternative considered**: Pure Python with csv module — would require reimplementing crosstab logic manually with no benefit.

### Decision 3: Output folder at project root
**Choice**: `vix_fii_pro_analysis/` at project root, script uses `__file__` to resolve paths relative to itself.

**Rationale**: User explicitly requested a new folder in root. Script lives in the same folder as its outputs for simplicity.

### Decision 4: Treat both Overestimated and Underestimated as "VIX wrong"
**Choice**: Analyze both categories separately rather than merging them.

**Rationale**: Both represent VIX misprediction, but the trading implications differ — Overestimated (calm day, VIX too high) vs Underestimated (volatile day, VIX too low). The dominant FII+Pro combinations likely differ between these scenarios. Presenting both gives the user richer insight.

### Decision 5: Combination ranking approach
**Choice**: Flatten the crosstab into (fii_view, pro_view, count, pct) rows, sort by count descending.

**Rationale**: A flat ranked list is more actionable than a 7x7 matrix for identifying which specific combinations dominate. The full crosstab matrix is also included in CSV output for completeness.

## Risks / Trade-offs

- **Sparse combinations**: With 49 possible combinations, many cells may have counts of 0-5. The ranking naturally surfaces only meaningful ones. → Mitigation: report all non-zero combinations, let the user judge significance from counts.
- **Underestimated sample size**: Only 278 rows (19%) are Underestimated, so individual combination counts will be small. → Mitigation: show percentages alongside counts so the user sees relative dominance even with small absolute numbers.
- **No statistical testing**: We report frequencies without p-values or chi-square tests. → Mitigation: this is exploratory analysis; statistical rigor can be added in a follow-up if patterns warrant it.
