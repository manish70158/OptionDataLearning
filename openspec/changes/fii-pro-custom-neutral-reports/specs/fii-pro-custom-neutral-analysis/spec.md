## Purpose

Generates FII×PRO combination analysis reports with configurable neutral zone thresholds (±10K, ±20K, ±25K, ±30K), reclassifying composite values and producing per-threshold markdown reports in the same structure as the existing 6-year analysis, plus a cross-threshold comparison report identifying threshold-proof and threshold-sensitive signals.

## ADDED Requirements

### Requirement: Configurable neutral zone classification

The system SHALL classify FII and PRO composite values into 7 categories using configurable neutral zone thresholds. The classification boundaries SHALL be:
- **Strong Bearish**: composite < -100,000
- **Bearish**: -100,000 ≤ composite < -50,000
- **Mildly Bearish**: -50,000 ≤ composite < -neutral_threshold
- **Neutral**: -neutral_threshold ≤ composite ≤ +neutral_threshold
- **Mildly Bullish**: +neutral_threshold < composite ≤ +50,000
- **Bullish**: +50,000 < composite ≤ +100,000
- **Strong Bullish**: composite > +100,000

Both `fii_composite` and `pro_composite` columns SHALL be reclassified independently using the same threshold scheme.

#### Scenario: ±30K neutral zone classification
- **WHEN** neutral_threshold is set to 30,000
- **THEN** composite values between -30,000 and +30,000 are classified as Neutral, values between ±30,000 and ±50,000 as Mildly Bullish/Bearish, and all other boundaries remain at ±50K/±100K. This matches the original classification used in the existing 6-year analysis.

#### Scenario: ±25K neutral zone classification
- **WHEN** neutral_threshold is set to 25,000
- **THEN** composite values between -25,000 and +25,000 are classified as Neutral, values between ±25,000 and ±50,000 as Mildly Bullish/Bearish, and all other boundaries remain at ±50K/±100K

#### Scenario: ±20K neutral zone classification
- **WHEN** neutral_threshold is set to 20,000
- **THEN** composite values between -20,000 and +20,000 are classified as Neutral, values between ±20,000 and ±50,000 as Mildly Bullish/Bearish, and all other boundaries remain at ±50K/±100K

#### Scenario: ±10K neutral zone classification
- **WHEN** neutral_threshold is set to 10,000
- **THEN** composite values between -10,000 and +10,000 are classified as Neutral, values between ±10,000 and ±50,000 as Mildly Bullish/Bearish, and all other boundaries remain at ±50K/±100K

### Requirement: Report output structure matches existing analysis format

Each generated report SHALL contain the following sections in order:
1. **Header**: Title with dataset metadata (day count, date range, combination count)
2. **FII View Distribution**: Table showing days and percentage per FII view category
3. **Master Summary Table**: All FII×PRO combinations sorted by Green% descending, with columns: FII View, PRO View, Days, Green%, Avg Chg%, Dominant Pattern, Exp G%, Non-Exp G%
4. **Per-FII-View Sections** (7 sections): Each FII view as a section header, table of PRO combinations within that view with Days, Green%, Avg Chg%, Avg Range%, Up from Open, Down from Open, Dominant Move, plus a pattern insight paragraph
5. **Top 5 Best/Worst Combinations**: Filtered to combinations with ≥5 days, sorted by Green% descending/ascending
6. **Top 5 Highest/Lowest Avg Change**: Filtered to ≥5 days, sorted by Avg Chg%
7. **Expiry vs Non-Expiry Divergence**: Combinations with >15% Green% divergence between expiry and non-expiry days, requiring ≥3 days each side
8. **Conclusion**: Key findings, actionable rules, and comparison observations

#### Scenario: Report contains all required sections
- **WHEN** a report is generated for any neutral zone threshold
- **THEN** the output markdown file contains all 8 section types listed above, using the same table formats as `FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md`

#### Scenario: Green day classification
- **WHEN** computing Green% for a combination
- **THEN** a day is Green when `nifty_day` column equals "Green", and Green% = (green_days / total_days) × 100

### Requirement: Four per-threshold report files in reports/ directory

The system SHALL generate exactly four per-threshold report files:
- `reports/FII_PRO_NEUTRAL_30K_ANALYSIS.md` using neutral_threshold = 30,000
- `reports/FII_PRO_NEUTRAL_25K_ANALYSIS.md` using neutral_threshold = 25,000
- `reports/FII_PRO_NEUTRAL_20K_ANALYSIS.md` using neutral_threshold = 20,000
- `reports/FII_PRO_NEUTRAL_10K_ANALYSIS.md` using neutral_threshold = 10,000

The generation script SHALL also reside in the `reports/` directory alongside the output files.

#### Scenario: All four per-threshold reports generated successfully
- **WHEN** the generation script runs to completion
- **THEN** all four per-threshold report files exist in `reports/` with non-empty content

#### Scenario: Reports directory already exists
- **WHEN** the `reports/` directory exists at project root
- **THEN** the script writes report files into it without error

### Requirement: Cross-threshold comparison report

The system SHALL generate a fifth report `reports/FII_PRO_NEUTRAL_ZONE_COMPARISON.md` that compares all four per-threshold reports side by side. The comparison report SHALL contain the following sections:
1. **Distribution Impact**: Table showing how Neutral, Mildly Bullish, and Mildly Bearish day counts change across all four thresholds
2. **Top 5 Best/Worst Combinations side by side**: One row per rank, columns for each threshold
3. **Threshold-Proof Good Signals**: Combinations that maintain ≥55% Green across ALL four thresholds with ≥5 days in each
4. **Threshold-Proof Bad Signals**: Combinations that stay ≤45% Green across ALL four thresholds with ≥5 days in each
5. **Most Threshold-Sensitive Combinations**: Combinations whose Green% spread across thresholds exceeds 10 percentage points, sorted by spread descending
6. **Key Findings**: Summary of trustworthy vs untrustworthy signals
7. **Quick Reference Actionable Rules**: Go long / avoid long rules based only on threshold-proof signals

#### Scenario: Comparison report generated with all sections
- **WHEN** the comparison report is generated
- **THEN** it contains all 7 section types listed above with data drawn from all four threshold analyses

#### Scenario: Threshold-proof identification
- **WHEN** identifying threshold-proof good signals
- **THEN** only combinations appearing with ≥5 days AND ≥55% Green in ALL four threshold analyses are included

#### Scenario: Threshold-sensitive identification
- **WHEN** identifying threshold-sensitive combinations
- **THEN** only combinations present in at least 3 of 4 thresholds (≥5 days each) with a Green% spread > 10 percentage points are included, sorted by spread descending

### Requirement: Data source reading

The system SHALL read `vix_fii_t1_intraday_daily_results.csv` as the primary data source. The following columns SHALL be used:
- `date`, `is_nifty_expiry`, `expiry_type` — for date and expiry classification
- `nifty_open`, `nifty_high`, `nifty_low`, `nifty_close` — for price data
- `actual_open_close_pct`, `actual_range_pct` — for change and range metrics
- `intraday_high_pct`, `intraday_low_pct` — for up-from-open and down-from-open
- `move_direction`, `nifty_day` — for direction and green/red classification
- `fii_composite`, `pro_composite` — for reclassification

#### Scenario: CSV parsing with all required columns
- **WHEN** the script reads `vix_fii_t1_intraday_daily_results.csv`
- **THEN** all listed columns are accessible and numeric columns are parsed as floats

### Requirement: Combination statistics computation

For each unique (FII_view, PRO_view) pair, the system SHALL compute:
- **Days**: Total count of rows with that combination
- **Green%**: Percentage of days where `nifty_day` = "Green"
- **Avg Chg%**: Mean of `actual_open_close_pct`
- **Avg Range%**: Mean of `actual_range_pct`
- **Up from Open**: Mean of `intraday_high_pct` × 100 (expressed as basis points from open)
- **Down from Open**: Mean of absolute value of `intraday_low_pct` × 100
- **Dominant Move**: Most frequent `move_direction` value with its percentage
- **Exp G%**: Green% for days where `is_nifty_expiry` = 1
- **Non-Exp G%**: Green% for days where `is_nifty_expiry` = 0

#### Scenario: Statistics computed for all combinations
- **WHEN** FII and PRO views are reclassified with a given threshold
- **THEN** statistics are computed for every (FII_view, PRO_view) pair that has at least 1 day of data

#### Scenario: Expiry statistics handle zero-count gracefully
- **WHEN** a combination has zero expiry days or zero non-expiry days
- **THEN** the corresponding Exp G% or Non-Exp G% is displayed as "-"
