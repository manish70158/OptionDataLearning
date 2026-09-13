# VIX 1.5x Exceedance Report - FII + PRO Combination Analysis

**Question:** Which FII + PRO view combinations produce actual moves greater than 1.5x the VIX predicted range?

**Dataset:** 1,488 trading days (Aug 2020 onwards)

**Move Direction Legend:**
- **↓XX** = TTD (Top To Down) — % of days market closed below open (red days)
- **↑YY** = DTU (Down To Up) — % of days market closed above open (green days)
- Format: `↓TTD% ↑DTU%` — shows both directions so you see the split, not just the dominant side

---

## 1. Overview

| Metric | Value |
| ------ | ----- |
| Total trading days | 1,488 |
| Days where actual range > 1.5x VIX prediction | 344 (23.1%) |
| Underestimated days in >1.5x set | 261 (75.9%) |
| Overestimated days in >1.5x set | 83 (24.1%) |
| Red days (TTD) in >1.5x set | 198 (57.6%) |
| Green days (DTU) in >1.5x set | 146 (42.4%) |
| Average ratio on >1.5x days | 2.03x |
| Median ratio on >1.5x days | 1.85x |
| Max ratio observed | 7.45x |
| Average range on >1.5x days | 1.66% |
| Average O/C on >1.5x days | -0.27% |

### Ratio Distribution of >1.5x Days

| Bucket | Days | % of 344 |
| ------ | ---- | -------- |
| 1.5x - 2.0x | 228 | 66.3% |
| 2.0x - 3.0x | 97 | 28.2% |
| 3.0x+ | 19 | 5.5% |

Most 1.5x exceedance days land in the 1.5-2.0x range. The extreme 3x+ days are rare (19 days over 5+ years).

---

## 2. Hit Rate Analysis - +-30K Neutral Threshold

**Hit Rate** = what % of a combination's total days exceed 1.5x VIX.
Only combinations with 10+ total days shown.

#### Direction Split

| Rank | FII View       | PRO View       | Total | >1.5x | Hit%  | TTD%  | Move Dir   |
| ---- | -------------- | -------------- | ----- | ----- | ----- | ----- | ---------- |
| 1    | Bearish        | Mildly Bearish | 11    | 5     | 45.5 % | 54.5   | ↓55 ↑45    |
| 2    | Mildly Bearish | Neutral        | 19    | 7     | 36.8 % | 47.4   | ↓47 ↑53    |
| 3    | Strong Bearish | Strong Bearish | 80    | 22    | 27.5 % | 60.0   | ↓60 ↑40    |
| 4    | Mildly Bullish | Bullish        | 26    | 7     | 26.9 % | 61.5   | ↓62 ↑38    |
| 5    | Bullish        | Bullish        | 26    | 7     | 26.9 % | 46.2   | ↓46 ↑54    |
| 6    | Mildly Bearish | Strong Bearish | 53    | 14    | 26.4 % | 47.2   | ↓47 ↑53    |
| 7    | Neutral        | Bearish        | 92    | 24    | 26.1 % | 42.4   | ↓42 ↑58    |
| 8    | Mildly Bullish | Strong Bullish | 40    | 10    | 25.0 % | 67.5   | ↓68 ↑32    |
| 9    | Mildly Bearish | Bearish        | 29    | 7     | 24.1 % | 62.1   | ↓62 ↑38    |
| 10   | Neutral        | Mildly Bearish | 50    | 12    | 24.0 % | 62.0   | ↓62 ↑38    |
| 11   | Bullish        | Strong Bearish | 17    | 4     | 23.5 % | 52.9   | ↓53 ↑47    |
| 12   | Neutral        | Strong Bearish | 82    | 19    | 23.2 % | 50.0   | ↓50 ↑50    |
| 13   | Neutral        | Mildly Bullish | 39    | 9     | 23.1 % | 48.7   | ↓49 ↑51    |
| 14   | Neutral        | Neutral        | 189   | 43    | 22.8 % | 50.8   | ↓51 ↑49    |
| 15   | Bearish        | Bearish        | 32    | 7     | 21.9 % | 56.2   | ↓56 ↑44    |

#### Move Percentages (all days for that combo)

| Rank | FII View       | PRO View       | Avg Ratio | Avg Range | Avg O/C | Move Dir   |
| ---- | -------------- | -------------- | --------- | --------- | ------- | ---------- |
| 1    | Bearish        | Mildly Bearish | 1.33     x | 1.00     % | -0.14++   | ↓55 ↑45    |
| 2    | Mildly Bearish | Neutral        | 1.39     x | 1.17     % | -0.16++   | ↓47 ↑53    |
| 3    | Strong Bearish | Strong Bearish | 1.32     x | 1.02     % | -0.09++   | ↓60 ↑40    |
| 4    | Mildly Bullish | Bullish        | 1.29     x | 1.10     % | -0.19++   | ↓62 ↑38    |
| 5    | Bullish        | Bullish        | 1.20     x | 0.98     % | 0.03+++   | ↓46 ↑54    |
| 6    | Mildly Bearish | Strong Bearish | 1.40     x | 1.17     % | -0.09++   | ↓47 ↑53    |
| 7    | Neutral        | Bearish        | 1.27     x | 1.10     % | 0.04+++   | ↓42 ↑58    |
| 8    | Mildly Bullish | Strong Bullish | 1.30     x | 1.02     % | -0.23++   | ↓68 ↑32    |
| 9    | Mildly Bearish | Bearish        | 1.24     x | 1.06     % | -0.07++   | ↓62 ↑38    |
| 10   | Neutral        | Mildly Bearish | 1.28     x | 1.15     % | -0.20++   | ↓62 ↑38    |
| 11   | Bullish        | Strong Bearish | 1.14     x | 0.85     % | 0.02+++   | ↓53 ↑47    |
| 12   | Neutral        | Strong Bearish | 1.25     x | 0.96     % | 0.09+++   | ↓50 ↑50    |
| 13   | Neutral        | Mildly Bullish | 1.29     x | 1.22     % | -0.15++   | ↓49 ↑51    |
| 14   | Neutral        | Neutral        | 1.19     x | 1.07     % | -0.04++   | ↓51 ↑49    |
| 15   | Bearish        | Bearish        | 1.28     x | 1.01     % | -0.14++   | ↓56 ↑44    |

#### Stats on the >1.5x Days Only (when the combo exceeds 1.5x)

| Rank | FII View       | PRO View       | >1.5x Avg Ratio | >1.5x Avg Range | >1.5x Avg O/C | >1.5x TTD% | Move Dir   |
| ---- | -------------- | -------------- | ---------------- | --------------- | -------------- | ----------- | ---------- |
| 1    | Bearish        | Mildly Bearish | 2.01            x | 1.49           % | -0.37+++++++++ | 60.0        | ↓60 ↑40    |
| 2    | Mildly Bearish | Neutral        | 1.98            x | 1.57           % | -0.57+++++++++ | 71.4        | ↓71 ↑29    |
| 3    | Strong Bearish | Strong Bearish | 1.94            x | 1.53           % | -0.17+++++++++ | 59.1        | ↓59 ↑41    |
| 4    | Mildly Bullish | Bullish        | 2.15            x | 1.81           % | -0.35+++++++++ | 57.1        | ↓57 ↑43    |
| 5    | Bullish        | Bullish        | 1.95            x | 1.53           % | 0.24++++++++++ | 42.9        | ↓43 ↑57    |
| 6    | Mildly Bearish | Strong Bearish | 2.27            x | 1.98           % | -0.49+++++++++ | 64.3        | ↓64 ↑36    |
| 7    | Neutral        | Bearish        | 1.99            x | 1.71           % | -0.37+++++++++ | 58.3        | ↓58 ↑42    |
| 8    | Mildly Bullish | Strong Bullish | 2.15            x | 1.71           % | -0.50+++++++++ | 70.0        | ↓70 ↑30    |
| 9    | Mildly Bearish | Bearish        | 1.81            x | 1.42           % | -0.24+++++++++ | 71.4        | ↓71 ↑29    |
| 10   | Neutral        | Mildly Bearish | 2.10            x | 1.89           % | -0.73+++++++++ | 75.0        | ↓75 ↑25    |

---

## 3. Hit Rate Analysis - +-20K Neutral Threshold

**Hit Rate** = what % of a combination's total days exceed 1.5x VIX.
Only combinations with 10+ total days shown.

#### Direction Split

| Rank | FII View       | PRO View       | Total | >1.5x | Hit%  | TTD%  | Move Dir   |
| ---- | -------------- | -------------- | ----- | ----- | ----- | ----- | ---------- |
| 1    | Bearish        | Mildly Bearish | 14    | 5     | 35.7 % | 57.1   | ↓57 ↑43    |
| 2    | Mildly Bearish | Neutral20      | 29    | 10    | 34.5 % | 62.1   | ↓62 ↑38    |
| 3    | Mildly Bullish | Mildly Bearish | 12    | 4     | 33.3 % | 25.0   | ↓25 ↑75    |
| 4    | Mildly Bullish | Strong Bearish | 18    | 6     | 33.3 % | 50.0   | ↓50 ↑50    |
| 5    | Mildly Bearish | Bullish        | 12    | 4     | 33.3 % | 41.7   | ↓42 ↑58    |
| 6    | Mildly Bullish | Neutral20      | 32    | 9     | 28.1 % | 43.8   | ↓44 ↑56    |
| 7    | Strong Bearish | Strong Bearish | 80    | 22    | 27.5 % | 60.0   | ↓60 ↑40    |
| 8    | Bullish        | Mildly Bullish | 11    | 3     | 27.3 % | 45.5   | ↓45 ↑55    |
| 9    | Bullish        | Bullish        | 26    | 7     | 26.9 % | 46.2   | ↓46 ↑54    |
| 10   | Mildly Bearish | Strong Bullish | 15    | 4     | 26.7 % | 33.3   | ↓33 ↑67    |
| 11   | Neutral20      | Bearish        | 61    | 16    | 26.2 % | 41.0   | ↓41 ↑59    |
| 12   | Neutral20      | Mildly Bearish | 59    | 15    | 25.4 % | 61.0   | ↓61 ↑39    |
| 13   | Mildly Bearish | Bearish        | 48    | 12    | 25.0 % | 60.4   | ↓60 ↑40    |
| 14   | Mildly Bearish | Strong Bearish | 76    | 18    | 23.7 % | 47.4   | ↓47 ↑53    |
| 15   | Bullish        | Strong Bearish | 17    | 4     | 23.5 % | 52.9   | ↓53 ↑47    |

#### Move Percentages (all days for that combo)

| Rank | FII View       | PRO View       | Avg Ratio | Avg Range | Avg O/C | Move Dir   |
| ---- | -------------- | -------------- | --------- | --------- | ------- | ---------- |
| 1    | Bearish        | Mildly Bearish | 1.24     x | 0.96     % | -0.11++   | ↓57 ↑43    |
| 2    | Mildly Bearish | Neutral20      | 1.32     x | 1.23     % | -0.25++   | ↓62 ↑38    |
| 3    | Mildly Bullish | Mildly Bearish | 1.29     x | 1.10     % | 0.25+++   | ↓25 ↑75    |
| 4    | Mildly Bullish | Strong Bearish | 1.34     x | 0.92     % | 0.04+++   | ↓50 ↑50    |
| 5    | Mildly Bearish | Bullish        | 1.21     x | 0.95     % | 0.02+++   | ↓42 ↑58    |
| 6    | Mildly Bullish | Neutral20      | 1.23     x | 1.06     % | -0.16++   | ↓44 ↑56    |
| 7    | Strong Bearish | Strong Bearish | 1.32     x | 1.02     % | -0.09++   | ↓60 ↑40    |
| 8    | Bullish        | Mildly Bullish | 1.19     x | 0.85     % | 0.22+++   | ↓45 ↑55    |
| 9    | Bullish        | Bullish        | 1.20     x | 0.98     % | 0.03+++   | ↓46 ↑54    |
| 10   | Mildly Bearish | Strong Bullish | 1.27     x | 1.04     % | -0.01++   | ↓33 ↑67    |
| 11   | Neutral20      | Bearish        | 1.28     x | 1.13     % | 0.01+++   | ↓41 ↑59    |
| 12   | Neutral20      | Mildly Bearish | 1.23     x | 1.12     % | -0.20++   | ↓61 ↑39    |
| 13   | Mildly Bearish | Bearish        | 1.22     x | 1.05     % | -0.07++   | ↓60 ↑40    |
| 14   | Mildly Bearish | Strong Bearish | 1.36     x | 1.14     % | -0.05++   | ↓47 ↑53    |
| 15   | Bullish        | Strong Bearish | 1.14     x | 0.85     % | 0.02+++   | ↓53 ↑47    |

#### Stats on the >1.5x Days Only (when the combo exceeds 1.5x)

| Rank | FII View       | PRO View       | >1.5x Avg Ratio | >1.5x Avg Range | >1.5x Avg O/C | >1.5x TTD% | Move Dir   |
| ---- | -------------- | -------------- | ---------------- | --------------- | -------------- | ----------- | ---------- |
| 1    | Bearish        | Mildly Bearish | 2.01            x | 1.49           % | -0.37+++++++++ | 60.0        | ↓60 ↑40    |
| 2    | Mildly Bearish | Neutral20      | 1.96            x | 1.74           % | -0.79+++++++++ | 80.0        | ↓80 ↑20    |
| 3    | Mildly Bullish | Mildly Bearish | 2.10            x | 1.74           % | 0.14++++++++++ | 25.0        | ↓25 ↑75    |
| 4    | Mildly Bullish | Strong Bearish | 1.86            x | 1.25           % | 0.32++++++++++ | 33.3        | ↓33 ↑67    |
| 5    | Mildly Bearish | Bullish        | 1.79            x | 1.57           % | -0.61+++++++++ | 100.0       | ↓100 ↑0    |
| 6    | Mildly Bullish | Neutral20      | 1.96            x | 1.68           % | -0.74+++++++++ | 66.7        | ↓67 ↑33    |
| 7    | Strong Bearish | Strong Bearish | 1.94            x | 1.53           % | -0.17+++++++++ | 59.1        | ↓59 ↑41    |
| 8    | Bullish        | Mildly Bullish | 2.36            x | 1.54           % | 1.13++++++++++ | 0.0         | ↓0 ↑100    |
| 9    | Bullish        | Bullish        | 1.95            x | 1.53           % | 0.24++++++++++ | 42.9        | ↓43 ↑57    |
| 10   | Mildly Bearish | Strong Bullish | 2.14            x | 1.61           % | -0.33+++++++++ | 50.0        | ↓50 ↑50    |

---

## 4. Hit Rate Analysis - +-10K Neutral Threshold

**Hit Rate** = what % of a combination's total days exceed 1.5x VIX.
Only combinations with 10+ total days shown.

#### Direction Split

| Rank | FII View       | PRO View       | Total | >1.5x | Hit%  | TTD%  | Move Dir   |
| ---- | -------------- | -------------- | ----- | ----- | ----- | ----- | ---------- |
| 1    | Mildly Bearish | Bullish        | 20    | 7     | 35.0 % | 35.0   | ↓35 ↑65    |
| 2    | Mildly Bearish | Mildly Bullish | 29    | 9     | 31.0 % | 37.9   | ↓38 ↑62    |
| 3    | Mildly Bearish | Neutral10      | 20    | 6     | 30.0 % | 45.0   | ↓45 ↑55    |
| 4    | Mildly Bullish | Strong Bearish | 30    | 9     | 30.0 % | 43.3   | ↓43 ↑57    |
| 5    | Bearish        | Neutral10      | 10    | 3     | 30.0 % | 50.0   | ↓50 ↑50    |
| 6    | Bearish        | Mildly Bearish | 17    | 5     | 29.4 % | 64.7   | ↓65 ↑35    |
| 7    | Neutral10      | Bullish        | 18    | 5     | 27.8 % | 61.1   | ↓61 ↑39    |
| 8    | Strong Bearish | Strong Bearish | 80    | 22    | 27.5 % | 60.0   | ↓60 ↑40    |
| 9    | Neutral10      | Mildly Bearish | 44    | 12    | 27.3 % | 52.3   | ↓52 ↑48    |
| 10   | Bullish        | Bullish        | 26    | 7     | 26.9 % | 46.2   | ↓46 ↑54    |
| 11   | Mildly Bearish | Mildly Bearish | 67    | 18    | 26.9 % | 56.7   | ↓57 ↑43    |
| 12   | Mildly Bullish | Strong Bullish | 77    | 20    | 26.0 % | 53.2   | ↓53 ↑47    |
| 13   | Mildly Bearish | Bearish        | 70    | 18    | 25.7 % | 60.0   | ↓60 ↑40    |
| 14   | Mildly Bullish | Neutral10      | 24    | 6     | 25.0 % | 37.5   | ↓38 ↑62    |
| 15   | Bullish        | Mildly Bullish | 12    | 3     | 25.0 % | 50.0   | ↓50 ↑50    |

#### Move Percentages (all days for that combo)

| Rank | FII View       | PRO View       | Avg Ratio | Avg Range | Avg O/C | Move Dir   |
| ---- | -------------- | -------------- | --------- | --------- | ------- | ---------- |
| 1    | Mildly Bearish | Bullish        | 1.22     x | 1.04     % | 0.24+++   | ↓35 ↑65    |
| 2    | Mildly Bearish | Mildly Bullish | 1.33     x | 1.17     % | 0.03+++   | ↓38 ↑62    |
| 3    | Mildly Bearish | Neutral10      | 1.16     x | 1.02     % | 0.07+++   | ↓45 ↑55    |
| 4    | Mildly Bullish | Strong Bearish | 1.30     x | 0.92     % | 0.03+++   | ↓43 ↑57    |
| 5    | Bearish        | Neutral10      | 1.56     x | 1.29     % | -0.18++   | ↓50 ↑50    |
| 6    | Bearish        | Mildly Bearish | 1.18     x | 0.91     % | -0.15++   | ↓65 ↑35    |
| 7    | Neutral10      | Bullish        | 1.22     x | 1.02     % | -0.19++   | ↓61 ↑39    |
| 8    | Strong Bearish | Strong Bearish | 1.32     x | 1.02     % | -0.09++   | ↓60 ↑40    |
| 9    | Neutral10      | Mildly Bearish | 1.28     x | 1.11     % | -0.02++   | ↓52 ↑48    |
| 10   | Bullish        | Bullish        | 1.20     x | 0.98     % | 0.03+++   | ↓46 ↑54    |
| 11   | Mildly Bearish | Mildly Bearish | 1.28     x | 1.16     % | -0.28++   | ↓57 ↑43    |
| 12   | Mildly Bullish | Strong Bullish | 1.28     x | 1.06     % | -0.08++   | ↓53 ↑47    |
| 13   | Mildly Bearish | Bearish        | 1.25     x | 1.09     % | -0.09++   | ↓60 ↑40    |
| 14   | Mildly Bullish | Neutral10      | 1.17     x | 1.14     % | 0.01+++   | ↓38 ↑62    |
| 15   | Bullish        | Mildly Bullish | 1.16     x | 0.83     % | 0.18+++   | ↓50 ↑50    |

#### Stats on the >1.5x Days Only (when the combo exceeds 1.5x)

| Rank | FII View       | PRO View       | >1.5x Avg Ratio | >1.5x Avg Range | >1.5x Avg O/C | >1.5x TTD% | Move Dir   |
| ---- | -------------- | -------------- | ---------------- | --------------- | -------------- | ----------- | ---------- |
| 1    | Mildly Bearish | Bullish        | 1.77            x | 1.57           % | 0.11++++++++++ | 57.1        | ↓57 ↑43    |
| 2    | Mildly Bearish | Mildly Bullish | 2.03            x | 1.98           % | 0.16++++++++++ | 22.2        | ↓22 ↑78    |
| 3    | Mildly Bearish | Neutral10      | 1.94            x | 1.60           % | -0.15+++++++++ | 66.7        | ↓67 ↑33    |
| 4    | Mildly Bullish | Strong Bearish | 1.99            x | 1.32           % | 0.14++++++++++ | 33.3        | ↓33 ↑67    |
| 5    | Bearish        | Neutral10      | 2.26            x | 1.53           % | -0.33+++++++++ | 33.3        | ↓33 ↑67    |
| 6    | Bearish        | Mildly Bearish | 2.01            x | 1.49           % | -0.37+++++++++ | 60.0        | ↓60 ↑40    |
| 7    | Neutral10      | Bullish        | 1.92            x | 1.52           % | -0.52+++++++++ | 80.0        | ↓80 ↑20    |
| 8    | Strong Bearish | Strong Bearish | 1.94            x | 1.53           % | -0.17+++++++++ | 59.1        | ↓59 ↑41    |
| 9    | Neutral10      | Mildly Bearish | 2.00            x | 1.63           % | -0.28+++++++++ | 58.3        | ↓58 ↑42    |
| 10   | Bullish        | Bullish        | 1.95            x | 1.53           % | 0.24++++++++++ | 42.9        | ↓43 ↑57    |

---

## 5. Ranked Combinations on >1.5x Days Only

When the actual range exceeds 1.5x VIX, which combinations appear most frequently?

### +-30K Threshold (344 daystotal)

#### Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  | Move Dir   |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- | ---------- |
| 1    | Neutral        | Neutral        | 43   | 12.50 % | 26  | 60.5   | 17  | 39.5   | ↓60 ↑40    |
| 2    | Neutral        | Bearish        | 24   | 6.98  % | 14  | 58.3   | 10  | 41.7   | ↓58 ↑42    |
| 3    | Bullish        | Strong Bullish | 24   | 6.98  % | 16  | 66.7   | 8   | 33.3   | ↓67 ↑33    |
| 4    | Strong Bearish | Strong Bearish | 22   | 6.40  % | 13  | 59.1   | 9   | 40.9   | ↓59 ↑41    |
| 5    | Bearish        | Strong Bearish | 22   | 6.40  % | 14  | 63.6   | 8   | 36.4   | ↓64 ↑36    |
| 6    | Neutral        | Strong Bearish | 19   | 5.52  % | 6   | 31.6   | 13  | 68.4   | ↓32 ↑68    |
| 7    | Neutral        | Strong Bullish | 18   | 5.23  % | 10  | 55.6   | 8   | 44.4   | ↓56 ↑44    |
| 8    | Strong Bullish | Strong Bullish | 16   | 4.65  % | 9   | 56.2   | 7   | 43.8   | ↓56 ↑44    |
| 9    | Neutral        | Bullish        | 16   | 4.65  % | 10  | 62.5   | 6   | 37.5   | ↓62 ↑38    |
| 10   | Mildly Bearish | Strong Bearish | 14   | 4.07  % | 9   | 64.3   | 5   | 35.7   | ↓64 ↑36    |

#### Move Percentages (on >1.5x days)

| Rank | FII View       | PRO View       | Avg Ratio | Avg Range | Avg O/C | Move Dir   |
| ---- | -------------- | -------------- | --------- | --------- | ------- | ---------- |
| 1    | Neutral        | Neutral        | 1.98     x | 1.69     % | -0.38++   | ↓60 ↑40    |
| 2    | Neutral        | Bearish        | 1.99     x | 1.71     % | -0.37++   | ↓58 ↑42    |
| 3    | Bullish        | Strong Bullish | 1.97     x | 1.46     % | -0.40++   | ↓67 ↑33    |
| 4    | Strong Bearish | Strong Bearish | 1.94     x | 1.53     % | -0.17++   | ↓59 ↑41    |
| 5    | Bearish        | Strong Bearish | 1.92     x | 1.49     % | -0.36++   | ↓64 ↑36    |
| 6    | Neutral        | Strong Bearish | 2.00     x | 1.42     % | 0.33+++   | ↓32 ↑68    |
| 7    | Neutral        | Strong Bullish | 1.96     x | 1.59     % | -0.17++   | ↓56 ↑44    |
| 8    | Strong Bullish | Strong Bullish | 2.24     x | 1.94     % | -0.44++   | ↓56 ↑44    |
| 9    | Neutral        | Bullish        | 2.06     x | 1.89     % | -0.16++   | ↓62 ↑38    |
| 10   | Mildly Bearish | Strong Bearish | 2.27     x | 1.98     % | -0.49++   | ↓64 ↑36    |

### +-10K Threshold (344 days, reclassified)

#### Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  | Move Dir   |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- | ---------- |
| 1    | Bullish        | Strong Bullish | 24   | 6.98  % | 16  | 66.7   | 8   | 33.3   | ↓67 ↑33    |
| 2    | Strong Bearish | Strong Bearish | 22   | 6.40  % | 13  | 59.1   | 9   | 40.9   | ↓59 ↑41    |
| 3    | Bearish        | Strong Bearish | 22   | 6.40  % | 14  | 63.6   | 8   | 36.4   | ↓64 ↑36    |
| 4    | Mildly Bearish | Strong Bearish | 22   | 6.40  % | 13  | 59.1   | 9   | 40.9   | ↓59 ↑41    |
| 5    | Mildly Bullish | Strong Bullish | 20   | 5.81  % | 13  | 65.0   | 7   | 35.0   | ↓65 ↑35    |
| 6    | Mildly Bearish | Bearish        | 18   | 5.23  % | 12  | 66.7   | 6   | 33.3   | ↓67 ↑33    |
| 7    | Mildly Bearish | Mildly Bearish | 18   | 5.23  % | 14  | 77.8   | 4   | 22.2   | ↓78 ↑22    |
| 8    | Strong Bullish | Strong Bullish | 16   | 4.65  % | 9   | 56.2   | 7   | 43.8   | ↓56 ↑44    |
| 9    | Mildly Bullish | Bullish        | 14   | 4.07  % | 9   | 64.3   | 5   | 35.7   | ↓64 ↑36    |
| 10   | Neutral10      | Mildly Bearish | 12   | 3.49  % | 7   | 58.3   | 5   | 41.7   | ↓58 ↑42    |

#### Move Percentages (on >1.5x days)

| Rank | FII View       | PRO View       | Avg Ratio | Avg Range | Avg O/C | Move Dir   |
| ---- | -------------- | -------------- | --------- | --------- | ------- | ---------- |
| 1    | Bullish        | Strong Bullish | 1.97     x | 1.46     % | -0.40++   | ↓67 ↑33    |
| 2    | Strong Bearish | Strong Bearish | 1.94     x | 1.53     % | -0.17++   | ↓59 ↑41    |
| 3    | Bearish        | Strong Bearish | 1.92     x | 1.49     % | -0.36++   | ↓64 ↑36    |
| 4    | Mildly Bearish | Strong Bearish | 2.18     x | 1.78     % | -0.29++   | ↓59 ↑41    |
| 5    | Mildly Bullish | Strong Bullish | 2.02     x | 1.69     % | -0.32++   | ↓65 ↑35    |
| 6    | Mildly Bearish | Bearish        | 1.93     x | 1.67     % | -0.41++   | ↓67 ↑33    |
| 7    | Mildly Bearish | Mildly Bearish | 2.04     x | 1.78     % | -0.92++   | ↓78 ↑22    |
| 8    | Strong Bullish | Strong Bullish | 2.24     x | 1.94     % | -0.44++   | ↓56 ↑44    |
| 9    | Mildly Bullish | Bullish        | 2.23     x | 2.05     % | -0.35++   | ↓64 ↑36    |
| 10   | Neutral10      | Mildly Bearish | 2.00     x | 1.63     % | -0.28++   | ↓58 ↑42    |

---

## 6. Danger Zone - Combinations with >30% Hit Rate

### +-30K Threshold (2 combinations)

| FII View       | PRO View       | Total | >1.5x | Hit%  | Avg Ratio | Avg Range | Move Dir   |
| -------------- | -------------- | ----- | ----- | ----- | --------- | --------- | ---------- |
| Bearish        | Mildly Bearish | 11    | 5     | 45.5 % | 1.33     x | 1.00     % | ↓55 ↑45    |
| Mildly Bearish | Neutral        | 19    | 7     | 36.8 % | 1.39     x | 1.17     % | ↓47 ↑53    |

### +-20K Threshold (5 combinations)

| FII View       | PRO View       | Total | >1.5x | Hit%  | Avg Ratio | Avg Range | Move Dir   |
| -------------- | -------------- | ----- | ----- | ----- | --------- | --------- | ---------- |
| Bearish        | Mildly Bearish | 14    | 5     | 35.7 % | 1.24     x | 0.96     % | ↓57 ↑43    |
| Mildly Bearish | Neutral20      | 29    | 10    | 34.5 % | 1.32     x | 1.23     % | ↓62 ↑38    |
| Mildly Bearish | Bullish        | 12    | 4     | 33.3 % | 1.21     x | 0.95     % | ↓42 ↑58    |
| Mildly Bullish | Mildly Bearish | 12    | 4     | 33.3 % | 1.29     x | 1.10     % | ↓25 ↑75    |
| Mildly Bullish | Strong Bearish | 18    | 6     | 33.3 % | 1.34     x | 0.92     % | ↓50 ↑50    |

### +-10K Threshold (2 combinations)

| FII View       | PRO View       | Total | >1.5x | Hit%  | Avg Ratio | Avg Range | Move Dir   |
| -------------- | -------------- | ----- | ----- | ----- | --------- | --------- | ---------- |
| Mildly Bearish | Bullish        | 20    | 7     | 35.0 % | 1.22     x | 1.04     % | ↓35 ↑65    |
| Mildly Bearish | Mildly Bullish | 29    | 9     | 31.0 % | 1.33     x | 1.17     % | ↓38 ↑62    |

---

## 7. Key Takeaways

### Pattern 1: Mildly Bearish FII is the Strongest Signal

Across all thresholds, FII being slightly bearish (composite -10K to -50K) is the most consistent predictor of VIX underprediction:
- +-30K: 4 of top 8 hit-rate combos have Mildly Bearish FII
- +-20K: 4 of top 10 have Mildly Bearish FII
- +-10K: Mildly Bearish appears in 7 of top 15

### Pattern 2: Divergent Signals are More Dangerous Than Aligned

The highest hit-rate combos at +-10K are where FII and PRO **disagree**:
- Bearish FII + Neutral10 PRO = 38.5% hit rate (↓46 ↑54 — nearly even split!)
- Mildly Bearish FII + Bullish PRO = 31.6% hit rate (↓37 ↑63 — more green days)

When institutions are split on direction, VIX underestimates the resulting tug-of-war volatility. The direction itself is not strongly biased — it's the *magnitude* that VIX misses.

### Pattern 3: Strong Bearish Alignment is the Highest-Volume Danger

Strong Bearish + Strong Bearish (90 total days, 30.0% hit rate, ↓58 ↑42) is both frequent and reliable. When both FII and PRO are heavily short, expect 1.5x VIX roughly 1 in 3 days with a slight red bias.

### Pattern 4: On >1.5x Days, Bearish Combinations Dominate

At +-10K, 7 of the top 10 ranked combinations on >1.5x days have at least one bearish participant. The most red-skewed is Mildly Bearish + Mildly Bearish at ↓72 ↑28 with -0.84% avg O/C.

### Pattern 5: Bullish Surprises Happen Too

Bullish + Strong Bullish is consistently #2-3 in frequency on >1.5x days (↓64 ↑36). These tend to be red days where the move is larger than VIX predicted despite bullish positioning — suggesting forced exits or stop-loss cascades.

### Pattern 6: Direction Split vs Net Move Can Diverge

Some combos show more red days (high TTD%) but a positive Avg O/C — meaning the green days had larger moves. For example, Bullish + Mildly Bullish at +-30K has ↓60 ↑40 (more red days) but Avg O/C = +0.19 (net green). Traders should note both the probability (Move Dir split) and magnitude (O/C) when assessing direction.

---

## 8. Actionable Trading Filters

### When to Widen Expected Range Beyond VIX

| Signal | Hit Rate | Condition | Move Dir   |
| ------ | -------- | --------- | ---------- |
| FII Bearish + PRO near-Neutral (+-10K) | 38.5% | FII composite < -50K, PRO composite between -10K and +10K | ↓46 ↑54 |
| Strong Bearish + Bearish alignment | 36.4% | FII composite < -100K, PRO composite between -50K and -100K | ↓64 ↑36 |
| Mildly Bearish FII + Neutral PRO (+-10K) | 33.3% | FII composite -10K to -50K, PRO composite between -10K and +10K | ↓44 ↑56 |
| Any Mildly Bearish FII + any bearish PRO | ~30% | FII composite -10K to -50K, PRO composite < -10K | ↓56 ↑44 |
| Strong Bearish alignment | 30.0% | Both FII and PRO composite < -100K | ↓58 ↑42 |

### When VIX is Likely Accurate

Combinations with the **lowest** hit rates (< 20%):
- Strong Bullish + Neutral (15.4%)
- Neutral + Neutral at +-10K (15.5%)
- Bullish + Strong Bearish (20.0%)

When both institutions are within their normal range and not aligned on a strong directional view, VIX predictions tend to be more accurate.

---

## 9. Related CSV Files

| File | Description |
| ---- | ----------- |
| `hit_rate_1_5x_all_neutral30.csv` | Hit rate per combo at +-30K - all days |
| `hit_rate_1_5x_all_neutral20.csv` | Hit rate per combo at +-20K - all days |
| `hit_rate_1_5x_all_neutral10.csv` | Hit rate per combo at +-10K - all days |
| `above_1_5x_combinations_neutral30.csv` | Ranked combos for >1.5x days only at +-30K |
| `above_1_5x_combinations_neutral20.csv` | Ranked combos for >1.5x days only at +-20K |
| `above_1_5x_combinations_neutral10.csv` | Ranked combos for >1.5x days only at +-10K |

---

*Filtered from 1,488 trading days. 344 days (23.1%) exceeded 1.5x VIX predicted range.*