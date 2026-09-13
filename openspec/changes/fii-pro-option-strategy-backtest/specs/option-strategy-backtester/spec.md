## Purpose

Backtesting engine that simulates options strategies (Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, Strangle) against historical NIFTY data to calculate P&L for each FII View × PRO View combination.

## ADDED Requirements

### Requirement: Strategy definitions
The system SHALL support the following option strategies: Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, and Strangle. Each strategy SHALL be defined by its leg structure (number of legs, option types, strike offsets from ATM) and payoff function.

#### Scenario: Iron Condor definition
- **WHEN** the system initializes an Iron Condor strategy
- **THEN** it SHALL construct 4 legs: sell OTM call, buy further OTM call, sell OTM put, buy further OTM put, with configurable strike offsets from ATM

#### Scenario: Iron Butterfly definition
- **WHEN** the system initializes an Iron Butterfly strategy
- **THEN** it SHALL construct 4 legs: sell ATM call, sell ATM put, buy OTM call, buy OTM put, with configurable wing widths

#### Scenario: Bull Call Spread definition
- **WHEN** the system initializes a Bull Call Spread strategy
- **THEN** it SHALL construct 2 legs: buy ATM/ITM call, sell OTM call, with configurable strike separation

#### Scenario: Bear Put Spread definition
- **WHEN** the system initializes a Bear Put Spread strategy
- **THEN** it SHALL construct 2 legs: buy ATM/ITM put, sell OTM put, with configurable strike separation

#### Scenario: Straddle definition
- **WHEN** the system initializes a Straddle strategy
- **THEN** it SHALL construct 2 legs: buy ATM call and buy ATM put at the same strike

#### Scenario: Strangle definition
- **WHEN** the system initializes a Strangle strategy
- **THEN** it SHALL construct 2 legs: buy OTM call and buy OTM put, with configurable strike offsets from ATM

### Requirement: Premium estimation from VIX
The system SHALL estimate option premiums using VIX-derived implied volatility when historical option chain data is unavailable. The estimation SHALL use the Black-Scholes model with VIX as the annualized volatility input, NIFTY open as the underlying price, and appropriate time-to-expiry based on the day's distance to the next expiry.

#### Scenario: Premium calculation for a trading day
- **WHEN** the backtester processes a trading day with VIX open = 20.0, NIFTY open = 11200, and 3 days to weekly expiry
- **THEN** it SHALL calculate option premiums for all required strikes using Black-Scholes with IV = 20%, S = 11200, T = 3/365, and risk-free rate from configuration

#### Scenario: Expiry day premium handling
- **WHEN** the backtester processes an expiry day (is_nifty_expiry = 1)
- **THEN** it SHALL use T = 1/365 (or intraday fraction) for premium calculation, reflecting rapid time decay

### Requirement: Daily P&L simulation
The system SHALL simulate entry at market open and exit at market close for each trading day. Entry premiums SHALL be calculated using NIFTY open and VIX open. Exit premiums SHALL be calculated using NIFTY close and VIX close. The daily P&L SHALL be the difference between entry and exit portfolio values, accounting for all legs.

#### Scenario: Profitable Iron Condor day
- **WHEN** the backtester runs Iron Condor on a day where NIFTY stays within the sold strikes (open = 11200, high = 11250, low = 11150, close = 11210)
- **THEN** the P&L SHALL be positive, reflecting premium collected minus reduced premium at close

#### Scenario: Losing directional day for Iron Condor
- **WHEN** the backtester runs Iron Condor on a day where NIFTY moves beyond a sold strike (open = 11200, close = 11500, range = 3%)
- **THEN** the P&L SHALL be negative, reflecting the loss on the breached side minus premium collected on the safe side

### Requirement: Intraday max loss tracking
The system SHALL track the maximum adverse excursion during the day using the intraday high and low prices. For each strategy on each day, the system SHALL record the worst-case intraday P&L (using NIFTY high for short call exposure and NIFTY low for short put exposure) in addition to the close-to-close P&L.

#### Scenario: Intraday drawdown exceeds close P&L
- **WHEN** NIFTY opens at 11200, drops to 11050 intraday (low), but closes at 11180
- **THEN** the system SHALL record both the close P&L (based on 11180) and the max intraday loss (based on 11050), with the intraday loss being worse

### Requirement: Strike selection relative to ATM
The system SHALL select strikes relative to the ATM strike at market open. ATM SHALL be the NIFTY strike nearest to NIFTY open (rounded to the nearest 50-point strike for NIFTY). OTM strike offsets SHALL be configurable, defaulting to: 100 points for Iron Condor short legs, 200 points for Iron Condor long legs, 200 points for Straddle/Strangle offsets, and 100 points for spread widths.

#### Scenario: ATM strike determination
- **WHEN** NIFTY opens at 11234
- **THEN** the ATM strike SHALL be 11250 (nearest 50-point increment)

#### Scenario: Configurable strike offsets
- **WHEN** a user configures Iron Condor with short_offset=150, wing_width=100
- **THEN** the system SHALL use strikes at ATM+150 (short call), ATM+250 (long call), ATM-150 (short put), ATM-250 (long put)

### Requirement: Backtest aggregation by FII/PRO combination
The system SHALL aggregate backtest results by each unique FII View × PRO View combination. For each combination and each strategy, the system SHALL compute: total P&L, average daily P&L, win rate (% of days with positive P&L), maximum single-day loss, maximum drawdown over consecutive losing days, and Sharpe-like ratio (average P&L / std deviation of daily P&L).

#### Scenario: Aggregation for a high-frequency combination
- **WHEN** the backtest completes for the Neutral × Neutral combination (328 days)
- **THEN** the system SHALL produce metrics for all 6 strategies, each with total P&L, avg daily P&L, win rate, max loss, max drawdown, and risk-adjusted ratio

#### Scenario: Aggregation for a low-frequency combination
- **WHEN** the backtest completes for a combination with fewer than 5 days
- **THEN** the system SHALL still compute all metrics but flag the result as "low sample size" in the output

### Requirement: Expiry vs non-expiry segmentation
The system SHALL separately compute all aggregation metrics for expiry days and non-expiry days within each FII/PRO combination, in addition to the combined total.

#### Scenario: Expiry segmentation output
- **WHEN** the backtest aggregates results for Neutral × Bearish (84 total days, 18 expiry, 66 non-expiry)
- **THEN** the output SHALL contain three rows per strategy: combined (84 days), expiry-only (18 days), non-expiry-only (66 days)
