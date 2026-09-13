# VIX Wrong - FII + PRO View Dominance Analysis

**Dataset:** `vix_fii_t1_intraday_daily_results.csv`
**Period:** August 2020 onwards (1,488 trading days)
**Objective:** When VIX accuracy prediction is wrong, which FII + PRO view combinations dominate?

---

## 1. Data Overview

| Metric                                          | Value          |
| ----------------------------------------------- | -------------- |
| Total trading days                              | 1,488          |
| VIX Overestimated (calmer day than predicted)   | 1,210 (81.3%)  |
| VIX Underestimated (more volatile than predicted) | 278 (18.7%)  |
| Green (up) days                                 | 728 (48.9%)    |
| Red (down) days                                 | 760 (51.1%)    |
| Unique FII views                                | 7              |
| Unique PRO views                                | 7              |
| Possible FII+PRO combinations                   | 49             |

### View Definitions - Composite Score Ranges

The `fii_view` and `pro_view` are derived from a **composite score** that combines futures, call, and put daily positioning data. The composite score determines the view label based on the following ranges:

#### FII View (based on `fii_composite`)

| View             | Composite Range              | Meaning                       | Count | %     |
| ---------------- | ---------------------------- | ----------------------------- | ----- | ----- |
| Strong Bearish   | -4,44,137 to -1,00,277       | Heavy net selling across F&O  |   111 |  7.5% |
| Bearish          | -97,601 to -50,111           | Moderate net selling          |   184 | 12.4% |
| Mildly Bearish   | -49,674 to -30,122           | Slight net selling            |   130 |  8.7% |
| **Neutral**      | **-29,958 to 29,655**       | **No clear directional bias** | **622** | **41.8%** |
| Mildly Bullish   | 30,132 to 49,838             | Slight net buying             |   128 |  8.6% |
| Bullish          | 50,011 to 99,440             | Moderate net buying           |   211 | 14.2% |
| Strong Bullish   | 1,00,054 to 3,28,658         | Heavy net buying across F&O   |    97 |  6.5% |

#### PRO View (based on `pro_composite`)

| View             | Composite Range              | Meaning                       | Count | %     |
| ---------------- | ---------------------------- | ----------------------------- | ----- | ----- |
| Strong Bearish   | -7,69,958 to -1,00,003       | Heavy net selling across F&O  |   351 | 23.6% |
| Bearish          | -99,954 to -50,418           | Moderate net selling          |   179 | 12.0% |
| Mildly Bearish   | -49,503 to -30,038           | Slight net selling            |    89 |  6.0% |
| **Neutral**      | **-29,889 to 29,814**       | **No clear directional bias** | **290** | **19.5%** |
| Mildly Bullish   | 30,289 to 49,764             | Slight net buying             |    69 |  4.6% |
| Bullish          | 50,809 to 99,983             | Moderate net buying           |   153 | 10.3% |
| Strong Bullish   | 1,00,224 to 8,04,728         | Heavy net buying across F&O   |   352 | 23.7% |

#### Summary of Threshold Boundaries

| Boundary                     | FII        | PRO        |
| ---------------------------- | ---------- | ---------- |
| Strong Bearish / Bearish     | ~-1,00,000 | ~-1,00,000 |
| Bearish / Mildly Bearish     | ~-50,000   | ~-50,000   |
| Mildly Bearish / Neutral     | ~-30,000   | ~-30,000   |
| Neutral / Mildly Bullish     | ~+30,000   | ~+30,000   |
| Mildly Bullish / Bullish     | ~+50,000   | ~+50,000   |
| Bullish / Strong Bullish     | ~+1,00,000 | ~+1,00,000 |

> **Neutral means the composite score is between approximately -30,000 and +30,000** - neither institution has taken a meaningful net directional position in futures + options combined. This is the most frequent state for FII (41.8%) and second-most for PRO (19.5%).

> **Note on Neutral stance diversity:** Even within the "Neutral" view, the underlying `t1_fii_stance` / `t1_pro_stance` can show activity like "Hedging (bought puts >20K)" or "Confident (sold puts >20K)" - but the *net composite* across all F&O instruments remains within the -30K to +30K band, so the overall positioning is classified as non-directional.

---

## 2. VIX Overestimated - Top 15 FII+PRO Combinations

VIX predicted a larger move than what actually occurred - the day was calmer than expected.
1,210 days total, 48 non-zero combinations observed.

**Column Guide:**
- TTD = Top to Down (Red day) | DTU = Down to Up (Green day)
- Avg Range = average high-low range % | Avg O/C = average open-close %

#### Combination Counts and Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- |
|    1 | Neutral        | Neutral        |  155 | 12.81% |  77 |  49.7 |  78 |  50.3 |
|    2 | Bullish        | Strong Bullish |  111 |  9.17% |  67 |  60.4 |  44 |  39.6 |
|    3 | Bearish        | Strong Bearish |   83 |  6.86% |  44 |  53.0 |  39 |  47.0 |
|    4 | Neutral        | Strong Bullish |   79 |  6.53% |  35 |  44.3 |  44 |  55.7 |
|    5 | Neutral        | Bearish        |   73 |  6.03% |  28 |  38.4 |  45 |  61.6 |
|    6 | Neutral        | Strong Bearish |   67 |  5.54% |  36 |  53.7 |  31 |  46.3 |
|    7 | Neutral        | Bullish        |   65 |  5.37% |  27 |  41.5 |  38 |  58.5 |
|    8 | Strong Bearish | Strong Bearish |   64 |  5.29% |  37 |  57.8 |  27 |  42.2 |
|    9 | Strong Bullish | Strong Bullish |   59 |  4.88% |  23 |  39.0 |  36 |  61.0 |
|   10 | Neutral        | Mildly Bearish |   40 |  3.31% |  24 |  60.0 |  16 |  40.0 |
|   11 | Mildly Bearish | Strong Bearish |   39 |  3.22% |  17 |  43.6 |  22 |  56.4 |
|   12 | Mildly Bullish | Strong Bullish |   31 |  2.56% |  21 |  67.7 |  10 |  32.3 |
|   13 | Neutral        | Mildly Bullish |   30 |  2.48% |  14 |  46.7 |  16 |  53.3 |
|   14 | Bearish        | Bearish        |   26 |  2.15% |  15 |  57.7 |  11 |  42.3 |
|   15 | Mildly Bullish | Neutral        |   24 |  1.98% |   8 |  33.3 |  16 |  66.7 |

#### Average Move Percentages

| Rank | FII View       | PRO View       | Avg Range | Avg O/C | TTD Range | TTD O/C | DTU Range | DTU O/C |
| ---- | -------------- | -------------- | --------- | ------- | --------- | ------- | --------- | ------- |
|    1 | Neutral        | Neutral        |      0.88 |   +0.04 |      0.85 |   -0.33 |      0.90 |   +0.40 |
|    2 | Bullish        | Strong Bullish |      0.76 |   -0.10 |      0.76 |   -0.39 |      0.74 |   +0.34 |
|    3 | Bearish        | Strong Bearish |      0.86 |   +0.01 |      0.84 |   -0.36 |      0.89 |   +0.42 |
|    4 | Neutral        | Strong Bullish |      0.83 |   +0.03 |      0.82 |   -0.41 |      0.84 |   +0.38 |
|    5 | Neutral        | Bearish        |      0.89 |   +0.17 |      0.81 |   -0.36 |      0.95 |   +0.49 |
|    6 | Neutral        | Strong Bearish |      0.81 |   +0.01 |      0.77 |   -0.36 |      0.86 |   +0.44 |
|    7 | Neutral        | Bullish        |      0.81 |   +0.10 |      0.77 |   -0.35 |      0.85 |   +0.42 |
|    8 | Strong Bearish | Strong Bearish |      0.84 |   -0.03 |      0.82 |   -0.36 |      0.87 |   +0.44 |
|    9 | Strong Bullish | Strong Bullish |      0.74 |   +0.08 |      0.72 |   -0.33 |      0.76 |   +0.35 |
|   10 | Neutral        | Mildly Bearish |      0.94 |   -0.05 |      0.93 |   -0.40 |      0.95 |   +0.48 |
|   11 | Mildly Bearish | Strong Bearish |      0.86 |   +0.02 |      0.86 |   -0.45 |      0.86 |   +0.39 |
|   12 | Mildly Bullish | Strong Bullish |      0.76 |   -0.17 |      0.76 |   -0.42 |      0.75 |   +0.36 |
|   13 | Neutral        | Mildly Bullish |      0.95 |   +0.01 |      1.02 |   -0.47 |      0.88 |   +0.44 |
|   14 | Bearish        | Bearish        |      0.86 |   -0.15 |      0.84 |   -0.41 |      0.89 |   +0.21 |
|   15 | Mildly Bullish | Neutral        |      0.84 |   +0.07 |      0.92 |   -0.49 |      0.80 |   +0.35 |

---

## 3. VIX Underestimated - Top 15 FII+PRO Combinations

VIX predicted a smaller move than what actually occurred - the day was more volatile than expected.
278 days total, 37 non-zero combinations observed.

#### Combination Counts and Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- |
|    1 | Neutral        | Neutral        |   39 | 14.03% |  23 |  59.0 |  16 |  41.0 |
|    2 | Bearish        | Strong Bearish |   19 |  6.83% |  12 |  63.2 |   7 |  36.8 |
|    3 | Neutral        | Bearish        |   19 |  6.83% |  11 |  57.9 |   8 |  42.1 |
|    4 | Bullish        | Strong Bullish |   18 |  6.47% |  12 |  66.7 |   6 |  33.3 |
|    5 | Strong Bearish | Strong Bearish |   16 |  5.76% |  11 |  68.8 |   5 |  31.2 |
|    6 | Neutral        | Strong Bearish |   15 |  5.40% |   5 |  33.3 |  10 |  66.7 |
|    7 | Neutral        | Bullish        |   14 |  5.04% |  10 |  71.4 |   4 |  28.6 |
|    8 | Mildly Bearish | Strong Bearish |   14 |  5.04% |   8 |  57.1 |   6 |  42.9 |
|    9 | Neutral        | Strong Bullish |   12 |  4.32% |   6 |  50.0 |   6 |  50.0 |
|   10 | Strong Bullish | Strong Bullish |   11 |  3.96% |   6 |  54.5 |   5 |  45.5 |
|   11 | Neutral        | Mildly Bearish |   10 |  3.60% |   7 |  70.0 |   3 |  30.0 |
|   12 | Neutral        | Mildly Bullish |    9 |  3.24% |   5 |  55.6 |   4 |  44.4 |
|   13 | Mildly Bullish | Strong Bullish |    9 |  3.24% |   6 |  66.7 |   3 |  33.3 |
|   14 | Mildly Bullish | Bullish        |    7 |  2.52% |   4 |  57.1 |   3 |  42.9 |
|   15 | Mildly Bearish | Bearish        |    7 |  2.52% |   4 |  57.1 |   3 |  42.9 |

#### Average Move Percentages

| Rank | FII View       | PRO View       | Avg Range | Avg O/C | TTD Range | TTD O/C | DTU Range | DTU O/C |
| ---- | -------------- | -------------- | --------- | ------- | --------- | ------- | --------- | ------- |
|    1 | Neutral        | Neutral        |      1.88 |   -0.44 |      2.06 |   -1.38 |      1.63 |   +0.91 |
|    2 | Bearish        | Strong Bearish |      1.73 |   -0.31 |      1.78 |   -1.05 |      1.66 |   +0.96 |
|    3 | Neutral        | Bearish        |      1.88 |   -0.43 |      1.99 |   -1.35 |      1.73 |   +0.82 |
|    4 | Bullish        | Strong Bullish |      1.59 |   -0.46 |      1.60 |   -1.16 |      1.57 |   +0.92 |
|    5 | Strong Bearish | Strong Bearish |      1.72 |   -0.36 |      1.60 |   -0.96 |      1.99 |   +0.97 |
|    6 | Neutral        | Strong Bearish |      1.64 |   +0.45 |      1.47 |   -0.91 |      1.73 |   +1.13 |
|    7 | Neutral        | Bullish        |      2.02 |   -0.29 |      1.96 |   -1.09 |      2.16 |   +1.69 |
|    8 | Mildly Bearish | Strong Bearish |      2.02 |   -0.39 |      2.16 |   -1.44 |      1.84 |   +1.00 |
|    9 | Neutral        | Strong Bullish |      1.96 |   -0.01 |      2.00 |   -1.25 |      1.92 |   +1.22 |
|   10 | Strong Bullish | Strong Bullish |      2.13 |   -0.39 |      2.56 |   -1.55 |      1.61 |   +1.00 |
|   11 | Neutral        | Mildly Bearish |      2.01 |   -0.79 |      2.09 |   -1.45 |      1.83 |   +0.74 |
|   12 | Neutral        | Mildly Bullish |      2.13 |   -0.72 |      2.51 |   -2.09 |      1.66 |   +1.00 |
|   13 | Mildly Bullish | Strong Bullish |      1.92 |   -0.47 |      1.89 |   -1.30 |      1.99 |   +1.19 |
|   14 | Mildly Bullish | Bullish        |      1.81 |   -0.35 |      1.92 |   -1.27 |      1.66 |   +0.89 |
|   15 | Mildly Bearish | Bearish        |      1.64 |   -0.05 |      1.61 |   -0.65 |      1.67 |   +0.75 |

---

### 8b. Top 10 Combinations - VIX Underestimated (by threshold)

#### Neutral30 (+-30K) - Underestimated - Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- |
|    1 | Neutral30      | Neutral30      |   37 | 13.31% |  21 |  56.8 |  16 |  43.2 |
|    2 | Neutral30      | Bearish        |   19 |  6.83% |  11 |  57.9 |   8 |  42.1 |
|    3 | Bearish        | Strong Bearish |   19 |  6.83% |  12 |  63.2 |   7 |  36.8 |
|    4 | Bullish        | Strong Bullish |   18 |  6.47% |  12 |  66.7 |   6 |  33.3 |
|    5 | Strong Bearish | Strong Bearish |   16 |  5.76% |  11 |  68.8 |   5 |  31.2 |
|    6 | Neutral30      | Strong Bearish |   15 |  5.40% |   5 |  33.3 |  10 |  66.7 |
|    7 | Neutral30      | Bullish        |   14 |  5.04% |  10 |  71.4 |   4 |  28.6 |
|    8 | Mildly Bearish | Strong Bearish |   14 |  5.04% |   8 |  57.1 |   6 |  42.9 |
|    9 | Neutral30      | Strong Bullish |   12 |  4.32% |   6 |  50.0 |   6 |  50.0 |
|   10 | Strong Bullish | Strong Bullish |   11 |  3.96% |   6 |  54.5 |   5 |  45.5 |

#### Neutral30 (+-30K) - Underestimated - Move Percentages

| Rank | FII View       | PRO View       | Avg Range | Avg O/C | TTD Range | TTD O/C | DTU Range | DTU O/C |
| ---- | -------------- | -------------- | --------- | ------- | --------- | ------- | --------- | ------- |
|    1 | Neutral30      | Neutral30      |      1.87 |   -0.39 |      2.05 |   -1.37 |      1.63 |   +0.91 |
|    2 | Neutral30      | Bearish        |      1.88 |   -0.43 |      1.99 |   -1.35 |      1.73 |   +0.82 |
|    3 | Bearish        | Strong Bearish |      1.73 |   -0.31 |      1.78 |   -1.05 |      1.66 |   +0.96 |
|    4 | Bullish        | Strong Bullish |      1.59 |   -0.46 |      1.60 |   -1.16 |      1.57 |   +0.92 |
|    5 | Strong Bearish | Strong Bearish |      1.72 |   -0.36 |      1.60 |   -0.96 |      1.99 |   +0.97 |
|    6 | Neutral30      | Strong Bearish |      1.64 |   +0.45 |      1.47 |   -0.91 |      1.73 |   +1.13 |
|    7 | Neutral30      | Bullish        |      2.02 |   -0.29 |      1.96 |   -1.09 |      2.16 |   +1.69 |
|    8 | Mildly Bearish | Strong Bearish |      2.02 |   -0.39 |      2.16 |   -1.44 |      1.84 |   +1.00 |
|    9 | Neutral30      | Strong Bullish |      1.96 |   -0.01 |      2.00 |   -1.25 |      1.92 |   +1.22 |
|   10 | Strong Bullish | Strong Bullish |      2.13 |   -0.39 |      2.56 |   -1.55 |      1.61 |   +1.00 |

#### Neutral20 (+-20K) - Underestimated - Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- |
|    1 | Bearish        | Strong Bearish |   19 |  6.83% |  12 |  63.2 |   7 |  36.8 |
|    2 | Bullish        | Strong Bullish |   18 |  6.47% |  12 |  66.7 |   6 |  33.3 |
|    3 | Mildly Bearish | Strong Bearish |   18 |  6.47% |  10 |  55.6 |   8 |  44.4 |
|    4 | Neutral20      | Neutral20      |   17 |  6.12% |   9 |  52.9 |   8 |  47.1 |
|    5 | Strong Bearish | Strong Bearish |   16 |  5.76% |  11 |  68.8 |   5 |  31.2 |
|    6 | Neutral20      | Mildly Bearish |   12 |  4.32% |   9 |  75.0 |   3 |  25.0 |
|    7 | Mildly Bullish | Strong Bullish |   12 |  4.32% |   8 |  66.7 |   4 |  33.3 |
|    8 | Neutral20      | Bearish        |   12 |  4.32% |   8 |  66.7 |   4 |  33.3 |
|    9 | Mildly Bearish | Bearish        |   12 |  4.32% |   6 |  50.0 |   6 |  50.0 |
|   10 | Mildly Bullish | Bullish        |   12 |  4.32% |   8 |  66.7 |   4 |  33.3 |

#### Neutral20 (+-20K) - Underestimated - Move Percentages

| Rank | FII View       | PRO View       | Avg Range | Avg O/C | TTD Range | TTD O/C | DTU Range | DTU O/C |
| ---- | -------------- | -------------- | --------- | ------- | --------- | ------- | --------- | ------- |
|    1 | Bearish        | Strong Bearish |      1.73 |   -0.31 |      1.78 |   -1.05 |      1.66 |   +0.96 |
|    2 | Bullish        | Strong Bullish |      1.59 |   -0.46 |      1.60 |   -1.16 |      1.57 |   +0.92 |
|    3 | Mildly Bearish | Strong Bearish |      1.97 |   -0.26 |      2.00 |   -1.33 |      1.94 |   +1.08 |
|    4 | Neutral20      | Neutral20      |      1.87 |   -0.20 |      2.10 |   -1.23 |      1.60 |   +0.97 |
|    5 | Strong Bearish | Strong Bearish |      1.72 |   -0.36 |      1.60 |   -0.96 |      1.99 |   +0.97 |
|    6 | Neutral20      | Mildly Bearish |      2.07 |   -0.88 |      2.15 |   -1.43 |      1.83 |   +0.74 |
|    7 | Mildly Bullish | Strong Bullish |      1.89 |   -0.48 |      1.87 |   -1.33 |      1.94 |   +1.22 |
|    8 | Neutral20      | Bearish        |      1.99 |   -0.58 |      2.00 |   -1.34 |      1.97 |   +0.94 |
|    9 | Mildly Bearish | Bearish        |      1.72 |   -0.14 |      1.82 |   -1.04 |      1.61 |   +0.76 |
|   10 | Mildly Bullish | Bullish        |      2.04 |   -0.48 |      2.13 |   -1.28 |      1.86 |   +1.13 |

#### Neutral10 (+-10K) - Underestimated - Direction Split

| Rank | FII View       | PRO View       | Days | %      | TTD | TTD%  | DTU | DTU%  |
| ---- | -------------- | -------------- | ---- | ------ | --- | ----- | --- | ----- |
|    1 | Mildly Bearish | Strong Bearish |   21 |  7.55% |  11 |  52.4 |  10 |  47.6 |
|    2 | Bearish        | Strong Bearish |   19 |  6.83% |  12 |  63.2 |   7 |  36.8 |
|    3 | Bullish        | Strong Bullish |   18 |  6.47% |  12 |  66.7 |   6 |  33.3 |
|    4 | Mildly Bearish | Mildly Bearish |   18 |  6.47% |  15 |  83.3 |   3 |  16.7 |
|    5 | Mildly Bearish | Bearish        |   17 |  6.12% |  10 |  58.8 |   7 |  41.2 |
|    6 | Strong Bearish | Strong Bearish |   16 |  5.76% |  11 |  68.8 |   5 |  31.2 |
|    7 | Mildly Bullish | Strong Bullish |   16 |  5.76% |   9 |  56.2 |   7 |  43.8 |
|    8 | Mildly Bullish | Bullish        |   14 |  5.04% |   9 |  64.3 |   5 |  35.7 |
|    9 | Strong Bullish | Strong Bullish |   11 |  3.96% |   6 |  54.5 |   5 |  45.5 |
|   10 | Mildly Bullish | Mildly Bullish |   10 |  3.60% |   5 |  50.0 |   5 |  50.0 |

#### Neutral10 (+-10K) - Underestimated - Move Percentages

| Rank | FII View       | PRO View       | Avg Range | Avg O/C | TTD Range | TTD O/C | DTU Range | DTU O/C |
| ---- | -------------- | -------------- | --------- | ------- | --------- | ------- | --------- | ------- |
|    1 | Mildly Bearish | Strong Bearish |      1.88 |   -0.16 |      1.93 |   -1.28 |      1.82 |   +1.06 |
|    2 | Bearish        | Strong Bearish |      1.73 |   -0.31 |      1.78 |   -1.05 |      1.66 |   +0.96 |
|    3 | Bullish        | Strong Bullish |      1.59 |   -0.46 |      1.60 |   -1.16 |      1.57 |   +0.92 |
|    4 | Mildly Bearish | Mildly Bearish |      1.83 |   -1.01 |      1.88 |   -1.25 |      1.58 |   +0.15 |
|    5 | Mildly Bearish | Bearish        |      1.79 |   -0.34 |      1.92 |   -1.19 |      1.61 |   +0.87 |
|    6 | Strong Bearish | Strong Bearish |      1.72 |   -0.36 |      1.60 |   -0.96 |      1.99 |   +0.97 |
|    7 | Mildly Bullish | Strong Bullish |      1.98 |   -0.17 |      1.89 |   -1.36 |      2.11 |   +1.37 |
|    8 | Mildly Bullish | Bullish        |      2.05 |   -0.35 |      2.11 |   -1.31 |      1.96 |   +1.37 |
|    9 | Strong Bullish | Strong Bullish |      2.13 |   -0.39 |      2.56 |   -1.55 |      1.61 |   +1.00 |
|   10 | Mildly Bullish | Mildly Bullish |      1.81 |   -0.19 |      2.07 |   -1.58 |      1.54 |   +1.19 |

---

## 9. Which Combinations Exceed 1.5x VIX Predicted Range?

Out of 1,488 trading days, **344 days (23.1%)** had an actual range exceeding 1.5x what VIX predicted. Of those, 261 were Underestimated and 83 were Overestimated.

The key metric here is **Hit Rate** - for each combination, what percentage of its total days exceeded 1.5x VIX? A high hit rate means that combination is a reliable signal for VIX underprediction.

### 9a. Hit Rate by Combination (+-30K threshold, min 10 days)

#### Direction Split

| Rank | FII View       | PRO View       | Total | >1.5x | Hit%  | TTD | TTD%  | DTU | DTU%  |
| ---- | -------------- | -------------- | ----- | ----- | ----- | --- | ----- | --- | ----- |
|    1 | Bearish        | Mildly Bearish |    11 |     5 | 45.5% |   6 |  54.5 |   5 |  45.5 |
|    2 | Mildly Bearish | Neutral        |    19 |     7 | 36.8% |   9 |  47.4 |  10 |  52.6 |
|    3 | Strong Bearish | Strong Bearish |    80 |    22 | 27.5% |  48 |  60.0 |  32 |  40.0 |
|    4 | Mildly Bullish | Bullish        |    26 |     7 | 26.9% |  16 |  61.5 |  10 |  38.5 |
|    5 | Bullish        | Bullish        |    26 |     7 | 26.9% |  12 |  46.2 |  14 |  53.8 |
|    6 | Mildly Bearish | Strong Bearish |    53 |    14 | 26.4% |  25 |  47.2 |  28 |  52.8 |
|    7 | Neutral        | Bearish        |    92 |    24 | 26.1% |  39 |  42.4 |  53 |  57.6 |
|    8 | Mildly Bullish | Strong Bullish |    40 |    10 | 25.0% |  27 |  67.5 |  13 |  32.5 |
|    9 | Mildly Bearish | Bearish        |    29 |     7 | 24.1% |  18 |  62.1 |  11 |  37.9 |
|   10 | Neutral        | Mildly Bearish |    50 |    12 | 24.0% |  31 |  62.0 |  19 |  38.0 |
|   11 | Bullish        | Strong Bearish |    17 |     4 | 23.5% |   9 |  52.9 |   8 |  47.1 |
|   12 | Neutral        | Strong Bearish |    82 |    19 | 23.2% |  41 |  50.0 |  41 |  50.0 |
|   13 | Neutral        | Neutral        |   194 |    45 | 23.2% | 100 |  51.5 |  94 |  48.5 |
|   14 | Neutral        | Mildly Bullish |    39 |     9 | 23.1% |  19 |  48.7 |  20 |  51.3 |
|   15 | Bearish        | Bearish        |    32 |     7 | 21.9% |  18 |  56.2 |  14 |  43.8 |

#### Move Percentages

| Rank | FII View       | PRO View       | Avg Ratio | Avg Range | Avg O/C |
| ---- | -------------- | -------------- | --------- | --------- | ------- |
|    1 | Bearish        | Mildly Bearish | 1.33x     | 1.00%     |   -0.14   |
|    2 | Mildly Bearish | Neutral        | 1.39x     | 1.17%     |   -0.16   |
|    3 | Strong Bearish | Strong Bearish | 1.32x     | 1.02%     |   -0.09   |
|    4 | Mildly Bullish | Bullish        | 1.29x     | 1.10%     |   -0.19   |
|    5 | Bullish        | Bullish        | 1.20x     | 0.98%     |   +0.03   |
|    6 | Mildly Bearish | Strong Bearish | 1.40x     | 1.17%     |   -0.09   |
|    7 | Neutral        | Bearish        | 1.27x     | 1.10%     |   +0.04   |
|    8 | Mildly Bullish | Strong Bullish | 1.30x     | 1.02%     |   -0.23   |
|    9 | Mildly Bearish | Bearish        | 1.24x     | 1.06%     |   -0.07   |
|   10 | Neutral        | Mildly Bearish | 1.28x     | 1.15%     |   -0.20   |
|   11 | Bullish        | Strong Bearish | 1.14x     | 0.85%     |   +0.02   |
|   12 | Neutral        | Strong Bearish | 1.25x     | 0.96%     |   +0.09   |
|   13 | Neutral        | Neutral        | 1.19x     | 1.08%     |   -0.06   |
|   14 | Neutral        | Mildly Bullish | 1.29x     | 1.22%     |   -0.15   |
|   15 | Bearish        | Bearish        | 1.28x     | 1.01%     |   -0.14   |

---

## 10. Files Generated

| File | Description |
| ---- | ----------- |
| **Script** | |
| `analyze_vix_fii_pro.py` | Python analysis script (all thresholds + 1.5x analysis) |
| **Original VIX Accuracy Rankings** | |
| `overestimated_combinations.csv` | Ranked combos for VIX Overestimated (original views) |
| `underestimated_combinations.csv` | Ranked combos for VIX Underestimated (original views) |
| `market_direction_breakdown.csv` | Combos split by vix_accuracy + nifty_day (4 subgroups) |
| **Multi-Threshold Rankings** | |
| `overestimated_neutral30.csv` | Overestimated combos with +-30K neutral |
| `underestimated_neutral30.csv` | Underestimated combos with +-30K neutral |
| `overestimated_neutral20.csv` | Overestimated combos with +-20K neutral |
| `underestimated_neutral20.csv` | Underestimated combos with +-20K neutral |
| `overestimated_neutral10.csv` | Overestimated combos with +-10K neutral |
| `underestimated_neutral10.csv` | Underestimated combos with +-10K neutral |
| **1.5x VIX Exceedance Analysis** | |
| `hit_rate_1_5x_all_neutral30.csv` | Hit rate per combo (+-30K) - all days |
| `hit_rate_1_5x_all_neutral20.csv` | Hit rate per combo (+-20K) - all days |
| `hit_rate_1_5x_all_neutral10.csv` | Hit rate per combo (+-10K) - all days |
| `above_1_5x_combinations_neutral30.csv` | Ranked combos for >1.5x days only (+-30K) |
| `above_1_5x_combinations_neutral20.csv` | Ranked combos for >1.5x days only (+-20K) |
| `above_1_5x_combinations_neutral10.csv` | Ranked combos for >1.5x days only (+-10K) |
| **Report** | |
| `ANALYSIS_REPORT.md` | This report |

---

*Generated from 1,488 trading days of VIX + FII/PRO positioning data.*