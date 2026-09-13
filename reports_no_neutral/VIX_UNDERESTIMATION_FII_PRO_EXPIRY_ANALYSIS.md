# VIX Underestimation x FII/PRO Combination Analysis — Expiry Days Only (No Neutral)

> **Dataset**: `vix_fii_t1_intraday_daily_results.csv` — 312 trading days (2020-08-06 to 2026-09-01)
>
> **Definition**: VIX "Underestimated" = actual intraday range exceeded VIX-predicted move (diff > 0%)
> (i.e., the market moved more than VIX implied it would, by any amount)
>
> **No Neutral Classification**: Every day is classified as directional — composite 0 maps to Mildly Bullish
> **Filter**: Nifty expiry days only — 312 days (239 weekly + 73 monthly)
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
| **Underestimated** | **184** | **59.0%** | 1.27% | +0.45% |
| Overestimated | 128 | 41.0% | 0.65% | -0.20% |
| **Total** | **312** | **100%** | 1.02% | 0.00% |

VIX underestimates the actual intraday range on **59.0%** of trading days — the market moves more than VIX predicts on the majority of days. Only 41% of days stay within VIX bounds. This report identifies which FII/PRO combinations amplify or dampen this systematic VIX bias.

---

## Alignment Category → Underestimation Rate

Which FII/PRO alignment type sees VIX underestimate most frequently?

| Alignment Category | Total Days | Underestimated | Rate | Share of All U/E | Avg Range (U/E) | Avg Diff (U/E) |
|--------------------|----------:|--------------:|-----:|-----------------:|----------------:|---------------:|
| **Bearish Alignment** | 117 | 79 | **67.5%** | 42.9% | 1.28% | +0.42% |
| **Bullish Alignment** | 104 | 60 | **57.7%** | 32.6% | 1.25% | +0.44% |
| FII Bearish + PRO Bullish | 38 | 20 | 52.6% | 10.9% | 1.40% | +0.61% |
| FII Bullish + PRO Bearish | 53 | 25 | 47.2% | 13.6% | 1.19% | +0.42% |

**Key insight**: Bearish Alignment has the highest underestimation rate (67.5%) while FII Bullish + PRO Bearish has the lowest (47.2%). The spread of 20.4 pp shows that FII/PRO positioning meaningfully influences how much actual volatility exceeds VIX predictions.

---

## Expiry Type Breakdown

| Expiry Type | Total | Under. | Rate | Avg Range% | Avg Diff% | Red% (U/E) | TTD% (U/E) |
|-------------|------:|-------:|-----:|-----------:|----------:|----------:|----------:|
| Weekly | 239 | 135 | 56.5% | 1.00% | +0.17% | 57.0% | 57.0% |
| Monthly | 73 | 49 | 67.1% | 1.07% | +0.22% | 46.9% | 46.9% |

---

## Per-Combination Underestimation Rate

All FII×PRO combinations with ≥3 days, sorted by underestimation rate.

| FII View | PRO View | Total Days | Underestimated | Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Avg Chg (U/E) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Mildly Bearish** | **Bullish** | 3 | 3 | **100.0%** | 0.0% | 1.34% | +0.56% | -0.700% |
| **Strong Bearish** | **Bearish** | 4 | 4 | **100.0%** | 25.0% | 1.10% | +0.18% | -0.267% |
| **Bearish** | **Strong Bearish** | 21 | 17 | **81.0%** | 35.3% | 1.27% | +0.41% | -0.344% |
| **Strong Bearish** | **Strong Bearish** | 10 | 8 | **80.0%** | 25.0% | 1.09% | +0.37% | -0.286% |
| **Mildly Bullish** | **Strong Bullish** | 19 | 14 | **73.7%** | 50.0% | 1.18% | +0.39% | -0.106% |
| **Mildly Bullish** | **Strong Bearish** | 14 | 10 | **71.4%** | 50.0% | 1.05% | +0.31% | +0.191% |
| **Bearish** | **Mildly Bearish** | 9 | 6 | **66.7%** | 50.0% | 1.12% | +0.31% | +0.042% |
| Bullish | Mildly Bullish | 3 | 2 | 66.7% | 100.0% | 1.72% | +1.07% | +1.355% |
| Strong Bearish | Strong Bullish | 3 | 2 | 66.7% | 0.0% | 1.35% | +0.60% | -0.675% |
| **Mildly Bearish** | **Bearish** | 20 | 13 | **65.0%** | 53.8% | 1.40% | +0.44% | +0.148% |
| **Mildly Bearish** | **Strong Bearish** | 30 | 19 | **63.3%** | 57.9% | 1.37% | +0.53% | -0.037% |
| **Bearish** | **Bearish** | 5 | 3 | **60.0%** | 33.3% | 1.14% | +0.14% | -0.290% |
| **Bullish** | **Strong Bearish** | 5 | 3 | **60.0%** | 66.7% | 1.22% | +0.46% | +0.410% |
| **Bullish** | **Strong Bullish** | 29 | 17 | **58.6%** | 52.9% | 1.16% | +0.41% | +0.016% |
| **Mildly Bullish** | **Bullish** | 24 | 14 | **58.3%** | 35.7% | 1.27% | +0.43% | -0.181% |
| **Strong Bullish** | **Strong Bullish** | 7 | 4 | **57.1%** | 100.0% | 0.95% | +0.14% | +0.395% |
| Bearish | Strong Bullish | 4 | 2 | 50.0% | 50.0% | 1.14% | +0.49% | +0.135% |
| Bullish | Bullish | 4 | 2 | 50.0% | 50.0% | 1.11% | +0.31% | +0.260% |
| **Mildly Bearish** | **Mildly Bearish** | 17 | 8 | **47.1%** | 37.5% | 1.38% | +0.53% | -0.414% |
| **Mildly Bearish** | **Mildly Bullish** | 15 | 7 | **46.7%** | 14.3% | 1.61% | +0.69% | -0.776% |
| **Mildly Bullish** | **Mildly Bearish** | 15 | 6 | **40.0%** | 50.0% | 1.29% | +0.49% | -0.038% |
| **Mildly Bullish** | **Mildly Bullish** | 15 | 6 | **40.0%** | 50.0% | 1.77% | +0.75% | -0.378% |
| **Mildly Bullish** | **Bearish** | 12 | 4 | **33.3%** | 75.0% | 1.39% | +0.66% | -0.037% |
| Bullish | Mildly Bearish | 7 | 2 | 28.6% | 50.0% | 1.18% | +0.21% | -0.160% |
| Mildly Bearish | Strong Bullish | 9 | 2 | 22.2% | 50.0% | 0.99% | +0.37% | 0.000% |

---

## Deep Dive: Bearish Alignment (Both FII & PRO Bearish-Leaning)

When both FII and PRO lean bearish (117 days total):

| Metric | Value |
|--------|------:|
| Total bearish alignment days | 117 |
| Underestimated | 79 (67.5%) |
| Avg range on underestimated days | 1.28% |
| Avg VIX miss (diff%) | +0.42% |
| Avg VIX predicted | 0.86% |
| Top to Down on U/E days | 45 (57.0%) |
| Down to Up on U/E days | 34 (43.0%) |
| Red (down close) on U/E days | 45 (57.0%) |

### Bearish Sub-Combinations

| FII View | PRO View | Days | U/E Days | U/E Rate | Avg Range (U/E) |
|---|---|---:|---:|---:|---:|
| Mildly Bearish | Mildly Bearish | 17 | 8 | 47.1% | 1.38% |
| Mildly Bearish | Bearish | 20 | 13 | 65.0% | 1.40% |
| Mildly Bearish | Strong Bearish | 30 | 19 | 63.3% | 1.37% |
| Bearish | Mildly Bearish | 9 | 6 | 66.7% | 1.12% |
| Bearish | Bearish | 5 | 3 | 60.0% | 1.14% |
| Bearish | Strong Bearish | 21 | 17 | 81.0% | 1.27% |
| Strong Bearish | Bearish | 4 | 4 | 100.0% | 1.10% |
| Strong Bearish | Strong Bearish | 10 | 8 | 80.0% | 1.09% |

**Takeaway**: Within bearish alignment, Strong Bearish × Bearish has the highest underestimation rate (100.0%, 4d) while Mildly Bearish × Mildly Bearish has the lowest (47.1%, 17d). Stronger bearish conviction on both sides correlates with higher VIX underestimation.

---

## Deep Dive: Bullish Alignment (Both FII & PRO Bullish-Leaning)

When both FII and PRO lean bullish (104 days total):

| Metric | Value |
|--------|------:|
| Total bullish alignment days | 104 |
| Underestimated | 60 (57.7%) |
| Avg range on underestimated days | 1.25% |
| Avg VIX miss (diff%) | +0.44% |
| Red (down close) on U/E days | 29 (48.3%) |
| Green (up close) on U/E days | 31 (51.7%) |

### Bullish Sub-Combinations

| FII View | PRO View | Days | U/E Days | U/E Rate | Avg Range (U/E) |
|---|---|---:|---:|---:|---:|
| Mildly Bullish | Mildly Bullish | 15 | 6 | 40.0% | 1.77% |
| Mildly Bullish | Bullish | 24 | 14 | 58.3% | 1.27% |
| Mildly Bullish | Strong Bullish | 19 | 14 | 73.7% | 1.18% |
| Bullish | Mildly Bullish | 3 | 2 | 66.7% | 1.72% |
| Bullish | Bullish | 4 | 2 | 50.0% | 1.11% |
| Bullish | Strong Bullish | 29 | 17 | 58.6% | 1.16% |
| Strong Bullish | Mildly Bullish | 2 | 0 | 0.0% | 0.00% |
| Strong Bullish | Strong Bullish | 7 | 4 | 57.1% | 0.95% |

Bullish alignment underestimates 57.7% of the time vs bearish alignment at 67.5% — a 9.8 pp gap. On bullish U/E days, the market closes RED 48.3% and GREEN 51.7%, showing the excess range works both ways.

---

## Divergent Alignment — Opposing FII & PRO Views

### FII Bullish + PRO Bearish (53 days)

- Underestimated: 25 (47.2%)
- Avg range on U/E days: 1.19%
- Avg diff: +0.42%
- Red close on U/E days: 11 (44.0%)
- Top to Down on U/E days: 11 (44.0%)

### FII Bearish + PRO Bullish (38 days)

- Underestimated: 20 (52.6%)
- Avg range on U/E days: 1.40%
- Avg diff: +0.61%
- Red close on U/E days: 15 (75.0%)
- Top to Down on U/E days: 15 (75.0%)


---

## VIX Regime Analysis

| VIX Regime | Total | Under. | Rate | Avg Range% | Avg Diff% |
|------------|------:|-------:|-----:|-----------:|----------:|
| Low (<15) | 158 | 100 | 63.3% | 0.87% | +0.21% |
| Normal (15-20) | 93 | 49 | 52.7% | 1.03% | +0.12% |
| Elevated (20-30) | 61 | 35 | 57.4% | 1.37% | +0.20% |

**Low (<15)** has the highest underestimation rate (63.3%) while **Normal (15-20)** has the lowest (52.7%). VIX underestimates the actual range across all regimes, confirming a systematic bias where the market routinely exceeds VIX-implied moves.

---

## Combined Composite Score → Underestimation Rate

FII + PRO composite summed together.

| Composite Range | Total | Under. | Rate | Avg Range (U/E) |
|-----------------|------:|-------:|-----:|----------------:|
| -200K & below | 49 | 39 | 79.6% | 1.25% |
| -200K to -100K | 53 | 34 | 64.2% | 1.25% |
| -100K to -50K | 32 | 18 | 56.2% | 1.29% |
| -50K to 0 | 31 | 13 | 41.9% | 1.44% |
| 0 to +50K | 33 | 16 | 48.5% | 1.44% |
| +50K to +100K | 22 | 13 | 59.1% | 1.37% |
| +100K to +200K | 41 | 20 | 48.8% | 1.26% |
| +200K & above | 51 | 31 | 60.8% | 1.13% |

---

## Section 1: FII STRONG BULLISH — Underestimation Profile (10 days, 50.0% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 7 | 4 | **57.1%** | 100.0% | 0.95% | +0.14% | 0.0% | 0.0% |

**FII Strong Bullish summary**: 5/10 days underestimated (50.0%). On U/E days: 20% red, 20% Top-to-Down.

## Section 2: FII BULLISH — Underestimation Profile (48 days, 54.2% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 29 | 17 | **58.6%** | 52.9% | 1.16% | +0.41% | 47.1% | 47.1% |
| Bullish | 4 | 2 | **50.0%** | 50.0% | 1.11% | +0.31% | 50.0% | 50.0% |
| Mildly Bullish | 3 | 2 | **66.7%** | 100.0% | 1.72% | +1.07% | 0.0% | 0.0% |
| Mildly Bearish | 7 | 2 | **28.6%** | 50.0% | 1.18% | +0.21% | 50.0% | 50.0% |
| Strong Bearish | 5 | 3 | **60.0%** | 66.7% | 1.22% | +0.46% | 33.3% | 33.3% |

**FII Bullish summary**: 26/48 days underestimated (54.2%). On U/E days: 42% red, 42% Top-to-Down.

## Section 3: FII MILDLY BULLISH — Underestimation Profile (99 days, 54.5% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 19 | 14 | **73.7%** | 50.0% | 1.18% | +0.39% | 50.0% | 50.0% |
| Bullish | 24 | 14 | **58.3%** | 35.7% | 1.27% | +0.43% | 64.3% | 64.3% |
| Mildly Bullish | 15 | 6 | **40.0%** | 50.0% | 1.77% | +0.75% | 50.0% | 50.0% |
| Mildly Bearish | 15 | 6 | **40.0%** | 50.0% | 1.29% | +0.49% | 50.0% | 50.0% |
| Bearish | 12 | 4 | **33.3%** | 75.0% | 1.39% | +0.66% | 25.0% | 25.0% |
| Strong Bearish | 14 | 10 | **71.4%** | 50.0% | 1.05% | +0.31% | 50.0% | 50.0% |

**FII Mildly Bullish summary**: 54/99 days underestimated (54.5%). On U/E days: 52% red, 52% Top-to-Down.

## Section 4: FII MILDLY BEARISH — Underestimation Profile (94 days, 55.3% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 9 | 2 | **22.2%** | 50.0% | 0.99% | +0.37% | 50.0% | 50.0% |
| Bullish | 3 | 3 | **100.0%** | 0.0% | 1.34% | +0.56% | 100.0% | 100.0% |
| Mildly Bullish | 15 | 7 | **46.7%** | 14.3% | 1.61% | +0.69% | 85.7% | 85.7% |
| Mildly Bearish | 17 | 8 | **47.1%** | 37.5% | 1.38% | +0.53% | 62.5% | 62.5% |
| Bearish | 20 | 13 | **65.0%** | 53.8% | 1.40% | +0.44% | 46.2% | 46.2% |
| Strong Bearish | 30 | 19 | **63.3%** | 57.9% | 1.37% | +0.53% | 42.1% | 42.1% |

**FII Mildly Bearish summary**: 52/94 days underestimated (55.3%). On U/E days: 56% red, 56% Top-to-Down.

## Section 5: FII BEARISH — Underestimation Profile (42 days, 73.8% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 4 | 2 | **50.0%** | 50.0% | 1.14% | +0.49% | 50.0% | 50.0% |
| Mildly Bearish | 9 | 6 | **66.7%** | 50.0% | 1.12% | +0.31% | 50.0% | 50.0% |
| Bearish | 5 | 3 | **60.0%** | 33.3% | 1.14% | +0.14% | 66.7% | 66.7% |
| Strong Bearish | 21 | 17 | **81.0%** | 35.3% | 1.27% | +0.41% | 64.7% | 64.7% |

**FII Bearish summary**: 31/42 days underestimated (73.8%). On U/E days: 61% red, 61% Top-to-Down.

## Section 6: FII STRONG BEARISH — Underestimation Profile (19 days, 84.2% U/E rate)

| PRO View | Days | U/E Days | U/E Rate | Green% (U/E) | Avg Range (U/E) | Avg Diff (U/E) | Red% (U/E) | TTD% (U/E) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Strong Bullish | 3 | 2 | **66.7%** | 0.0% | 1.35% | +0.60% | 100.0% | 100.0% |
| Bearish | 4 | 4 | **100.0%** | 25.0% | 1.10% | +0.18% | 75.0% | 75.0% |
| Strong Bearish | 10 | 8 | **80.0%** | 25.0% | 1.09% | +0.37% | 75.0% | 75.0% |

**FII Strong Bearish summary**: 16/19 days underestimated (84.2%). On U/E days: 75% red, 75% Top-to-Down.


---

## Day of Week → Underestimation Rate

| Day | Total | Under. | Rate |
|-----|------:|-------:|-----:|
| Monday | 3 | 3 | 100.0% |
| Tuesday | 49 | 28 | 57.1% |
| Wednesday | 12 | 6 | 50.0% |
| Thursday | 248 | 147 | 59.3% |

---

## Year → Underestimation Rate

| Year | Total | Under. | Rate |
|------|------:|-------:|-----:|
| 2020 | 21 | 5 | 23.8% |
| 2021 | 52 | 27 | 51.9% |
| 2022 | 51 | 31 | 60.8% |
| 2023 | 51 | 38 | 74.5% |
| 2024 | 51 | 32 | 62.7% |
| 2025 | 52 | 30 | 57.7% |
| 2026 | 34 | 21 | 61.8% |

---

## Top 20 Largest VIX Misses (Extreme Underestimation Days)

| Date | FII View | PRO View | VIX Pred% | Actual Range% | Miss | Direction | Close |
|------|----------|----------|----------:|--------------:|-----:|-----------|-------|
| 2022-06-16 | Mildly Bullish | Mildly Bullish | 1.16% | 3.33% | **+2.17%** | Top to Down | Red |
| 2020-10-15 | Mildly Bearish | Mildly Bullish | 1.06% | 3.00% | **+1.94%** | Top to Down | Red |
| 2026-02-03 | Bearish | Mildly Bullish | 0.73% | 2.66% | **+1.93%** | Top to Down | Red |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 1.28% | 3.01% | **+1.73%** | Top to Down | Red |
| 2025-05-15 | Mildly Bullish | Strong Bullish | 0.90% | 2.52% | **+1.62%** | Down to Up | Green |
| 2025-04-17 | Mildly Bullish | Bullish | 0.83% | 2.45% | **+1.62%** | Down to Up | Green |
| 2021-03-18 | Mildly Bearish | Bearish | 1.06% | 2.63% | **+1.57%** | Top to Down | Red |
| 2024-12-05 | Mildly Bullish | Mildly Bearish | 0.76% | 2.29% | **+1.53%** | Down to Up | Green |
| 2021-10-28 | Bearish | Strong Bearish | 0.88% | 2.13% | **+1.25%** | Top to Down | Red |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 0.71% | 1.96% | **+1.25%** | Down to Up | Green |
| 2025-01-02 | Bullish | Mildly Bullish | 0.76% | 2.00% | **+1.24%** | Down to Up | Green |
| 2024-11-28 | Mildly Bullish | Bearish | 0.77% | 1.95% | **+1.18%** | Top to Down | Red |
| 2026-01-20 | Mildly Bearish | Mildly Bearish | 0.62% | 1.62% | **+1.00%** | Top to Down | Red |
| 2024-10-03 | Strong Bearish | Strong Bullish | 0.63% | 1.61% | **+0.98%** | Top to Down | Red |
| 2024-04-18 | Mildly Bullish | Strong Bullish | 0.66% | 1.64% | **+0.98%** | Top to Down | Red |
| 2024-03-28 | Bearish | Strong Bullish | 0.66% | 1.59% | **+0.93%** | Down to Up | Green |
| 2020-09-24 | Mildly Bearish | Mildly Bearish | 1.10% | 2.03% | **+0.93%** | Top to Down | Red |
| 2021-03-25 | Mildly Bearish | Strong Bearish | 1.18% | 2.10% | **+0.92%** | Top to Down | Red |
| 2022-08-04 | Mildly Bearish | Bullish | 0.97% | 1.88% | **+0.91%** | Top to Down | Red |
| 2024-04-25 | Bullish | Mildly Bullish | 0.54% | 1.44% | **+0.90%** | Down to Up | Green |

**Observation**: Of the top 20, **13 were red days** and **13 were Top to Down** moves. Extreme VIX misses overwhelmingly resolve with downside price action.

---

## Key Findings

1. **VIX systematically underestimates** actual intraday range on 59.0% of trading days. The market routinely moves more than VIX implies — this is the baseline, not the exception.
2. **Bearish Alignment = most underestimated** (67.5%) vs **FII Bullish + PRO Bearish = least underestimated** (47.2%): A 20.4 pp spread shows FII/PRO positioning meaningfully modulates how much the market exceeds VIX predictions.
3. **Highest underestimation combo**: Mildly Bearish FII + Bullish PRO — **100.0%** across 3 days. **Lowest**: Mildly Bearish FII + Strong Bullish PRO — **22.2%** across 9 days.
4. **Bearish alignment amplifies VIX underestimation**: Bearish at 67.5% vs Bullish at 57.7% (+9.8 pp gap). Bearish institutional positioning produces larger-than-expected moves more consistently.
5. **Most range-bound combination (≥5 days)**: Mildly Bearish FII + Strong Bullish PRO — 22.2% underestimation across 9 days (VIX is more accurate for this combo). 
6. **VIX regime**: Low (<15) has the highest underestimation (63.3%), Normal (15-20) has the lowest (52.7%). VIX underestimates across all regimes — the bias is structural, not regime-dependent.
7. **Day of week**: Mondays (100.0%) are most prone to underestimation. Wednesdays (50.0%) are least prone.
8. **Extreme outliers**: The largest VIX misses (>+1.5%) often occur in combinations where positioning doesn't fully explain the move — suggesting exogenous shocks (geopolitical, macro, election results) drive the most extreme blowouts.

---

## Trading Implications

**Baseline reality**: VIX underestimates the actual range on 59% of days. Any options strategy priced off VIX is likely underpricing actual movement on most days.

- **Highest excess volatility** (top quartile, ≥67% U/E rate): Bearish+Strong Bearish (81%), Strong Bearish+Strong Bearish (80%), Mildly Bullish+Strong Bullish (74%), Mildly Bullish+Strong Bearish (71%), Bearish+Mildly Bearish (67%) — straddles/strangles priced off VIX are most likely to be cheap for these combos
- **Most VIX-accurate combos** (bottom quartile, ≤40% U/E rate): Mildly Bullish+Mildly Bearish (40%), Mildly Bullish+Mildly Bullish (40%), Mildly Bullish+Bearish (33%), Bullish+Mildly Bearish (29%), Mildly Bearish+Strong Bullish (22%) — iron condors and range-bound strategies are relatively safer here
- **Bearish alignment + weekend effect**: When both FII/PRO lean bearish on Mondays/Fridays, the probability of range exceeding VIX is highest — widen stop-losses or buy premium
- **VIX is a floor, not a ceiling**: With 59% underestimation rate, treat VIX-predicted range as the minimum expected move, not the maximum
- **This is retrospective analysis using T+1 data** — use as a volatility framework, not as an intraday entry signal

---

*Generated: 2026-09-12 | Data: 2020-08-06 to 2026-09-01 | Source: vix_fii_t1_intraday_daily_results.csv | No Neutral Classification | Expiry Days Only*
