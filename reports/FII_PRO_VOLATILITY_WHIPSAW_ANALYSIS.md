# FII VIEW x PRO VIEW — Volatility & Whipsaw Analysis (Half-VIX Threshold)

**Dataset**: 1,488 days | 2020-08-06 to 2026-09-09 | ±20K Neutral Classification
**Intraday data**: 30-min candles from 2021-09-13 to 2026-09-11 (1242 days)
**VIX Threshold**: Half-VIX = VIX predicted move × 0.5 — a move in one direction must exceed this to count as "significant"

### Label Guide
- **Neutral20** = composite between ±20K (i.e. -20K to +20K)
- **MildBull20** = Mildly Bullish = composite +20K to +50K
- **MildBear20** = Mildly Bearish = composite -20K to -50K
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)

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
| **Bearish** | **Strong Bullish** | 10 | **20.0%** | 30.0% | 0.829% | 0.827% | 1.16 | 50.0% | +0.085% |
| **Strong Bearish** | **Strong Bullish** | 5 | **20.0%** | 40.0% | 1.052% | 1.056% | 1.52 | 20.0% | -0.270% |
| **Bullish** | **MildBull20** | 11 | **18.2%** | 18.2% | 0.853% | 0.854% | 1.19 | 54.5% | +0.217% |
| **MildBear20** | **Strong Bearish** | 76 | **17.1%** | 30.3% | 1.135% | 1.135% | 1.36 | 52.6% | -0.047% |
| **Strong Bearish** | **Neutral20** | 6 | **16.7%** | 50.0% | 0.923% | 0.923% | 1.18 | 33.3% | -0.212% |
| **Neutral20** | **Neutral20** | 108 | **15.7%** | 25.0% | 1.078% | 1.078% | 1.20 | 51.9% | -0.018% |
| **Bearish** | **Strong Bearish** | 102 | **15.7%** | 30.4% | 1.022% | 1.022% | 1.25 | 45.1% | -0.054% |
| **Bullish** | **Neutral20** | 13 | **15.4%** | 23.1% | 0.872% | 0.872% | 1.11 | 69.2% | +0.299% |
| MildBear20 | Bearish | 48 | 14.6% | 31.2% | 1.046% | 1.045% | 1.22 | 39.6% | -0.070% |
| Strong Bullish | MildBull20 | 7 | 14.3% | 14.3% | 1.117% | 1.119% | 1.23 | 42.9% | -0.011% |
| Strong Bearish | Strong Bearish | 80 | 13.8% | 27.5% | 1.016% | 1.016% | 1.32 | 40.0% | -0.092% |
| Bearish | Neutral20 | 15 | 13.3% | 26.7% | 1.138% | 1.138% | 1.39 | 40.0% | -0.199% |
| MildBear20 | Strong Bullish | 15 | 13.3% | 20.0% | 1.043% | 1.041% | 1.27 | 66.7% | -0.010% |
| MildBear20 | MildBull20 | 8 | 12.5% | 12.5% | 1.250% | 1.250% | 1.47 | 75.0% | +0.057% |
| Bullish | Strong Bearish | 17 | 11.8% | 29.4% | 0.850% | 0.851% | 1.14 | 47.1% | +0.024% |
| Neutral20 | Bearish | 61 | 11.5% | 27.9% | 1.129% | 1.129% | 1.28 | 59.0% | +0.008% |
| Strong Bullish | Strong Bullish | 70 | 11.4% | 27.1% | 0.963% | 0.962% | 1.23 | 58.6% | +0.010% |
| Neutral20 | MildBull20 | 54 | 11.1% | 18.5% | 1.201% | 1.201% | 1.26 | 46.3% | -0.128% |
| MildBear20 | Neutral20 | 29 | 10.3% | 17.2% | 1.232% | 1.231% | 1.32 | 37.9% | -0.255% |
| Neutral20 | Strong Bearish | 52 | 9.6% | 19.2% | 0.900% | 0.900% | 1.20 | 48.1% | +0.082% |
| MildBull20 | Bearish | 22 | 9.1% | 22.7% | 0.972% | 0.972% | 1.26 | 59.1% | +0.130% |
| MildBull20 | MildBear20 | 12 | 8.3% | 16.7% | 1.097% | 1.097% | 1.29 | 75.0% | +0.249% |
| MildBear20 | Bullish | 12 | 8.3% | 16.7% | 0.950% | 0.950% | 1.21 | 58.3% | +0.016% |
| Bullish | MildBear20 | 12 | 8.3% | 8.3% | 0.915% | 0.915% | 0.99 | 41.7% | -0.186% |
| Neutral20 | Strong Bullish | 63 | 7.9% | 19.0% | 0.977% | 0.978% | 1.19 | 54.0% | +0.071% |
| Bullish | Bullish | 26 | 7.7% | 19.2% | 0.980% | 0.981% | 1.20 | 53.8% | +0.030% |
| Bearish | MildBear20 | 14 | 7.1% | 21.4% | 0.957% | 0.956% | 1.24 | 42.9% | -0.111% |
| Neutral20 | MildBear20 | 59 | 6.8% | 25.4% | 1.122% | 1.122% | 1.23 | 39.0% | -0.203% |
| Bearish | Bearish | 32 | 6.2% | 28.1% | 1.005% | 1.006% | 1.28 | 43.8% | -0.135% |
| Bullish | Strong Bullish | 129 | 6.2% | 27.1% | 0.872% | 0.872% | 1.15 | 38.8% | -0.151% |
| MildBull20 | Strong Bearish | 18 | 5.6% | 27.8% | 0.921% | 0.921% | 1.34 | 50.0% | +0.036% |
| MildBull20 | Strong Bullish | 60 | 5.0% | 16.7% | 1.017% | 1.016% | 1.26 | 41.7% | -0.174% |
| MildBull20 | Bullish | 51 | 3.9% | 23.5% | 1.071% | 1.071% | 1.25 | 45.1% | -0.118% |
| MildBull20 | MildBull20 | 26 | 3.8% | 19.2% | 1.055% | 1.055% | 1.03 | 65.4% | +0.258% |
| MildBear20 | MildBear20 | 30 | 3.3% | 6.7% | 0.918% | 0.918% | 1.15 | 60.0% | -0.046% |
| MildBull20 | Neutral20 | 32 | 3.1% | 15.6% | 1.066% | 1.065% | 1.23 | 56.2% | -0.161% |
| Strong Bearish | MildBear20 | 7 | 0.0% | 14.3% | 1.086% | 1.087% | 1.44 | 28.6% | -0.463% |
| Neutral20 | Bullish | 49 | 0.0% | 12.2% | 1.025% | 1.025% | 1.15 | 51.0% | +0.039% |
| Strong Bullish | Strong Bearish | 6 | 0.0% | 50.0% | 0.783% | 0.788% | 1.05 | 50.0% | +0.065% |

---

## Top 10 Highest Total Swing Combinations (≥5 days)

Total Swing = (High - Open) + |Low - Open|. This measures how much ground the market covered in both directions.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | VIX Pred% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.423%** | 0.850% | 0.573% | 1.421% | 0.769% | 28.6% | 85.7% |
| 2 | MildBear20 | MildBull20 | 8 | **1.250%** | 0.640% | 0.610% | 1.250% | 0.802% | 12.5% | 75.0% |
| 3 | MildBear20 | Neutral20 | 29 | **1.232%** | 0.375% | 0.857% | 1.231% | 0.952% | 10.3% | 37.9% |
| 4 | Neutral20 | MildBull20 | 54 | **1.201%** | 0.495% | 0.706% | 1.201% | 0.930% | 11.1% | 46.3% |
| 5 | Bearish | Neutral20 | 15 | **1.138%** | 0.439% | 0.699% | 1.138% | 0.829% | 13.3% | 40.0% |
| 6 | MildBear20 | Strong Bearish | 76 | **1.135%** | 0.485% | 0.651% | 1.135% | 0.837% | 17.1% | 52.6% |
| 7 | Neutral20 | Bearish | 61 | **1.129%** | 0.505% | 0.624% | 1.129% | 0.897% | 11.5% | 59.0% |
| 8 | Neutral20 | MildBear20 | 59 | **1.122%** | 0.386% | 0.736% | 1.122% | 0.911% | 6.8% | 39.0% |
| 9 | Strong Bullish | MildBull20 | 7 | **1.117%** | 0.479% | 0.639% | 1.119% | 0.860% | 14.3% | 42.9% |
| 10 | MildBull20 | MildBear20 | 12 | **1.097%** | 0.711% | 0.387% | 1.097% | 0.886% | 8.3% | 75.0% |

---

## Top 10 Lowest Total Swing Combinations (≥5 days)

These combinations produce the calmest, most directional days with minimal whipsaw.

| Rank | FII View | PRO View | Days | Avg Total Swing | Avg Up% | Avg Down% | Avg Range% | Whipsaw Ex% | Green% |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Strong Bullish | Strong Bearish | 6 | **0.783%** | 0.450% | 0.333% | 0.788% | 0.0% | 50.0% |
| 2 | Bearish | Strong Bullish | 10 | **0.829%** | 0.470% | 0.359% | 0.827% | 20.0% | 50.0% |
| 3 | Strong Bullish | Bullish | 5 | **0.842%** | 0.512% | 0.330% | 0.842% | 40.0% | 80.0% |
| 4 | Bullish | Strong Bearish | 17 | **0.850%** | 0.367% | 0.483% | 0.851% | 11.8% | 47.1% |
| 5 | Bullish | MildBull20 | 11 | **0.853%** | 0.506% | 0.346% | 0.854% | 18.2% | 54.5% |
| 6 | Strong Bearish | Bearish | 9 | **0.872%** | 0.377% | 0.496% | 0.871% | 33.3% | 44.4% |
| 7 | Bullish | Neutral20 | 13 | **0.872%** | 0.606% | 0.266% | 0.872% | 15.4% | 69.2% |
| 8 | Bullish | Strong Bullish | 129 | **0.872%** | 0.340% | 0.532% | 0.872% | 6.2% | 38.8% |
| 9 | Neutral20 | Strong Bearish | 52 | **0.900%** | 0.441% | 0.459% | 0.900% | 9.6% | 48.1% |
| 10 | Bullish | MildBear20 | 12 | **0.915%** | 0.432% | 0.483% | 0.915% | 8.3% | 41.7% |

---

## Swing Asymmetry — Which Side Dominates?

**Swing Bias** = Avg Up Ratio - Avg Down Ratio. Positive = upside swings dominate, Negative = downside swings dominate.

### Up-Biased Combinations (swing bias > +0.15)
These combinations swing MORE to the upside relative to VIX. The upside move consumes more of the VIX budget.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| MildBull20 | MildBear20 | 12 | 1.75 | 0.83 | **+0.92** | 75.0% | +0.249% |
| Bullish | Neutral20 | 13 | 1.55 | 0.66 | **+0.89** | 69.2% | +0.299% |
| Bearish | Bullish | 7 | 2.20 | 1.47 | **+0.73** | 85.7% | +0.490% |
| Bullish | MildBull20 | 11 | 1.51 | 0.87 | **+0.64** | 54.5% | +0.217% |
| MildBull20 | Bearish | 22 | 1.57 | 0.96 | **+0.60** | 59.1% | +0.130% |
| Strong Bullish | Bullish | 5 | 1.48 | 1.02 | **+0.45** | 80.0% | +0.238% |
| Bearish | Strong Bullish | 10 | 1.33 | 0.99 | **+0.35** | 50.0% | +0.085% |
| Strong Bullish | Strong Bearish | 6 | 1.21 | 0.88 | **+0.33** | 50.0% | +0.065% |
| MildBear20 | MildBull20 | 8 | 1.55 | 1.38 | **+0.17** | 75.0% | +0.057% |
| MildBull20 | MildBull20 | 26 | 1.12 | 0.95 | **+0.17** | 65.4% | +0.258% |

### Down-Biased Combinations (swing bias < -0.15)
These combinations swing MORE to the downside. Sellers dominate the intraday action.

| FII View | PRO View | Days | Avg Up Ratio | Avg Down Ratio | Swing Bias | Green% | Avg Chg% |
|---|---|---|---|---|---|---|---|
| Strong Bearish | MildBear20 | 7 | 0.86 | 2.03 | **-1.17** | 28.6% | -0.463% |
| MildBear20 | Neutral20 | 29 | 0.84 | 1.80 | **-0.96** | 37.9% | -0.255% |
| Neutral20 | MildBear20 | 59 | 0.83 | 1.64 | **-0.81** | 39.0% | -0.203% |
| Strong Bullish | MildBull20 | 7 | 0.86 | 1.59 | **-0.73** | 42.9% | -0.011% |
| MildBull20 | Bullish | 51 | 0.93 | 1.56 | **-0.64** | 45.1% | -0.118% |
| MildBull20 | Strong Bullish | 60 | 0.96 | 1.57 | **-0.60** | 41.7% | -0.174% |
| Bearish | Bearish | 32 | 0.98 | 1.58 | **-0.60** | 43.8% | -0.135% |
| Bearish | Neutral20 | 15 | 1.11 | 1.68 | **-0.58** | 40.0% | -0.199% |
| Bullish | Strong Bullish | 129 | 0.86 | 1.43 | **-0.56** | 38.8% | -0.151% |
| Strong Bearish | Strong Bullish | 5 | 1.26 | 1.76 | **-0.49** | 20.0% | -0.270% |
| MildBear20 | Bullish | 12 | 0.96 | 1.45 | **-0.49** | 58.3% | +0.016% |
| Strong Bearish | Strong Bearish | 80 | 1.08 | 1.55 | **-0.47** | 40.0% | -0.092% |
| MildBull20 | Neutral20 | 32 | 1.00 | 1.45 | **-0.45** | 56.2% | -0.161% |
| Bearish | MildBear20 | 14 | 1.02 | 1.46 | **-0.44** | 42.9% | -0.111% |
| Strong Bearish | Neutral20 | 6 | 0.96 | 1.40 | **-0.43** | 33.3% | -0.212% |
| Bearish | Strong Bearish | 102 | 1.03 | 1.46 | **-0.43** | 45.1% | -0.054% |
| MildBear20 | Strong Bearish | 76 | 1.15 | 1.57 | **-0.42** | 52.6% | -0.047% |
| Neutral20 | MildBull20 | 54 | 1.06 | 1.46 | **-0.41** | 46.3% | -0.128% |
| Bullish | Strong Bearish | 17 | 0.95 | 1.33 | **-0.39** | 47.1% | +0.024% |
| MildBear20 | Bearish | 48 | 1.04 | 1.41 | **-0.37** | 39.6% | -0.070% |
| MildBear20 | MildBear20 | 30 | 0.98 | 1.31 | **-0.33** | 60.0% | -0.046% |
| Strong Bullish | Strong Bullish | 70 | 1.08 | 1.39 | **-0.31** | 58.6% | +0.010% |
| Neutral20 | Bearish | 61 | 1.13 | 1.42 | **-0.29** | 59.0% | +0.008% |
| Strong Bearish | Bearish | 9 | 0.99 | 1.27 | **-0.28** | 44.4% | -0.076% |
| Neutral20 | Neutral20 | 108 | 1.10 | 1.31 | **-0.21** | 51.9% | -0.018% |

---

## Section 1: FII STRONG BULLISH — Volatility Profile (88 days, 12.5% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bullish | 5 | 40.0% | 40.0% | 0.842% | 0.842% | 1.25 | 1.48 | 1.02 | 80.0% |
| MildBull20 | 7 | 14.3% | 14.3% | 1.117% | 1.119% | 1.23 | 0.86 | 1.59 | 42.9% |
| Strong Bullish | 70 | 11.4% | 27.1% | 0.963% | 0.962% | 1.23 | 1.08 | 1.39 | 58.6% |
| Strong Bearish | 6 | 0.0% | 50.0% | 0.783% | 0.788% | 1.05 | 1.21 | 0.88 | 50.0% |

**Volatility pattern**: Most whipsaw with Bullish PRO (40% extreme days, 0.842% avg swing). Calmest with Strong Bearish PRO (0% extreme, 0.783% avg swing).

## Section 2: FII BULLISH — Volatility Profile (208 days, 8.2% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| MildBull20 | 11 | 18.2% | 18.2% | 0.853% | 0.854% | 1.19 | 1.51 | 0.87 | 54.5% |
| Neutral20 | 13 | 15.4% | 23.1% | 0.872% | 0.872% | 1.11 | 1.55 | 0.66 | 69.2% |
| Strong Bearish | 17 | 11.8% | 29.4% | 0.850% | 0.851% | 1.14 | 0.95 | 1.33 | 47.1% |
| MildBear20 | 12 | 8.3% | 8.3% | 0.915% | 0.915% | 0.99 | 0.96 | 1.03 | 41.7% |
| Bullish | 26 | 7.7% | 19.2% | 0.980% | 0.981% | 1.20 | 1.23 | 1.17 | 53.8% |
| Strong Bullish | 129 | 6.2% | 27.1% | 0.872% | 0.872% | 1.15 | 0.86 | 1.43 | 38.8% |

**Volatility pattern**: Most whipsaw with MildBull20 PRO (18% extreme days, 0.853% avg swing). Calmest with Strong Bullish PRO (6% extreme, 0.872% avg swing).

## Section 3: FII MILDBULL20 — Volatility Profile (221 days, 5.0% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 22 | 9.1% | 22.7% | 0.972% | 0.972% | 1.26 | 1.57 | 0.96 | 59.1% |
| MildBear20 | 12 | 8.3% | 16.7% | 1.097% | 1.097% | 1.29 | 1.75 | 0.83 | 75.0% |
| Strong Bearish | 18 | 5.6% | 27.8% | 0.921% | 0.921% | 1.34 | 1.40 | 1.28 | 50.0% |
| Strong Bullish | 60 | 5.0% | 16.7% | 1.017% | 1.016% | 1.26 | 0.96 | 1.57 | 41.7% |
| Bullish | 51 | 3.9% | 23.5% | 1.071% | 1.071% | 1.25 | 0.93 | 1.56 | 45.1% |
| MildBull20 | 26 | 3.8% | 19.2% | 1.055% | 1.055% | 1.03 | 1.12 | 0.95 | 65.4% |
| Neutral20 | 32 | 3.1% | 15.6% | 1.066% | 1.065% | 1.23 | 1.00 | 1.45 | 56.2% |

**Volatility pattern**: Most whipsaw with Bearish PRO (9% extreme days, 0.972% avg swing). Calmest with Neutral20 PRO (3% extreme, 1.066% avg swing).

## Section 4: FII NEUTRAL20 — Volatility Profile (446 days, 9.9% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Neutral20 | 108 | 15.7% | 25.0% | 1.078% | 1.078% | 1.20 | 1.10 | 1.31 | 51.9% |
| Bearish | 61 | 11.5% | 27.9% | 1.129% | 1.129% | 1.28 | 1.13 | 1.42 | 59.0% |
| MildBull20 | 54 | 11.1% | 18.5% | 1.201% | 1.201% | 1.26 | 1.06 | 1.46 | 46.3% |
| Strong Bearish | 52 | 9.6% | 19.2% | 0.900% | 0.900% | 1.20 | 1.15 | 1.25 | 48.1% |
| Strong Bullish | 63 | 7.9% | 19.0% | 0.977% | 0.978% | 1.19 | 1.14 | 1.23 | 54.0% |
| MildBear20 | 59 | 6.8% | 25.4% | 1.122% | 1.122% | 1.23 | 0.83 | 1.64 | 39.0% |
| Bullish | 49 | 0.0% | 12.2% | 1.025% | 1.025% | 1.15 | 1.10 | 1.21 | 51.0% |

**Volatility pattern**: Most whipsaw with Neutral20 PRO (16% extreme days, 1.078% avg swing). Calmest with Bullish PRO (0% extreme, 1.025% avg swing).

## Section 5: FII MILDBEAR20 — Volatility Profile (218 days, 12.8% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Strong Bearish | 76 | 17.1% | 30.3% | 1.135% | 1.135% | 1.36 | 1.15 | 1.57 | 52.6% |
| Bearish | 48 | 14.6% | 31.2% | 1.046% | 1.045% | 1.22 | 1.04 | 1.41 | 39.6% |
| Strong Bullish | 15 | 13.3% | 20.0% | 1.043% | 1.041% | 1.27 | 1.21 | 1.33 | 66.7% |
| MildBull20 | 8 | 12.5% | 12.5% | 1.250% | 1.250% | 1.47 | 1.55 | 1.38 | 75.0% |
| Neutral20 | 29 | 10.3% | 17.2% | 1.232% | 1.231% | 1.32 | 0.84 | 1.80 | 37.9% |
| Bullish | 12 | 8.3% | 16.7% | 0.950% | 0.950% | 1.21 | 0.96 | 1.45 | 58.3% |
| MildBear20 | 30 | 3.3% | 6.7% | 0.918% | 0.918% | 1.15 | 0.98 | 1.31 | 60.0% |

**Volatility pattern**: Most whipsaw with Strong Bearish PRO (17% extreme days, 1.135% avg swing). Calmest with MildBear20 PRO (3% extreme, 0.918% avg swing).

## Section 6: FII BEARISH — Volatility Profile (180 days, 13.9% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bullish | 7 | 28.6% | 42.9% | 1.423% | 1.421% | 1.83 | 2.20 | 1.47 | 85.7% |
| Strong Bullish | 10 | 20.0% | 30.0% | 0.829% | 0.827% | 1.16 | 1.33 | 0.99 | 50.0% |
| Strong Bearish | 102 | 15.7% | 30.4% | 1.022% | 1.022% | 1.25 | 1.03 | 1.46 | 45.1% |
| Neutral20 | 15 | 13.3% | 26.7% | 1.138% | 1.138% | 1.39 | 1.11 | 1.68 | 40.0% |
| MildBear20 | 14 | 7.1% | 21.4% | 0.957% | 0.956% | 1.24 | 1.02 | 1.46 | 42.9% |
| Bearish | 32 | 6.2% | 28.1% | 1.005% | 1.006% | 1.28 | 0.98 | 1.58 | 43.8% |

**Volatility pattern**: Most whipsaw with Bullish PRO (29% extreme days, 1.423% avg swing). Calmest with Bearish PRO (6% extreme, 1.005% avg swing).

## Section 7: FII STRONG BEARISH — Volatility Profile (107 days, 15.0% avg whipsaw)

| PRO View | Days | Whipsaw Ex% | Strong% | Avg Total Swing | Avg Range% | Range/VIX | Up Ratio | Down Ratio | Green% |
|---|---|---|---|---|---|---|---|---|---|
| Bearish | 9 | 33.3% | 44.4% | 0.872% | 0.871% | 1.13 | 0.99 | 1.27 | 44.4% |
| Strong Bullish | 5 | 20.0% | 40.0% | 1.052% | 1.056% | 1.52 | 1.26 | 1.76 | 20.0% |
| Neutral20 | 6 | 16.7% | 50.0% | 0.923% | 0.923% | 1.18 | 0.96 | 1.40 | 33.3% |
| Strong Bearish | 80 | 13.8% | 27.5% | 1.016% | 1.016% | 1.32 | 1.08 | 1.55 | 40.0% |
| MildBear20 | 7 | 0.0% | 14.3% | 1.086% | 1.087% | 1.44 | 0.86 | 2.03 | 28.6% |

**Volatility pattern**: Most whipsaw with Bearish PRO (33% extreme days, 0.872% avg swing). Calmest with MildBear20 PRO (0% extreme, 1.086% avg swing).


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
| MildBull20 | 11 | 4 (36%) | 6 (55%) | 0 (0%) | 1 (9%) |
| Neutral20 | 34 | 11 (32%) | 17 (50%) | 1 (3%) | 5 (15%) |
| MildBear20 | 24 | 9 (38%) | 15 (62%) | 0 (0%) | 0 (0%) |
| Bearish | 24 | 8 (33%) | 12 (50%) | 0 (0%) | 4 (17%) |
| Strong Bearish | 15 | 7 (47%) | 6 (40%) | 1 (7%) | 1 (7%) |

---

## Range vs VIX — Which Combos Exceed VIX Predictions?

Range/VIX Ratio > 1.0 means the actual daily range exceeded the VIX-predicted range. Higher = more volatile than expected.

### Top 10 Combos that EXCEED VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bearish | Bullish | 7 | **1.83** | 1.421% | 0.769% | 28.6% |
| 2 | Strong Bearish | Strong Bullish | 5 | **1.52** | 1.056% | 0.706% | 20.0% |
| 3 | MildBear20 | MildBull20 | 8 | **1.47** | 1.250% | 0.802% | 12.5% |
| 4 | Strong Bearish | MildBear20 | 7 | **1.44** | 1.087% | 0.744% | 0.0% |
| 5 | Bearish | Neutral20 | 15 | **1.39** | 1.138% | 0.829% | 13.3% |
| 6 | MildBear20 | Strong Bearish | 76 | **1.36** | 1.135% | 0.837% | 17.1% |
| 7 | MildBull20 | Strong Bearish | 18 | **1.34** | 0.921% | 0.711% | 5.6% |
| 8 | MildBear20 | Neutral20 | 29 | **1.32** | 1.231% | 0.952% | 10.3% |
| 9 | Strong Bearish | Strong Bearish | 80 | **1.32** | 1.016% | 0.764% | 13.8% |
| 10 | MildBull20 | MildBear20 | 12 | **1.29** | 1.097% | 0.886% | 8.3% |

### Top 10 Combos UNDER VIX (≥5 days)

| Rank | FII View | PRO View | Days | Avg Range/VIX | Avg Range% | Avg VIX% | Whipsaw Ex% |
|---|---|---|---|---|---|---|---|
| 1 | Bullish | MildBear20 | 12 | **0.99** | 0.915% | 0.904% | 8.3% |
| 2 | MildBull20 | MildBull20 | 26 | **1.03** | 1.055% | 1.030% | 3.8% |
| 3 | Strong Bullish | Strong Bearish | 6 | **1.05** | 0.788% | 0.758% | 0.0% |
| 4 | Bullish | Neutral20 | 13 | **1.11** | 0.872% | 0.810% | 15.4% |
| 5 | Strong Bearish | Bearish | 9 | **1.13** | 0.871% | 0.811% | 33.3% |
| 6 | Bullish | Strong Bearish | 17 | **1.14** | 0.851% | 0.746% | 11.8% |
| 7 | Bullish | Strong Bullish | 129 | **1.15** | 0.872% | 0.772% | 6.2% |
| 8 | MildBear20 | MildBear20 | 30 | **1.15** | 0.918% | 0.825% | 3.3% |
| 9 | Neutral20 | Bullish | 49 | **1.15** | 1.025% | 0.893% | 0.0% |
| 10 | Bearish | Strong Bullish | 10 | **1.16** | 0.827% | 0.711% | 20.0% |

---

## Conclusion

### Key Findings:

1. **Most whipsaw-prone combination**: Strong Bullish FII + Bullish PRO — **40.0%** of days are extreme whipsaws (both sides exceed half VIX), with 0.842% average total swing across 5 days.
2. **Calmest combination**: Strong Bullish FII + Strong Bearish PRO — only **0.0%** extreme whipsaw days, 0.783% avg swing across 6 days.
3. **Whipsaw vs Green% correlation**: r = 0.26. Volatile days tend to close green (reversal pattern).
4. **Range exceeds VIX**: 41 out of 42 combinations (≥5 days) have average range > VIX prediction. VIX tends to underestimate actual volatility for most FII×PRO combos.
5. **Dominant whipsaw pattern**: "Down Morning → Up Afternoon" accounts for 53% of extreme whipsaw days.

### Actionable Rules:

- **Expect whipsaw**: Strong Bullish+Bullish (40%), Strong Bearish+Bearish (33%), Bearish+Bullish (29%)
- **Expect directional/calm**: Strong Bullish+Strong Bearish (0%), Neutral20+Bullish (0%), Strong Bearish+MildBear20 (0%)
- **Straddle/strangle candidates** (high whipsaw + high range/VIX): Strong Bullish+Bullish, Strong Bearish+Bearish, Bearish+Bullish, Bearish+Strong Bullish, Strong Bearish+Strong Bullish
- **Iron condor / range-bound candidates** (low whipsaw + low range/VIX): MildBull20+MildBull20, Strong Bullish+Strong Bearish, Bullish+Strong Bullish, MildBear20+MildBear20
