## Purpose

Provides a binary directional classification system for FII/PRO composite scores that eliminates the neutral zone, treating every trading day as either bullish or bearish, and generates analysis reports across three dimensions: directional combination stats, volatility whipsaw, and reversal traps.

## ADDED Requirements

### Requirement: Six-tier directional classification without neutral
The system SHALL classify FII and PRO composite scores into exactly six tiers with no neutral category:
- **Strong Bullish**: composite > +100,000
- **Bullish**: +50,001 to +100,000
- **Mildly Bullish**: 0 to +50,000 (inclusive of zero)
- **Mildly Bearish**: -50,000 to -1 (exclusive of zero)
- **Bearish**: -100,000 to -50,001
- **Strong Bearish**: < -100,000

NaN composite values SHALL be classified as Mildly Bullish (zero-equivalent).

#### Scenario: Positive composite near zero
- **WHEN** a composite score is 500
- **THEN** the system classifies it as "Mildly Bullish"

#### Scenario: Negative composite near zero
- **WHEN** a composite score is -500
- **THEN** the system classifies it as "Mildly Bearish"

#### Scenario: Zero composite
- **WHEN** a composite score is exactly 0
- **THEN** the system classifies it as "Mildly Bullish"

#### Scenario: NaN composite
- **WHEN** a composite score is NaN
- **THEN** the system classifies it as "Mildly Bullish"

### Requirement: Separate output directory
The system SHALL write all generated reports and scripts into a `reports_no_neutral/` directory at the project root, parallel to the existing `reports/` directory. The existing `reports/` directory SHALL NOT be modified.

#### Scenario: Output location
- **WHEN** any report is generated
- **THEN** the output file resides under `reports_no_neutral/` at the project root

### Requirement: Directional combination analysis report
The system SHALL generate a directional combination analysis report that groups days by FII view x PRO view and computes per-combination:
- Day count
- Green day percentage
- Average open-to-close change percentage
- Average range percentage
- Average up-from-open and down-from-open
- Dominant intraday move direction (shown if >= 55% dominance, else "Mixed")
- Expiry vs non-expiry Green% with divergence flagging (>15%)

The report SHALL include: label guide, FII distribution, master summary table sorted by Green%, per-FII-view sections, top/bottom 5 rankings, expiry divergence table, and a conclusion with actionable rules.

#### Scenario: Complete directional report generation
- **WHEN** the directional combination analysis script is executed
- **THEN** a single markdown report is produced covering all 36 possible FII x PRO combinations (6 FII tiers x 6 PRO tiers) using the no-neutral classification

#### Scenario: Bold formatting threshold
- **WHEN** a combination has >= 5 days of data
- **THEN** that row is displayed in bold in the master table

### Requirement: Volatility whipsaw analysis report
The system SHALL generate volatility whipsaw reports using VIX-fraction thresholds (0.5x and 0.3x VIX), computing per FII x PRO combination:
- Whipsaw tier classification (Extreme/Strong/Moderate based on up_ratio and down_ratio)
- Extreme/Strong/Moderate whipsaw day percentages
- Average total swing percentage
- Swing asymmetry (up-biased vs down-biased)
- Intraday swing timing (morning vs afternoon highs/lows)

Reports SHALL use the no-neutral 6-tier classification for FII and PRO views.

#### Scenario: Whipsaw report with 0.5x VIX
- **WHEN** the volatility whipsaw script is executed
- **THEN** a report is produced using 0.5x VIX as the fraction threshold with the no-neutral classification

#### Scenario: Whipsaw report with 0.3x VIX
- **WHEN** the volatility whipsaw script is executed
- **THEN** a second report is produced using 0.3x VIX as the fraction threshold with the no-neutral classification

### Requirement: Reversal trap analysis report
The system SHALL generate a reversal trap analysis report detecting four trap patterns per FII x PRO combination:
- Bull Trap: up >= 0.3xVIX first, then down >= 0.5xVIX (Top to Down)
- Bear Trap: down >= 0.3xVIX first, then up >= 0.5xVIX (Down to Up)
- Rally Fade: up >= 0.5xVIX first, then down >= 0.3xVIX (Top to Down)
- Drop Bounce: down >= 0.5xVIX first, then up >= 0.3xVIX (Down to Up)

The report SHALL use the no-neutral 6-tier classification for FII and PRO views.

#### Scenario: Reversal trap report generation
- **WHEN** the reversal trap script is executed
- **THEN** a markdown report is produced with pattern rates, per-FII sections, and summary of which combinations are most trap-prone, using the no-neutral classification

### Requirement: FII section ordering
All reports SHALL present per-FII sections in this order: Strong Bullish, Bullish, Mildly Bullish, Mildly Bearish, Bearish, Strong Bearish.

#### Scenario: Section order in directional report
- **WHEN** the directional report is generated
- **THEN** FII sections appear in order: Strong Bullish, Bullish, Mildly Bullish, Mildly Bearish, Bearish, Strong Bearish

### Requirement: Consistent label naming
All reports SHALL use the labels "Mildly Bullish" and "Mildly Bearish" (without numeric suffixes) since there is no variable neutral threshold.

#### Scenario: Label format
- **WHEN** any report references the 0-to-50K tier
- **THEN** the label reads "Mildly Bullish" (not "MildBull20" or similar)
