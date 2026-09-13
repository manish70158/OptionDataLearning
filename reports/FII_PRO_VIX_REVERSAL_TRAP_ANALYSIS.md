# FII VIEW x PRO VIEW — VIX Reversal & Trap Analysis

**Dataset**: 1,488 days | 2020-08-06 to 2026-09-09 | ±20K Neutral Classification
**Intraday data**: 30-min candles from 2021-09-13 to 2026-09-11 (1242 days)

### Label Guide
- **Neutral20** = composite between ±20K (i.e. -20K to +20K)
- **MildBull20** = Mildly Bullish = composite +20K to +50K
- **MildBear20** = Mildly Bearish = composite -20K to -50K
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)

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

**Key insight**: Bull Trap + Bear Trap (small move → big reversal) capture 406 days — these are the "trap" days where the initial move is deceptive. Rally Fade + Drop Bounce (big move → small reversal) capture 224 days — these are the "giveback" days where an initial strong move partially unwinds.

---

## Bull Trap — Up 0.3×VIX First → Down 0.5×VIX

**181 days** (12.2%) — Market rallies at least 0.3×VIX from open, then reverses and drops at least 0.5×VIX from open. The morning rally was a trap.

### Combinations by Bull Trap Rate

| FII View | PRO View | Pattern Days | Total Days | Pattern Rate | Green% | Avg Chg% | Avg Up% | Avg Down% |
|---|---|---|---|---|---|---|---|---|
| Strong Bearish | Neutral20 | 3 | 6 | 50.0% | 0.0% | -0.613% | 0.327% | 0.777% |
| Strong Bearish | Strong Bullish | 2 | 5 | 40.0% | 0.0% | -0.675% | 0.555% | 0.785% |
| Strong Bearish | Bearish | 3 | 9 | 33.3% | 0.0% | -0.377% | 0.380% | 0.637% |
| MildBull20 | Strong Bearish | 4 | 18 | 22.2% | 0.0% | -0.475% | 0.290% | 0.782% |
| Bearish | Strong Bullish | 2 | 10 | 20.0% | 0.0% | -0.135% | 0.515% | 0.580% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 0.0% | -0.320% | 0.420% | 0.530% |
| **MildBear20** | **Bearish** | 9 | 48 | **18.8%** | 0.0% | -0.363% | 0.403% | 0.612% |
| **Strong Bearish** | **Strong Bearish** | 15 | 80 | **18.8%** | 0.0% | -0.386% | 0.382% | 0.737% |
| MildBull20 | Bearish | 4 | 22 | 18.2% | 0.0% | -0.688% | 0.495% | 0.905% |
| Strong Bullish | Strong Bearish | 1 | 6 | 16.7% | 0.0% | -0.360% | 0.250% | 0.410% |
| **Bullish** | **Strong Bullish** | 20 | 129 | **15.5%** | 0.0% | -0.457% | 0.367% | 0.688% |
| **Neutral20** | **Neutral20** | 16 | 108 | **14.8%** | 0.0% | -0.443% | 0.485% | 0.767% |
| Strong Bearish | MildBear20 | 1 | 7 | 14.3% | 0.0% | -1.060% | 0.230% | 1.550% |
| Bearish | MildBear20 | 2 | 14 | 14.3% | 0.0% | -0.340% | 0.205% | 0.625% |
| Bearish | Bullish | 1 | 7 | 14.3% | 0.0% | -1.120% | 0.260% | 1.320% |
| **Neutral20** | **MildBear20** | 8 | 59 | **13.6%** | 0.0% | -0.465% | 0.370% | 0.780% |
| MildBear20 | Strong Bullish | 2 | 15 | 13.3% | 0.0% | -0.905% | 0.330% | 1.145% |
| **Neutral20** | **MildBull20** | 7 | 54 | **13.0%** | 0.0% | -0.641% | 0.490% | 0.951% |
| **Bearish** | **Strong Bearish** | 13 | 102 | **12.7%** | 0.0% | -0.510% | 0.438% | 0.801% |
| **MildBull20** | **Bullish** | 6 | 51 | **11.8%** | 0.0% | -0.582% | 0.415% | 1.055% |
| Bullish | Bullish | 3 | 26 | 11.5% | 0.0% | -0.327% | 0.757% | 0.513% |
| **Strong Bullish** | **Strong Bullish** | 8 | 70 | **11.4%** | 0.0% | -0.304% | 0.406% | 0.518% |
| **MildBear20** | **Strong Bearish** | 8 | 76 | **10.5%** | 0.0% | -0.812% | 0.465% | 1.163% |
| **Neutral20** | **Bullish** | 5 | 49 | **10.2%** | 0.0% | -0.422% | 0.302% | 0.686% |
| MildBear20 | MildBear20 | 3 | 30 | 10.0% | 0.0% | -0.387% | 0.333% | 0.697% |
| **Neutral20** | **Strong Bullish** | 6 | 63 | **9.5%** | 0.0% | -0.443% | 0.468% | 0.890% |
| Bearish | Bearish | 3 | 32 | 9.4% | 0.0% | -0.660% | 0.297% | 0.923% |
| Bullish | MildBull20 | 1 | 11 | 9.1% | 0.0% | -0.600% | 0.340% | 0.950% |
| MildBear20 | Bullish | 1 | 12 | 8.3% | 0.0% | -0.650% | 0.450% | 1.070% |
| Bullish | MildBear20 | 1 | 12 | 8.3% | 0.0% | -0.210% | 0.370% | 0.560% |
| **Neutral20** | **Bearish** | 5 | 61 | **8.2%** | 0.0% | -0.718% | 0.408% | 1.098% |
| Neutral20 | Strong Bearish | 4 | 52 | 7.7% | 0.0% | -0.205% | 0.302% | 0.468% |
| MildBear20 | Neutral20 | 2 | 29 | 6.9% | 0.0% | -0.385% | 0.600% | 0.660% |
| Bearish | Neutral20 | 1 | 15 | 6.7% | 0.0% | -0.750% | 0.360% | 0.810% |
| MildBull20 | Neutral20 | 2 | 32 | 6.2% | 0.0% | -0.770% | 0.325% | 0.955% |
| Bullish | Strong Bearish | 1 | 17 | 5.9% | 0.0% | -0.830% | 0.320% | 1.100% |
| MildBull20 | Strong Bullish | 3 | 60 | 5.0% | 0.0% | -0.313% | 0.327% | 0.577% |
| MildBull20 | MildBull20 | 1 | 26 | 3.8% | 0.0% | -0.580% | 0.500% | 0.830% |

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
| MildBear20 | Strong Bullish | 4 | 15 | 26.7% | 100.0% | +0.370% | 0.720% | 0.388% |
| Bullish | Strong Bearish | 4 | 17 | 23.5% | 100.0% | +0.725% | 0.870% | 0.480% |
| Strong Bearish | Bearish | 2 | 9 | 22.2% | 100.0% | +0.425% | 0.555% | 0.530% |
| **MildBear20** | **Strong Bearish** | 16 | 76 | **21.1%** | 100.0% | +0.650% | 0.847% | 0.493% |
| Bearish | Neutral20 | 3 | 15 | 20.0% | 100.0% | +0.427% | 0.533% | 0.353% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 100.0% | +0.240% | 0.560% | 0.430% |
| **Bearish** | **Strong Bearish** | 20 | 102 | **19.6%** | 100.0% | +0.552% | 0.739% | 0.480% |
| **Neutral20** | **Strong Bearish** | 10 | 52 | **19.2%** | 100.0% | +0.850% | 0.978% | 0.429% |
| **Strong Bearish** | **Strong Bearish** | 15 | 80 | **18.8%** | 100.0% | +0.560% | 0.821% | 0.455% |
| Bullish | MildBull20 | 2 | 11 | 18.2% | 100.0% | +0.430% | 0.580% | 0.345% |
| **Neutral20** | **Bearish** | 11 | 61 | **18.0%** | 100.0% | +0.505% | 0.820% | 0.458% |
| **MildBull20** | **Bullish** | 9 | 51 | **17.6%** | 100.0% | +0.563% | 0.763% | 0.392% |
| **Strong Bullish** | **Strong Bullish** | 12 | 70 | **17.1%** | 100.0% | +0.415% | 0.565% | 0.375% |
| **MildBear20** | **Bearish** | 8 | 48 | **16.7%** | 100.0% | +0.550% | 0.896% | 0.515% |
| Strong Bearish | Neutral20 | 1 | 6 | 16.7% | 100.0% | +0.640% | 0.710% | 0.250% |
| Bullish | MildBear20 | 2 | 12 | 16.7% | 100.0% | +0.145% | 0.920% | 0.460% |
| MildBull20 | Strong Bearish | 3 | 18 | 16.7% | 100.0% | +0.670% | 0.863% | 0.320% |
| **MildBull20** | **Neutral20** | 5 | 32 | **15.6%** | 100.0% | +0.330% | 0.776% | 0.374% |
| Bullish | Bullish | 4 | 26 | 15.4% | 100.0% | +0.710% | 0.765% | 0.290% |
| Bullish | Neutral20 | 2 | 13 | 15.4% | 100.0% | +0.375% | 0.605% | 0.485% |
| **Neutral20** | **MildBear20** | 9 | 59 | **15.3%** | 100.0% | +0.373% | 0.744% | 0.457% |
| **Neutral20** | **MildBull20** | 8 | 54 | **14.8%** | 100.0% | +0.741% | 0.956% | 0.478% |
| Bearish | MildBear20 | 2 | 14 | 14.3% | 100.0% | +0.750% | 0.885% | 0.430% |
| Strong Bullish | MildBull20 | 1 | 7 | 14.3% | 100.0% | +1.870% | 2.020% | 0.760% |
| **MildBull20** | **Strong Bullish** | 8 | 60 | **13.3%** | 100.0% | +0.516% | 0.845% | 0.505% |
| **Neutral20** | **Strong Bullish** | 8 | 63 | **12.7%** | 100.0% | +0.637% | 0.900% | 0.480% |
| MildBear20 | MildBull20 | 1 | 8 | 12.5% | 100.0% | +0.270% | 0.340% | 0.560% |
| Bearish | Bearish | 4 | 32 | 12.5% | 100.0% | +0.385% | 0.755% | 0.402% |
| **Neutral20** | **Neutral20** | 12 | 108 | **11.1%** | 100.0% | +0.631% | 0.823% | 0.626% |
| MildBear20 | Neutral20 | 3 | 29 | 10.3% | 100.0% | +0.553% | 0.693% | 0.600% |
| **Neutral20** | **Bullish** | 5 | 49 | **10.2%** | 100.0% | +0.700% | 1.000% | 0.370% |
| Bearish | Strong Bullish | 1 | 10 | 10.0% | 100.0% | +0.210% | 0.530% | 0.720% |
| MildBear20 | MildBear20 | 3 | 30 | 10.0% | 100.0% | +0.287% | 0.500% | 0.307% |
| MildBull20 | Bearish | 2 | 22 | 9.1% | 100.0% | +0.585% | 0.805% | 0.330% |
| MildBull20 | MildBear20 | 1 | 12 | 8.3% | 100.0% | +0.660% | 1.300% | 0.990% |
| MildBear20 | Bullish | 1 | 12 | 8.3% | 100.0% | +0.410% | 0.490% | 0.460% |
| **Bullish** | **Strong Bullish** | 10 | 129 | **7.8%** | 100.0% | +0.421% | 0.642% | 0.338% |
| MildBull20 | MildBull20 | 2 | 26 | 7.7% | 100.0% | +0.980% | 1.110% | 0.510% |

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
| Strong Bearish | Strong Bullish | 1 | 5 | 20.0% | 0.0% | -0.730% | 0.730% | 0.870% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 0.0% | -0.320% | 0.420% | 0.530% |
| Strong Bearish | Neutral20 | 1 | 6 | 16.7% | 0.0% | -0.140% | 0.360% | 0.410% |
| Strong Bullish | Strong Bearish | 1 | 6 | 16.7% | 0.0% | -0.090% | 0.450% | 0.330% |
| **MildBear20** | **Bearish** | 7 | 48 | **14.6%** | 0.0% | -0.329% | 0.500% | 0.579% |
| Strong Bearish | Bearish | 1 | 9 | 11.1% | 0.0% | -0.440% | 0.430% | 0.550% |
| **Neutral20** | **Neutral20** | 11 | 108 | **10.2%** | 0.0% | -0.353% | 0.628% | 0.669% |
| **Strong Bearish** | **Strong Bearish** | 8 | 80 | **10.0%** | 0.0% | -0.329% | 0.537% | 0.713% |
| **Bearish** | **Strong Bearish** | 10 | 102 | **9.8%** | 0.0% | -0.387% | 0.515% | 0.658% |
| MildBull20 | Bearish | 2 | 22 | 9.1% | 0.0% | -0.275% | 0.695% | 0.400% |
| **MildBear20** | **Strong Bearish** | 6 | 76 | **7.9%** | 0.0% | -0.878% | 0.558% | 1.235% |
| Bullish | Bullish | 2 | 26 | 7.7% | 0.0% | -0.265% | 1.000% | 0.535% |
| MildBear20 | Strong Bullish | 1 | 15 | 6.7% | 0.0% | -1.370% | 0.440% | 1.770% |
| Bearish | Neutral20 | 1 | 15 | 6.7% | 0.0% | -0.130% | 0.550% | 0.330% |
| Bearish | Bearish | 2 | 32 | 6.2% | 0.0% | -0.170% | 0.475% | 0.365% |
| **Bullish** | **Strong Bullish** | 8 | 129 | **6.2%** | 0.0% | -0.239% | 0.541% | 0.396% |
| Bullish | Strong Bearish | 1 | 17 | 5.9% | 0.0% | -0.830% | 0.320% | 1.100% |
| Neutral20 | Bearish | 3 | 61 | 4.9% | 0.0% | -0.330% | 0.563% | 0.477% |
| Strong Bullish | Strong Bullish | 3 | 70 | 4.3% | 0.0% | -0.473% | 0.640% | 0.570% |
| MildBull20 | Bullish | 2 | 51 | 3.9% | 0.0% | -0.650% | 0.665% | 1.410% |
| MildBull20 | MildBull20 | 1 | 26 | 3.8% | 0.0% | -0.580% | 0.500% | 0.830% |
| Neutral20 | MildBull20 | 2 | 54 | 3.7% | 0.0% | -0.650% | 0.845% | 0.750% |
| MildBear20 | Neutral20 | 1 | 29 | 3.4% | 0.0% | -0.690% | 0.960% | 0.880% |
| Neutral20 | MildBear20 | 2 | 59 | 3.4% | 0.0% | -0.325% | 0.420% | 0.725% |
| Neutral20 | Strong Bullish | 2 | 63 | 3.2% | 0.0% | -0.420% | 0.515% | 0.695% |
| Neutral20 | Strong Bearish | 1 | 52 | 1.9% | 0.0% | -0.160% | 0.490% | 0.440% |
| MildBull20 | Strong Bullish | 1 | 60 | 1.7% | 0.0% | -0.110% | 0.350% | 0.220% |

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
| Strong Bearish | Bearish | 2 | 9 | 22.2% | 100.0% | +0.425% | 0.555% | 0.530% |
| Strong Bullish | Bullish | 1 | 5 | 20.0% | 100.0% | +0.240% | 0.560% | 0.430% |
| Bullish | MildBull20 | 2 | 11 | 18.2% | 100.0% | +0.430% | 0.580% | 0.345% |
| **MildBear20** | **Strong Bearish** | 12 | 76 | **15.8%** | 100.0% | +0.745% | 0.934% | 0.666% |
| **Strong Bullish** | **Strong Bullish** | 11 | 70 | **15.7%** | 100.0% | +0.338% | 0.475% | 0.565% |
| Bullish | Neutral20 | 2 | 13 | 15.4% | 100.0% | +0.375% | 0.605% | 0.485% |
| Strong Bullish | MildBull20 | 1 | 7 | 14.3% | 100.0% | +1.870% | 2.020% | 0.760% |
| Strong Bearish | MildBear20 | 1 | 7 | 14.3% | 100.0% | +0.240% | 0.240% | 0.300% |
| **Neutral20** | **Neutral20** | 15 | 108 | **13.9%** | 100.0% | +0.445% | 0.568% | 0.671% |
| Bearish | Neutral20 | 2 | 15 | 13.3% | 100.0% | +0.385% | 0.470% | 0.405% |
| **Neutral20** | **Bearish** | 8 | 61 | **13.1%** | 100.0% | +0.364% | 0.734% | 0.651% |
| **Bearish** | **Strong Bearish** | 13 | 102 | **12.7%** | 100.0% | +0.442% | 0.579% | 0.565% |
| MildBear20 | MildBull20 | 1 | 8 | 12.5% | 100.0% | +0.270% | 0.340% | 0.560% |
| Bearish | Bearish | 4 | 32 | 12.5% | 100.0% | +0.338% | 0.530% | 0.583% |
| Bearish | Strong Bullish | 1 | 10 | 10.0% | 100.0% | +0.210% | 0.530% | 0.720% |
| **Neutral20** | **Strong Bearish** | 5 | 52 | **9.6%** | 100.0% | +0.406% | 0.546% | 0.512% |
| **Neutral20** | **MildBull20** | 5 | 54 | **9.3%** | 100.0% | +0.644% | 0.948% | 0.614% |
| MildBear20 | Bullish | 1 | 12 | 8.3% | 100.0% | +0.410% | 0.490% | 0.460% |
| MildBull20 | MildBear20 | 1 | 12 | 8.3% | 100.0% | +0.660% | 1.300% | 0.990% |
| Bullish | MildBear20 | 1 | 12 | 8.3% | 100.0% | +0.280% | 0.700% | 0.620% |
| **Neutral20** | **Strong Bullish** | 5 | 63 | **7.9%** | 100.0% | +0.772% | 0.980% | 0.652% |
| MildBull20 | Bullish | 4 | 51 | 7.8% | 100.0% | +0.580% | 0.722% | 0.547% |
| Bearish | MildBear20 | 1 | 14 | 7.1% | 100.0% | +0.660% | 0.690% | 0.490% |
| MildBear20 | Neutral20 | 2 | 29 | 6.9% | 100.0% | +0.495% | 0.680% | 0.715% |
| MildBear20 | MildBear20 | 2 | 30 | 6.7% | 100.0% | +0.370% | 0.395% | 0.735% |
| MildBear20 | Strong Bullish | 1 | 15 | 6.7% | 100.0% | +0.620% | 0.840% | 0.780% |
| MildBull20 | Neutral20 | 2 | 32 | 6.2% | 100.0% | +0.255% | 0.725% | 1.165% |
| **Strong Bearish** | **Strong Bearish** | 5 | 80 | **6.2%** | 100.0% | +0.724% | 1.114% | 0.824% |
| **Bullish** | **Strong Bullish** | 8 | 129 | **6.2%** | 100.0% | +0.356% | 0.519% | 0.644% |
| Bullish | Strong Bearish | 1 | 17 | 5.9% | 100.0% | +0.610% | 0.770% | 0.930% |
| MildBull20 | Strong Bearish | 1 | 18 | 5.6% | 100.0% | +0.550% | 0.770% | 0.360% |
| Neutral20 | MildBear20 | 3 | 59 | 5.1% | 100.0% | +0.180% | 0.750% | 0.823% |
| MildBull20 | Strong Bullish | 3 | 60 | 5.0% | 100.0% | +0.757% | 1.020% | 0.783% |
| MildBear20 | Bearish | 2 | 48 | 4.2% | 100.0% | +0.070% | 0.525% | 0.990% |
| MildBull20 | MildBull20 | 1 | 26 | 3.8% | 100.0% | +0.510% | 0.630% | 0.700% |
| Bullish | Bullish | 1 | 26 | 3.8% | 100.0% | +0.090% | 0.460% | 0.630% |
| Neutral20 | Bullish | 1 | 49 | 2.0% | 100.0% | +0.190% | 0.380% | 0.830% |

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
| MildBull20 | 7 | 0.0% | 14.3% | 0.0% | 14.3% | **14.3%** |
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
| MildBull20 | 11 | 9.1% | 18.2% | 0.0% | 18.2% | **27.3%** |
| Neutral20 | 13 | 0.0% | 15.4% | 0.0% | 15.4% | **15.4%** |
| MildBear20 | 12 | 8.3% | 16.7% | 0.0% | 8.3% | **25.0%** |
| Strong Bearish | 17 | 5.9% | 23.5% | 5.9% | 5.9% | **29.4%** |

**Dominant reversal**: Bull Trap (26 days, 12.3%). Total reversals: 60/211 (28.4%).

## Section 3: FII MILDBULL20 — Reversal Profile (221 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 20 | 9.0% | 0.0% |
| Bear Trap | 30 | 13.6% | 100.0% |
| Rally Fade | 6 | 2.7% | 0.0% |
| Drop Bounce | 12 | 5.4% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 60 | 5.0% | 13.3% | 1.7% | 5.0% | **20.0%** |
| Bullish | 51 | 11.8% | 17.6% | 3.9% | 7.8% | **35.3%** |
| MildBull20 | 26 | 3.8% | 7.7% | 3.8% | 3.8% | **15.4%** |
| Neutral20 | 32 | 6.2% | 15.6% | 0.0% | 6.2% | **25.0%** |
| MildBear20 | 12 | 0.0% | 8.3% | 0.0% | 8.3% | **8.3%** |
| Bearish | 22 | 18.2% | 9.1% | 9.1% | 0.0% | **27.3%** |
| Strong Bearish | 18 | 22.2% | 16.7% | 0.0% | 5.6% | **38.9%** |

**Dominant reversal**: Bear Trap (30 days, 13.6%). Total reversals: 56/221 (25.3%).

## Section 4: FII NEUTRAL20 — Reversal Profile (446 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 51 | 11.4% | 0.0% |
| Bear Trap | 63 | 14.1% | 100.0% |
| Rally Fade | 21 | 4.7% | 0.0% |
| Drop Bounce | 42 | 9.4% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 63 | 9.5% | 12.7% | 3.2% | 7.9% | **25.4%** |
| Bullish | 49 | 10.2% | 10.2% | 0.0% | 2.0% | **22.4%** |
| MildBull20 | 54 | 13.0% | 14.8% | 3.7% | 9.3% | **29.6%** |
| Neutral20 | 108 | 14.8% | 11.1% | 10.2% | 13.9% | **34.3%** |
| MildBear20 | 59 | 13.6% | 15.3% | 3.4% | 5.1% | **30.5%** |
| Bearish | 61 | 8.2% | 18.0% | 4.9% | 13.1% | **32.8%** |
| Strong Bearish | 52 | 7.7% | 19.2% | 1.9% | 9.6% | **28.8%** |

**Dominant reversal**: Bear Trap (63 days, 14.1%). Total reversals: 133/446 (29.8%).

## Section 5: FII MILDBEAR20 — Reversal Profile (218 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 25 | 11.5% | 0.0% |
| Bear Trap | 36 | 16.5% | 100.0% |
| Rally Fade | 15 | 6.9% | 0.0% |
| Drop Bounce | 21 | 9.6% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 15 | 13.3% | 26.7% | 6.7% | 6.7% | **40.0%** |
| Bullish | 12 | 8.3% | 8.3% | 0.0% | 8.3% | **16.7%** |
| MildBull20 | 8 | 0.0% | 12.5% | 0.0% | 12.5% | **12.5%** |
| Neutral20 | 29 | 6.9% | 10.3% | 3.4% | 6.9% | **17.2%** |
| MildBear20 | 30 | 10.0% | 10.0% | 0.0% | 6.7% | **23.3%** |
| Bearish | 48 | 18.8% | 16.7% | 14.6% | 4.2% | **37.5%** |
| Strong Bearish | 76 | 10.5% | 21.1% | 7.9% | 15.8% | **36.8%** |

**Dominant reversal**: Bear Trap (36 days, 16.5%). Total reversals: 67/218 (30.7%).

## Section 6: FII BEARISH — Reversal Profile (184 days)

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
| Neutral20 | 15 | 6.7% | 20.0% | 6.7% | 13.3% | **33.3%** |
| MildBear20 | 14 | 14.3% | 14.3% | 0.0% | 7.1% | **28.6%** |
| Bearish | 32 | 9.4% | 12.5% | 6.2% | 12.5% | **34.4%** |
| Strong Bearish | 102 | 12.7% | 19.6% | 9.8% | 12.7% | **38.2%** |

**Dominant reversal**: Bear Trap (33 days, 17.9%). Total reversals: 67/184 (36.4%).

## Section 7: FII STRONG BEARISH — Reversal Profile (111 days)

| Pattern | Days | Rate | Green% |
|---|---|---|---|
| Bull Trap | 24 | 21.6% | 0.0% |
| Bear Trap | 20 | 18.0% | 100.0% |
| Rally Fade | 11 | 9.9% | 0.0% |
| Drop Bounce | 9 | 8.1% | 100.0% |

| PRO View | Days | Bull Trap% | Bear Trap% | Rally Fade% | Drop Bounce% | Any Reversal% |
|---|---|---|---|---|---|---|
| Strong Bullish | 5 | 40.0% | 0.0% | 20.0% | 0.0% | **40.0%** |
| Neutral20 | 6 | 50.0% | 16.7% | 16.7% | 0.0% | **66.7%** |
| MildBear20 | 7 | 14.3% | 0.0% | 0.0% | 14.3% | **28.6%** |
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
3. **Highest Bull Trap rate**: Strong Bearish FII + Neutral20 PRO — **50.0%** of days are Bull Traps (3/6 days). This combo is most likely to trap morning buyers.
4. **Highest Bear Trap rate**: Strong Bullish FII + Strong Bearish PRO — **33.3%** of days are Bear Traps (2/6 days). This combo is most likely to trap morning sellers.
5. **FII view reversal rates**: Highest = Strong Bearish (42.3%, 111d), Lowest = MildBull20 (25.3%, 221d).

### Actionable Rules:

- **Buy morning dips** (high Bear Trap rate): MildBear20+Strong Bullish (27%), Bullish+Strong Bearish (24%), MildBear20+Strong Bearish (21%)
- **Sell/short morning rallies** (high Bull Trap rate): MildBull20+Strong Bearish (22%), Bearish+Strong Bullish (20%), Strong Bearish+Strong Bearish (19%)
- **Trend-follow (low reversal rate)**: MildBull20+MildBear20 (8%), MildBull20+MildBull20 (15%), Bullish+Neutral20 (15%)
- **Expiry caution**: Reversal patterns may be amplified on expiry days due to options unwinding
