# FII VIEW x PRO VIEW — VIX Reversal & Trap Analysis (No Neutral)

**Dataset**: 1,488 days | 2020-08-06 to 2026-09-09 | No Neutral Classification
**Intraday data**: 30-min candles from 2021-09-13 to 2026-09-11 (1242 days)

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional

## How This Report Works

**Concept**: This report identifies days where the market makes a meaningful move in one direction (using VIX as the benchmark), then **reverses** to make a meaningful move in the opposite direction. These are "trap" or "reversal" patterns — the initial move lures traders in, then the reversal punishes them.

**Two VIX thresholds**:
- **0.3×VIX** = "moderate" move (30% of VIX-predicted daily range)
- **0.5×VIX** = "large" move (50% of VIX-predicted daily range, i.e. half the expected range)

**Four reversal patterns**:

| Pattern | First Move | Then Reverses To | Meaning | Days |
|---|---|---|---|---|
| **Bull Trap** | Up ≥ 0.3×VIX | Down ≥ 0.5×VIX | Morning rally lures buyers, then sells off hard | 181 (12.2%) |
| **Bear Trap** | Down ≥ 0.3×VIX | Up ≥ 0.5×VIX | Morning selloff lures sellers, then rallies hard | 225 (15.1%) |
| **Rally Fade** | Up ≥ 0.5×VIX | Down ≥ 0.3×VIX | Big rally fades, partial giveback | 86 (5.8%) |
| **Drop Bounce** | Down ≥ 0.5×VIX | Up ≥ 0.3×VIX | Big drop bounces, partial recovery | 138 (9.3%) |

**Total reversal days**: 466 (31.3%) — nearly 1 in 3 days has a meaningful reversal pattern.

**Key insight**: Bull Trap + Bear Trap (small move → big reversal) are the "trap" days where the initial move is deceptive. Rally Fade + Drop Bounce (big move → small reversal) are the "giveback" days where an initial strong move partially unwinds.

---

## Bull Trap — Up 0.3×VIX First → Down 0.5×VIX

**181 days** (12.2%) — Market rallies at least 0.3×VIX from open, then reverses and drops at least 0.5×VIX from open. The morning rally was a trap.

### Combinations by Bull Trap Rate

| FII View | PRO View | Pattern Days | Total Days | Pattern Rate | Green% | Avg Chg% | Avg Up% | Avg Down% |
|---|---|---|---|---|---|---|---|---|
| Strong Bearish | Strong Bullish | 2 | 5 | 40.0% | 0.0% | -0.675% | 0.555% | 0.785% |
| Strong Bearish | Bearish | 3 | 9 | 33.3% | 0.0% | -0.377% | 0.380% | 0.637% |
| Strong Bearish | Mildly Bearish | 3 | 10 | 30.0% | 0.0% | -0.920% | 0.283% | 1.157% |
| Bearish | Strong Bullish | 2 | 10 | 20.0% | 0.0% | -0.135% | 0.515% | 0.580% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 0.0% | -0.320% | 0.420% | 0.530% |
| **Strong Bearish** | **Strong Bearish** | 15 | 80 | **18.8%** | 0.0% | -0.386% | 0.382% | 0.737% |
| Bearish | Mildly Bullish | 2 | 11 | 18.2% | 0.0% | -1.030% | 0.510% | 1.145% |
| Strong Bullish | Strong Bearish | 1 | 6 | 16.7% | 0.0% | -0.360% | 0.250% | 0.410% |
| **Bullish** | **Strong Bullish** | 20 | 129 | **15.5%** | 0.0% | -0.457% | 0.367% | 0.688% |
| **Mildly Bearish** | **Strong Bullish** | 6 | 40 | **15.0%** | 0.0% | -0.552% | 0.423% | 0.993% |
| Bearish | Bullish | 1 | 7 | 14.3% | 0.0% | -1.120% | 0.260% | 1.320% |
| **Mildly Bullish** | **Bearish** | 6 | 43 | **14.0%** | 0.0% | -0.897% | 0.458% | 1.227% |
| **Mildly Bearish** | **Bearish** | 12 | 88 | **13.6%** | 0.0% | -0.353% | 0.408% | 0.605% |
| **Mildly Bearish** | **Mildly Bullish** | 9 | 69 | **13.0%** | 0.0% | -0.393% | 0.494% | 0.837% |
| **Bearish** | **Strong Bearish** | 13 | 102 | **12.7%** | 0.0% | -0.510% | 0.438% | 0.801% |
| **Mildly Bullish** | **Mildly Bullish** | 13 | 105 | **12.4%** | 0.0% | -0.568% | 0.452% | 0.812% |
| **Mildly Bullish** | **Mildly Bearish** | 9 | 78 | **11.5%** | 0.0% | -0.459% | 0.378% | 0.684% |
| Bullish | Bullish | 3 | 26 | 11.5% | 0.0% | -0.327% | 0.757% | 0.513% |
| **Strong Bullish** | **Strong Bullish** | 8 | 70 | **11.4%** | 0.0% | -0.304% | 0.406% | 0.518% |
| **Mildly Bearish** | **Strong Bearish** | 12 | 106 | **11.3%** | 0.0% | -0.610% | 0.411% | 0.931% |
| Strong Bullish | Mildly Bullish | 1 | 9 | 11.1% | 0.0% | -0.290% | 0.360% | 0.490% |
| **Mildly Bullish** | **Bullish** | 9 | 84 | **10.7%** | 0.0% | -0.593% | 0.397% | 0.997% |
| Mildly Bearish | Bullish | 3 | 28 | 10.7% | 0.0% | -0.303% | 0.293% | 0.620% |
| Mildly Bullish | Strong Bearish | 4 | 40 | 10.0% | 0.0% | -0.475% | 0.290% | 0.782% |
| Bearish | Bearish | 3 | 32 | 9.4% | 0.0% | -0.660% | 0.297% | 0.923% |
| Bearish | Mildly Bearish | 2 | 22 | 9.1% | 0.0% | -0.340% | 0.205% | 0.625% |
| **Mildly Bearish** | **Mildly Bearish** | 8 | 106 | **7.5%** | 0.0% | -0.536% | 0.472% | 0.886% |
| Bullish | Strong Bearish | 1 | 17 | 5.9% | 0.0% | -0.830% | 0.320% | 1.100% |
| Bullish | Mildly Bearish | 1 | 17 | 5.9% | 0.0% | -0.210% | 0.370% | 0.560% |
| Bullish | Mildly Bullish | 1 | 19 | 5.3% | 0.0% | -0.600% | 0.340% | 0.950% |
| **Mildly Bullish** | **Strong Bullish** | 5 | 98 | **5.1%** | 0.0% | -0.420% | 0.382% | 0.680% |

**Timing (155 days with intraday data)**:
- Initial move peaks in Morning 126 (81%), Afternoon 29 (19%)
- Reversal completes in Morning 23 (15%), Afternoon 132 (85%)
- Green day rate: 0/155 (0.0%)

**Overall Bull Trap outcome**: 0.0% close Green — most days close red as expected after a failed rally.

---

## Bear Trap — Down 0.3×VIX First → Up 0.5×VIX

**225 days** (15.1%) — Market drops at least 0.3×VIX from open, then reverses and rallies at least 0.5×VIX from open. The morning dip was a trap.

### Combinations by Bear Trap Rate

| FII View | PRO View | Pattern Days | Total Days | Pattern Rate | Green% | Avg Chg% | Avg Up% | Avg Down% |
|---|---|---|---|---|---|---|---|---|
| Strong Bullish | Strong Bearish | 2 | 6 | 33.3% | 100.0% | +0.315% | 0.710% | 0.360% |
| Bearish | Bullish | 2 | 7 | 28.6% | 100.0% | +0.865% | 1.010% | 0.920% |
| Bearish | Mildly Bullish | 3 | 11 | 27.3% | 100.0% | +0.527% | 0.637% | 0.350% |
| Bullish | Strong Bearish | 4 | 17 | 23.5% | 100.0% | +0.725% | 0.870% | 0.480% |
| Strong Bullish | Mildly Bullish | 2 | 9 | 22.2% | 100.0% | +1.160% | 1.270% | 0.565% |
| Strong Bearish | Bearish | 2 | 9 | 22.2% | 100.0% | +0.425% | 0.555% | 0.530% |
| **Mildly Bearish** | **Strong Bearish** | 22 | 106 | **20.8%** | 100.0% | +0.758% | 0.940% | 0.474% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 100.0% | +0.240% | 0.560% | 0.430% |
| **Bearish** | **Strong Bearish** | 20 | 102 | **19.6%** | 100.0% | +0.552% | 0.739% | 0.480% |
| **Strong Bearish** | **Strong Bearish** | 15 | 80 | **18.8%** | 100.0% | +0.560% | 0.821% | 0.455% |
| **Mildly Bullish** | **Bearish** | 8 | 43 | **18.6%** | 100.0% | +0.610% | 0.782% | 0.369% |
| **Mildly Bearish** | **Bullish** | 5 | 28 | **17.9%** | 100.0% | +0.664% | 0.956% | 0.380% |
| Bullish | Mildly Bearish | 3 | 17 | 17.6% | 100.0% | +0.193% | 0.770% | 0.457% |
| **Mildly Bullish** | **Strong Bearish** | 7 | 40 | **17.5%** | 100.0% | +0.606% | 0.750% | 0.389% |
| **Strong Bullish** | **Strong Bullish** | 12 | 70 | **17.1%** | 100.0% | +0.415% | 0.565% | 0.375% |
| **Mildly Bearish** | **Mildly Bullish** | 11 | 69 | **15.9%** | 100.0% | +0.775% | 0.995% | 0.569% |
| Bullish | Mildly Bullish | 3 | 19 | 15.8% | 100.0% | +0.440% | 0.633% | 0.403% |
| Bullish | Bullish | 4 | 26 | 15.4% | 100.0% | +0.710% | 0.765% | 0.290% |
| **Mildly Bearish** | **Strong Bullish** | 6 | 40 | **15.0%** | 100.0% | +0.348% | 0.668% | 0.350% |
| **Mildly Bearish** | **Bearish** | 13 | 88 | **14.8%** | 100.0% | +0.480% | 0.888% | 0.528% |
| **Mildly Bullish** | **Strong Bullish** | 14 | 98 | **14.3%** | 100.0% | +0.616% | 0.916% | 0.524% |
| Bearish | Mildly Bearish | 3 | 22 | 13.6% | 100.0% | +0.627% | 0.740% | 0.443% |
| **Mildly Bullish** | **Mildly Bullish** | 14 | 105 | **13.3%** | 100.0% | +0.525% | 0.751% | 0.439% |
| Bearish | Bearish | 4 | 32 | 12.5% | 100.0% | +0.385% | 0.755% | 0.402% |
| **Mildly Bullish** | **Bullish** | 10 | 84 | **11.9%** | 100.0% | +0.566% | 0.758% | 0.394% |
| **Mildly Bearish** | **Mildly Bearish** | 12 | 106 | **11.3%** | 100.0% | +0.336% | 0.715% | 0.557% |
| Bearish | Strong Bullish | 1 | 10 | 10.0% | 100.0% | +0.210% | 0.530% | 0.720% |
| **Mildly Bullish** | **Mildly Bearish** | 7 | 78 | **9.0%** | 100.0% | +0.574% | 0.786% | 0.500% |
| **Bullish** | **Strong Bullish** | 10 | 129 | **7.8%** | 100.0% | +0.421% | 0.642% | 0.338% |

**Timing (183 days with intraday data)**:
- Initial move peaks in Morning 160 (87%), Afternoon 23 (13%)
- Reversal completes in Morning 26 (14%), Afternoon 157 (86%)
- Green day rate: 183/183 (100.0%)

**Overall Bear Trap outcome**: 100.0% close Green — the reversal rally holds and most days close green.

---

## Rally Fade — Up 0.5×VIX First → Down 0.3×VIX

**86 days** (5.8%) — Market rallies strongly (≥0.5×VIX from open), then gives back at least 0.3×VIX on the downside. A partial unwind of morning strength.

### Combinations by Rally Fade Rate

| FII View | PRO View | Pattern Days | Total Days | Pattern Rate | Green% | Avg Chg% | Avg Up% | Avg Down% |
|---|---|---|---|---|---|---|---|---|
| Bearish | Strong Bullish | 2 | 10 | 20.0% | 0.0% | -0.135% | 0.515% | 0.580% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 0.0% | -0.320% | 0.420% | 0.530% |
| Strong Bearish | Strong Bullish | 1 | 5 | 20.0% | 0.0% | -0.730% | 0.730% | 0.870% |
| Strong Bullish | Strong Bearish | 1 | 6 | 16.7% | 0.0% | -0.090% | 0.450% | 0.330% |
| **Mildly Bearish** | **Bearish** | 10 | 88 | **11.4%** | 0.0% | -0.329% | 0.519% | 0.548% |
| Strong Bearish | Bearish | 1 | 9 | 11.1% | 0.0% | -0.440% | 0.430% | 0.550% |
| **Strong Bearish** | **Strong Bearish** | 8 | 80 | **10.0%** | 0.0% | -0.329% | 0.537% | 0.713% |
| **Bearish** | **Strong Bearish** | 10 | 102 | **9.8%** | 0.0% | -0.387% | 0.515% | 0.658% |
| Bearish | Mildly Bullish | 1 | 11 | 9.1% | 0.0% | -1.310% | 0.660% | 1.480% |
| Bullish | Bullish | 2 | 26 | 7.7% | 0.0% | -0.265% | 1.000% | 0.535% |
| **Mildly Bearish** | **Strong Bearish** | 7 | 106 | **6.6%** | 0.0% | -0.776% | 0.549% | 1.121% |
| **Mildly Bullish** | **Mildly Bearish** | 5 | 78 | **6.4%** | 0.0% | -0.142% | 0.532% | 0.452% |
| Bearish | Bearish | 2 | 32 | 6.2% | 0.0% | -0.170% | 0.475% | 0.365% |
| **Bullish** | **Strong Bullish** | 8 | 129 | **6.2%** | 0.0% | -0.239% | 0.541% | 0.396% |
| Bullish | Strong Bearish | 1 | 17 | 5.9% | 0.0% | -0.830% | 0.320% | 1.100% |
| Mildly Bearish | Mildly Bullish | 4 | 69 | 5.8% | 0.0% | -0.318% | 0.717% | 0.575% |
| Mildly Bearish | Strong Bullish | 2 | 40 | 5.0% | 0.0% | -0.730% | 0.480% | 1.015% |
| **Mildly Bullish** | **Mildly Bullish** | 5 | 105 | **4.8%** | 0.0% | -0.518% | 0.704% | 0.772% |
| Mildly Bullish | Bearish | 2 | 43 | 4.7% | 0.0% | -0.275% | 0.695% | 0.400% |
| Bearish | Mildly Bearish | 1 | 22 | 4.5% | 0.0% | -0.130% | 0.550% | 0.330% |
| Strong Bullish | Strong Bullish | 3 | 70 | 4.3% | 0.0% | -0.473% | 0.640% | 0.570% |
| Mildly Bearish | Mildly Bearish | 3 | 106 | 2.8% | 0.0% | -0.843% | 0.617% | 1.200% |
| Mildly Bullish | Bullish | 2 | 84 | 2.4% | 0.0% | -0.650% | 0.665% | 1.410% |
| Mildly Bullish | Strong Bullish | 2 | 98 | 2.0% | 0.0% | -0.430% | 0.430% | 0.675% |

**Timing (75 days with intraday data)**:
- Initial move peaks in Morning 55 (73%), Afternoon 20 (27%)
- Reversal completes in Morning 12 (16%), Afternoon 63 (84%)
- Green day rate: 0/75 (0.0%)

**Overall Rally Fade outcome**: 0.0% close Green — the fade dominates and most days close red.

---

## Drop Bounce — Down 0.5×VIX First → Up 0.3×VIX

**138 days** (9.3%) — Market drops sharply (≥0.5×VIX from open), then bounces back at least 0.3×VIX on the upside. A partial recovery from morning weakness.

### Combinations by Drop Bounce Rate

| FII View | PRO View | Pattern Days | Total Days | Pattern Rate | Green% | Avg Chg% | Avg Up% | Avg Down% |
|---|---|---|---|---|---|---|---|---|
| Bearish | Bullish | 2 | 7 | 28.6% | 100.0% | +0.865% | 1.010% | 0.920% |
| Strong Bullish | Mildly Bullish | 2 | 9 | 22.2% | 100.0% | +1.160% | 1.270% | 0.565% |
| Strong Bearish | Bearish | 2 | 9 | 22.2% | 100.0% | +0.425% | 0.555% | 0.530% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 100.0% | +0.240% | 0.560% | 0.430% |
| Bearish | Mildly Bullish | 2 | 11 | 18.2% | 100.0% | +0.535% | 0.625% | 0.400% |
| Bullish | Mildly Bullish | 3 | 19 | 15.8% | 100.0% | +0.440% | 0.633% | 0.403% |
| **Strong Bullish** | **Strong Bullish** | 11 | 70 | **15.7%** | 100.0% | +0.338% | 0.475% | 0.565% |
| **Mildly Bearish** | **Mildly Bullish** | 9 | 69 | **13.0%** | 100.0% | +0.707% | 0.907% | 0.612% |
| **Bearish** | **Strong Bearish** | 13 | 102 | **12.7%** | 100.0% | +0.442% | 0.579% | 0.565% |
| Bearish | Bearish | 4 | 32 | 12.5% | 100.0% | +0.338% | 0.530% | 0.583% |
| **Mildly Bullish** | **Strong Bearish** | 5 | 40 | **12.5%** | 100.0% | +0.412% | 0.558% | 0.458% |
| **Mildly Bearish** | **Strong Bearish** | 13 | 106 | **12.3%** | 100.0% | +0.728% | 0.917% | 0.663% |
| Bullish | Mildly Bearish | 2 | 17 | 11.8% | 100.0% | +0.285% | 0.585% | 0.535% |
| **Mildly Bullish** | **Mildly Bullish** | 11 | 105 | **10.5%** | 100.0% | +0.333% | 0.524% | 0.742% |
| Bearish | Strong Bullish | 1 | 10 | 10.0% | 100.0% | +0.210% | 0.530% | 0.720% |
| Strong Bearish | Mildly Bearish | 1 | 10 | 10.0% | 100.0% | +0.240% | 0.240% | 0.300% |
| Bearish | Mildly Bearish | 2 | 22 | 9.1% | 100.0% | +0.520% | 0.570% | 0.480% |
| **Mildly Bullish** | **Strong Bullish** | 8 | 98 | **8.2%** | 100.0% | +0.766% | 0.995% | 0.701% |
| **Mildly Bearish** | **Bearish** | 7 | 88 | **8.0%** | 100.0% | +0.260% | 0.741% | 0.746% |
| Mildly Bearish | Bullish | 2 | 28 | 7.1% | 100.0% | +0.300% | 0.435% | 0.645% |
| Mildly Bullish | Bearish | 3 | 43 | 7.0% | 100.0% | +0.410% | 0.577% | 0.657% |
| **Mildly Bearish** | **Mildly Bearish** | 7 | 106 | **6.6%** | 100.0% | +0.303% | 0.623% | 0.821% |
| **Mildly Bullish** | **Mildly Bearish** | 5 | 78 | **6.4%** | 100.0% | +0.396% | 0.620% | 0.734% |
| **Strong Bearish** | **Strong Bearish** | 5 | 80 | **6.2%** | 100.0% | +0.724% | 1.114% | 0.824% |
| **Bullish** | **Strong Bullish** | 8 | 129 | **6.2%** | 100.0% | +0.356% | 0.519% | 0.644% |
| Bullish | Strong Bearish | 1 | 17 | 5.9% | 100.0% | +0.610% | 0.770% | 0.930% |
| Mildly Bullish | Bullish | 4 | 84 | 4.8% | 100.0% | +0.580% | 0.722% | 0.547% |
| Bullish | Bullish | 1 | 26 | 3.8% | 100.0% | +0.090% | 0.460% | 0.630% |
| Mildly Bearish | Strong Bullish | 1 | 40 | 2.5% | 100.0% | +0.620% | 0.840% | 0.780% |

**Timing (116 days with intraday data)**:
- Initial move peaks in Morning 99 (85%), Afternoon 17 (15%)
- Reversal completes in Morning 13 (11%), Afternoon 103 (89%)
- Green day rate: 116/116 (100.0%)

**Overall Drop Bounce outcome**: 100.0% close Green — the bounce often carries through to a green close.

---

## Section 1: FII STRONG BULLISH — Reversal Profile (97 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 12 | 12.4% | 0.0% |
| Bear Trap | 17 | 17.5% | 100.0% |
| Rally Fade | 6 | 6.2% | 0.0% |
| Drop Bounce | 14 | 14.4% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 70 | 11.4% | 17.1% | 4.3% | 15.7% | **37.1%** |
| Bullish | 5 | 20.0% | 20.0% | 20.0% | 20.0% | **40.0%** |
| Mildly Bullish | 9 | 11.1% | 22.2% | 0.0% | 22.2% | **33.3%** |
| Strong Bearish | 6 | 16.7% | 33.3% | 16.7% | 0.0% | **66.7%** |

**Dominant reversal**: Bear Trap (17 days, 17.5%). Total reversals: 36/97 (37.1%).

## Section 2: FII BULLISH — Reversal Profile (211 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 26 | 12.3% | 0.0% |
| Bear Trap | 26 | 12.3% | 100.0% |
| Rally Fade | 11 | 5.2% | 0.0% |
| Drop Bounce | 16 | 7.6% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 129 | 15.5% | 7.8% | 6.2% | 6.2% | **28.7%** |
| Bullish | 26 | 11.5% | 15.4% | 7.7% | 3.8% | **30.8%** |
| Mildly Bullish | 19 | 5.3% | 15.8% | 0.0% | 15.8% | **21.1%** |
| Mildly Bearish | 17 | 5.9% | 17.6% | 0.0% | 11.8% | **23.5%** |
| Strong Bearish | 17 | 5.9% | 23.5% | 5.9% | 5.9% | **29.4%** |

**Dominant reversal**: Bull Trap (26 days, 12.3%). Total reversals: 60/211 (28.4%).

## Section 3: FII MILDLY BULLISH — Reversal Profile (448 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 46 | 10.3% | 0.0% |
| Bear Trap | 60 | 13.4% | 100.0% |
| Rally Fade | 16 | 3.6% | 0.0% |
| Drop Bounce | 36 | 8.0% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 98 | 5.1% | 14.3% | 2.0% | 8.2% | **21.4%** |
| Bullish | 84 | 10.7% | 11.9% | 2.4% | 4.8% | **26.2%** |
| Mildly Bullish | 105 | 12.4% | 13.3% | 4.8% | 10.5% | **31.4%** |
| Mildly Bearish | 78 | 11.5% | 9.0% | 6.4% | 6.4% | **26.9%** |
| Bearish | 43 | 14.0% | 18.6% | 4.7% | 7.0% | **34.9%** |
| Strong Bearish | 40 | 10.0% | 17.5% | 0.0% | 12.5% | **30.0%** |

**Dominant reversal**: Bear Trap (60 days, 13.4%). Total reversals: 124/448 (27.7%).

## Section 4: FII MILDLY BEARISH — Reversal Profile (437 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 50 | 11.4% | 0.0% |
| Bear Trap | 69 | 15.8% | 100.0% |
| Rally Fade | 26 | 5.9% | 0.0% |
| Drop Bounce | 39 | 8.9% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 40 | 15.0% | 15.0% | 5.0% | 2.5% | **32.5%** |
| Bullish | 28 | 10.7% | 17.9% | 0.0% | 7.1% | **32.1%** |
| Mildly Bullish | 69 | 13.0% | 15.9% | 5.8% | 13.0% | **31.9%** |
| Mildly Bearish | 106 | 7.5% | 11.3% | 2.8% | 6.6% | **19.8%** |
| Bearish | 88 | 13.6% | 14.8% | 11.4% | 8.0% | **33.0%** |
| Strong Bearish | 106 | 11.3% | 20.8% | 6.6% | 12.3% | **35.8%** |

**Dominant reversal**: Bear Trap (69 days, 15.8%). Total reversals: 132/437 (30.2%).

## Section 5: FII BEARISH — Reversal Profile (184 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 23 | 12.5% | 0.0% |
| Bear Trap | 33 | 17.9% | 100.0% |
| Rally Fade | 16 | 8.7% | 0.0% |
| Drop Bounce | 24 | 13.0% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 10 | 20.0% | 10.0% | 20.0% | 10.0% | **30.0%** |
| Bullish | 7 | 14.3% | 28.6% | 0.0% | 28.6% | **42.9%** |
| Mildly Bullish | 11 | 18.2% | 27.3% | 9.1% | 18.2% | **45.5%** |
| Mildly Bearish | 22 | 9.1% | 13.6% | 4.5% | 9.1% | **27.3%** |
| Bearish | 32 | 9.4% | 12.5% | 6.2% | 12.5% | **34.4%** |
| Strong Bearish | 102 | 12.7% | 19.6% | 9.8% | 12.7% | **38.2%** |

**Dominant reversal**: Bear Trap (33 days, 17.9%). Total reversals: 67/184 (36.4%).

## Section 6: FII STRONG BEARISH — Reversal Profile (111 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 24 | 21.6% | 0.0% |
| Bear Trap | 20 | 18.0% | 100.0% |
| Rally Fade | 11 | 9.9% | 0.0% |
| Drop Bounce | 9 | 8.1% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 5 | 40.0% | 0.0% | 20.0% | 0.0% | **40.0%** |
| Mildly Bearish | 10 | 30.0% | 0.0% | 0.0% | 10.0% | **40.0%** |
| Bearish | 9 | 33.3% | 22.2% | 11.1% | 22.2% | **55.6%** |
| Strong Bearish | 80 | 18.8% | 18.8% | 10.0% | 6.2% | **40.0%** |

**Dominant reversal**: Bull Trap (24 days, 21.6%). Total reversals: 47/111 (42.3%).


---

## Conclusion

### Pattern Summary

| Pattern | Days | % of All | Green% | Meaning |
|---|---|---|---|---|
| Bull Trap | 181 | 12.2% | 0.0% | Morning rally → selloff |
| Bear Trap | 225 | 15.1% | 100.0% | Morning dip → rally |
| Rally Fade | 86 | 5.8% | 0.0% | Big rally → partial giveback |
| Drop Bounce | 138 | 9.3% | 100.0% | Big drop → partial bounce |

### Key Findings:

1. **Bear Traps outnumber Bull Traps** (225 vs 181): The market is more likely to dip first then rally hard (Down 0.3→Up 0.5) than to rally first then sell off. This aligns with the "Down to Up" dominance seen in the main analysis.
2. **Bear Trap days close Green 100% of the time** vs Bull Trap at 0%. When the morning dip is a trap, the reversal rally usually holds through close.
3. **Highest Bull Trap rate**: Strong Bearish FII + Strong Bullish PRO — **40.0%** of days are Bull Traps (2/5 days). This combo is most likely to trap morning buyers.
4. **Highest Bear Trap rate**: Strong Bullish FII + Strong Bearish PRO — **33.3%** of days are Bear Traps (2/6 days). This combo is most likely to trap morning sellers.
5. **FII view reversal rates**: Highest = Strong Bearish (42.3%, 111d), Lowest = Mildly Bullish (27.7%, 448d).

### Actionable Rules:

- **Buy morning dips** (high Bear Trap rate): Bearish+Mildly Bullish (27%), Bullish+Strong Bearish (24%), Mildly Bearish+Strong Bearish (21%)
- **Sell/short morning rallies** (high Bull Trap rate): Strong Bearish+Mildly Bearish (30%), Bearish+Strong Bullish (20%), Strong Bearish+Strong Bearish (19%)
- **Trend-follow (low reversal rate)**: Mildly Bearish+Mildly Bearish (20%), Bullish+Mildly Bullish (21%), Mildly Bullish+Strong Bullish (21%)
- **Expiry caution**: Reversal patterns may be amplified on expiry days due to options unwinding
