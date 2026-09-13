## Purpose

Backtest parameter configuration panel that controls how the simulation runs — date range, entry/exit timing, risk management rules, and market condition filters.

## ADDED Requirements

### Requirement: Date range selection
The configuration panel SHALL provide a date range picker for selecting the backtest period. The maximum range SHALL be 2 years from the current date. The minimum range SHALL be 1 trading day.

#### Scenario: Selecting a valid date range
- **WHEN** user selects a start date of 2024-09-01 and end date of 2026-09-01
- **THEN** the system SHALL accept the range and display the number of trading days in that period

#### Scenario: Range exceeds 2 years
- **WHEN** user attempts to select a date range longer than 2 years
- **THEN** the system SHALL prevent selection and display "Maximum backtest period is 2 years"

#### Scenario: Start date after end date
- **WHEN** user selects a start date that is after the end date
- **THEN** the system SHALL display a validation error "Start date must be before end date"

### Requirement: Entry and exit time
The panel SHALL allow configuring the time of day for trade entry and exit. Entry time SHALL default to 09:20 IST (after market open). Exit time SHALL default to 15:15 IST (before market close). Both SHALL be configurable in 5-minute increments between 09:15 and 15:30 IST.

#### Scenario: Default times
- **WHEN** user opens the backtest config
- **THEN** entry time SHALL be 09:20 and exit time SHALL be 15:15

#### Scenario: Custom entry time
- **WHEN** user sets entry time to 10:00
- **THEN** the backtest SHALL simulate entering positions at 10:00 IST on each trading day

#### Scenario: Exit before entry
- **WHEN** user sets exit time earlier than entry time
- **THEN** the system SHALL display a validation error "Exit time must be after entry time"

### Requirement: Stop loss configuration
The panel SHALL support stop loss in two modes: percentage of premium and absolute points. Stop loss SHALL be optional (can be disabled). Default: enabled at 50% of premium received/paid.

#### Scenario: Percentage stop loss
- **WHEN** user sets stop loss to 30% in percentage mode
- **THEN** the backtest SHALL exit the position when strategy loss reaches 30% of initial premium

#### Scenario: Points stop loss
- **WHEN** user sets stop loss to 50 points
- **THEN** the backtest SHALL exit the position when strategy loss reaches 50 points

#### Scenario: Stop loss disabled
- **WHEN** user toggles stop loss off
- **THEN** the backtest SHALL hold positions until exit time regardless of loss

### Requirement: Target profit configuration
The panel SHALL support target profit in two modes: percentage of premium and absolute points. Target profit SHALL be optional. Default: disabled.

#### Scenario: Percentage target
- **WHEN** user sets target profit to 50% in percentage mode
- **THEN** the backtest SHALL exit the position when strategy profit reaches 50% of initial premium

#### Scenario: Target disabled
- **WHEN** user leaves target profit disabled
- **THEN** the backtest SHALL hold positions until exit time or stop loss

### Requirement: Trailing stop loss
The panel SHALL offer an optional trailing stop loss that adjusts the stop level as the position moves into profit. Configurable as percentage or points trail distance.

#### Scenario: Trailing SL enabled
- **WHEN** user enables trailing SL at 20 points
- **THEN** the backtest SHALL move the stop loss up by the profit amount minus 20 points as the position gains

#### Scenario: Trailing SL with initial SL
- **WHEN** user sets both initial SL (50 points) and trailing SL (20 points)
- **THEN** the initial SL SHALL apply first, then trailing SL SHALL activate once position is in profit

### Requirement: VIX filter
The panel SHALL allow filtering trading days by India VIX range. User can set minimum and/or maximum VIX threshold. Days outside the range SHALL be excluded from the backtest.

#### Scenario: VIX range set
- **WHEN** user sets VIX filter to 15-25
- **THEN** the backtest SHALL only simulate trades on days where India VIX was between 15 and 25

#### Scenario: No VIX filter
- **WHEN** user leaves VIX filter empty
- **THEN** all trading days in the date range SHALL be included

### Requirement: Day of week filter
The panel SHALL allow selecting which days of the week to include in the backtest. All weekdays SHALL be selected by default.

#### Scenario: Only expiry days
- **WHEN** user selects only Thursday
- **THEN** the backtest SHALL only simulate trades on Thursdays (weekly expiry days)

#### Scenario: Exclude Monday
- **WHEN** user deselects Monday
- **THEN** Mondays SHALL be excluded from the backtest simulation

### Requirement: Run backtest action
The panel SHALL have a "Run Backtest" button that validates all inputs and submits the strategy + configuration to the backend. The button SHALL be disabled while a backtest is running and display a progress indicator.

#### Scenario: Valid submission
- **WHEN** user clicks "Run Backtest" with valid strategy and config
- **THEN** the system SHALL submit the request, show a loading indicator, and navigate to results when complete

#### Scenario: Validation failure
- **WHEN** user clicks "Run Backtest" with invalid config (e.g., no legs)
- **THEN** the system SHALL highlight invalid fields and display specific error messages without submitting

### Requirement: Stop Loss scope toggle
Inside the Stop Loss section (visible only when SL is enabled) the panel SHALL expose a **"SL applies to"** toggle with two mutually exclusive options: **Per-leg** and **Combined**. Default is Per-leg. A caption SHALL describe the active mode:
- Per-leg: "Each leg exits at its own SL price; others continue."
- Combined: "Whole position exits when net P&L crosses threshold."

The selected mode SHALL be sent as `sl_scope: "per_leg" | "combined"` in the backtest request.

#### Scenario: Choose per-leg SL
- **WHEN** user leaves the default Per-leg selected and runs a short-straddle backtest
- **THEN** the backend SHALL evaluate each leg's premium independently against its own SL threshold and stop only breaching legs

#### Scenario: Choose combined SL
- **WHEN** user switches to Combined
- **THEN** the backend SHALL evaluate net strategy P&L against a single SL threshold and exit the whole position on breach — matching the pre-refinement behaviour
