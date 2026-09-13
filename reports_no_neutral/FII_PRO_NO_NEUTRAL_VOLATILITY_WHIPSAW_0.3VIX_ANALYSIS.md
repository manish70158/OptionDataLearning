# FII VIEW x PRO VIEW — Volatility & Whipsaw Analysis (0.3×VIX Threshold, No Neutral)

**Dataset**: 1,488 days | 2020-08-06 to 2026-09-09 | No Neutral Classification
**Intraday data**: 30-min candles from 2021-09-13 to 2026-09-11 (1242 days)
**VIX Threshold**: 0.3×VIX = VIX predicted move × 0.3 — a move in one direction must exceed this to count as "significant"

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional

## How This Report Works

**Concept**: On any given day, VIX predicts an expected daily range. A "whipsaw" day is when the market swings significantly in BOTH directions from the open — going up by a meaningful fraction of the VIX range AND down by a meaningful fraction.

**Threshold used**: **0.3×VIX** = VIX predicted move × 0.3. This is a tighter threshold than half-VIX (0.5), so MORE days qualify as whipsaw since the bar for significance is lower (30% of VIX vs 50%).

**Metrics**:
- **0.3×VIX** = VIX predicted move × 0.3. This is the benchmark for a "significant" move in one direction.
- **Up Ratio** = (High - Open) / 0.3×VIX. How much of the VIX budget was used going up.
- **Down Ratio** = |Low - Open| / 0.3×VIX. How much of the VIX budget was used going down.
- **Whipsaw Extreme**: Both Up Ratio AND Down Ratio > 1.0 (both sides exceeded 0.3×VIX)
- **Whipsaw Strong**: Both > 0.75
- **Whipsaw Moderate**: Both > 0.50

**Overall Stats**:
- Whipsaw Extreme days: **531** (35.7% of all days)
- Whipsaw Strong days: **748** (50.3% of all days)
- Average Up Ratio: 1.79 | Average Down Ratio: 2.32

---

## Master Table — Combinations Sorted by Whipsaw Extreme %

Combinations with ≥5 days, sorted by % of days that had extreme whipsaw (both sides > half VIX).

| FII View | PRO View | Days | Whipsaw Extreme % | Whipsaw Strong % | Avg Total Swing | Avg Range% | Range/VIX | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|---|---|
| **Strong Bullish** | **Strong Bearish** | 6 | **66.7%** | 83.3% | 0.783% | 0.788% | 1.05 | 50.0% | +0.065% |
| **Strong Bearish** | **Bearish** | 9 | **66.7%** | 66.7% | 0.872% | 0.871% | 1.13 | 44.4% | -0.076% |
| **Bearish** | **Bullish** | 7 | **57.1%** | 85.7% | 1.423% | 1.421% | 1.83 | 85.7% | +0.490% |
| **Bullish** | **Strong Bearish** | 17 | **47.1%** | 64.7% | 0.850% | 0.851% | 1.14 | 47.1% | +0.024% |
| **Bearish** | **Mildly Bullish** | 11 | **45.5%** | 54.5% | 1.256% | 1.258% | 1.52 | 36.4% | -0.405% |
| **Strong Bearish** | **Strong Bearish** | 80 | **42.5%** | 57.5% | 1.016% | 1.016% | 1.32 | 40.0% | -0.092% |
| **Mildly Bullish** | **Bearish** | 43 | **41.9%** | 58.1% | 1.033% | 1.032% | 1.26 | 62.8% | +0.080% |
| **Bullish** | **Mildly Bearish** | 17 | **41.2%** | 58.8% | 0.886% | 0.885% | 1.01 | 52.9% | -0.030% |
| **Bearish** | **Bearish** | 32 | **40.6%** | 53.1% | 1.005% | 1.006% | 1.28 | 43.8% | -0.135% |
| **Strong Bullish** | **Bullish** | 5 | **40.0%** | 60.0% | 0.842% | 0.842% | 1.25 | 80.0% | +0.238% |
| **Strong Bearish** | **Strong Bullish** | 5 | **40.0%** | 60.0% | 1.052% | 1.056% | 1.52 | 20.0% | -0.270% |
| **Strong Bearish** | **Mildly Bearish** | 10 | **40.0%** | 80.0% | 1.098% | 1.100% | 1.37 | 20.0% | -0.502% |
| **Strong Bullish** | **Strong Bullish** | 70 | **40.0%** | 55.7% | 0.963% | 0.962% | 1.23 | 58.6% | +0.010% |
| **Bearish** | **Strong Bearish** | 102 | **39.2%** | 51.0% | 1.022% | 1.022% | 1.25 | 45.1% | -0.054% |
| **Mildly Bearish** | **Bearish** | 88 | **38.6%** | 54.5% | 1.091% | 1.091% | 1.25 | 46.6% | -0.039% |
| **Mildly Bearish** | **Strong Bearish** | 106 | **37.7%** | 51.9% | 1.086% | 1.086% | 1.33 | 50.9% | +0.017% |
| **Mildly Bearish** | **Mildly Bullish** | 69 | **37.7%** | 52.2% | 1.097% | 1.097% | 1.23 | 53.6% | +0.016% |
| **Bullish** | **Strong Bullish** | 129 | **36.4%** | 44.2% | 0.872% | 0.872% | 1.15 | 38.8% | -0.151% |
| **Mildly Bearish** | **Bullish** | 28 | **35.7%** | 60.7% | 0.966% | 0.966% | 1.16 | 64.3% | +0.201% |
| **Mildly Bullish** | **Strong Bearish** | 40 | **35.0%** | 52.5% | 0.863% | 0.863% | 1.24 | 50.0% | -0.011% |
| **Mildly Bullish** | **Mildly Bearish** | 78 | **34.6%** | 46.2% | 1.004% | 1.004% | 1.16 | 56.4% | +0.005% |
| **Bullish** | **Bullish** | 26 | **34.6%** | 50.0% | 0.980% | 0.981% | 1.20 | 53.8% | +0.030% |
| **Mildly Bullish** | **Mildly Bullish** | 105 | **34.3%** | 45.7% | 1.094% | 1.094% | 1.17 | 52.4% | -0.042% |
| **Strong Bullish** | **Mildly Bullish** | 9 | **33.3%** | 33.3% | 1.062% | 1.064% | 1.21 | 44.4% | +0.009% |
| **Mildly Bearish** | **Strong Bullish** | 40 | **32.5%** | 55.0% | 0.962% | 0.962% | 1.17 | 52.5% | -0.063% |
| **Bearish** | **Mildly Bearish** | 22 | **31.8%** | 40.9% | 0.957% | 0.956% | 1.21 | 40.9% | -0.051% |
| **Bullish** | **Mildly Bullish** | 19 | **31.6%** | 52.6% | 0.876% | 0.876% | 1.17 | 57.9% | +0.240% |
| **Bearish** | **Strong Bullish** | 10 | **30.0%** | 60.0% | 0.829% | 0.827% | 1.16 | 50.0% | +0.085% |
| **Mildly Bullish** | **Bullish** | 84 | **28.6%** | 47.6% | 1.062% | 1.062% | 1.21 | 44.0% | -0.114% |
| **Mildly Bullish** | **Strong Bullish** | 98 | **27.6%** | 42.9% | 1.018% | 1.018% | 1.25 | 49.0% | -0.037% |
| **Mildly Bearish** | **Mildly Bearish** | 106 | **21.7%** | 36.8% | 1.194% | 1.193% | 1.31 | 44.3% | -0.204% |

---

## Top 10 Highest Total Swing Combinations (≥5 days)

Total Swing = (High - Open) + |Low - Open|. This measures how much ground the market covered in both directions.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | VIX Pred% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.423%** | 0.850% | 0.573% | 1.421% | 0.769% | 57.1% | 85.7% |
| 2 | Bearish | Mildly Bullish | 11 | **1.256%** | 0.410% | 0.846% | 1.258% | 0.825% | 45.5% | 36.4% |
| 3 | Mildly Bearish | Mildly Bearish | 106 | **1.194%** | 0.424% | 0.770% | 1.193% | 0.926% | 21.7% | 44.3% |
| 4 | Strong Bearish | Mildly Bearish | 10 | **1.098%** | 0.324% | 0.774% | 1.100% | 0.821% | 40.0% | 20.0% |
| 5 | Mildly Bearish | Mildly Bullish | 69 | **1.097%** | 0.521% | 0.577% | 1.097% | 0.890% | 37.7% | 53.6% |
| 6 | Mildly Bullish | Mildly Bullish | 105 | **1.094%** | 0.468% | 0.626% | 1.094% | 0.939% | 34.3% | 52.4% |
| 7 | Mildly Bearish | Bearish | 88 | **1.091%** | 0.475% | 0.617% | 1.091% | 0.875% | 38.6% | 46.6% |
| 8 | Mildly Bearish | Strong Bearish | 106 | **1.086%** | 0.499% | 0.587% | 1.086% | 0.820% | 37.7% | 50.9% |
| 9 | Strong Bullish | Mildly Bullish | 9 | **1.062%** | 0.470% | 0.592% | 1.064% | 0.842% | 33.3% | 44.4% |
| 10 | Mildly Bullish | Bullish | 84 | **1.062%** | 0.409% | 0.653% | 1.062% | 0.876% | 28.6% | 44.0% |

---

## Top 10 Lowest Total Swing Combinations (≥5 days)

These combinations produce the calmest, most directional days with minimal whipsaw.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Strong Bullish | Strong Bearish | 6 | **0.783%** | 0.450% | 0.333% | 0.788% | 66.7% | 50.0% |
| 2 | Bearish | Strong Bullish | 10 | **0.829%** | 0.470% | 0.359% | 0.827% | 30.0% | 50.0% |
| 3 | Strong Bullish | Bullish | 5 | **0.842%** | 0.512% | 0.330% | 0.842% | 40.0% | 80.0% |
| 4 | Bullish | Strong Bearish | 17 | **0.850%** | 0.367% | 0.483% | 0.851% | 47.1% | 47.1% |
| 5 | Mildly Bullish | Strong Bearish | 40 | **0.863%** | 0.390% | 0.474% | 0.863% | 35.0% | 50.0% |
| 6 | Strong Bearish | Bearish | 9 | **0.872%** | 0.377% | 0.496% | 0.871% | 66.7% | 44.4% |
| 7 | Bullish | Strong Bullish | 129 | **0.872%** | 0.340% | 0.532% | 0.872% | 36.4% | 38.8% |
| 8 | Bullish | Mildly Bullish | 19 | **0.876%** | 0.564% | 0.312% | 0.876% | 31.6% | 57.9% |
| 9 | Bullish | Mildly Bearish | 17 | **0.886%** | 0.465% | 0.421% | 0.885% | 41.2% | 52.9% |
| 10 | Bearish | Mildly Bearish | 22 | **0.957%** | 0.415% | 0.542% | 0.956% | 31.8% | 40.9% |

---

## Swing Asymmetry — Which Side Dominates?

**Swing Bias** = Avg Up Ratio - Avg Down Ratio. Positive = upside swings dominate, Negative = downside swings dominate.

### Up-Biased Combinations (swing bias > +0.15)
These combinations swing MORE to the upside relative to VIX. The upside move consumes more of the VIX budget.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| Bullish | Mildly Bullish | 19 | 2.60 | 1.29 | **+1.31** | 57.9% | +0.240% |
| Bearish | Bullish | 7 | 3.66 | 2.45 | **+1.22** | 85.7% | +0.490% |
| Strong Bullish | Bullish | 5 | 2.46 | 1.71 | **+0.75** | 80.0% | +0.238% |
| Bearish | Strong Bullish | 10 | 2.22 | 1.64 | **+0.58** | 50.0% | +0.085% |
| Strong Bullish | Strong Bearish | 6 | 2.02 | 1.46 | **+0.55** | 50.0% | +0.065% |
| Mildly Bullish | Bearish | 43 | 2.25 | 1.96 | **+0.29** | 62.8% | +0.080% |
| Bullish | Mildly Bearish | 17 | 1.82 | 1.55 | **+0.27** | 52.9% | -0.030% |

### Down-Biased Combinations (swing bias < -0.15)
These combinations swing MORE to the downside. Sellers dominate the intraday action.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| Strong Bearish | Mildly Bearish | 10 | 1.34 | 3.23 | **-1.89** | 20.0% | -0.502% |
| Bearish | Mildly Bullish | 11 | 1.80 | 3.27 | **-1.47** | 36.4% | -0.405% |
| Mildly Bearish | Mildly Bearish | 106 | 1.57 | 2.79 | **-1.22** | 44.3% | -0.204% |
| Bearish | Bearish | 32 | 1.63 | 2.63 | **-1.00** | 43.8% | -0.135% |
| Bullish | Strong Bullish | 129 | 1.44 | 2.38 | **-0.94** | 38.8% | -0.151% |
| Strong Bullish | Mildly Bullish | 9 | 1.54 | 2.47 | **-0.92** | 44.4% | +0.009% |
| Mildly Bullish | Bullish | 84 | 1.57 | 2.48 | **-0.91** | 44.0% | -0.114% |
| Strong Bearish | Strong Bullish | 5 | 2.11 | 2.93 | **-0.82** | 20.0% | -0.270% |
| Strong Bearish | Strong Bearish | 80 | 1.81 | 2.58 | **-0.78** | 40.0% | -0.092% |
| Bearish | Strong Bearish | 102 | 1.72 | 2.43 | **-0.72** | 45.1% | -0.054% |
| Bullish | Strong Bearish | 17 | 1.58 | 2.22 | **-0.65** | 47.1% | +0.024% |
| Bearish | Mildly Bearish | 22 | 1.72 | 2.31 | **-0.59** | 40.9% | -0.051% |
| Mildly Bullish | Mildly Bullish | 105 | 1.65 | 2.24 | **-0.59** | 52.4% | -0.042% |
| Mildly Bullish | Strong Bullish | 98 | 1.80 | 2.37 | **-0.57** | 49.0% | -0.037% |
| Mildly Bearish | Bearish | 88 | 1.80 | 2.36 | **-0.56** | 46.6% | -0.039% |
| Strong Bullish | Strong Bullish | 70 | 1.80 | 2.31 | **-0.51** | 58.6% | +0.010% |
| Strong Bearish | Bearish | 9 | 1.65 | 2.11 | **-0.46** | 44.4% | -0.076% |
| Mildly Bearish | Strong Bullish | 40 | 1.74 | 2.18 | **-0.44** | 52.5% | -0.063% |
| Mildly Bearish | Strong Bearish | 106 | 2.01 | 2.41 | **-0.40** | 50.9% | +0.017% |
| Mildly Bullish | Strong Bearish | 40 | 1.87 | 2.26 | **-0.39** | 50.0% | -0.011% |
| Mildly Bullish | Mildly Bearish | 78 | 1.85 | 2.03 | **-0.19** | 56.4% | +0.005% |

---

## Section 1: FII STRONG BULLISH — Volatility Profile (90 days, 41.1% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 6 | 66.7% | 83.3% | 0.783% | 0.788% | 1.05 | 2.02 | 1.46 | 50.0% |
| Bullish | 5 | 40.0% | 60.0% | 0.842% | 0.842% | 1.25 | 2.46 | 1.71 | 80.0% |
| Strong Bullish | 70 | 40.0% | 55.7% | 0.963% | 0.962% | 1.23 | 1.80 | 2.31 | 58.6% |
| Mildly Bullish | 9 | 33.3% | 33.3% | 1.062% | 1.064% | 1.21 | 1.54 | 2.47 | 44.4% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (67% extreme days, 0.783% avg swing). Calmest with Mildly Bullish PRO (33% extreme, 1.062% avg swing).

## Section 2: FII BULLISH — Volatility Profile (208 days, 37.0% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 17 | 47.1% | 64.7% | 0.850% | 0.851% | 1.14 | 1.58 | 2.22 | 47.1% |
| Mildly Bearish | 17 | 41.2% | 58.8% | 0.886% | 0.885% | 1.01 | 1.82 | 1.55 | 52.9% |
| Strong Bullish | 129 | 36.4% | 44.2% | 0.872% | 0.872% | 1.15 | 1.44 | 2.38 | 38.8% |
| Bullish | 26 | 34.6% | 50.0% | 0.980% | 0.981% | 1.20 | 2.04 | 1.95 | 53.8% |
| Mildly Bullish | 19 | 31.6% | 52.6% | 0.876% | 0.876% | 1.17 | 2.60 | 1.29 | 57.9% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (47% extreme days, 0.850% avg swing). Calmest with Mildly Bullish PRO (32% extreme, 0.876% avg swing).

## Section 3: FII MILDLY BULLISH — Volatility Profile (448 days, 32.6% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 43 | 41.9% | 58.1% | 1.033% | 1.032% | 1.26 | 2.25 | 1.96 | 62.8% |
| Strong Bearish | 40 | 35.0% | 52.5% | 0.863% | 0.863% | 1.24 | 1.87 | 2.26 | 50.0% |
| Mildly Bearish | 78 | 34.6% | 46.2% | 1.004% | 1.004% | 1.16 | 1.85 | 2.03 | 56.4% |
| Mildly Bullish | 105 | 34.3% | 45.7% | 1.094% | 1.094% | 1.17 | 1.65 | 2.24 | 52.4% |
| Bullish | 84 | 28.6% | 47.6% | 1.062% | 1.062% | 1.21 | 1.57 | 2.48 | 44.0% |
| Strong Bullish | 98 | 27.6% | 42.9% | 1.018% | 1.018% | 1.25 | 1.80 | 2.37 | 49.0% |

**Volatility pattern**: Most whipsaw with Bearish PRO (42% extreme days, 1.033% avg swing). Calmest with Strong Bullish PRO (28% extreme, 1.018% avg swing).

## Section 4: FII MILDLY BEARISH — Volatility Profile (437 days, 33.4% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 88 | 38.6% | 54.5% | 1.091% | 1.091% | 1.25 | 1.80 | 2.36 | 46.6% |
| Strong Bearish | 106 | 37.7% | 51.9% | 1.086% | 1.086% | 1.33 | 2.01 | 2.41 | 50.9% |
| Mildly Bullish | 69 | 37.7% | 52.2% | 1.097% | 1.097% | 1.23 | 2.00 | 2.09 | 53.6% |
| Bullish | 28 | 35.7% | 60.7% | 0.966% | 0.966% | 1.16 | 2.01 | 1.87 | 64.3% |
| Strong Bullish | 40 | 32.5% | 55.0% | 0.962% | 0.962% | 1.17 | 1.74 | 2.18 | 52.5% |
| Mildly Bearish | 106 | 21.7% | 36.8% | 1.194% | 1.193% | 1.31 | 1.57 | 2.79 | 44.3% |

**Volatility pattern**: Most whipsaw with Bearish PRO (39% extreme days, 1.091% avg swing). Calmest with Mildly Bearish PRO (22% extreme, 1.194% avg swing).

## Section 5: FII BEARISH — Volatility Profile (184 days, 39.1% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bullish | 7 | 57.1% | 85.7% | 1.423% | 1.421% | 1.83 | 3.66 | 2.45 | 85.7% |
| Mildly Bullish | 11 | 45.5% | 54.5% | 1.256% | 1.258% | 1.52 | 1.80 | 3.27 | 36.4% |
| Bearish | 32 | 40.6% | 53.1% | 1.005% | 1.006% | 1.28 | 1.63 | 2.63 | 43.8% |
| Strong Bearish | 102 | 39.2% | 51.0% | 1.022% | 1.022% | 1.25 | 1.72 | 2.43 | 45.1% |
| Mildly Bearish | 22 | 31.8% | 40.9% | 0.957% | 0.956% | 1.21 | 1.72 | 2.31 | 40.9% |
| Strong Bullish | 10 | 30.0% | 60.0% | 0.829% | 0.827% | 1.16 | 2.22 | 1.64 | 50.0% |

**Volatility pattern**: Most whipsaw with Bullish PRO (57% extreme days, 1.423% avg swing). Calmest with Strong Bullish PRO (30% extreme, 0.829% avg swing).

## Section 6: FII STRONG BEARISH — Volatility Profile (104 days, 44.2% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 9 | 66.7% | 66.7% | 0.872% | 0.871% | 1.13 | 1.65 | 2.11 | 44.4% |
| Strong Bearish | 80 | 42.5% | 57.5% | 1.016% | 1.016% | 1.32 | 1.81 | 2.58 | 40.0% |
| Mildly Bearish | 10 | 40.0% | 80.0% | 1.098% | 1.100% | 1.37 | 1.34 | 3.23 | 20.0% |
| Strong Bullish | 5 | 40.0% | 60.0% | 1.052% | 1.056% | 1.52 | 2.11 | 2.93 | 20.0% |

**Volatility pattern**: Most whipsaw with Bearish PRO (67% extreme days, 0.872% avg swing). Calmest with Strong Bullish PRO (40% extreme, 1.052% avg swing).


---

## Intraday Swing Timing — When Do Whipsaws Happen?

Analysis of 433 extreme whipsaw days with intraday data available.

### Overall Swing Pattern (Extreme Whipsaw Days)

| Pattern | Days | % |
|---|---|---|
| Down Morning → Up Afternoon | 201 | 46.4% |
| Up Morning → Down Afternoon | 159 | 36.7% |
| Both Afternoon | 37 | 8.5% |
| Both Morning | 36 | 8.3% |

### Sequence — Does High or Low Come First?

| Sequence | Days | % |
|---|---|---|
| Low First | 235 | 54.3% |
| High First | 197 | 45.5% |
| Simultaneous | 1 | 0.2% |

### Swing Pattern by FII View (Extreme Whipsaw Days)

| FII View | Days | Up AM→Down PM | Down AM→Up PM | Both AM | Both PM |
|---|---|---|---|---|---|
| Strong Bullish | 37 | 10 (27%) | 22 (59%) | 1 (3%) | 4 (11%) |
| Bullish | 71 | 33 (46%) | 29 (41%) | 8 (11%) | 1 (1%) |
| Mildly Bullish | 104 | 34 (33%) | 52 (50%) | 6 (6%) | 12 (12%) |
| Mildly Bearish | 106 | 37 (35%) | 48 (45%) | 12 (11%) | 9 (8%) |
| Bearish | 68 | 26 (38%) | 33 (49%) | 3 (4%) | 6 (9%) |
| Strong Bearish | 47 | 19 (40%) | 17 (36%) | 6 (13%) | 5 (11%) |

---

## Range vs VIX — Which Combos Exceed VIX Predictions?

Range/VIX Ratio > 1.0 means the actual daily range exceeded the VIX-predicted range. Higher = more volatile than expected.

### Top 10 Combos that EXCEED VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.83** | 1.421% | 0.769% | 57.1% |
| 2 | Bearish | Mildly Bullish | 11 | **1.52** | 1.258% | 0.825% | 45.5% |
| 3 | Strong Bearish | Strong Bullish | 5 | **1.52** | 1.056% | 0.706% | 40.0% |
| 4 | Strong Bearish | Mildly Bearish | 10 | **1.37** | 1.100% | 0.821% | 40.0% |
| 5 | Mildly Bearish | Strong Bearish | 106 | **1.33** | 1.086% | 0.820% | 37.7% |
| 6 | Strong Bearish | Strong Bearish | 80 | **1.32** | 1.016% | 0.764% | 42.5% |
| 7 | Mildly Bearish | Mildly Bearish | 106 | **1.31** | 1.193% | 0.926% | 21.7% |
| 8 | Bearish | Bearish | 32 | **1.28** | 1.006% | 0.802% | 40.6% |
| 9 | Mildly Bullish | Bearish | 43 | **1.26** | 1.032% | 0.827% | 41.9% |
| 10 | Mildly Bearish | Bearish | 88 | **1.25** | 1.091% | 0.875% | 38.6% |

### Top 10 Combos UNDER VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bullish | Mildly Bearish | 17 | **1.01** | 0.885% | 0.865% | 41.2% |
| 2 | Strong Bullish | Strong Bearish | 6 | **1.05** | 0.788% | 0.758% | 66.7% |
| 3 | Strong Bearish | Bearish | 9 | **1.13** | 0.871% | 0.811% | 66.7% |
| 4 | Bullish | Strong Bearish | 17 | **1.14** | 0.851% | 0.746% | 47.1% |
| 5 | Bullish | Strong Bullish | 129 | **1.15** | 0.872% | 0.772% | 36.4% |
| 6 | Bearish | Strong Bullish | 10 | **1.16** | 0.827% | 0.711% | 30.0% |
| 7 | Mildly Bullish | Mildly Bearish | 78 | **1.16** | 1.004% | 0.882% | 34.6% |
| 8 | Mildly Bearish | Bullish | 28 | **1.16** | 0.966% | 0.820% | 35.7% |
| 9 | Mildly Bullish | Mildly Bullish | 105 | **1.17** | 1.094% | 0.939% | 34.3% |
| 10 | Bullish | Mildly Bullish | 19 | **1.17** | 0.876% | 0.779% | 31.6% |

---

## Conclusion

### Key Findings:

1. **Most whipsaw-prone combination**: Strong Bullish FII + Strong Bearish PRO — **66.7%** of days are extreme whipsaws (both sides exceed half VIX), with 0.783% average total swing across 6 days.
2. **Calmest combination**: Mildly Bearish FII + Mildly Bearish PRO — only **21.7%** extreme whipsaw days, 1.194% avg swing across 106 days.
3. **Whipsaw vs Green% correlation**: r = 0.12. Volatile days tend to close green (reversal pattern).
4. **Range exceeds VIX**: 31 out of 31 combinations (≥5 days) have average range > VIX prediction. VIX tends to underestimate actual volatility for most FII×PRO combos.
5. **Dominant whipsaw pattern**: "Down Morning → Up Afternoon" accounts for 46% of extreme whipsaw days.

### Actionable Rules:

- **Expect whipsaw**: Strong Bullish+Strong Bearish (67%), Strong Bearish+Bearish (67%), Bearish+Bullish (57%)
- **Expect directional/calm**: Mildly Bearish+Mildly Bearish (22%), Mildly Bullish+Strong Bullish (28%), Mildly Bullish+Bullish (29%)
- **Straddle/strangle candidates** (high whipsaw + high range/VIX): Strong Bullish+Strong Bearish, Strong Bearish+Bearish, Bearish+Bullish, Bullish+Strong Bearish, Bearish+Mildly Bullish
- **Iron condor / range-bound candidates**: Most combos exceed VIX prediction; look for Mildly Bullish+Mildly Bullish (lowest whipsaw+range/VIX ratio)
