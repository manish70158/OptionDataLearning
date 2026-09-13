## Purpose

Report generator that maps each FII View × PRO View combination to option strategy profitability metrics and produces ranked analysis with visual summaries for identifying the optimal strategy per market condition.

## ADDED Requirements

### Requirement: Strategy ranking per FII/PRO combination
The system SHALL produce a ranked table for each FII View × PRO View combination showing all 6 strategies ordered by total P&L (descending). Each row SHALL include: strategy name, total P&L (points), average daily P&L, win rate, max single-day loss, max consecutive drawdown, risk-adjusted ratio, and sample size (number of days).

#### Scenario: Ranking output for a bullish combination
- **WHEN** the report generates rankings for Mildly Bearish × Mildly Bearish (100% Green, +0.351% avg)
- **THEN** directional bullish strategies (Bull Call Spread) SHALL rank higher than neutral strategies (Iron Condor), and the table SHALL show all 6 strategies with complete metrics

#### Scenario: Ranking output for a bearish combination
- **WHEN** the report generates rankings for Bullish × Strong Bullish (36.5% Green, -0.179% avg)
- **THEN** directional bearish strategies (Bear Put Spread) or premium-selling strategies (Iron Condor/Butterfly) SHALL rank higher than bullish strategies

### Requirement: Best strategy summary matrix
The system SHALL produce a single summary matrix with FII Views as rows and PRO Views as columns. Each cell SHALL contain the name of the highest-P&L strategy for that combination, its total P&L, and its win rate. Cells with fewer than 5 sample days SHALL be marked with an asterisk.

#### Scenario: Full matrix generation
- **WHEN** the report generates the summary matrix across all 47 observed FII × PRO combinations
- **THEN** it SHALL produce a 7×7 grid (7 FII views × 7 PRO views) with the best strategy in each observed cell and "N/A" for unobserved combinations

#### Scenario: Low sample size marking
- **WHEN** a combination has fewer than 5 trading days (e.g., Strong Bullish × Mildly Bearish = 1 day)
- **THEN** the cell SHALL display the strategy name with an asterisk and the sample size

### Requirement: Expiry vs non-expiry comparison
The system SHALL include a section comparing strategy performance on expiry days versus non-expiry days for each FII/PRO combination where both segments have at least 3 data points. The comparison SHALL highlight combinations where the optimal strategy differs between expiry and non-expiry days.

#### Scenario: Divergent optimal strategies
- **WHEN** for Neutral × Bearish, Iron Condor is best on expiry days but Bull Call Spread is best on non-expiry days
- **THEN** the report SHALL flag this combination in a "Strategy Divergence" table showing both strategies and their respective metrics

#### Scenario: Insufficient data for comparison
- **WHEN** a combination has fewer than 3 expiry days or fewer than 3 non-expiry days
- **THEN** the report SHALL omit that combination from the expiry comparison section

### Requirement: Daily recommendation output
The system SHALL accept today's FII View, PRO View, and current VIX as inputs and output a recommendation containing: the historically best strategy for that combination, the recommended strike structure (offsets from current NIFTY level), expected daily P&L range (mean ± 1 std dev from backtest), the win rate, and a confidence indicator (High/Medium/Low based on sample size: ≥30 days = High, 10–29 = Medium, <10 = Low).

#### Scenario: High-confidence recommendation
- **WHEN** today's FII View = Neutral, PRO View = Neutral (328 historical days)
- **THEN** the recommendation SHALL include the best strategy, its strike structure, expected P&L range, win rate, and confidence = "High"

#### Scenario: Low-confidence recommendation
- **WHEN** today's FII View = Strong Bearish, PRO View = Bullish (2 historical days)
- **THEN** the recommendation SHALL include the best strategy but mark confidence = "Low" and note the limited sample size

### Requirement: Report output formats
The system SHALL generate the profitability report in Markdown format by default. It SHALL optionally support HTML output (with embedded charts) and CSV export of the raw metrics tables. The CLI SHALL accept an `--output-format` flag with values `md`, `html`, or `csv`.

#### Scenario: Markdown report generation
- **WHEN** the user runs the report with `--output-format md` or no format flag
- **THEN** the system SHALL write a `.md` file with all tables formatted in GitHub-flavored Markdown

#### Scenario: HTML report with charts
- **WHEN** the user runs the report with `--output-format html`
- **THEN** the system SHALL write an `.html` file with styled tables and embedded bar/heatmap charts for strategy comparison

#### Scenario: CSV export
- **WHEN** the user runs the report with `--output-format csv`
- **THEN** the system SHALL write one CSV file per major table (strategy rankings, summary matrix, expiry comparison)

### Requirement: VIX regime segmentation
The system SHALL segment results by VIX regime in addition to FII/PRO combination. VIX regimes SHALL be: Low (VIX < 15), Normal (15 ≤ VIX < 20), Elevated (20 ≤ VIX < 25), High (VIX ≥ 25). The report SHALL include a section showing how the optimal strategy changes across VIX regimes for the most common FII/PRO combinations (those with ≥30 total days).

#### Scenario: VIX regime breakdown for Neutral × Neutral
- **WHEN** the report generates VIX regime analysis for Neutral × Neutral (328 days)
- **THEN** it SHALL show the best strategy and its metrics separately for Low VIX, Normal VIX, Elevated VIX, and High VIX sub-periods

#### Scenario: Skip VIX regime for small combinations
- **WHEN** a FII/PRO combination has fewer than 30 total days
- **THEN** the VIX regime section SHALL omit that combination
