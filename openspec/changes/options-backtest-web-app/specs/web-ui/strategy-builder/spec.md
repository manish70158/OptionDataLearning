## Purpose

Interactive multi-leg option strategy builder that lets traders visually construct option positions by selecting underlying, adding/removing legs with strike configuration, position type, and lot sizing.

## ADDED Requirements

### Requirement: Underlying selection
The strategy builder SHALL display a dropdown to select the underlying instrument. Supported underlyings SHALL include NIFTY, BANKNIFTY, and SENSEX. The selected underlying SHALL determine available expiry dates, lot size, and strike interval used elsewhere in the app.

#### Scenario: User selects underlying
- **WHEN** user opens the strategy builder page
- **THEN** a dropdown SHALL display NIFTY, BANKNIFTY, and SENSEX as options, with NIFTY selected by default

#### Scenario: Changing underlying resets legs
- **WHEN** user changes the underlying (e.g., NIFTY → BANKNIFTY, or BANKNIFTY → SENSEX) while legs are configured
- **THEN** the system SHALL reset all leg strike selections to reflect the new strike interval (50 for NIFTY, 100 for BANKNIFTY and SENSEX) and update available expiry dates

#### Scenario: SENSEX selected
- **WHEN** user selects SENSEX
- **THEN** strike offsets in each leg SHALL step in 100-point increments and downstream backtest results SHALL use lot_size=20 when computing INR P&L

### Requirement: Expiry type selection
The strategy builder SHALL allow selecting between weekly and monthly expiry types. The selected expiry type SHALL affect which expiry dates are available for backtesting.

#### Scenario: Weekly expiry selected
- **WHEN** user selects "Weekly" expiry type
- **THEN** the system SHALL use weekly expiry dates (Thursdays) for the backtest simulation

#### Scenario: Monthly expiry selected
- **WHEN** user selects "Monthly" expiry type
- **THEN** the system SHALL use monthly expiry dates (last Thursday of each month) for the backtest simulation

### Requirement: Add option leg
The strategy builder SHALL allow adding up to 8 option legs to a strategy. Each leg SHALL have: position type (Buy/Sell), option type (CE/PE), strike selection relative to ATM (e.g., ATM, ATM+50, ATM-100, ATM+200), and number of lots.

#### Scenario: Adding a first leg
- **WHEN** user clicks "Add Leg"
- **THEN** a new leg row SHALL appear with defaults: Buy, CE, ATM, 1 lot

#### Scenario: Configuring a leg
- **WHEN** user sets a leg to Sell PE ATM-100 with 2 lots
- **THEN** the leg row SHALL display "Sell 2x PE ATM-100" and the strategy summary SHALL update to reflect this leg

#### Scenario: Maximum legs reached
- **WHEN** the strategy already has 8 legs
- **THEN** the "Add Leg" button SHALL be disabled with a tooltip indicating the maximum has been reached

### Requirement: Remove option leg
The strategy builder SHALL allow removing any individual leg. At least 1 leg MUST remain for a valid strategy.

#### Scenario: Removing a leg
- **WHEN** user clicks the remove button on a leg and more than 1 leg exists
- **THEN** that leg SHALL be removed and the strategy summary SHALL update

#### Scenario: Cannot remove last leg
- **WHEN** only 1 leg remains
- **THEN** the remove button SHALL be disabled

### Requirement: Strike selection
Strike selection SHALL be relative to ATM (At The Money). Available offsets SHALL be based on the underlying's strike interval: 50 points for NIFTY, 100 points for BANKNIFTY. The range SHALL cover ATM-1000 to ATM+1000.

#### Scenario: NIFTY strike options
- **WHEN** underlying is NIFTY
- **THEN** strike dropdown SHALL show options in 50-point increments: ATM-1000, ATM-950, ..., ATM, ..., ATM+950, ATM+1000

#### Scenario: BANKNIFTY strike options
- **WHEN** underlying is BANKNIFTY
- **THEN** strike dropdown SHALL show options in 100-point increments: ATM-1000, ATM-900, ..., ATM, ..., ATM+900, ATM+1000

### Requirement: Preset strategy templates
The builder SHALL offer preset templates for common strategies: Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, Strangle, Short Straddle, Short Strangle. Selecting a template SHALL populate the legs automatically.

#### Scenario: Loading a preset
- **WHEN** user selects "Iron Condor" from the template dropdown
- **THEN** the builder SHALL populate 4 legs: Sell CE ATM+100, Buy CE ATM+200, Sell PE ATM-100, Buy PE ATM-200, each with 1 lot

#### Scenario: Template does not lock editing
- **WHEN** user loads a preset template
- **THEN** all leg fields SHALL remain editable, allowing customization of the template

### Requirement: Strategy summary
The builder SHALL display a real-time summary showing: total legs, net position (debit/credit indicator), max profit potential, max loss potential, and breakeven points — all calculated from the current leg configuration.

#### Scenario: Summary updates on leg change
- **WHEN** user modifies any leg parameter
- **THEN** the summary SHALL recalculate and display updated values within 500ms

#### Scenario: Incomplete strategy
- **WHEN** no legs are configured
- **THEN** the summary SHALL display "Add legs to see strategy summary"
