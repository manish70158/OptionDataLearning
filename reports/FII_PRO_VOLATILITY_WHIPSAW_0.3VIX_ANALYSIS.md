# FII VIEW x PRO VIEW — Volatility & Whipsaw Analysis (0.3×VIX Threshold)

**Dataset**: 1,488 days | 2020-08-06 to 2026-09-09 | ±20K Neutral Classification
**Intraday data**: 30-min candles from 2021-09-13 to 2026-09-11 (1242 days)
**VIX Threshold**: 0.3×VIX = VIX predicted move × 0.3 — a move in one direction must exceed this to count as "significant"

### Label Guide
- **Neutral20** = composite between ±20K (i.e. -20K to +20K)
- **MildBull20** = Mildly Bullish = composite +20K to +50K
- **MildBear20** = Mildly Bearish = composite -20K to -50K
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)

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
| **Strong Bearish** | **Neutral20** | 6 | **66.7%** | 83.3% | 0.923% | 0.923% | 1.18 | 33.3% | -0.212% |
| **Strong Bearish** | **Bearish** | 9 | **66.7%** | 66.7% | 0.872% | 0.871% | 1.13 | 44.4% | -0.076% |
| **Bearish** | **Bullish** | 7 | **57.1%** | 85.7% | 1.423% | 1.421% | 1.83 | 85.7% | +0.490% |
| **Bullish** | **Strong Bearish** | 17 | **47.1%** | 64.7% | 0.850% | 0.851% | 1.14 | 47.1% | +0.024% |
| **MildBear20** | **Bearish** | 48 | **45.8%** | 64.6% | 1.046% | 1.045% | 1.22 | 39.6% | -0.070% |
| **MildBull20** | **Strong Bearish** | 18 | **44.4%** | 55.6% | 0.921% | 0.921% | 1.34 | 50.0% | +0.036% |
| **Strong Bearish** | **Strong Bearish** | 80 | **42.5%** | 57.5% | 1.016% | 1.016% | 1.32 | 40.0% | -0.092% |
| **Bullish** | **MildBear20** | 12 | **41.7%** | 50.0% | 0.915% | 0.915% | 0.99 | 41.7% | -0.186% |
| **MildBear20** | **Strong Bearish** | 76 | **40.8%** | 52.6% | 1.135% | 1.135% | 1.36 | 52.6% | -0.047% |
| **Bearish** | **Bearish** | 32 | **40.6%** | 53.1% | 1.005% | 1.006% | 1.28 | 43.8% | -0.135% |
| **Strong Bullish** | **Bullish** | 5 | **40.0%** | 60.0% | 0.842% | 0.842% | 1.25 | 80.0% | +0.238% |
| **Strong Bearish** | **Strong Bullish** | 5 | **40.0%** | 60.0% | 1.052% | 1.056% | 1.52 | 20.0% | -0.270% |
| **MildBear20** | **Strong Bullish** | 15 | **40.0%** | 80.0% | 1.043% | 1.041% | 1.27 | 66.7% | -0.010% |
| **Strong Bullish** | **Strong Bullish** | 70 | **40.0%** | 55.7% | 0.963% | 0.962% | 1.23 | 58.6% | +0.010% |
| **Neutral20** | **Neutral20** | 108 | **39.8%** | 49.1% | 1.078% | 1.078% | 1.20 | 51.9% | -0.018% |
| **Bearish** | **Strong Bearish** | 102 | **39.2%** | 51.0% | 1.022% | 1.022% | 1.25 | 45.1% | -0.054% |
| **Neutral20** | **Bearish** | 61 | **37.7%** | 52.5% | 1.129% | 1.129% | 1.28 | 59.0% | +0.008% |
| **Bullish** | **Strong Bullish** | 129 | **36.4%** | 44.2% | 0.872% | 0.872% | 1.15 | 38.8% | -0.151% |
| **Bullish** | **MildBull20** | 11 | **36.4%** | 45.5% | 0.853% | 0.854% | 1.19 | 54.5% | +0.217% |
| **Bearish** | **MildBear20** | 14 | **35.7%** | 50.0% | 0.957% | 0.956% | 1.24 | 42.9% | -0.111% |
| **MildBull20** | **Bullish** | 51 | **35.3%** | 47.1% | 1.071% | 1.071% | 1.25 | 45.1% | -0.118% |
| **Bullish** | **Bullish** | 26 | **34.6%** | 50.0% | 0.980% | 0.981% | 1.20 | 53.8% | +0.030% |
| **MildBull20** | **Neutral20** | 32 | **34.4%** | 43.8% | 1.066% | 1.065% | 1.23 | 56.2% | -0.161% |
| **Bearish** | **Neutral20** | 15 | **33.3%** | 33.3% | 1.138% | 1.138% | 1.39 | 40.0% | -0.199% |
| **Neutral20** | **MildBull20** | 54 | **33.3%** | 42.6% | 1.201% | 1.201% | 1.26 | 46.3% | -0.128% |
| **Neutral20** | **MildBear20** | 59 | **32.2%** | 52.5% | 1.122% | 1.122% | 1.23 | 39.0% | -0.203% |
| **MildBull20** | **Bearish** | 22 | **31.8%** | 45.5% | 0.972% | 0.972% | 1.26 | 59.1% | +0.130% |
| **Bullish** | **Neutral20** | 13 | **30.8%** | 69.2% | 0.872% | 0.872% | 1.11 | 69.2% | +0.299% |
| **Neutral20** | **Strong Bullish** | 63 | **30.2%** | 47.6% | 0.977% | 0.978% | 1.19 | 54.0% | +0.071% |
| **Bearish** | **Strong Bullish** | 10 | **30.0%** | 60.0% | 0.829% | 0.827% | 1.16 | 50.0% | +0.085% |
| **Neutral20** | **Strong Bearish** | 52 | **28.8%** | 50.0% | 0.900% | 0.900% | 1.20 | 48.1% | +0.082% |
| **Strong Bearish** | **MildBear20** | 7 | **28.6%** | 71.4% | 1.086% | 1.087% | 1.44 | 28.6% | -0.463% |
| **MildBear20** | **MildBear20** | 30 | **26.7%** | 40.0% | 0.918% | 0.918% | 1.15 | 60.0% | -0.046% |
| **Neutral20** | **Bullish** | 49 | **26.5%** | 53.1% | 1.025% | 1.025% | 1.15 | 51.0% | +0.039% |
| **MildBull20** | **Strong Bullish** | 60 | **25.0%** | 36.7% | 1.017% | 1.016% | 1.26 | 41.7% | -0.174% |
| **MildBear20** | **Bullish** | 12 | **25.0%** | 58.3% | 0.950% | 0.950% | 1.21 | 58.3% | +0.016% |
| **MildBull20** | **MildBull20** | 26 | **19.2%** | 42.3% | 1.055% | 1.055% | 1.03 | 65.4% | +0.258% |
| **MildBear20** | **Neutral20** | 29 | **17.2%** | 31.0% | 1.232% | 1.231% | 1.32 | 37.9% | -0.255% |
| **MildBull20** | **MildBear20** | 12 | **16.7%** | 25.0% | 1.097% | 1.097% | 1.29 | 75.0% | +0.249% |
| Strong Bullish | MildBull20 | 7 | 14.3% | 14.3% | 1.117% | 1.119% | 1.23 | 42.9% | -0.011% |
| MildBear20 | MildBull20 | 8 | 12.5% | 37.5% | 1.250% | 1.250% | 1.47 | 75.0% | +0.057% |

---

## Top 10 Highest Total Swing Combinations (≥5 days)

Total Swing = (High - Open) + |Low - Open|. This measures how much ground the market covered in both directions.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | VIX Pred% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.423%** | 0.850% | 0.573% | 1.421% | 0.769% | 57.1% | 85.7% |
| 2 | MildBear20 | MildBull20 | 8 | **1.250%** | 0.640% | 0.610% | 1.250% | 0.802% | 12.5% | 75.0% |
| 3 | MildBear20 | Neutral20 | 29 | **1.232%** | 0.375% | 0.857% | 1.231% | 0.952% | 17.2% | 37.9% |
| 4 | Neutral20 | MildBull20 | 54 | **1.201%** | 0.495% | 0.706% | 1.201% | 0.930% | 33.3% | 46.3% |
| 5 | Bearish | Neutral20 | 15 | **1.138%** | 0.439% | 0.699% | 1.138% | 0.829% | 33.3% | 40.0% |
| 6 | MildBear20 | Strong Bearish | 76 | **1.135%** | 0.485% | 0.651% | 1.135% | 0.837% | 40.8% | 52.6% |
| 7 | Neutral20 | Bearish | 61 | **1.129%** | 0.505% | 0.624% | 1.129% | 0.897% | 37.7% | 59.0% |
| 8 | Neutral20 | MildBear20 | 59 | **1.122%** | 0.386% | 0.736% | 1.122% | 0.911% | 32.2% | 39.0% |
| 9 | Strong Bullish | MildBull20 | 7 | **1.117%** | 0.479% | 0.639% | 1.119% | 0.860% | 14.3% | 42.9% |
| 10 | MildBull20 | MildBear20 | 12 | **1.097%** | 0.711% | 0.387% | 1.097% | 0.886% | 16.7% | 75.0% |

---

## Top 10 Lowest Total Swing Combinations (≥5 days)

These combinations produce the calmest, most directional days with minimal whipsaw.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Strong Bullish | Strong Bearish | 6 | **0.783%** | 0.450% | 0.333% | 0.788% | 66.7% | 50.0% |
| 2 | Bearish | Strong Bullish | 10 | **0.829%** | 0.470% | 0.359% | 0.827% | 30.0% | 50.0% |
| 3 | Strong Bullish | Bullish | 5 | **0.842%** | 0.512% | 0.330% | 0.842% | 40.0% | 80.0% |
| 4 | Bullish | Strong Bearish | 17 | **0.850%** | 0.367% | 0.483% | 0.851% | 47.1% | 47.1% |
| 5 | Bullish | MildBull20 | 11 | **0.853%** | 0.506% | 0.346% | 0.854% | 36.4% | 54.5% |
| 6 | Strong Bearish | Bearish | 9 | **0.872%** | 0.377% | 0.496% | 0.871% | 66.7% | 44.4% |
| 7 | Bullish | Neutral20 | 13 | **0.872%** | 0.606% | 0.266% | 0.872% | 30.8% | 69.2% |
| 8 | Bullish | Strong Bullish | 129 | **0.872%** | 0.340% | 0.532% | 0.872% | 36.4% | 38.8% |
| 9 | Neutral20 | Strong Bearish | 52 | **0.900%** | 0.441% | 0.459% | 0.900% | 28.8% | 48.1% |
| 10 | Bullish | MildBear20 | 12 | **0.915%** | 0.432% | 0.483% | 0.915% | 41.7% | 41.7% |

---

## Swing Asymmetry — Which Side Dominates?

**Swing Bias** = Avg Up Ratio - Avg Down Ratio. Positive = upside swings dominate, Negative = downside swings dominate.

### Up-Biased Combinations (swing bias > +0.15)
These combinations swing MORE to the upside relative to VIX. The upside move consumes more of the VIX budget.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| MildBull20 | MildBear20 | 12 | 2.92 | 1.38 | **+1.54** | 75.0% | +0.249% |
| Bullish | Neutral20 | 13 | 2.59 | 1.10 | **+1.48** | 69.2% | +0.299% |
| Bearish | Bullish | 7 | 3.66 | 2.45 | **+1.22** | 85.7% | +0.490% |
| Bullish | MildBull20 | 11 | 2.51 | 1.45 | **+1.06** | 54.5% | +0.217% |
| MildBull20 | Bearish | 22 | 2.62 | 1.61 | **+1.01** | 59.1% | +0.130% |
| Strong Bullish | Bullish | 5 | 2.46 | 1.71 | **+0.75** | 80.0% | +0.238% |
| Bearish | Strong Bullish | 10 | 2.22 | 1.64 | **+0.58** | 50.0% | +0.085% |
| Strong Bullish | Strong Bearish | 6 | 2.02 | 1.46 | **+0.55** | 50.0% | +0.065% |
| MildBear20 | MildBull20 | 8 | 2.59 | 2.30 | **+0.29** | 75.0% | +0.057% |
| MildBull20 | MildBull20 | 26 | 1.86 | 1.58 | **+0.28** | 65.4% | +0.258% |
| MildBull20 | Strong Bearish | 18 | 2.34 | 2.13 | **+0.21** | 50.0% | +0.036% |

### Down-Biased Combinations (swing bias < -0.15)
These combinations swing MORE to the downside. Sellers dominate the intraday action.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| Strong Bearish | MildBear20 | 7 | 1.43 | 3.38 | **-1.94** | 28.6% | -0.463% |
| MildBear20 | Neutral20 | 29 | 1.41 | 3.00 | **-1.59** | 37.9% | -0.255% |
| Neutral20 | MildBear20 | 59 | 1.38 | 2.73 | **-1.35** | 39.0% | -0.203% |
| Strong Bullish | MildBull20 | 7 | 1.43 | 2.65 | **-1.22** | 42.9% | -0.011% |
| MildBull20 | Bullish | 51 | 1.55 | 2.60 | **-1.06** | 45.1% | -0.118% |
| MildBull20 | Strong Bullish | 60 | 1.60 | 2.61 | **-1.01** | 41.7% | -0.174% |
| Bearish | Bearish | 32 | 1.63 | 2.63 | **-1.00** | 43.8% | -0.135% |
| Bearish | Neutral20 | 15 | 1.85 | 2.81 | **-0.96** | 40.0% | -0.199% |
| Bullish | Strong Bullish | 129 | 1.44 | 2.38 | **-0.94** | 38.8% | -0.151% |
| Strong Bearish | Strong Bullish | 5 | 2.11 | 2.93 | **-0.82** | 20.0% | -0.270% |
| MildBear20 | Bullish | 12 | 1.61 | 2.42 | **-0.81** | 58.3% | +0.016% |
| Strong Bearish | Strong Bearish | 80 | 1.81 | 2.58 | **-0.78** | 40.0% | -0.092% |
| MildBull20 | Neutral20 | 32 | 1.67 | 2.42 | **-0.75** | 56.2% | -0.161% |
| Bearish | MildBear20 | 14 | 1.71 | 2.44 | **-0.73** | 42.9% | -0.111% |
| Strong Bearish | Neutral20 | 6 | 1.61 | 2.33 | **-0.72** | 33.3% | -0.212% |
| Bearish | Strong Bearish | 102 | 1.72 | 2.43 | **-0.72** | 45.1% | -0.054% |
| MildBear20 | Strong Bearish | 76 | 1.92 | 2.62 | **-0.70** | 52.6% | -0.047% |
| Neutral20 | MildBull20 | 54 | 1.76 | 2.44 | **-0.68** | 46.3% | -0.128% |
| Bullish | Strong Bearish | 17 | 1.58 | 2.22 | **-0.65** | 47.1% | +0.024% |
| MildBear20 | Bearish | 48 | 1.73 | 2.34 | **-0.61** | 39.6% | -0.070% |
| MildBear20 | MildBear20 | 30 | 1.63 | 2.19 | **-0.56** | 60.0% | -0.046% |
| Strong Bullish | Strong Bullish | 70 | 1.80 | 2.31 | **-0.51** | 58.6% | +0.010% |
| Neutral20 | Bearish | 61 | 1.88 | 2.37 | **-0.49** | 59.0% | +0.008% |
| Strong Bearish | Bearish | 9 | 1.65 | 2.11 | **-0.46** | 44.4% | -0.076% |
| Neutral20 | Neutral20 | 108 | 1.84 | 2.18 | **-0.34** | 51.9% | -0.018% |
| MildBear20 | Strong Bullish | 15 | 2.02 | 2.21 | **-0.19** | 66.7% | -0.010% |
| Neutral20 | Bullish | 49 | 1.84 | 2.01 | **-0.18** | 51.0% | +0.039% |
| Neutral20 | Strong Bearish | 52 | 1.91 | 2.09 | **-0.17** | 48.1% | +0.082% |
| Neutral20 | Strong Bullish | 63 | 1.90 | 2.05 | **-0.15** | 54.0% | +0.071% |

---

## Section 1: FII STRONG BULLISH — Volatility Profile (88 days, 39.8% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 6 | 66.7% | 83.3% | 0.783% | 0.788% | 1.05 | 2.02 | 1.46 | 50.0% |
| Bullish | 5 | 40.0% | 60.0% | 0.842% | 0.842% | 1.25 | 2.46 | 1.71 | 80.0% |
| Strong Bullish | 70 | 40.0% | 55.7% | 0.963% | 0.962% | 1.23 | 1.80 | 2.31 | 58.6% |
| MildBull20 | 7 | 14.3% | 14.3% | 1.117% | 1.119% | 1.23 | 1.43 | 2.65 | 42.9% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (67% extreme days, 0.783% avg swing). Calmest with MildBull20 PRO (14% extreme, 1.117% avg swing).

## Section 2: FII BULLISH — Volatility Profile (208 days, 37.0% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 17 | 47.1% | 64.7% | 0.850% | 0.851% | 1.14 | 1.58 | 2.22 | 47.1% |
| MildBear20 | 12 | 41.7% | 50.0% | 0.915% | 0.915% | 0.99 | 1.59 | 1.71 | 41.7% |
| Strong Bullish | 129 | 36.4% | 44.2% | 0.872% | 0.872% | 1.15 | 1.44 | 2.38 | 38.8% |
| MildBull20 | 11 | 36.4% | 45.5% | 0.853% | 0.854% | 1.19 | 2.51 | 1.45 | 54.5% |
| Bullish | 26 | 34.6% | 50.0% | 0.980% | 0.981% | 1.20 | 2.04 | 1.95 | 53.8% |
| Neutral20 | 13 | 30.8% | 69.2% | 0.872% | 0.872% | 1.11 | 2.59 | 1.10 | 69.2% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (47% extreme days, 0.850% avg swing). Calmest with Neutral20 PRO (31% extreme, 0.872% avg swing).

## Section 3: FII MILDBULL20 — Volatility Profile (221 days, 29.9% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 18 | 44.4% | 55.6% | 0.921% | 0.921% | 1.34 | 2.34 | 2.13 | 50.0% |
| Bullish | 51 | 35.3% | 47.1% | 1.071% | 1.071% | 1.25 | 1.55 | 2.60 | 45.1% |
| Neutral20 | 32 | 34.4% | 43.8% | 1.066% | 1.065% | 1.23 | 1.67 | 2.42 | 56.2% |
| Bearish | 22 | 31.8% | 45.5% | 0.972% | 0.972% | 1.26 | 2.62 | 1.61 | 59.1% |
| Strong Bullish | 60 | 25.0% | 36.7% | 1.017% | 1.016% | 1.26 | 1.60 | 2.61 | 41.7% |
| MildBull20 | 26 | 19.2% | 42.3% | 1.055% | 1.055% | 1.03 | 1.86 | 1.58 | 65.4% |
| MildBear20 | 12 | 16.7% | 25.0% | 1.097% | 1.097% | 1.29 | 2.92 | 1.38 | 75.0% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (44% extreme days, 0.921% avg swing). Calmest with MildBear20 PRO (17% extreme, 1.097% avg swing).

## Section 4: FII NEUTRAL20 — Volatility Profile (446 days, 33.6% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Neutral20 | 108 | 39.8% | 49.1% | 1.078% | 1.078% | 1.20 | 1.84 | 2.18 | 51.9% |
| Bearish | 61 | 37.7% | 52.5% | 1.129% | 1.129% | 1.28 | 1.88 | 2.37 | 59.0% |
| MildBull20 | 54 | 33.3% | 42.6% | 1.201% | 1.201% | 1.26 | 1.76 | 2.44 | 46.3% |
| MildBear20 | 59 | 32.2% | 52.5% | 1.122% | 1.122% | 1.23 | 1.38 | 2.73 | 39.0% |
| Strong Bullish | 63 | 30.2% | 47.6% | 0.977% | 0.978% | 1.19 | 1.90 | 2.05 | 54.0% |
| Strong Bearish | 52 | 28.8% | 50.0% | 0.900% | 0.900% | 1.20 | 1.91 | 2.09 | 48.1% |
| Bullish | 49 | 26.5% | 53.1% | 1.025% | 1.025% | 1.15 | 1.84 | 2.01 | 51.0% |

**Volatility pattern**: Most whipsaw with Neutral20 PRO (40% extreme days, 1.078% avg swing). Calmest with Bullish PRO (27% extreme, 1.025% avg swing).

## Section 5: FII MILDBEAR20 — Volatility Profile (218 days, 34.9% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 48 | 45.8% | 64.6% | 1.046% | 1.045% | 1.22 | 1.73 | 2.34 | 39.6% |
| Strong Bearish | 76 | 40.8% | 52.6% | 1.135% | 1.135% | 1.36 | 1.92 | 2.62 | 52.6% |
| Strong Bullish | 15 | 40.0% | 80.0% | 1.043% | 1.041% | 1.27 | 2.02 | 2.21 | 66.7% |
| MildBear20 | 30 | 26.7% | 40.0% | 0.918% | 0.918% | 1.15 | 1.63 | 2.19 | 60.0% |
| Bullish | 12 | 25.0% | 58.3% | 0.950% | 0.950% | 1.21 | 1.61 | 2.42 | 58.3% |
| Neutral20 | 29 | 17.2% | 31.0% | 1.232% | 1.231% | 1.32 | 1.41 | 3.00 | 37.9% |
| MildBull20 | 8 | 12.5% | 37.5% | 1.250% | 1.250% | 1.47 | 2.59 | 2.30 | 75.0% |

**Volatility pattern**: Most whipsaw with Bearish PRO (46% extreme days, 1.046% avg swing). Calmest with MildBull20 PRO (12% extreme, 1.250% avg swing).

## Section 6: FII BEARISH — Volatility Profile (180 days, 38.9% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bullish | 7 | 57.1% | 85.7% | 1.423% | 1.421% | 1.83 | 3.66 | 2.45 | 85.7% |
| Bearish | 32 | 40.6% | 53.1% | 1.005% | 1.006% | 1.28 | 1.63 | 2.63 | 43.8% |
| Strong Bearish | 102 | 39.2% | 51.0% | 1.022% | 1.022% | 1.25 | 1.72 | 2.43 | 45.1% |
| MildBear20 | 14 | 35.7% | 50.0% | 0.957% | 0.956% | 1.24 | 1.71 | 2.44 | 42.9% |
| Neutral20 | 15 | 33.3% | 33.3% | 1.138% | 1.138% | 1.39 | 1.85 | 2.81 | 40.0% |
| Strong Bullish | 10 | 30.0% | 60.0% | 0.829% | 0.827% | 1.16 | 2.22 | 1.64 | 50.0% |

**Volatility pattern**: Most whipsaw with Bullish PRO (57% extreme days, 1.423% avg swing). Calmest with Strong Bullish PRO (30% extreme, 0.829% avg swing).

## Section 7: FII STRONG BEARISH — Volatility Profile (107 days, 44.9% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 9 | 66.7% | 66.7% | 0.872% | 0.871% | 1.13 | 1.65 | 2.11 | 44.4% |
| Neutral20 | 6 | 66.7% | 83.3% | 0.923% | 0.923% | 1.18 | 1.61 | 2.33 | 33.3% |
| Strong Bearish | 80 | 42.5% | 57.5% | 1.016% | 1.016% | 1.32 | 1.81 | 2.58 | 40.0% |
| Strong Bullish | 5 | 40.0% | 60.0% | 1.052% | 1.056% | 1.52 | 2.11 | 2.93 | 20.0% |
| MildBear20 | 7 | 28.6% | 71.4% | 1.086% | 1.087% | 1.44 | 1.43 | 3.38 | 28.6% |

**Volatility pattern**: Most whipsaw with Bearish PRO (67% extreme days, 0.872% avg swing). Calmest with MildBear20 PRO (29% extreme, 1.086% avg swing).


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
| MildBull20 | 52 | 21 (40%) | 27 (52%) | 2 (4%) | 2 (4%) |
| Neutral20 | 98 | 29 (30%) | 43 (44%) | 10 (10%) | 16 (16%) |
| MildBear20 | 60 | 21 (35%) | 30 (50%) | 6 (10%) | 3 (5%) |
| Bearish | 68 | 26 (38%) | 33 (49%) | 3 (4%) | 6 (9%) |
| Strong Bearish | 47 | 19 (40%) | 17 (36%) | 6 (13%) | 5 (11%) |

---

## Range vs VIX — Which Combos Exceed VIX Predictions?

Range/VIX Ratio > 1.0 means the actual daily range exceeded the VIX-predicted range. Higher = more volatile than expected.

### Top 10 Combos that EXCEED VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.83** | 1.421% | 0.769% | 57.1% |
| 2 | Strong Bearish | Strong Bullish | 5 | **1.52** | 1.056% | 0.706% | 40.0% |
| 3 | MildBear20 | MildBull20 | 8 | **1.47** | 1.250% | 0.802% | 12.5% |
| 4 | Strong Bearish | MildBear20 | 7 | **1.44** | 1.087% | 0.744% | 28.6% |
| 5 | Bearish | Neutral20 | 15 | **1.39** | 1.138% | 0.829% | 33.3% |
| 6 | MildBear20 | Strong Bearish | 76 | **1.36** | 1.135% | 0.837% | 40.8% |
| 7 | MildBull20 | Strong Bearish | 18 | **1.34** | 0.921% | 0.711% | 44.4% |
| 8 | MildBear20 | Neutral20 | 29 | **1.32** | 1.231% | 0.952% | 17.2% |
| 9 | Strong Bearish | Strong Bearish | 80 | **1.32** | 1.016% | 0.764% | 42.5% |
| 10 | MildBull20 | MildBear20 | 12 | **1.29** | 1.097% | 0.886% | 16.7% |

### Top 10 Combos UNDER VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bullish | MildBear20 | 12 | **0.99** | 0.915% | 0.904% | 41.7% |
| 2 | MildBull20 | MildBull20 | 26 | **1.03** | 1.055% | 1.030% | 19.2% |
| 3 | Strong Bullish | Strong Bearish | 6 | **1.05** | 0.788% | 0.758% | 66.7% |
| 4 | Bullish | Neutral20 | 13 | **1.11** | 0.872% | 0.810% | 30.8% |
| 5 | Strong Bearish | Bearish | 9 | **1.13** | 0.871% | 0.811% | 66.7% |
| 6 | Bullish | Strong Bearish | 17 | **1.14** | 0.851% | 0.746% | 47.1% |
| 7 | Bullish | Strong Bullish | 129 | **1.15** | 0.872% | 0.772% | 36.4% |
| 8 | MildBear20 | MildBear20 | 30 | **1.15** | 0.918% | 0.825% | 26.7% |
| 9 | Neutral20 | Bullish | 49 | **1.15** | 1.025% | 0.893% | 26.5% |
| 10 | Bearish | Strong Bullish | 10 | **1.16** | 0.827% | 0.711% | 30.0% |

---

## Conclusion

### Key Findings:

1. **Most whipsaw-prone combination**: Strong Bullish FII + Strong Bearish PRO — **66.7%** of days are extreme whipsaws (both sides exceed half VIX), with 0.783% average total swing across 6 days.
2. **Calmest combination**: MildBear20 FII + MildBull20 PRO — only **12.5%** extreme whipsaw days, 1.250% avg swing across 8 days.
3. **Whipsaw vs Green% correlation**: r = -0.15. Volatile days tend to close red.
4. **Range exceeds VIX**: 41 out of 42 combinations (≥5 days) have average range > VIX prediction. VIX tends to underestimate actual volatility for most FII×PRO combos.
5. **Dominant whipsaw pattern**: "Down Morning → Up Afternoon" accounts for 46% of extreme whipsaw days.

### Actionable Rules:

- **Expect whipsaw**: Strong Bullish+Strong Bearish (67%), Strong Bearish+Neutral20 (67%), Strong Bearish+Bearish (67%)
- **Expect directional/calm**: MildBear20+MildBull20 (12%), Strong Bullish+MildBull20 (14%), MildBull20+MildBear20 (17%)
- **Straddle/strangle candidates** (high whipsaw + high range/VIX): Strong Bullish+Strong Bearish, Strong Bearish+Neutral20, Strong Bearish+Bearish, Bearish+Bullish, Bullish+Strong Bearish
- **Iron condor / range-bound candidates**: Most combos exceed VIX prediction; use MildlyBullish+MildlyBullish (lowest whipsaw+range/VIX ratio) or Bullish+StrongBearish
