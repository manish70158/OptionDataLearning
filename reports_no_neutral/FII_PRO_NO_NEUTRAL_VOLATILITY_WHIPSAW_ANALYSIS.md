# FII VIEW x PRO VIEW — Volatility & Whipsaw Analysis (Half-VIX Threshold, No Neutral)

**Dataset**: 1,488 days | 2020-08-06 to 2026-09-09 | No Neutral Classification
**Intraday data**: 30-min candles from 2021-09-13 to 2026-09-11 (1242 days)
**VIX Threshold**: Half-VIX = VIX predicted move × 0.5 — a move in one direction must exceed this to count as "significant"

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional

## How This Report Works

**Concept**: On any given day, VIX predicts an expected daily range. A "whipsaw" day is when the market swings significantly in BOTH directions from the open — going up by a meaningful fraction of the VIX range AND down by a meaningful fraction.

**Threshold used**: **Half-VIX** = VIX predicted move × 0.5. This is the standard half-VIX benchmark.

**Metrics**:
- **Half-VIX** = VIX predicted move × 0.5. This is the benchmark for a "significant" move in one direction.
- **Up Ratio** = (High - Open) / Half-VIX. How much of the VIX budget was used going up.
- **Down Ratio** = |Low - Open| / Half-VIX. How much of the VIX budget was used going down.
- **Whipsaw Extreme**: Both Up Ratio AND Down Ratio > 1.0 (both sides exceeded Half-VIX)
- **Whipsaw Strong**: Both > 0.75
- **Whipsaw Moderate**: Both > 0.50

**Overall Stats**:
- Whipsaw Extreme days: **157** (10.6% of all days)
- Whipsaw Strong days: **361** (24.3% of all days)
- Average Up Ratio: 1.08 | Average Down Ratio: 1.39

---

## Master Table — Combinations Sorted by Whipsaw Extreme %

Combinations with ≥5 days, sorted by % of days that had extreme whipsaw (both sides > half VIX).

| FII View | PRO View | Days | Whipsaw Extreme % | Whipsaw Strong % | Avg Total Swing | Avg Range% | Range/VIX | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|---|---|
| **Strong Bullish** | **Bullish** | 5 | **40.0%** | 40.0% | 0.842% | 0.842% | 1.25 | 80.0% | +0.238% |
| **Strong Bearish** | **Bearish** | 9 | **33.3%** | 44.4% | 0.872% | 0.871% | 1.13 | 44.4% | -0.076% |
| **Bearish** | **Bullish** | 7 | **28.6%** | 42.9% | 1.423% | 1.421% | 1.83 | 85.7% | +0.490% |
| **Bearish** | **Mildly Bullish** | 11 | **27.3%** | 36.4% | 1.256% | 1.258% | 1.52 | 36.4% | -0.405% |
| **Strong Bullish** | **Mildly Bullish** | 9 | **22.2%** | 33.3% | 1.062% | 1.064% | 1.21 | 44.4% | +0.009% |
| **Bearish** | **Strong Bullish** | 10 | **20.0%** | 30.0% | 0.829% | 0.827% | 1.16 | 50.0% | +0.085% |
| **Strong Bearish** | **Strong Bullish** | 5 | **20.0%** | 40.0% | 1.052% | 1.056% | 1.52 | 20.0% | -0.270% |
| **Mildly Bearish** | **Mildly Bullish** | 69 | **15.9%** | 23.2% | 1.097% | 1.097% | 1.23 | 53.6% | +0.016% |
| **Bullish** | **Mildly Bullish** | 19 | **15.8%** | 21.1% | 0.876% | 0.876% | 1.17 | 57.9% | +0.240% |
| **Bearish** | **Strong Bearish** | 102 | **15.7%** | 30.4% | 1.022% | 1.022% | 1.25 | 45.1% | -0.054% |
| Mildly Bearish | Strong Bearish | 106 | 14.2% | 27.4% | 1.086% | 1.086% | 1.33 | 50.9% | +0.017% |
| Strong Bearish | Strong Bearish | 80 | 13.8% | 27.5% | 1.016% | 1.016% | 1.32 | 40.0% | -0.092% |
| Mildly Bearish | Bearish | 88 | 13.6% | 29.5% | 1.091% | 1.091% | 1.25 | 46.6% | -0.039% |
| Bullish | Mildly Bearish | 17 | 11.8% | 11.8% | 0.886% | 0.885% | 1.01 | 52.9% | -0.030% |
| Bullish | Strong Bearish | 17 | 11.8% | 29.4% | 0.850% | 0.851% | 1.14 | 47.1% | +0.024% |
| Strong Bullish | Strong Bullish | 70 | 11.4% | 27.1% | 0.963% | 0.962% | 1.23 | 58.6% | +0.010% |
| Mildly Bullish | Strong Bearish | 40 | 10.0% | 22.5% | 0.863% | 0.863% | 1.24 | 50.0% | -0.011% |
| Mildly Bullish | Mildly Bullish | 105 | 9.5% | 20.0% | 1.094% | 1.094% | 1.17 | 52.4% | -0.042% |
| Mildly Bullish | Bearish | 43 | 9.3% | 25.6% | 1.033% | 1.032% | 1.26 | 62.8% | +0.080% |
| Bearish | Mildly Bearish | 22 | 9.1% | 22.7% | 0.957% | 0.956% | 1.21 | 40.9% | -0.051% |
| Mildly Bearish | Mildly Bearish | 106 | 8.5% | 13.2% | 1.194% | 1.193% | 1.31 | 44.3% | -0.204% |
| Mildly Bullish | Strong Bullish | 98 | 8.2% | 19.4% | 1.018% | 1.018% | 1.25 | 49.0% | -0.037% |
| Bullish | Bullish | 26 | 7.7% | 19.2% | 0.980% | 0.981% | 1.20 | 53.8% | +0.030% |
| Mildly Bullish | Mildly Bearish | 78 | 6.4% | 26.9% | 1.004% | 1.004% | 1.16 | 56.4% | +0.005% |
| Bearish | Bearish | 32 | 6.2% | 28.1% | 1.005% | 1.006% | 1.28 | 43.8% | -0.135% |
| Bullish | Strong Bullish | 129 | 6.2% | 27.1% | 0.872% | 0.872% | 1.15 | 38.8% | -0.151% |
| Mildly Bearish | Strong Bullish | 40 | 5.0% | 15.0% | 0.962% | 0.962% | 1.17 | 52.5% | -0.063% |
| Mildly Bearish | Bullish | 28 | 3.6% | 17.9% | 0.966% | 0.966% | 1.16 | 64.3% | +0.201% |
| Mildly Bullish | Bullish | 84 | 2.4% | 17.9% | 1.062% | 1.062% | 1.21 | 44.0% | -0.114% |
| Strong Bearish | Mildly Bearish | 10 | 0.0% | 20.0% | 1.098% | 1.100% | 1.37 | 20.0% | -0.502% |
| Strong Bullish | Strong Bearish | 6 | 0.0% | 50.0% | 0.783% | 0.788% | 1.05 | 50.0% | +0.065% |

---

## Top 10 Highest Total Swing Combinations (≥5 days)

Total Swing = (High - Open) + |Low - Open|. This measures how much ground the market covered in both directions.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | VIX Pred% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.423%** | 0.850% | 0.573% | 1.421% | 0.769% | 28.6% | 85.7% |
| 2 | Bearish | Mildly Bullish | 11 | **1.256%** | 0.410% | 0.846% | 1.258% | 0.825% | 27.3% | 36.4% |
| 3 | Mildly Bearish | Mildly Bearish | 106 | **1.194%** | 0.424% | 0.770% | 1.193% | 0.926% | 8.5% | 44.3% |
| 4 | Strong Bearish | Mildly Bearish | 10 | **1.098%** | 0.324% | 0.774% | 1.100% | 0.821% | 0.0% | 20.0% |
| 5 | Mildly Bearish | Mildly Bullish | 69 | **1.097%** | 0.521% | 0.577% | 1.097% | 0.890% | 15.9% | 53.6% |
| 6 | Mildly Bullish | Mildly Bullish | 105 | **1.094%** | 0.468% | 0.626% | 1.094% | 0.939% | 9.5% | 52.4% |
| 7 | Mildly Bearish | Bearish | 88 | **1.091%** | 0.475% | 0.617% | 1.091% | 0.875% | 13.6% | 46.6% |
| 8 | Mildly Bearish | Strong Bearish | 106 | **1.086%** | 0.499% | 0.587% | 1.086% | 0.820% | 14.2% | 50.9% |
| 9 | Strong Bullish | Mildly Bullish | 9 | **1.062%** | 0.470% | 0.592% | 1.064% | 0.842% | 22.2% | 44.4% |
| 10 | Mildly Bullish | Bullish | 84 | **1.062%** | 0.409% | 0.653% | 1.062% | 0.876% | 2.4% | 44.0% |

---

## Top 10 Lowest Total Swing Combinations (≥5 days)

These combinations produce the calmest, most directional days with minimal whipsaw.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Strong Bullish | Strong Bearish | 6 | **0.783%** | 0.450% | 0.333% | 0.788% | 0.0% | 50.0% |
| 2 | Bearish | Strong Bullish | 10 | **0.829%** | 0.470% | 0.359% | 0.827% | 20.0% | 50.0% |
| 3 | Strong Bullish | Bullish | 5 | **0.842%** | 0.512% | 0.330% | 0.842% | 40.0% | 80.0% |
| 4 | Bullish | Strong Bearish | 17 | **0.850%** | 0.367% | 0.483% | 0.851% | 11.8% | 47.1% |
| 5 | Mildly Bullish | Strong Bearish | 40 | **0.863%** | 0.390% | 0.474% | 0.863% | 10.0% | 50.0% |
| 6 | Strong Bearish | Bearish | 9 | **0.872%** | 0.377% | 0.496% | 0.871% | 33.3% | 44.4% |
| 7 | Bullish | Strong Bullish | 129 | **0.872%** | 0.340% | 0.532% | 0.872% | 6.2% | 38.8% |
| 8 | Bullish | Mildly Bullish | 19 | **0.876%** | 0.564% | 0.312% | 0.876% | 15.8% | 57.9% |
| 9 | Bullish | Mildly Bearish | 17 | **0.886%** | 0.465% | 0.421% | 0.885% | 11.8% | 52.9% |
| 10 | Bearish | Mildly Bearish | 22 | **0.957%** | 0.415% | 0.542% | 0.956% | 9.1% | 40.9% |

---

## Swing Asymmetry — Which Side Dominates?

**Swing Bias** = Avg Up Ratio - Avg Down Ratio. Positive = upside swings dominate, Negative = downside swings dominate.

### Up-Biased Combinations (swing bias > +0.15)
These combinations swing MORE to the upside relative to VIX. The upside move consumes more of the VIX budget.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| Bullish | Mildly Bullish | 19 | 1.56 | 0.77 | **+0.79** | 57.9% | +0.240% |
| Bearish | Bullish | 7 | 2.20 | 1.47 | **+0.73** | 85.7% | +0.490% |
| Strong Bullish | Bullish | 5 | 1.48 | 1.02 | **+0.45** | 80.0% | +0.238% |
| Bearish | Strong Bullish | 10 | 1.33 | 0.99 | **+0.35** | 50.0% | +0.085% |
| Strong Bullish | Strong Bearish | 6 | 1.21 | 0.88 | **+0.33** | 50.0% | +0.065% |
| Mildly Bullish | Bearish | 43 | 1.35 | 1.18 | **+0.17** | 62.8% | +0.080% |
| Bullish | Mildly Bearish | 17 | 1.09 | 0.93 | **+0.16** | 52.9% | -0.030% |

### Down-Biased Combinations (swing bias < -0.15)
These combinations swing MORE to the downside. Sellers dominate the intraday action.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| Strong Bearish | Mildly Bearish | 10 | 0.81 | 1.94 | **-1.13** | 20.0% | -0.502% |
| Bearish | Mildly Bullish | 11 | 1.08 | 1.96 | **-0.88** | 36.4% | -0.405% |
| Mildly Bearish | Mildly Bearish | 106 | 0.94 | 1.68 | **-0.73** | 44.3% | -0.204% |
| Bearish | Bearish | 32 | 0.98 | 1.58 | **-0.60** | 43.8% | -0.135% |
| Bullish | Strong Bullish | 129 | 0.86 | 1.43 | **-0.56** | 38.8% | -0.151% |
| Strong Bullish | Mildly Bullish | 9 | 0.93 | 1.48 | **-0.55** | 44.4% | +0.009% |
| Mildly Bullish | Bullish | 84 | 0.94 | 1.49 | **-0.55** | 44.0% | -0.114% |
| Strong Bearish | Strong Bullish | 5 | 1.26 | 1.76 | **-0.49** | 20.0% | -0.270% |
| Strong Bearish | Strong Bearish | 80 | 1.08 | 1.55 | **-0.47** | 40.0% | -0.092% |
| Bearish | Strong Bearish | 102 | 1.03 | 1.46 | **-0.43** | 45.1% | -0.054% |
| Bullish | Strong Bearish | 17 | 0.95 | 1.33 | **-0.39** | 47.1% | +0.024% |
| Bearish | Mildly Bearish | 22 | 1.03 | 1.39 | **-0.35** | 40.9% | -0.051% |
| Mildly Bullish | Mildly Bullish | 105 | 0.99 | 1.34 | **-0.35** | 52.4% | -0.042% |
| Mildly Bullish | Strong Bullish | 98 | 1.08 | 1.42 | **-0.34** | 49.0% | -0.037% |
| Mildly Bearish | Bearish | 88 | 1.08 | 1.42 | **-0.34** | 46.6% | -0.039% |
| Strong Bullish | Strong Bullish | 70 | 1.08 | 1.39 | **-0.31** | 58.6% | +0.010% |
| Strong Bearish | Bearish | 9 | 0.99 | 1.27 | **-0.28** | 44.4% | -0.076% |
| Mildly Bearish | Strong Bullish | 40 | 1.04 | 1.31 | **-0.26** | 52.5% | -0.063% |
| Mildly Bearish | Strong Bearish | 106 | 1.20 | 1.45 | **-0.24** | 50.9% | +0.017% |
| Mildly Bullish | Strong Bearish | 40 | 1.12 | 1.35 | **-0.23** | 50.0% | -0.011% |

---

## Section 1: FII STRONG BULLISH — Volatility Profile (90 days, 13.3% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bullish | 5 | 40.0% | 40.0% | 0.842% | 0.842% | 1.25 | 1.48 | 1.02 | 80.0% |
| Mildly Bullish | 9 | 22.2% | 33.3% | 1.062% | 1.064% | 1.21 | 0.93 | 1.48 | 44.4% |
| Strong Bullish | 70 | 11.4% | 27.1% | 0.963% | 0.962% | 1.23 | 1.08 | 1.39 | 58.6% |
| Strong Bearish | 6 | 0.0% | 50.0% | 0.783% | 0.788% | 1.05 | 1.21 | 0.88 | 50.0% |

**Volatility pattern**: Most whipsaw with Bullish PRO (40% extreme days, 0.842% avg swing). Calmest with Strong Bearish PRO (0% extreme, 0.783% avg swing).

## Section 2: FII BULLISH — Volatility Profile (208 days, 8.2% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Mildly Bullish | 19 | 15.8% | 21.1% | 0.876% | 0.876% | 1.17 | 1.56 | 0.77 | 57.9% |
| Mildly Bearish | 17 | 11.8% | 11.8% | 0.886% | 0.885% | 1.01 | 1.09 | 0.93 | 52.9% |
| Strong Bearish | 17 | 11.8% | 29.4% | 0.850% | 0.851% | 1.14 | 0.95 | 1.33 | 47.1% |
| Bullish | 26 | 7.7% | 19.2% | 0.980% | 0.981% | 1.20 | 1.23 | 1.17 | 53.8% |
| Strong Bullish | 129 | 6.2% | 27.1% | 0.872% | 0.872% | 1.15 | 0.86 | 1.43 | 38.8% |

**Volatility pattern**: Most whipsaw with Mildly Bullish PRO (16% extreme days, 0.876% avg swing). Calmest with Strong Bullish PRO (6% extreme, 0.872% avg swing).

## Section 3: FII MILDLY BULLISH — Volatility Profile (448 days, 7.4% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 40 | 10.0% | 22.5% | 0.863% | 0.863% | 1.24 | 1.12 | 1.35 | 50.0% |
| Mildly Bullish | 105 | 9.5% | 20.0% | 1.094% | 1.094% | 1.17 | 0.99 | 1.34 | 52.4% |
| Bearish | 43 | 9.3% | 25.6% | 1.033% | 1.032% | 1.26 | 1.35 | 1.18 | 62.8% |
| Strong Bullish | 98 | 8.2% | 19.4% | 1.018% | 1.018% | 1.25 | 1.08 | 1.42 | 49.0% |
| Mildly Bearish | 78 | 6.4% | 26.9% | 1.004% | 1.004% | 1.16 | 1.11 | 1.22 | 56.4% |
| Bullish | 84 | 2.4% | 17.9% | 1.062% | 1.062% | 1.21 | 0.94 | 1.49 | 44.0% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (10% extreme days, 0.863% avg swing). Calmest with Bullish PRO (2% extreme, 1.062% avg swing).

## Section 4: FII MILDLY BEARISH — Volatility Profile (437 days, 11.4% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Mildly Bullish | 69 | 15.9% | 23.2% | 1.097% | 1.097% | 1.23 | 1.20 | 1.26 | 53.6% |
| Strong Bearish | 106 | 14.2% | 27.4% | 1.086% | 1.086% | 1.33 | 1.20 | 1.45 | 50.9% |
| Bearish | 88 | 13.6% | 29.5% | 1.091% | 1.091% | 1.25 | 1.08 | 1.42 | 46.6% |
| Mildly Bearish | 106 | 8.5% | 13.2% | 1.194% | 1.193% | 1.31 | 0.94 | 1.68 | 44.3% |
| Strong Bullish | 40 | 5.0% | 15.0% | 0.962% | 0.962% | 1.17 | 1.04 | 1.31 | 52.5% |
| Bullish | 28 | 3.6% | 17.9% | 0.966% | 0.966% | 1.16 | 1.21 | 1.12 | 64.3% |

**Volatility pattern**: Most whipsaw with Mildly Bullish PRO (16% extreme days, 1.097% avg swing). Calmest with Bullish PRO (4% extreme, 0.966% avg swing).

## Section 5: FII BEARISH — Volatility Profile (184 days, 14.7% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bullish | 7 | 28.6% | 42.9% | 1.423% | 1.421% | 1.83 | 2.20 | 1.47 | 85.7% |
| Mildly Bullish | 11 | 27.3% | 36.4% | 1.256% | 1.258% | 1.52 | 1.08 | 1.96 | 36.4% |
| Strong Bullish | 10 | 20.0% | 30.0% | 0.829% | 0.827% | 1.16 | 1.33 | 0.99 | 50.0% |
| Strong Bearish | 102 | 15.7% | 30.4% | 1.022% | 1.022% | 1.25 | 1.03 | 1.46 | 45.1% |
| Mildly Bearish | 22 | 9.1% | 22.7% | 0.957% | 0.956% | 1.21 | 1.03 | 1.39 | 40.9% |
| Bearish | 32 | 6.2% | 28.1% | 1.005% | 1.006% | 1.28 | 0.98 | 1.58 | 43.8% |

**Volatility pattern**: Most whipsaw with Bullish PRO (29% extreme days, 1.423% avg swing). Calmest with Bearish PRO (6% extreme, 1.005% avg swing).

## Section 6: FII STRONG BEARISH — Volatility Profile (104 days, 14.4% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 9 | 33.3% | 44.4% | 0.872% | 0.871% | 1.13 | 0.99 | 1.27 | 44.4% |
| Strong Bullish | 5 | 20.0% | 40.0% | 1.052% | 1.056% | 1.52 | 1.26 | 1.76 | 20.0% |
| Strong Bearish | 80 | 13.8% | 27.5% | 1.016% | 1.016% | 1.32 | 1.08 | 1.55 | 40.0% |
| Mildly Bearish | 10 | 0.0% | 20.0% | 1.098% | 1.100% | 1.37 | 0.81 | 1.94 | 20.0% |

**Volatility pattern**: Most whipsaw with Bearish PRO (33% extreme days, 0.872% avg swing). Calmest with Mildly Bearish PRO (0% extreme, 1.098% avg swing).


---

## Intraday Swing Timing — When Do Whipsaws Happen?

Analysis of 136 extreme whipsaw days with intraday data available.

### Overall Swing Pattern (Extreme Whipsaw Days)

| Pattern | Days | % |
|---|---|---|
| Down Morning → Up Afternoon | 72 | 52.9% |
| Up Morning → Down Afternoon | 46 | 33.8% |
| Both Afternoon | 14 | 10.3% |
| Both Morning | 4 | 2.9% |

### Sequence — Does High or Low Come First?

| Sequence | Days | % |
|---|---|---|
| Low First | 79 | 58.1% |
| High First | 57 | 41.9% |

### Swing Pattern by FII View (Extreme Whipsaw Days)

| FII View | Days | Up AM→Down PM | Down AM→Up PM | Both AM | Both PM |
|---|---|---|---|---|---|
| Strong Bullish | 12 | 1 (8%) | 8 (67%) | 0 (0%) | 3 (25%) |
| Bullish | 16 | 6 (38%) | 8 (50%) | 2 (12%) | 0 (0%) |
| Mildly Bullish | 26 | 7 (27%) | 15 (58%) | 0 (0%) | 4 (15%) |
| Mildly Bearish | 43 | 17 (40%) | 23 (53%) | 1 (2%) | 2 (5%) |
| Bearish | 24 | 8 (33%) | 12 (50%) | 0 (0%) | 4 (17%) |
| Strong Bearish | 15 | 7 (47%) | 6 (40%) | 1 (7%) | 1 (7%) |

---

## Range vs VIX — Which Combos Exceed VIX Predictions?

Range/VIX Ratio > 1.0 means the actual daily range exceeded the VIX-predicted range. Higher = more volatile than expected.

### Top 10 Combos that EXCEED VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.83** | 1.421% | 0.769% | 28.6% |
| 2 | Bearish | Mildly Bullish | 11 | **1.52** | 1.258% | 0.825% | 27.3% |
| 3 | Strong Bearish | Strong Bullish | 5 | **1.52** | 1.056% | 0.706% | 20.0% |
| 4 | Strong Bearish | Mildly Bearish | 10 | **1.37** | 1.100% | 0.821% | 0.0% |
| 5 | Mildly Bearish | Strong Bearish | 106 | **1.33** | 1.086% | 0.820% | 14.2% |
| 6 | Strong Bearish | Strong Bearish | 80 | **1.32** | 1.016% | 0.764% | 13.8% |
| 7 | Mildly Bearish | Mildly Bearish | 106 | **1.31** | 1.193% | 0.926% | 8.5% |
| 8 | Bearish | Bearish | 32 | **1.28** | 1.006% | 0.802% | 6.2% |
| 9 | Mildly Bullish | Bearish | 43 | **1.26** | 1.032% | 0.827% | 9.3% |
| 10 | Mildly Bearish | Bearish | 88 | **1.25** | 1.091% | 0.875% | 13.6% |

### Top 10 Combos UNDER VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bullish | Mildly Bearish | 17 | **1.01** | 0.885% | 0.865% | 11.8% |
| 2 | Strong Bullish | Strong Bearish | 6 | **1.05** | 0.788% | 0.758% | 0.0% |
| 3 | Strong Bearish | Bearish | 9 | **1.13** | 0.871% | 0.811% | 33.3% |
| 4 | Bullish | Strong Bearish | 17 | **1.14** | 0.851% | 0.746% | 11.8% |
| 5 | Bullish | Strong Bullish | 129 | **1.15** | 0.872% | 0.772% | 6.2% |
| 6 | Bearish | Strong Bullish | 10 | **1.16** | 0.827% | 0.711% | 20.0% |
| 7 | Mildly Bullish | Mildly Bearish | 78 | **1.16** | 1.004% | 0.882% | 6.4% |
| 8 | Mildly Bearish | Bullish | 28 | **1.16** | 0.966% | 0.820% | 3.6% |
| 9 | Mildly Bullish | Mildly Bullish | 105 | **1.17** | 1.094% | 0.939% | 9.5% |
| 10 | Bullish | Mildly Bullish | 19 | **1.17** | 0.876% | 0.779% | 15.8% |

---

## Conclusion

### Key Findings:

1. **Most whipsaw-prone combination**: Strong Bullish FII + Bullish PRO — **40.0%** of days are extreme whipsaws (both sides exceed half VIX), with 0.842% average total swing across 5 days.
2. **Calmest combination**: Strong Bullish FII + Strong Bearish PRO — only **0.0%** extreme whipsaw days, 0.783% avg swing across 6 days.
3. **Whipsaw vs Green% correlation**: r = 0.31. Volatile days tend to close green (reversal pattern).
4. **Range exceeds VIX**: 31 out of 31 combinations (≥5 days) have average range > VIX prediction. VIX tends to underestimate actual volatility for most FII×PRO combos.
5. **Dominant whipsaw pattern**: "Down Morning → Up Afternoon" accounts for 53% of extreme whipsaw days.

### Actionable Rules:

- **Expect whipsaw**: Strong Bullish+Bullish (40%), Strong Bearish+Bearish (33%), Bearish+Bullish (29%)
- **Expect directional/calm**: Strong Bullish+Strong Bearish (0%), Strong Bearish+Mildly Bearish (0%), Mildly Bullish+Bullish (2%)
- **Straddle/strangle candidates** (high whipsaw + high range/VIX): Strong Bullish+Bullish, Strong Bearish+Bearish, Bearish+Bullish, Bearish+Mildly Bullish, Strong Bullish+Mildly Bullish
- **Iron condor / range-bound candidates** (low whipsaw + low range/VIX): Strong Bullish+Strong Bearish, Bullish+Strong Bullish
