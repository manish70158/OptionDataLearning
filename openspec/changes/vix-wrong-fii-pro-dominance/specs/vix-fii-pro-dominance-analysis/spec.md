## Purpose

Identifies which FII+Pro view combinations dominate when VIX accuracy predictions are wrong (Overestimated or Underestimated), providing cross-tabulated frequency analysis with market direction breakdowns.

## ADDED Requirements

### Requirement: Load and validate source data
The system SHALL read `vix_fii_t1_intraday_daily_results.csv` from the project root and validate that columns `vix_accuracy`, `fii_view`, `pro_view`, and `nifty_day` exist with non-empty values.

#### Scenario: Successful data load
- **WHEN** the script is executed with the CSV file present at the expected path
- **THEN** the system loads all rows and confirms column presence, reporting total row count

#### Scenario: Missing CSV file
- **WHEN** the CSV file is not found at the expected path
- **THEN** the system prints an error message indicating the file path and exits

### Requirement: Filter rows by VIX accuracy category
The system SHALL partition data into two groups: rows where `vix_accuracy` is "Overestimated" and rows where `vix_accuracy` is "Underestimated". Both represent VIX being wrong.

#### Scenario: Partition by Overestimated
- **WHEN** filtering for Overestimated rows
- **THEN** all rows where `vix_accuracy == "Overestimated"` are selected

#### Scenario: Partition by Underestimated
- **WHEN** filtering for Underestimated rows
- **THEN** all rows where `vix_accuracy == "Underestimated"` are selected

### Requirement: Cross-tabulate FII view and Pro view combinations
For each VIX accuracy category, the system SHALL compute a cross-tabulation of `fii_view` x `pro_view` showing frequency count and percentage of total for each combination.

#### Scenario: Cross-tab for Overestimated
- **WHEN** analyzing Overestimated rows
- **THEN** a matrix of all `fii_view` values (rows) x `pro_view` values (columns) is produced with count and percentage in each cell

#### Scenario: Cross-tab for Underestimated
- **WHEN** analyzing Underestimated rows
- **THEN** a matrix of all `fii_view` values (rows) x `pro_view` values (columns) is produced with count and percentage in each cell

### Requirement: Rank dominant FII+Pro combinations
The system SHALL rank all FII+Pro view combinations by frequency (descending) for each VIX accuracy category, showing the top combinations that dominate when VIX is wrong.

#### Scenario: Top combinations for Overestimated
- **WHEN** ranking combinations for Overestimated
- **THEN** all non-zero combinations are listed sorted by count descending, with rank, count, and percentage

#### Scenario: Top combinations for Underestimated
- **WHEN** ranking combinations for Underestimated
- **THEN** all non-zero combinations are listed sorted by count descending, with rank, count, and percentage

### Requirement: Breakdown by market direction
The system SHALL further split each VIX accuracy category by `nifty_day` (Green/Red) and repeat the combination ranking to reveal whether the dominant FII+Pro combination shifts with market direction.

#### Scenario: Green day breakdown for Overestimated
- **WHEN** filtering Overestimated rows where `nifty_day == "Green"`
- **THEN** ranked FII+Pro combinations are produced for that subset

#### Scenario: Red day breakdown for Underestimated
- **WHEN** filtering Underestimated rows where `nifty_day == "Red"`
- **THEN** ranked FII+Pro combinations are produced for that subset

### Requirement: Export results to CSV files
The system SHALL write analysis results to CSV files in the `vix_fii_pro_analysis/` output folder.

#### Scenario: CSV output files created
- **WHEN** the analysis completes
- **THEN** the following CSV files are written to `vix_fii_pro_analysis/`:
  - `overestimated_combinations.csv` — ranked FII+Pro combinations for Overestimated
  - `underestimated_combinations.csv` — ranked FII+Pro combinations for Underestimated
  - `market_direction_breakdown.csv` — combinations split by nifty_day within each VIX accuracy category

### Requirement: Print console summary report
The system SHALL print a human-readable summary to the console showing key findings: top 5 dominant combinations per VIX accuracy category, and notable shifts between Green/Red days.

#### Scenario: Console report output
- **WHEN** the analysis completes
- **THEN** a formatted summary is printed showing top 5 combinations for Overestimated, top 5 for Underestimated, and a comparison highlighting which combinations are unique to each category
