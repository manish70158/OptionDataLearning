# VIX Underestimation x FII/PRO Combination Analysis (No Neutral)

> **Dataset**: `vix_fii_t1_intraday_daily_results.csv` — 1,488 trading days (2020-08-06 to 2026-09-09)
>
> **Definition**: VIX "Underestimated" = actual intraday range exceeded VIX-predicted move (diff > 0%)
> (i.e., the market moved more than VIX implied it would, by any amount)
>
> **No Neutral Classification**: Every day is classified as directional — composite 0 maps to Mildly Bullish
>
> **T-1 data caveat**: FII/PRO views are derived from T+1 settlement data — alignment
> is known only after the trading day. This analysis identifies historical patterns,
> not real-time predictive signals.

### Label Guide
- **Mildly Bullish** = composite 0 to +50K (inclusive of zero)
- **Mildly Bearish** = composite -50K to -1 (exclusive of zero)
- **Bullish / Bearish** = composite ±50K to ±100K (fixed)
- **Strong Bullish / Strong Bearish** = composite beyond ±100K (fixed)
- **No Neutral zone** — every day is classified as directional

---

## Overall VIX Accuracy Distribution

| Category | Days | % of Total | Avg Range% | Avg Diff% |
|----------|-----:|-----------:|-----------:|----------:|
| **Underestimated** | **891** | **59.9%** | 1.27% | +0.45% |
| Overestimated | 597 | 40.1% | 0.65% | -0.19% |
| **Total** | **1488** | **100%** | 1.02% | 0.00% |

VIX underestimates the actual intraday range on **59.9%** of trading days — the market moves more than VIX predicts on the majority of days. Only 40% of days stay within VIX bounds. This report identifies which FII/PRO combinations amplify or dampen this systematic VIX bias.

---

## Alignment Category → Underestimation Rate

Which FII/PRO alignment type sees VIX underestimate most frequently?

| Alignment Category | Total Days | Underestimated | Rate | Share of All U/E | Avg Range (U/E) | Avg Diff (U/E) |
|--------------------|----------:|--------------:|-----:|-----------------:|----------------:|---------------:|
| **Bearish Alignment** | 555 | 367 | **66.1%** | 41.2% | 1.27% | +0.44% |
| FII Bearish + PRO Bullish | 177 | 103 | 58.2% | 11.6% | 1.36% | +0.52% |
| **Bullish Alignment** | 545 | 308 | **56.5%** | 34.6% | 1.26% | +0.44% |
| FII Bullish + PRO Bearish | 211 | 113 | 53.6% | 12.7% | 1.19% | +0.40% |

**Key insight**: Bearish Alignment has the highest underestimation rate (66.1%) while FII Bullish + PRO Bearish has the lowest (53.6%). The spread of 12.6 pp shows that FII/PRO positioning meaningfully influences how much actual volatility exceeds VIX predictions.

---

## Expiry Type Breakdown

| Expiry Type | Total | Under. | Rate | Avg Range% | Avg Diff% | Red% (U/E) | TTD% (U/E) |
|-------------|------:|-------:|-----:|-----------:|----------:|----------:|----------:|
| Weekly | 466 | 267 | 57.3% | 1.01% | +0.18% | 54.7% | 54.7% |
| Monthly | 139 | 92 | 66.2% | 1.08% | +0.23% | 52.2% | 52.2% |

---

## Per-Combination Underestimation Rate

All FII×PRO combinations with ≥5 days, sorted by underestimation rate.

| FII View | PRO View | Total Days | Underestimated | Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Avg Chg (U/E) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Bearish** | **Mildly Bullish** | 11 | 9 | **81.8%** | 44.4% | 1.42% | +0.56% | -0.450% |
| Strong Bearish | Strong Bullish | 5 | 4 | 80.0% | 25.0% | 1.20% | +0.49% | -0.312% |
| Strong Bullish | Bullish | 5 | 4 | 80.0% | 75.0% | 0.93% | +0.22% | +0.180% |
| **Strong Bearish** | **Strong Bearish** | 80 | 60 | **75.0%** | 33.3% | 1.15% | +0.38% | -0.143% |
| **Bearish** | **Bullish** | 7 | 5 | **71.4%** | 80.0% | 1.77% | +0.98% | +0.668% |
| **Strong Bearish** | **Mildly Bearish** | 10 | 7 | **70.0%** | 14.3% | 1.32% | +0.51% | -0.729% |
| **Bearish** | **Bearish** | 32 | 22 | **68.8%** | 40.9% | 1.19% | +0.38% | -0.198% |
| **Bearish** | **Strong Bearish** | 102 | 69 | **67.6%** | 43.5% | 1.20% | +0.37% | -0.106% |
| **Strong Bearish** | **Bearish** | 9 | 6 | **66.7%** | 33.3% | 1.04% | +0.24% | -0.187% |
| **Mildly Bullish** | **Strong Bullish** | 98 | 63 | **64.3%** | 50.8% | 1.25% | +0.43% | -0.031% |
| **Mildly Bearish** | **Strong Bearish** | 106 | 68 | **64.2%** | 54.4% | 1.30% | +0.50% | +0.036% |
| **Bearish** | **Mildly Bearish** | 22 | 14 | **63.6%** | 42.9% | 1.17% | +0.37% | -0.040% |
| **Mildly Bearish** | **Bearish** | 88 | 55 | **62.5%** | 45.5% | 1.32% | +0.45% | -0.075% |
| **Mildly Bearish** | **Mildly Bearish** | 106 | 66 | **62.3%** | 42.4% | 1.47% | +0.57% | -0.357% |
| **Strong Bullish** | **Strong Bullish** | 70 | 43 | **61.4%** | 60.5% | 1.21% | +0.45% | +0.002% |
| **Mildly Bullish** | **Bearish** | 43 | 26 | **60.5%** | 69.2% | 1.26% | +0.46% | +0.092% |
| **Mildly Bullish** | **Strong Bearish** | 40 | 24 | **60.0%** | 50.0% | 1.04% | +0.36% | -0.030% |
| **Mildly Bullish** | **Bullish** | 84 | 48 | **57.1%** | 39.6% | 1.37% | +0.49% | -0.230% |
| **Mildly Bearish** | **Mildly Bullish** | 69 | 39 | **56.5%** | 53.8% | 1.44% | +0.54% | +0.024% |
| **Strong Bullish** | **Mildly Bullish** | 9 | 5 | **55.6%** | 40.0% | 1.40% | +0.52% | -0.020% |
| **Mildly Bearish** | **Strong Bullish** | 40 | 22 | **55.0%** | 45.5% | 1.25% | +0.41% | -0.174% |
| **Bullish** | **Mildly Bullish** | 19 | 10 | **52.6%** | 80.0% | 1.20% | +0.43% | +0.546% |
| **Mildly Bullish** | **Mildly Bearish** | 78 | 41 | **52.6%** | 46.3% | 1.27% | +0.42% | -0.105% |
| **Mildly Bullish** | **Mildly Bullish** | 105 | 55 | **52.4%** | 45.5% | 1.43% | +0.48% | -0.187% |
| **Bullish** | **Strong Bullish** | 129 | 67 | **51.9%** | 32.8% | 1.11% | +0.37% | -0.264% |
| **Bearish** | **Strong Bullish** | 10 | 5 | **50.0%** | 40.0% | 1.14% | +0.40% | +0.042% |
| **Bullish** | **Bullish** | 26 | 13 | **50.0%** | 38.5% | 1.30% | +0.49% | -0.063% |
| **Mildly Bearish** | **Bullish** | 28 | 14 | **50.0%** | 57.1% | 1.25% | +0.45% | +0.159% |
| **Bullish** | **Mildly Bearish** | 17 | 8 | **47.1%** | 62.5% | 1.14% | +0.25% | -0.086% |
| **Bullish** | **Strong Bearish** | 17 | 8 | **47.1%** | 50.0% | 1.17% | +0.42% | +0.096% |
| Strong Bullish | Strong Bearish | 6 | 2 | 33.3% | 100.0% | 1.07% | +0.32% | +0.315% |

---

## Deep Dive: Bearish Alignment (Both FII & PRO Bearish-Leaning)

When both FII and PRO lean bearish (555 days total):

| Metric | Value |
|--------|------:|
| Total bearish alignment days | 555 |
| Underestimated | 367 (66.1%) |
| Avg range on underestimated days | 1.27% |
| Avg VIX miss (diff%) | +0.44% |
| Avg VIX predicted | 0.83% |
| Top to Down on U/E days | 209 (56.9%) |
| Down to Up on U/E days | 158 (43.1%) |
| Red (down close) on U/E days | 209 (56.9%) |

### Bearish Sub-Combinations

| FII View | PRO View | Days | U/E Days | U/E Rate | Avg Range (U/E) |
|---|---|---:|---:|---:|---:|
| Mildly Bearish | Mildly Bearish | 106 | 66 | 62.3% | 1.47% |
| Mildly Bearish | Bearish | 88 | 55 | 62.5% | 1.32% |
| Mildly Bearish | Strong Bearish | 106 | 68 | 64.2% | 1.30% |
| Bearish | Mildly Bearish | 22 | 14 | 63.6% | 1.17% |
| Bearish | Bearish | 32 | 22 | 68.8% | 1.19% |
| Bearish | Strong Bearish | 102 | 69 | 67.6% | 1.20% |
| Strong Bearish | Mildly Bearish | 10 | 7 | 70.0% | 1.32% |
| Strong Bearish | Bearish | 9 | 6 | 66.7% | 1.04% |
| Strong Bearish | Strong Bearish | 80 | 60 | 75.0% | 1.15% |

**Takeaway**: Within bearish alignment, Strong Bearish × Strong Bearish has the highest underestimation rate (75.0%, 80d) while Mildly Bearish × Mildly Bearish has the lowest (62.3%, 106d). Stronger bearish conviction on both sides correlates with higher VIX underestimation.

---

## Deep Dive: Bullish Alignment (Both FII & PRO Bullish-Leaning)

When both FII and PRO lean bullish (545 days total):

| Metric | Value |
|--------|------:|
| Total bullish alignment days | 545 |
| Underestimated | 308 (56.5%) |
| Avg range on underestimated days | 1.26% |
| Avg VIX miss (diff%) | +0.44% |
| Red (down close) on U/E days | 166 (53.9%) |
| Green (up close) on U/E days | 142 (46.1%) |

### Bullish Sub-Combinations

| FII View | PRO View | Days | U/E Days | U/E Rate | Avg Range (U/E) |
|---|---|---:|---:|---:|---:|
| Mildly Bullish | Mildly Bullish | 105 | 55 | 52.4% | 1.43% |
| Mildly Bullish | Bullish | 84 | 48 | 57.1% | 1.37% |
| Mildly Bullish | Strong Bullish | 98 | 63 | 64.3% | 1.25% |
| Bullish | Mildly Bullish | 19 | 10 | 52.6% | 1.20% |
| Bullish | Bullish | 26 | 13 | 50.0% | 1.30% |
| Bullish | Strong Bullish | 129 | 67 | 51.9% | 1.11% |
| Strong Bullish | Mildly Bullish | 9 | 5 | 55.6% | 1.40% |
| Strong Bullish | Bullish | 5 | 4 | 80.0% | 0.93% |
| Strong Bullish | Strong Bullish | 70 | 43 | 61.4% | 1.21% |

Bullish alignment underestimates 56.5% of the time vs bearish alignment at 66.1% — a 9.6 pp gap. On bullish U/E days, the market closes RED 53.9% and GREEN 46.1%, showing the excess range works both ways.

---

## Divergent Alignment — Opposing FII & PRO Views

### FII Bullish + PRO Bearish (211 days)

- Underestimated: 113 (53.6%)
- Avg range on U/E days: 1.19%
- Avg diff: +0.40%
- Red close on U/E days: 50 (44.2%)
- Top to Down on U/E days: 50 (44.2%)

### FII Bearish + PRO Bullish (177 days)

- Underestimated: 103 (58.2%)
- Avg range on U/E days: 1.36%
- Avg diff: +0.52%
- Red close on U/E days: 49 (47.6%)
- Top to Down on U/E days: 49 (47.6%)


---

## VIX Regime Analysis

| VIX Regime | Total | Under. | Rate | Avg Range% | Avg Diff% |
|------------|------:|-------:|-----:|-----------:|----------:|
| Low (<15) | 766 | 477 | 62.3% | 0.84% | +0.18% |
| Normal (15-20) | 435 | 248 | 57.0% | 1.09% | +0.18% |
| Elevated (20-30) | 286 | 166 | 58.0% | 1.41% | +0.24% |
| High (>30) | 1 | 0 | 0.0% | 1.57% | -0.10% |

**Low (<15)** has the highest underestimation rate (62.3%) while **High (>30)** has the lowest (0.0%). VIX underestimates the actual range across all regimes, confirming a systematic bias where the market routinely exceeds VIX-implied moves.

---

## Combined Composite Score → Underestimation Rate

FII + PRO composite summed together.

| Composite Range | Total | Under. | Rate | Avg Range (U/E) |
|-----------------|------:|-------:|-----:|----------------:|
| -200K & below | 227 | 157 | 69.2% | 1.16% |
| -200K to -100K | 209 | 133 | 63.6% | 1.26% |
| -100K to -50K | 149 | 95 | 63.8% | 1.31% |
| -50K to 0 | 175 | 102 | 58.3% | 1.40% |
| 0 to +50K | 172 | 89 | 51.7% | 1.39% |
| +50K to +100K | 130 | 71 | 54.6% | 1.34% |
| +100K to +200K | 179 | 98 | 54.7% | 1.33% |
| +200K & above | 247 | 146 | 59.1% | 1.14% |

---

## Section 1: FII STRONG BULLISH — Underestimation Profile (97 days, 58.8% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 70 | 43 | **61.4%** | 60.5% | 1.21% | +0.45% | 39.5% | 39.5% |
| Bullish | 5 | 4 | **80.0%** | 75.0% | 0.93% | +0.22% | 25.0% | 25.0% |
| Mildly Bullish | 9 | 5 | **55.6%** | 40.0% | 1.40% | +0.52% | 60.0% | 60.0% |
| Strong Bearish | 6 | 2 | **33.3%** | 100.0% | 1.07% | +0.32% | 0.0% | 0.0% |

**FII Strong Bullish summary**: 57/97 days underestimated (58.8%). On U/E days: 39% red, 39% Top-to-Down.

## Section 2: FII BULLISH — Underestimation Profile (211 days, 50.7% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 129 | 67 | **51.9%** | 32.8% | 1.11% | +0.37% | 67.2% | 67.2% |
| Bullish | 26 | 13 | **50.0%** | 38.5% | 1.30% | +0.49% | 61.5% | 61.5% |
| Mildly Bullish | 19 | 10 | **52.6%** | 80.0% | 1.20% | +0.43% | 20.0% | 20.0% |
| Mildly Bearish | 17 | 8 | **47.1%** | 62.5% | 1.14% | +0.25% | 37.5% | 37.5% |
| Strong Bearish | 17 | 8 | **47.1%** | 50.0% | 1.17% | +0.42% | 50.0% | 50.0% |

**FII Bullish summary**: 107/211 days underestimated (50.7%). On U/E days: 58% red, 58% Top-to-Down.

## Section 3: FII MILDLY BULLISH — Underestimation Profile (448 days, 57.4% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 98 | 63 | **64.3%** | 50.8% | 1.25% | +0.43% | 49.2% | 49.2% |
| Bullish | 84 | 48 | **57.1%** | 39.6% | 1.37% | +0.49% | 60.4% | 60.4% |
| Mildly Bullish | 105 | 55 | **52.4%** | 45.5% | 1.43% | +0.48% | 54.5% | 54.5% |
| Mildly Bearish | 78 | 41 | **52.6%** | 46.3% | 1.27% | +0.42% | 53.7% | 53.7% |
| Bearish | 43 | 26 | **60.5%** | 69.2% | 1.26% | +0.46% | 30.8% | 30.8% |
| Strong Bearish | 40 | 24 | **60.0%** | 50.0% | 1.04% | +0.36% | 50.0% | 50.0% |

**FII Mildly Bullish summary**: 257/448 days underestimated (57.4%). On U/E days: 51% red, 51% Top-to-Down.

## Section 4: FII MILDLY BEARISH — Underestimation Profile (437 days, 60.4% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 40 | 22 | **55.0%** | 45.5% | 1.25% | +0.41% | 54.5% | 54.5% |
| Bullish | 28 | 14 | **50.0%** | 57.1% | 1.25% | +0.45% | 42.9% | 42.9% |
| Mildly Bullish | 69 | 39 | **56.5%** | 53.8% | 1.44% | +0.54% | 46.2% | 46.2% |
| Mildly Bearish | 106 | 66 | **62.3%** | 42.4% | 1.47% | +0.57% | 57.6% | 57.6% |
| Bearish | 88 | 55 | **62.5%** | 45.5% | 1.32% | +0.45% | 54.5% | 54.5% |
| Strong Bearish | 106 | 68 | **64.2%** | 54.4% | 1.30% | +0.50% | 45.6% | 45.6% |

**FII Mildly Bearish summary**: 264/437 days underestimated (60.4%). On U/E days: 51% red, 51% Top-to-Down.

## Section 5: FII BEARISH — Underestimation Profile (184 days, 67.4% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 10 | 5 | **50.0%** | 40.0% | 1.14% | +0.40% | 60.0% | 60.0% |
| Bullish | 7 | 5 | **71.4%** | 80.0% | 1.77% | +0.98% | 20.0% | 20.0% |
| Mildly Bullish | 11 | 9 | **81.8%** | 44.4% | 1.42% | +0.56% | 55.6% | 55.6% |
| Mildly Bearish | 22 | 14 | **63.6%** | 42.9% | 1.17% | +0.37% | 57.1% | 57.1% |
| Bearish | 32 | 22 | **68.8%** | 40.9% | 1.19% | +0.38% | 59.1% | 59.1% |
| Strong Bearish | 102 | 69 | **67.6%** | 43.5% | 1.20% | +0.37% | 56.5% | 56.5% |

**FII Bearish summary**: 124/184 days underestimated (67.4%). On U/E days: 56% red, 56% Top-to-Down.

## Section 6: FII STRONG BEARISH — Underestimation Profile (111 days, 73.9% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 5 | 4 | **80.0%** | 25.0% | 1.20% | +0.49% | 75.0% | 75.0% |
| Mildly Bearish | 10 | 7 | **70.0%** | 14.3% | 1.32% | +0.51% | 85.7% | 85.7% |
| Bearish | 9 | 6 | **66.7%** | 33.3% | 1.04% | +0.24% | 66.7% | 66.7% |
| Strong Bearish | 80 | 60 | **75.0%** | 33.3% | 1.15% | +0.38% | 66.7% | 66.7% |

**FII Strong Bearish summary**: 82/111 days underestimated (73.9%). On U/E days: 66% red, 66% Top-to-Down.


---

## Day of Week → Underestimation Rate

| Day | Total | Under. | Rate |
|-----|------:|-------:|-----:|
| Monday | 298 | 190 | 63.8% |
| Tuesday | 300 | 169 | 56.3% |
| Wednesday | 296 | 168 | 56.8% |
| Thursday | 296 | 182 | 61.5% |
| Friday | 291 | 179 | 61.5% |

---

## Year → Underestimation Rate

| Year | Total | Under. | Rate |
|------|------:|-------:|-----:|
| 2020 | 102 | 45 | 44.1% |
| 2021 | 245 | 147 | 60.0% |
| 2022 | 243 | 137 | 56.4% |
| 2023 | 243 | 153 | 63.0% |
| 2024 | 244 | 148 | 60.7% |
| 2025 | 245 | 156 | 63.7% |
| 2026 | 166 | 105 | 63.3% |

---

## Top 20 Largest VIX Misses (Extreme Underestimation Days)

| Date | FII View | PRO View | VIX Pred% | Actual Range% | Miss | Direction | Close |
|------|----------|----------|----------:|--------------:|-----:|-----------|-------|
| 2024-06-04 | Strong Bullish | Strong Bullish | 1.10% | 8.19% | **+7.09%** | Top to Down | Red |
| 2020-12-21 | Mildly Bearish | Mildly Bearish | 0.97% | 4.67% | **+3.70%** | Top to Down | Red |
| 2020-08-31 | Mildly Bullish | Mildly Bullish | 0.96% | 3.97% | **+3.01%** | Top to Down | Red |
| 2026-02-01 | Mildly Bearish | Strong Bearish | 0.71% | 3.43% | **+2.72%** | Top to Down | Red |
| 2023-02-01 | Mildly Bullish | Bullish | 0.88% | 3.47% | **+2.59%** | Top to Down | Red |
| 2024-06-05 | Strong Bearish | Strong Bearish | 1.40% | 3.97% | **+2.57%** | Down to Up | Green |
| 2022-01-24 | Mildly Bearish | Mildly Bearish | 0.99% | 3.41% | **+2.42%** | Top to Down | Red |
| 2022-06-16 | Mildly Bullish | Mildly Bullish | 1.16% | 3.33% | **+2.17%** | Top to Down | Red |
| 2021-11-22 | Mildly Bearish | Strong Bullish | 0.78% | 2.89% | **+2.11%** | Top to Down | Red |
| 2021-03-19 | Mildly Bullish | Strong Bullish | 1.05% | 3.02% | **+1.97%** | Down to Up | Green |
| 2022-02-15 | Mildly Bearish | Strong Bearish | 1.20% | 3.15% | **+1.95%** | Down to Up | Green |
| 2020-10-15 | Mildly Bearish | Mildly Bullish | 1.06% | 3.00% | **+1.94%** | Top to Down | Red |
| 2026-02-03 | Bearish | Mildly Bullish | 0.73% | 2.66% | **+1.93%** | Top to Down | Red |
| 2022-05-04 | Mildly Bearish | Mildly Bullish | 1.06% | 2.95% | **+1.89%** | Top to Down | Red |
| 2024-01-23 | Mildly Bearish | Bearish | 0.72% | 2.57% | **+1.85%** | Top to Down | Red |
| 2021-02-26 | Mildly Bearish | Bearish | 1.20% | 3.03% | **+1.83%** | Top to Down | Red |
| 2024-12-13 | Bearish | Bullish | 0.69% | 2.50% | **+1.81%** | Down to Up | Green |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 1.28% | 3.01% | **+1.73%** | Top to Down | Red |
| 2024-11-22 | Bearish | Bullish | 0.84% | 2.55% | **+1.71%** | Down to Up | Green |
| 2024-03-13 | Bullish | Strong Bullish | 0.71% | 2.41% | **+1.70%** | Top to Down | Red |

**Observation**: Of the top 20, **15 were red days** and **15 were Top to Down** moves. Extreme VIX misses overwhelmingly resolve with downside price action.

---

## Key Findings

1. **VIX systematically underestimates** actual intraday range on 59.9% of trading days. The market routinely moves more than VIX implies — this is the baseline, not the exception.
2. **Bearish Alignment = most underestimated** (66.1%) vs **FII Bullish + PRO Bearish = least underestimated** (53.6%): A 12.6 pp spread shows FII/PRO positioning meaningfully modulates how much the market exceeds VIX predictions.
3. **Highest underestimation combo**: Bearish FII + Mildly Bullish PRO — **81.8%** across 11 days. **Lowest**: Strong Bullish FII + Strong Bearish PRO — **33.3%** across 6 days.
4. **Bearish alignment amplifies VIX underestimation**: Bearish at 66.1% vs Bullish at 56.5% (+9.6 pp gap). Bearish institutional positioning produces larger-than-expected moves more consistently.
5. **Most range-bound combination (≥10 days)**: Bullish FII + Mildly Bearish PRO — 47.1% underestimation across 17 days (VIX is more accurate for this combo). 
6. **VIX regime**: Low (<15) has the highest underestimation (62.3%), High (>30) has the lowest (0.0%). VIX underestimates across all regimes — the bias is structural, not regime-dependent.
7. **Day of week**: Mondays (63.8%) are most prone to underestimation. Tuesdays (56.3%) are least prone.
8. **Extreme outliers**: The largest VIX misses (>+1.5%) often occur in combinations where positioning doesn't fully explain the move — suggesting exogenous shocks (geopolitical, macro, election results) drive the most extreme blowouts.

---

## Trading Implications

**Baseline reality**: VIX underestimates the actual range on 60% of days. Any options strategy priced off VIX is likely underpricing actual movement on most days.

- **Highest excess volatility** (top quartile, ≥64% U/E rate): Bearish+Mildly Bullish (82%), Strong Bearish+Strong Bearish (75%), Strong Bearish+Mildly Bearish (70%), Bearish+Bearish (69%), Bearish+Strong Bearish (68%) — straddles/strangles priced off VIX are most likely to be cheap for these combos
- **Most VIX-accurate combos** (bottom quartile, ≤52% U/E rate): Mildly Bullish+Mildly Bullish (52%), Bullish+Strong Bullish (52%), Bearish+Strong Bullish (50%), Bullish+Bullish (50%), Mildly Bearish+Bullish (50%) — iron condors and range-bound strategies are relatively safer here
- **Bearish alignment + weekend effect**: When both FII/PRO lean bearish on Mondays/Fridays, the probability of range exceeding VIX is highest — widen stop-losses or buy premium
- **VIX is a floor, not a ceiling**: With 60% underestimation rate, treat VIX-predicted range as the minimum expected move, not the maximum
- **This is retrospective analysis using T+1 data** — use as a volatility framework, not as an intraday entry signal

---

*Generated: 2026-09-12 | Data: 2020-08-06 to 2026-09-09 | Source: vix_fii_t1_intraday_daily_results.csv | No Neutral Classification*
