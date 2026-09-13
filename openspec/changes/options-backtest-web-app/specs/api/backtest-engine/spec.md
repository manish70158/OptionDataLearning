## Purpose

REST API endpoint that accepts a multi-leg option strategy definition and backtest configuration, runs the simulation against historical data, and returns structured results.

## ADDED Requirements

### Requirement: Backtest execution endpoint
The API SHALL expose a POST endpoint at `/api/backtest` that accepts a JSON payload containing the strategy definition (legs, underlying, expiry type) and backtest configuration (date range, entry/exit times, SL, TP, trailing SL, filters). The endpoint SHALL return structured JSON results.

#### Scenario: Successful backtest
- **WHEN** a valid POST request is sent to `/api/backtest` with a complete strategy and config
- **THEN** the API SHALL return HTTP 200 with JSON containing: summary statistics, daily trade records, equity curve data, and drawdown series

#### Scenario: Invalid strategy
- **WHEN** a POST request is sent with zero legs or invalid leg parameters
- **THEN** the API SHALL return HTTP 422 with a JSON error body listing the specific validation failures

#### Scenario: No historical data available
- **WHEN** a backtest is requested for a date range where historical data has not been fetched
- **THEN** the API SHALL return HTTP 400 with message "Historical data not available for the requested date range. Please sync data first."

### Requirement: Strategy definition schema
The strategy definition SHALL include: underlying (NIFTY or BANKNIFTY), expiry type (weekly or monthly), and an array of legs. Each leg SHALL specify: position (buy or sell), option_type (CE or PE), strike_offset (integer, points relative to ATM), and lots (positive integer).

#### Scenario: Multi-leg strategy
- **WHEN** a request includes 4 legs defining an Iron Condor on NIFTY weekly
- **THEN** the engine SHALL simulate all 4 legs as a combined position, calculating net premium at entry and net P&L at exit

#### Scenario: Single leg strategy
- **WHEN** a request includes 1 leg (Buy 1 lot ATM CE)
- **THEN** the engine SHALL simulate a naked long call position

### Requirement: Simulation logic
The engine SHALL simulate each trading day in the date range as follows: at entry time, price each leg using the historical option premium closest to the configured strike; track position P&L through the day using OHLCV data; apply exit rules (SL, TP, trailing SL) based on intraday price movement; exit remaining positions at exit time.

#### Scenario: Intraday stop loss hit
- **WHEN** the combined strategy P&L reaches the stop loss threshold during the trading day
- **THEN** the engine SHALL record exit at the stop loss level with exit_reason "stop_loss" and the approximate exit time

#### Scenario: Target profit hit
- **WHEN** the combined strategy P&L reaches the target profit threshold
- **THEN** the engine SHALL record exit at the target level with exit_reason "target_profit"

#### Scenario: Time-based exit
- **WHEN** neither SL nor TP is triggered during the day
- **THEN** the engine SHALL exit all positions at the configured exit time with exit_reason "time_exit"

### Requirement: Result schema
The backtest result SHALL include: summary object (total_pnl, num_trades, win_rate, max_drawdown, max_drawdown_pct, sharpe_ratio, avg_win, avg_loss, profit_factor, max_consecutive_wins, max_consecutive_losses), trades array (one object per trading day with date, entry_time, exit_time, entry_premium, exit_premium, pnl_points, exit_reason, cumulative_pnl, vix), equity_curve array (date + cumulative_pnl pairs), drawdown array (date + drawdown_pct pairs), monthly_pnl object (year-month keys with total P&L values).

#### Scenario: Complete result returned
- **WHEN** a backtest completes over 250 trading days
- **THEN** the result SHALL contain exactly 250 entries in the trades array, 250 entries in the equity curve, and month-by-month breakdown in monthly_pnl

### Requirement: Backtest progress reporting
For long-running backtests, the API SHALL support progress reporting. The endpoint SHALL return a task ID, and the client SHALL poll a GET endpoint `/api/backtest/{task_id}/status` for progress.

#### Scenario: Long backtest with progress
- **WHEN** a backtest covers 2 years of data
- **THEN** the API SHALL return HTTP 202 with a task_id, and the status endpoint SHALL report progress as percentage (0-100) until completion

#### Scenario: Completed task retrieval
- **WHEN** client polls `/api/backtest/{task_id}/status` after completion
- **THEN** the API SHALL return status "completed" with the full result payload

### Requirement: Saved backtest retrieval
The API SHALL expose GET `/api/backtest/{backtest_id}` to retrieve previously completed and saved backtest results.

#### Scenario: Retrieve saved backtest
- **WHEN** a GET request is sent with a valid backtest_id
- **THEN** the API SHALL return the full result payload including strategy config and results

#### Scenario: Invalid backtest ID
- **WHEN** a GET request is sent with a non-existent backtest_id
- **THEN** the API SHALL return HTTP 404 with message "Backtest not found"

### Requirement: Days-to-expiry on trade records
Each trade record in the result SHALL include `dte` (integer days between trade date and the effective expiry) and `expiry_date` (ISO date string of the effective expiry used for DTE display). Because the Upstox instruments master only lists live/future contracts, the engine SHALL infer the weekly-expiry weekday from the modal weekday of near-term cached expiries (excluding month-end monthlies), then use the resolved expiry when it is within 7 days of the trade date and otherwise project to the next occurrence of the inferred weekday.

#### Scenario: Expiry-day trade
- **WHEN** a NIFTY weekly backtest includes a trading day whose weekday matches the inferred weekly-expiry weekday
- **THEN** the trade record for that day SHALL have `dte = 0` and `expiry_date` equal to that day's date

#### Scenario: Historical date beyond cached expiries
- **WHEN** the resolved nearest expiry from the instruments master is more than 7 days away because only a distant future expiry is cached (e.g. an August trade against a September monthly)
- **THEN** the engine SHALL substitute the projected weekly expiry (based on inferred weekday) and set `dte` accordingly rather than emitting a distant DTE (30+)

### Requirement: Intraday-aware entry and exit pricing
For each leg, the engine SHALL price entry and exit using the 5-minute option candle at or after the configured `entry_time`/`exit_time`. When intraday data is unavailable (no credentials, no network, unlisted contract, illiquid strike), the engine SHALL fall back to the cached daily open/close premium, and finally to Black-Scholes estimation.

#### Scenario: Real 5-min entry price
- **WHEN** `entry_time` is 09:20 and a 5-minute intraday candle exists for the option contract at 09:20
- **THEN** the engine SHALL use that candle's open as the leg's entry premium and mark the record `pricing_source = "real"`

#### Scenario: Fallback to daily open
- **WHEN** the intraday fetch fails or returns no candles
- **THEN** the engine SHALL fall back to the cached daily open premium; if that is also missing it SHALL fall back to Black-Scholes with `pricing_source = "estimated"`

### Requirement: Real exit P&L on time-based exits
When no intraday SL/TP triggers, `exit_pnl` SHALL be computed from the real per-leg 5-minute exit prices: `exit_pnl = entry_total + exit_total - 2 * n_legs * lot_size` (slippage matches the intraday-evaluation formula). The `exit_premium` displayed in the trade log SHALL be `abs(exit_total)/lot_size` on time-exit. On intraday SL/TP exits (which trigger against Black-Scholes intraday estimates), `exit_premium` MAY be back-calculated as `entry_premium + pnl_points` since no observed intraday trigger price exists.

#### Scenario: Time-exit displays real 15:15 premium
- **WHEN** a single-leg long CE trade time-exits on 2026-09-11 with `exit_time = 15:15` and the real 5-min bar at 15:15 opens at ₹241.70
- **THEN** the trade record SHALL show `exit_premium = 241.70`, not a Black-Scholes estimate

#### Scenario: Multi-leg net exit premium
- **WHEN** an Iron Condor time-exits with real 5-min prices for each of 4 legs
- **THEN** `exit_premium` SHALL be the absolute net cash flow per lot from closing all four legs, computed from the summed leg prices with buy/sell signs

### Requirement: SENSEX as supported underlying
The strategy definition SHALL accept `underlying = "SENSEX"` in addition to `NIFTY` and `BANKNIFTY`. The engine SHALL use SENSEX-specific constants: `lot_size = 20`, `strike_interval = 100`, `strike_range = ±2000`, and index instrument key `BSE_INDEX|SENSEX`. The weekly-expiry weekday for SENSEX SHALL be inferred from the instruments cache (no hard-coded weekday).

#### Scenario: SENSEX strategy accepted
- **WHEN** a POST `/api/backtest` request has `strategy.underlying = "SENSEX"` and legs at ATM ± 100 strike offsets
- **THEN** the engine SHALL run the backtest, compute ATM as `round(spot/100)*100`, and return `total_pnl_inr = total_pnl * 20`

#### Scenario: SENSEX weekly expiry inference
- **WHEN** the instruments cache lists SENSEX weekly expiries on a specific weekday
- **THEN** the engine SHALL use that weekday when projecting DTE for historical SENSEX trade dates

### Requirement: Historical expiry calendar
The engine SHALL resolve trade-date expiries using a rule-based historical calendar (`WEEKLY_EXPIRY_WEEKDAY` per underlying plus a `HOLIDAYS` set), NOT the Upstox live-instruments master, because the live master only lists currently-live contracts and would misattribute historical trades to a future weekly. The calendar SHALL support weekday transitions per underlying (e.g. NIFTY Thursday → Wednesday Nov 2024 → Thursday Apr 2025 → Tuesday Sep 2025) and SHALL shift back to the previous business day when the computed expiry lands on a holiday or weekend.

#### Scenario: Historical 0-DTE trade
- **WHEN** a NIFTY backtest includes 2026-08-25 (Tuesday, weekly-expiry weekday under Sep-2025+ rule)
- **THEN** the trade record's `dte` SHALL equal 0 and `expiry_date` SHALL equal `2026-08-25`

#### Scenario: Holiday shift-back
- **WHEN** the calendar's weekday rule places expiry on a listed market holiday (e.g. Holi)
- **THEN** the engine SHALL shift the resolved expiry back to the previous business day (matching NSE / BSE convention)

### Requirement: ATM computed at entry_time
ATM strike SHALL be computed from the index spot at the configured `entry_time`, NOT from the daily open (which is the 9:15 opening tick and misrepresents any entry later in the day). The engine SHALL fetch and cache 5-minute index intraday candles for each trading day; on cache miss the engine SHALL fetch on demand via Upstox v3.

#### Scenario: 15:14 entry after intraday move
- **WHEN** entry_time is 15:14 and the day's 5-min index candle at 15:14 shows spot=24463.45
- **THEN** ATM SHALL be `round(24463.45 / strike_interval) * strike_interval` (24450 for NIFTY), not `round(daily_open / interval) * interval`

### Requirement: Per-leg vs Combined stop loss
The engine SHALL support two SL scopes via `config.sl_scope`:
- `combined` (previous behaviour): whole position exits when net strategy P&L crosses the SL threshold.
- `per_leg` (default): each leg exits independently when its own premium crosses its per-leg SL price.

For per-leg mode:
- SELL leg SL price = `entry_premium × (1 + pct)` (or `entry_premium + points`)
- BUY leg SL price = `entry_premium × (1 − pct)` (or `entry_premium − points`)
- The engine SHALL check cached 5-min per-leg option candles between `entry_time` and `exit_time` and record the FIRST bar whose high (sell) or low (buy) crosses the SL price.
- When per-leg intraday data is not available, the engine SHALL BS-simulate the leg's intraday journey using each cached 5-min index candle's spot high/low (option-type-adverse) plus the per-contract calibrated IV.
- Stopped legs SHALL exit at the SL price with `source: "stop_loss"`; non-stopped legs continue to `exit_time`.
- Aggregate `exit_reason` SHALL be `stop_loss` when all legs stopped or `stop_loss (partial)` when only some legs stopped.

Trailing SL SHALL remain combined-only.

#### Scenario: One leg of a straddle stops, the other continues
- **WHEN** a short 24250 straddle enters with CE=₹20 and PE=₹99 and per-leg 50% SL is enabled
- **THEN** the CE SHALL exit at ₹30 with `source: "stop_loss"` on the first bar its high crosses ₹30
- **AND** the PE SHALL continue to `exit_time` and exit at its real 5-min bar price with `source: "real"` or `"iv_calibrated"`
- **AND** the trade record SHALL show `exit_reason = "stop_loss (partial)"`

### Requirement: Real intraday premiums for expired contracts
When the engine needs a leg's premium at a specific intraday time and the option contract is already expired (not in Upstox's live instruments master), the engine SHALL fetch real 5-minute intraday premiums via Upstox's expired-instruments historical-candle endpoint using the NSE token stored in `option_premiums.nse_token` (populated during bhavcopy backfill). Only when that call fails SHALL the engine fall back to BS with the calibrated IV, and only when there is no calibrated IV SHALL the engine fall back to the coarse VIX-derived estimate.

#### Scenario: Real 5-min bars for a 0-DTE historical Tuesday
- **WHEN** a NIFTY backtest on 2026-08-25 needs the 24250 CE premium at 09:20 and bhavcopy backfill has run for that date
- **THEN** the engine SHALL request `/v2/expired-instruments/historical-candle/NSE_FO|{token}|25-08-2026/1minute/2026-08-25/2026-08-25`
- **AND** downsample the returned 1-min bars into 5-min buckets, insert into `intraday_candles`
- **AND** return the 09:20 bucket's open as the entry premium with `source: "real"`

#### Scenario: Fallback ladder
- **WHEN** the leg's per-contract intraday cache is empty and Upstox's expired-instruments endpoint fails or the row lacks `nse_token`
- **THEN** the engine SHALL fall back to Black-Scholes using the calibrated IV from `option_premiums.implied_vol` at the index-intraday spot for that time, returning `source: "iv_calibrated"`
- **AND** when there is no calibrated IV, SHALL fall back to the coarse spot-range VIX estimate with `source: "estimated"`

### Requirement: Time-exit P&L uses real per-leg prices
When a trade time-exits (no intraday SL/TP trigger), the engine SHALL compute exit P&L from the real per-leg 5-minute prices at `exit_time` (via the fallback ladder above), NOT from Black-Scholes at `spot_close`. Aggregate `exit_premium` displayed in the trade log SHALL be `abs(exit_total)/lot_size` — the true net premium of closing all legs at the observed exit-time prices.

#### Scenario: Time-exit exit premium matches real 5-min bar
- **WHEN** a 24250 CE single-leg buy exits at 15:15 with the 15:15 5-min bar showing open=₹241.70
- **THEN** the trade record's `exit_premium` SHALL be ₹241.70, not a BS-at-spot-close estimate

### Requirement: Calibrated implied volatility per contract per day
The pricing engine SHALL persist an implied volatility per (instrument, date, expiry, strike, option_type) derived by reverse-Black-Scholes from the day's close premium (via bhavcopy). BS fallback pricing SHALL prefer this calibrated IV over the coarse spot-range VIX estimate whenever it is available. Rows where the close premium violates the intrinsic-value floor SHALL persist `implied_vol IS NULL` and fall through to the coarser estimator.

#### Scenario: BS pricing with calibrated IV
- **WHEN** a 24200 CE 08-25 weekly is needed at 15:14 spot=24182.80 and its cached `implied_vol` is 0.0973 (9.73%)
- **THEN** BS SHALL use `sigma = 0.0973` (skew = 1.0), not the coarse VIX estimate — producing a premium consistent with the observed close IV rather than a hard-coded 10% guess
