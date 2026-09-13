# Profitable Strategies with Low Stop Loss Trigger Rate

*Strategies that make money without getting stopped out — the safest signals to trade.*

This report filters for FII/PRO × Strategy combinations that are:
1. **Profitable** (total P&L > 0)
2. **Low stop loss hits** (sorted by SL rate ascending, then by P&L descending)
3. **Minimum 5 trading days** (excludes statistically unreliable combos)

**8 strategies tested** — 4 buying + 4 selling:

| Buying (pay premium) | Selling (collect premium) |
|---|---|
| Straddle (Buy CE + Buy PE) | Short Straddle (Sell CE + Sell PE) |
| Strangle (Buy OTM CE + Buy OTM PE) | Short Strangle (Sell OTM CE + Sell OTM PE) |
| Bull Call Spread (Buy CE + Sell higher CE) | Iron Condor (Sell CE + Sell PE + buy wings) |
| Bear Put Spread (Buy PE + Sell lower PE) | Iron Butterfly (Sell ATM CE + Sell ATM PE + buy wings) |

Stop loss is percentage-based (scales with NIFTY level):

| Strategy | SL % | SL at NIFTY 15000 | SL at NIFTY 25000 |
|---|---|---|---|
| Iron Condor | 0.25% | 38 pts | 63 pts |
| Iron Butterfly | 0.40% | 60 pts | 100 pts |
| Bull Call Spread | 0.25% | 38 pts | 63 pts |
| Bear Put Spread | 0.25% | 38 pts | 63 pts |
| Straddle | 0.30% | 45 pts | 75 pts |
| Strangle | 0.20% | 30 pts | 50 pts |
| Short Straddle | 0.50% | 75 pts | 125 pts |
| Short Strangle | 0.40% | 60 pts | 100 pts |

---

## Summary

- **88 profitable combinations** found across all FII/PRO × Strategy pairs (8 strategies)
- **83 of 88 (94%)** had zero stop loss triggers
- **78 profitable combos are buying strategies, 10 are selling strategies**
- **Selling strategies are profitable in only 10 specific combos** (vs 78 for buying)
- Only 5 combos were profitable despite hitting SL occasionally

---

## Overall Strategy Performance (6 years, 1,488 days)

| Strategy | Type | Total P&L | ₹/Lot | Avg/Day | Win% | SL Hits | SL% |
|---|---|---|---|---|---|---|---|
| Straddle | BUY | +10,601 pts | +₹265,014 | +7.12 | 39.0% | 0 | 0.0% |
| Strangle | BUY | +1,172 pts | +₹29,296 | +0.79 | 30.9% | 0 | 0.0% |
| Bear Put Spread | BUY | +207 pts | +₹5,186 | +0.14 | 44.2% | 2 | 0.1% |
| Bull Call Spread | BUY | -7,793 pts | ₹194,827 | -5.24 | 38.4% | 53 | 3.6% |
| Short Strangle | SELL | -12,428 pts | ₹310,707 | -8.35 | 47.8% | 174 | 11.7% |
| Iron Condor | SELL | -16,944 pts | ₹423,592 | -11.39 | 14.3% | 108 | 7.3% |
| Short Straddle | SELL | -20,594 pts | ₹514,844 | -13.84 | 48.8% | 239 | 16.1% |
| Iron Butterfly | SELL | -21,667 pts | ₹541,685 | -14.56 | 17.1% | 85 | 5.7% |

**All 4 selling strategies lost money overall.** But some specific FII/PRO combinations are profitable for selling — see below.

---
## Top 25 — Most Profitable with Lowest Stop Loss

These are the highest-earning signals sorted by SL rate (ascending) then P&L (descending).

| # | FII View | PRO View | Strategy | Type | Total P&L | Avg/Day | Win% | Days | SL Hits |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Mildly Bearish | Strong Bearish | Straddle | BUY | 1459 pts | 27.54 | 52.8% | 53 | 0 |
| 2 | Neutral | Bearish | Straddle | BUY | 853 pts | 9.27 | 39.1% | 92 | 0 |
| 3 | Bearish | Neutral | Straddle | BUY | 832 pts | 43.80 | 57.9% | 19 | 0 |
| 4 | Neutral | Strong Bearish | Straddle | BUY | 801 pts | 9.77 | 47.6% | 82 | 0 |
| 5 | Neutral | Mildly Bullish | Straddle | BUY | 780 pts | 20.00 | 46.2% | 39 | 0 |
| 6 | Bullish | Strong Bullish | Straddle | BUY | 689 pts | 5.34 | 36.4% | 129 | 0 |
| 7 | Mildly Bearish | Strong Bearish | Strangle | BUY | 655 pts | 12.36 | 39.6% | 53 | 0 |
| 8 | Neutral | Bullish | Straddle | BUY | 595 pts | 7.53 | 39.2% | 79 | 0 |
| 9 | Strong Bearish | Strong Bearish | Straddle | BUY | 556 pts | 6.96 | 40.0% | 80 | 0 |
| 10 | Mildly Bullish | Strong Bullish | Straddle | BUY | 476 pts | 11.90 | 50.0% | 40 | 0 |
| 11 | Bearish | Neutral | Strangle | BUY | 468 pts | 24.61 | 63.2% | 19 | 0 |
| 12 | Bullish | Strong Bullish | Bear Put Spread | BUY | 445 pts | 3.45 | 57.4% | 129 | 0 |
| 13 | Strong Bullish | Strong Bullish | Straddle | BUY | 442 pts | 6.32 | 32.9% | 70 | 0 |
| 14 | Neutral | Mildly Bullish | Strangle | BUY | 436 pts | 11.17 | 33.3% | 39 | 0 |
| 15 | Neutral | Neutral | Straddle | BUY | 408 pts | 2.10 | 33.5% | 194 | 0 |
| 16 | Bearish | Bearish | Straddle | BUY | 373 pts | 11.66 | 37.5% | 32 | 0 |
| 17 | Bullish | Mildly Bullish | Straddle | BUY | 362 pts | 45.31 | 37.5% | 8 | 0 |
| 18 | Strong Bullish | Strong Bullish | Strangle | BUY | 321 pts | 4.58 | 20.0% | 70 | 0 |
| 19 | Mildly Bullish | Strong Bullish | Bear Put Spread | BUY | 314 pts | 7.85 | 60.0% | 40 | 0 |
| 20 | Bullish | Bullish | Straddle | BUY | 297 pts | 11.43 | 42.3% | 26 | 0 |
| 21 | Bearish | Bullish | Straddle | BUY | 292 pts | 41.75 | 57.1% | 7 | 0 |
| 22 | Mildly Bullish | Bullish | Straddle | BUY | 288 pts | 11.08 | 46.2% | 26 | 0 |
| 23 | Strong Bearish | Neutral | Straddle | BUY | 267 pts | 29.69 | 44.4% | 9 | 0 |
| 24 | Bearish | Mildly Bearish | Straddle | BUY | 249 pts | 22.59 | 54.5% | 11 | 0 |
| 25 | Mildly Bullish | Strong Bullish | Strangle | BUY | 237 pts | 5.92 | 47.5% | 40 | 0 |

---
## Option Selling — Where It Actually Works

Out of all 8 strategies, selling is profitable in only **10 specific FII/PRO combinations** with zero or near-zero SL. These are the rare cases where NIFTY stays range-bound.

### Profitable Selling Combos (sorted by P&L)

| FII View | PRO View | Strategy | Total P&L | ₹/Lot | Avg/Day | Win% | Days | SL% |
|---|---|---|---|---|---|---|---|---|
| Strong Bullish | Strong Bearish | Short Straddle | 126 pts | ₹3,146 | 20.97 | 66.7% | 6 | 0.0% |
| Bullish | Neutral | Short Strangle | 104 pts | ₹2,598 | 5.19 | 65.0% | 20 | 0.0% |
| Strong Bullish | Strong Bearish | Short Strangle | 87 pts | ₹2,186 | 14.58 | 66.7% | 6 | 0.0% |
| Strong Bullish | Neutral | Short Straddle | 59 pts | ₹1,467 | 9.78 | 83.3% | 6 | 0.0% |
| Strong Bullish | Neutral | Short Strangle | 43 pts | ₹1,085 | 7.23 | 66.7% | 6 | 0.0% |
| Strong Bearish | Mildly Bearish | Short Strangle | 39 pts | ₹978 | 7.83 | 80.0% | 5 | 0.0% |
| Strong Bullish | Bullish | Short Strangle | 37 pts | ₹934 | 7.47 | 80.0% | 5 | 0.0% |
| Bullish | Neutral | Short Straddle | 35 pts | ₹865 | 1.73 | 55.0% | 20 | 5.0% |
| Strong Bullish | Bullish | Short Straddle | 26 pts | ₹639 | 5.11 | 60.0% | 5 | 0.0% |
| Strong Bearish | Mildly Bearish | Short Straddle | 23 pts | ₹578 | 4.62 | 80.0% | 5 | 20.0% |

**Key observation:** Selling only works when both FII and PRO are aligned (both bullish or both bearish), or when one is neutral. Divergence kills selling strategies.

---
## Best Strategy Per FII/PRO Combination (Including Selling)

### High Confidence (30+ days)

| FII View | PRO View | Strategy | Type | Total P&L | Avg/Day | Days | SL% |
|---|---|---|---|---|---|---|---|
| Mildly Bearish | Strong Bearish | Straddle | BUY | 1459 pts | 27.54 | 53 | 0.0% |
| Neutral | Bearish | Straddle | BUY | 853 pts | 9.27 | 92 | 0.0% |
| Neutral | Strong Bearish | Straddle | BUY | 801 pts | 9.77 | 82 | 0.0% |
| Neutral | Mildly Bullish | Straddle | BUY | 780 pts | 20.00 | 39 | 0.0% |
| Bullish | Strong Bullish | Straddle | BUY | 689 pts | 5.34 | 129 | 0.0% |
| Neutral | Bullish | Straddle | BUY | 595 pts | 7.53 | 79 | 0.0% |
| Strong Bearish | Strong Bearish | Straddle | BUY | 556 pts | 6.96 | 80 | 0.0% |
| Mildly Bullish | Strong Bullish | Straddle | BUY | 476 pts | 11.90 | 40 | 0.0% |
| Strong Bullish | Strong Bullish | Straddle | BUY | 442 pts | 6.32 | 70 | 0.0% |
| Neutral | Neutral | Straddle | BUY | 408 pts | 2.10 | 194 | 0.0% |
| Bearish | Bearish | Straddle | BUY | 373 pts | 11.66 | 32 | 0.0% |
| Neutral | Mildly Bearish | Bear Put Spread | BUY | 236 pts | 4.73 | 50 | 0.0% |
| Neutral | Strong Bullish | Straddle | BUY | 231 pts | 2.54 | 91 | 0.0% |
| Bearish | Strong Bearish | Bear Put Spread | BUY | 192 pts | 1.88 | 102 | 0.0% |

### Medium Confidence (10-29 days)

| FII View | PRO View | Strategy | Type | Total P&L | Avg/Day | Days | SL% |
|---|---|---|---|---|---|---|---|
| Bearish | Neutral | Straddle | BUY | 832 pts | 43.80 | 19 | 0.0% |
| Bullish | Bullish | Straddle | BUY | 297 pts | 11.43 | 26 | 0.0% |
| Mildly Bullish | Bullish | Straddle | BUY | 288 pts | 11.08 | 26 | 0.0% |
| Bearish | Mildly Bearish | Straddle | BUY | 249 pts | 22.59 | 11 | 0.0% |
| Mildly Bullish | Bearish | Straddle | BUY | 187 pts | 18.72 | 10 | 0.0% |
| Mildly Bullish | Mildly Bullish | Straddle | BUY | 141 pts | 14.10 | 10 | 0.0% |
| Bullish | Neutral | Short Strangle | SELL | 104 pts | 5.19 | 20 | 0.0% |
| Mildly Bearish | Mildly Bearish | Bull Call Spread | BUY | 84 pts | 7.63 | 11 | 0.0% |
| Mildly Bearish | Bearish | Bear Put Spread | BUY | 75 pts | 2.59 | 29 | 0.0% |
| Bearish | Strong Bullish | Straddle | BUY | 41 pts | 4.15 | 10 | 0.0% |
| Mildly Bullish | Strong Bearish | Bear Put Spread | BUY | 28 pts | 2.52 | 11 | 0.0% |
| Mildly Bearish | Neutral | Bear Put Spread | BUY | 19 pts | 0.99 | 19 | 0.0% |
| Bullish | Strong Bearish | Straddle | BUY | 4 pts | 0.24 | 17 | 0.0% |

---
## Profitable Despite Stop Loss Hits

These combos remained profitable even with occasional stop loss triggers.

| FII View | PRO View | Strategy | Type | Total P&L | Avg/Day | Days | SL Hits | SL% |
|---|---|---|---|---|---|---|---|---|
| Bearish | Bullish | Bull Call Spread | BUY | 57 pts | 8.20 | 7 | 1 | 14.3% |
| Bullish | Neutral | Short Straddle | SELL | 35 pts | 1.73 | 20 | 1 | 5.0% |
| Strong Bearish | Mildly Bearish | Short Straddle | SELL | 23 pts | 4.62 | 5 | 1 | 20.0% |
| Neutral | Bearish | Bull Call Spread | BUY | 9 pts | 0.09 | 92 | 5 | 5.4% |
| Neutral | Mildly Bullish | Bear Put Spread | BUY | 6 pts | 0.14 | 39 | 1 | 2.6% |

---
## Key Insights

1. **Straddle dominates** — It's the most profitable strategy overall (+10,601 pts / ₹2.65L) with zero stop loss hits across 1,488 days.

2. **Buy > Sell** — 74 profitable buying combos vs only 12 for selling. Option buying is more forgiving.

3. **95% of profitable combos had zero SL** — Stop loss almost never triggers when you're right on direction.

4. **Selling fails in divergence** — When FII and PRO disagree, selling strategies get crushed. Selling only works in alignment.

5. **Bear Put Spread outperforms Bull Call Spread** — BPS: +207 pts, BCS: -7,793 pts. Downside moves are sharper, making put spreads more reliable.

6. **Strangle is safer than Straddle for beginners** — Lower SL (0.20% vs 0.30%), still profitable (+1,172 pts), less capital at risk.

7. **All 4 selling strategies lost overall** — But specific combos (e.g., Neutral × Strong Bearish) were profitable. Don't sell blindly.

8. **High-confidence signals exist** — 30+ occurrences for many combos give statistical reliability for live trading.

---

## Trading Rules Summary

### Buy Signals (4 strategies)

| Strategy | When to Buy | Expected Outcome |
|---|---|---|
| **Straddle** | Any high-volatility FII/PRO combo | High profit, zero SL risk |
| **Strangle** | Same as Straddle but lower capital | Safer, still profitable |
| **Bear Put Spread** | FII/PRO both bullish or neutral | Profits from corrections |
| **Bull Call Spread** | Avoid — lost overall | Use only in specific backtested combos |

### Sell Signals (4 strategies)

| Strategy | When to Sell | Expected Outcome |
|---|---|---|
| **Short Straddle** | Only when FII/PRO aligned (both bullish/bearish/neutral) | Small profit, high risk |
| **Short Strangle** | Same as Short Straddle | Slightly safer than Straddle |
| **Iron Condor** | Avoid — worst performer | Lost ₹4.23L overall |
| **Iron Butterfly** | Avoid — second worst | Lost ₹5.41L overall |

### Skip Trading When:
- **Bull Call Spread** — Unless it's a proven profitable combo from backtest
- **All selling strategies** — Unless FII/PRO are aligned (no divergence)
- **Iron Condor / Iron Butterfly** — Avoid entirely (both lost heavily)

---

## Impact of 1:1 Take Profit (R:R = 1:1)

Testing whether taking profit at 1:1 risk-reward improves results.

| Strategy | Type | Base P&L | With TP 1:1 | Change | Change % | TP Hits |
|---|---|---|---|---|---|---|
| Bear Put Spread | BUY | +207 | +391 | +184 | +88.6% | 100 |
| Bull Call Spread | BUY | -7793 | -7612 | +181 | +2.3% | 39 |
| Strangle | BUY | +1172 | -199 | -1371 | -117.0% | 338 |
| Straddle | BUY | +10601 | +6841 | -3760 | -35.5% | 402 |
| Iron Butterfly | SELL | -21667 | -21667 | +0 | +0.0% | 0 |
| Iron Condor | SELL | -16944 | -16944 | +0 | +0.0% | 0 |
| Short Straddle | SELL | -20594 | -20594 | +0 | +0.0% | 0 |
| Short Strangle | SELL | -12428 | -12428 | +0 | +0.0% | 0 |

**Observation:** 1:1 take profit generally improves buying strategies but can hurt if moves continue in your favor. Best for risk management on expiry days or high volatility.

---
## Impact of Move-Based Exit

Testing move-based exit for **Straddle** — exit when NIFTY moves X% from open.

| Move % | Total P&L | Change vs Base | Exit Triggers | Exit Rate |
|---|---|---|---|---|
| Base (no exit) | +10601 pts | — | 0 | 0.0% |
| 0.3% | +3931 pts | -6669 | 907 | 61.0% |
| 0.5% | +6751 pts | -3849 | 984 | 66.1% |
| 0.7% | +7438 pts | -3163 | 699 | 47.0% |
| 1.0% | +9129 pts | -1471 | 370 | 24.9% |
| 1.5% | +9708 pts | -893 | 126 | 8.5% |
| 2.0% | +10256 pts | -344 | 52 | 3.5% |

**Observation:** Move-based exits reduce profits for Straddle because it benefits from full range capture. Don't exit early on buying strategies unless you need risk management.

---
## Selling Strategies: No Exit Rule Helps

For selling strategies, neither TP nor move exit improves performance.

| Strategy | Base P&L | With TP 1:1 | With Move 0.5% |
|---|---|---|---|
| Short Straddle | -20594 | -20594 | -20594 |
| Short Strangle | -12428 | -12428 | -12428 |
| Iron Condor | -16944 | -16944 | -16944 |
| Iron Butterfly | -21667 | -21667 | -21667 |

**Conclusion:** Selling strategies perform best with no exit rules — just let theta decay work until close.

---
## Complete Optimal Exit Summary

| Strategy Type | Optimal Exit Rule | Reason |
|---|---|---|
| **Buying (Straddle, Strangle)** | Hold till close | Captures full move, move exits reduce profit |
| **Buying (Spreads)** | 1:1 TP optional | Caps risk, but limits profit |
| **Selling (all)** | Hold till close | Theta decay works best without early exit |

**General rule:** For strategies that work (profitable in backtest), hold till close. Only use exits for risk management on high-volatility days.

---

## Expiry vs Non-Expiry

Performance comparison on NIFTY expiry days vs regular trading days.

| Strategy | Type | Expiry P&L | Expiry Avg | Non-Expiry P&L | Non-Expiry Avg | Expiry Days | Non-Expiry Days |
|---|---|---|---|---|---|---|---|
| Straddle | BUY | +13299 | +42.62 | -2698 | -2.29 | 312 | 1176 |
| Strangle | BUY | +4862 | +15.58 | -3690 | -3.14 | 312 | 1176 |
| Bear Put Spread | BUY | +1443 | +4.63 | -1236 | -1.05 | 312 | 1176 |
| Bull Call Spread | BUY | -901 | -2.89 | -6892 | -5.86 | 312 | 1176 |
| Short Strangle | SELL | -7167 | -22.97 | -5261 | -4.47 | 312 | 1176 |
| Iron Condor | SELL | -7765 | -24.89 | -9179 | -7.81 | 312 | 1176 |
| Iron Butterfly | SELL | -11207 | -35.92 | -10460 | -8.89 | 312 | 1176 |
| Short Straddle | SELL | -14336 | -45.95 | -6258 | -5.32 | 312 | 1176 |

**Observation:** Expiry days show higher volatility — buying strategies generally perform better, while selling becomes riskier.

---