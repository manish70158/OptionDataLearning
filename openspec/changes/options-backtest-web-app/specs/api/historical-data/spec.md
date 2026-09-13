## Purpose

Upstox API integration for fetching, caching, and serving 2 years of historical OHLCV and option chain data for NIFTY and BANKNIFTY to power backtest simulations.

## ADDED Requirements

### Requirement: Historical OHLCV data fetching
The system SHALL fetch daily OHLCV candle data for NIFTY 50 and BANKNIFTY indices from the Upstox API v2 historical candles endpoint. The system SHALL support fetching up to 2 years of data from the current date.

#### Scenario: Fetch NIFTY daily data
- **WHEN** a data sync is triggered for NIFTY with a 2-year range
- **THEN** the system SHALL call the Upstox historical candles API for instrument key `NSE_INDEX|Nifty 50` with interval `day` and store all OHLCV records

#### Scenario: Fetch BANKNIFTY daily data
- **WHEN** a data sync is triggered for BANKNIFTY with a 2-year range
- **THEN** the system SHALL call the Upstox historical candles API for instrument key `NSE_INDEX|Nifty Bank` with interval `day` and store all OHLCV records

### Requirement: Instruments master file parsing
The system SHALL download and parse the Upstox instruments master CSV file from `https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz`. The system SHALL build a lookup mapping `(underlying, strike, expiry, option_type)` → `instrument_key` for NSE_FO option contracts.

#### Scenario: Parse instruments CSV
- **WHEN** the instruments master file is downloaded
- **THEN** the system SHALL filter for rows where:
  - `exchange` = "NSE_FO" (not "NFO")
  - `instrument_type` = "OPTIDX"
  - `option_type` IN ("CE", "PE")
  - `name` IN ("NIFTY", "BANKNIFTY")
- **AND** the system SHALL extract `instrument_key`, `strike`, `expiry`, `option_type` columns (note: `strike` not `strike_price`)
- **AND** the system SHALL cache the mapping for option premium lookups

#### Scenario: Dynamic expiry resolution
- **WHEN** fetching option data for a given date
- **THEN** the system SHALL determine the nearest available expiry by:
  - Extracting all unique expiry dates from the instruments cache for that underlying
  - For weekly expiries: selecting the nearest expiry >= current date within 14 days
  - For monthly expiries: selecting the nearest expiry >= current date with day >= 20
- **AND** the system SHALL NOT assume expiries are on Thursdays (expiries can vary due to holidays, e.g., Tuesdays in September 2026)

### Requirement: Historical option chain data fetching
The system SHALL fetch end-of-day option premiums (OHLC) for all strikes within a relevant range of ATM for each trading day. The range SHALL cover ATM +/- 1000 points for NIFTY and ATM +/- 2000 points for BANKNIFTY.

#### Scenario: Option premium data for a trading day
- **WHEN** historical data is synced for a specific date
- **THEN** the system SHALL:
  - Load the instruments master and resolve the nearest expiry for that date
  - Calculate ATM strike from spot close price
  - Generate strike list: ATM +/- range at strike intervals (50 for NIFTY, 100 for BANKNIFTY)
  - For each strike and option type (CE/PE), resolve the instrument key from instruments cache
  - Fetch daily OHLC data from Upstox API for each option contract
  - Store open, high, low, close premiums in the option_premiums table
- **AND** the system SHALL always fetch option data for all trading days, even if OHLCV data already exists in cache

#### Scenario: Missing strike data
- **WHEN** a specific strike has no trading data for a given day (illiquid far-OTM strike)
- **THEN** the system SHALL skip that strike (instrument key not found or API returns no candles) and the backtest engine SHALL fall back to Black-Scholes estimation for that leg

### Requirement: Intraday candle data
The system SHALL fetch intraday candle data (5-minute intervals) for option contracts to enable intraday SL/TP simulation. At minimum, the system SHALL store high and low prices for each 5-minute interval during market hours (09:15-15:30 IST).

#### Scenario: Intraday data for SL simulation
- **WHEN** the backtest engine needs to check if SL was hit during a day
- **THEN** the system SHALL provide 5-minute interval high/low data for the option contracts, allowing the engine to determine the approximate time and level of SL trigger

### Requirement: Local data cache
The system SHALL cache all fetched historical data in a local SQLite database. Cache keys SHALL be: instrument, date, interval, and strike (for options). The cache SHALL avoid redundant API calls for already-fetched date ranges.

#### Scenario: Cache hit
- **WHEN** the backtest engine requests NIFTY data for a date already in cache
- **THEN** the system SHALL serve data from the local SQLite cache without calling the Upstox API

#### Scenario: Incremental OHLCV sync
- **WHEN** cache contains OHLCV data up to 2026-09-10 and user requests data through 2026-09-13
- **THEN** the system SHALL fetch only the missing OHLCV days (2026-09-11, 2026-09-12, 2026-09-13) from Upstox API
- **AND** the system SHALL fetch option premiums for ALL trading days in the requested range (including days that already have OHLCV data)

#### Scenario: Cache freshness
- **WHEN** the current day's data is requested before market close
- **THEN** the system SHALL NOT cache the current day's data (mark as incomplete) to avoid stale partial data

### Requirement: Data sync API endpoint
The system SHALL expose POST `/api/data/sync` to trigger data fetching. The endpoint SHALL accept: underlying (NIFTY or BANKNIFTY), start_date, end_date. It SHALL report progress and status.

#### Scenario: Trigger sync
- **WHEN** POST `/api/data/sync` is called with underlying=NIFTY, start_date=2024-09-13, end_date=2026-09-13
- **THEN** the system SHALL begin fetching data, return HTTP 202 with a task_id, and report sync progress via GET `/api/data/sync/{task_id}/status`

#### Scenario: Partial sync needed
- **WHEN** sync is requested for a date range where OHLCV data exists but option premium data is missing
- **THEN** the system SHALL skip fetching OHLCV but SHALL fetch all option premiums for the trading days in the range

### Requirement: Rate limit handling
The system SHALL respect Upstox API rate limits. When a 429 response is received, the system SHALL wait for the Retry-After duration and retry. The system SHALL batch requests with configurable delay between calls (default 250ms).

#### Scenario: Rate limited
- **WHEN** the Upstox API returns HTTP 429 during data sync
- **THEN** the system SHALL pause, wait for the Retry-After header duration, and resume fetching without data loss

### Requirement: Authentication
The system SHALL authenticate with the Upstox API using credentials from environment variables (UPSTOX_API_KEY, UPSTOX_API_SECRET, UPSTOX_ACCESS_TOKEN) or from `~/.upstox/config.json`. The system SHALL display a clear error if credentials are missing or expired.

#### Scenario: Valid credentials
- **WHEN** the server starts with valid Upstox credentials
- **THEN** the system SHALL successfully authenticate and be ready to fetch data

#### Scenario: Missing credentials
- **WHEN** the server starts without Upstox credentials configured
- **THEN** the system SHALL log a warning and the data sync endpoint SHALL return HTTP 401 with "Upstox credentials not configured"

#### Scenario: Expired token
- **WHEN** an API call fails with HTTP 401 (token expired)
- **THEN** the system SHALL return a clear error indicating the access token needs to be refreshed via Upstox OAuth flow

### Requirement: Upstox v3 intraday 5-minute fetching
The system SHALL fetch 5-minute option candles via **Upstox API v3** at `https://api.upstox.com/v3/historical-candle/{instrumentKey}/{unit}/{interval}/{to}/{from}` with `unit = "minutes"` and `interval = 5`. Upstox v2 SHALL NOT be used for intraday option candles because it only accepts `1minute`/`30minute`/`day`/`week`/`month` intervals. Each returned record SHALL be normalised to `{time: "HH:MM", open, high, low, close}` and stored in the `intraday_candles` table.

#### Scenario: Fetch 5-min candles for a day
- **WHEN** the engine requests 5-minute candles for a NIFTY option on a valid trading day
- **THEN** the system SHALL call the v3 endpoint and return approximately 75 candles spanning 09:15–15:30 IST, sorted ascending by time

#### Scenario: v2 rejection prevented
- **WHEN** a caller mistakenly passes `interval = "5minute"` to the v2 endpoint
- **THEN** the system SHALL NOT issue that request; the fetcher's public interface SHALL only expose the v3 path for sub-daily granularity below 30 minutes

### Requirement: On-demand intraday caching
When the backtest engine requests a leg price at a specific `time_hhmm`, the pricing layer SHALL check `intraday_candles` for that option-day and, if empty, fetch 5-minute candles from Upstox v3 and bulk-insert them. Subsequent requests for the same option-day SHALL be served from cache without additional API calls.

#### Scenario: Cache miss then hit
- **WHEN** backtest A requests the 09:20 entry premium for NIFTY 23250 CE on 2026-09-11 (no intraday rows exist)
- **THEN** the system SHALL fetch the day's 5-min candles from Upstox v3, insert them, and return the 09:20 bar's open
- **AND** a subsequent request for the same (instrument, date, strike, option_type, expiry) SHALL NOT trigger another network call

#### Scenario: Intraday unavailable
- **WHEN** Upstox v3 returns no candles for an option-day (illiquid strike, unlisted contract, credentials missing)
- **THEN** the pricing layer SHALL fall back to the cached daily premium, then to Black-Scholes estimation, without raising an error

### Requirement: Weekly expiry weekday inference
The system SHALL provide a helper that returns the modal weekday among near-term expiries in the instruments cache (excluding month-end monthlies where `day >= 20`). This helper SHALL be used by the backtest engine to project realistic DTE values when the resolved expiry from `_get_nearest_expiry` is more than 7 days from the trade date.

#### Scenario: Inferred weekday for NIFTY
- **WHEN** the instruments cache lists NIFTY weeklies on 2026-09-15, 2026-09-22, 2026-09-29 (all Tuesdays)
- **THEN** the helper SHALL return `1` (Tuesday) as the inferred weekly weekday

#### Scenario: No inferrable weekday
- **WHEN** the instruments cache contains only monthly expiries or is empty
- **THEN** the helper SHALL return `None` and the engine SHALL fall back to using the resolved expiry directly

### Requirement: SENSEX historical data support
The system SHALL fetch and cache historical data for SENSEX in addition to NIFTY and BANKNIFTY:
- Index OHLCV via instrument key `BSE_INDEX|SENSEX` and interval `day`.
- Instruments master parsing SHALL accept rows where `exchange = "BSE_FO"` and `name = "SENSEX"` (in addition to the existing `NSE_FO` filter for NIFTY/BANKNIFTY).
- Strike-range sync SHALL use ATM ± 2000 points at 100-point intervals.
- Rate limiting, retry, and cache behaviour SHALL match the existing NIFTY/BANKNIFTY path.

#### Scenario: SENSEX instruments loaded
- **WHEN** `fetch_instruments_master()` runs
- **THEN** the cache SHALL contain SENSEX option contracts under keys `(SENSEX, strike, expiry, CE/PE)` sourced from BSE_FO rows

#### Scenario: SENSEX daily OHLCV
- **WHEN** POST `/api/data/sync` is called with `underlying = "SENSEX"` and a 1-week range
- **THEN** the system SHALL fetch daily OHLCV via `BSE_INDEX|SENSEX` and option premiums for each strike within ATM ± 2000 at 100-point steps

### Requirement: NSE/BSE bhavcopy historical backfill
The system SHALL expose `POST /api/data/backfill-bhavcopy` which accepts `{underlying, start_date, end_date}` and, for each trading day in the range, downloads that day's F&O bhavcopy CSV, parses option contracts, and populates `option_premiums` with real daily OHLC + `nse_token` + `underlying_close` + calibrated `implied_vol` — including contracts whose expiry has already passed (which Upstox's live instruments master no longer lists).

- NSE URL: `https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip`
- BSE URL: `https://www.bseindia.com/download/Bhavcopy/Derivative/BhavCopy_BSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip`
- Parser handles the modern NSE column schema (`TradDt`, `XpryDt`, `StrkPric`, `OptnTp`, `TckrSymb`, `FinInstrmTp=IDO`, `OpnPric/HghPric/LwPric/ClsPric`, `UndrlygPric`, `FinInstrmId`).
- Progress SHALL stream through the shared task registry, pollable at `/api/data/sync/{task_id}/status`. Final message SHALL include daily-row count and intraday cache stats.

#### Scenario: Backfill historical daily premiums
- **WHEN** POST `/api/data/backfill-bhavcopy` is called with `underlying = "NIFTY"` and a 3-day window
- **THEN** for each business day the system SHALL download the day's bhavcopy zip, parse option rows, and INSERT OR REPLACE into `option_premiums` with `expiry` set to the contract's actual historical expiry (not the current-forward weekly)
- **AND** the response SHALL be a 202 with a `task_id` pollable at `/api/data/sync/{task_id}/status`

#### Scenario: Bhavcopy row includes NSE token
- **WHEN** the parser reads a row with `FinInstrmId = 46995` for NIFTY 24250 CE 2026-09-01
- **THEN** the inserted `option_premiums` row SHALL have `nse_token = 46995` so downstream code can construct the Upstox expired-instruments key `NSE_FO|46995|01-09-2026`

### Requirement: Calibrated implied volatility per bhavcopy row
Bhavcopy backfill SHALL reverse-BS the close premium into an implied volatility per (date, expiry, strike, option_type). The system SHALL persist `implied_vol` (decimal, e.g. 0.0973 for 9.73%) and `underlying_close` (spot at day close, from bhavcopy's `UndrlygPric`) on the same row. Rows whose close premium violates the intrinsic-value floor SHALL persist `implied_vol IS NULL`.

#### Scenario: IV calibration
- **WHEN** bhavcopy shows NIFTY 24200 CE 2026-08-25 weekly with `ClsPric = 61.75` and `UndrlygPric = 24334.55` at 0 DTE
- **THEN** the row SHALL be stored with `implied_vol = 0.0973` (approx) and `underlying_close = 24334.55`

#### Scenario: Arbitrage-violating close
- **WHEN** bhavcopy shows a call whose close price is below intrinsic value (e.g. deep-ITM stale close)
- **THEN** the row SHALL be stored with `implied_vol IS NULL` and BS fallback pricing SHALL use the coarse VIX estimate for that contract

### Requirement: Upstox expired-instruments intraday endpoint
The system SHALL fetch 1-minute historical candles for already-expired option contracts via Upstox v2 at `/v2/expired-instruments/historical-candle/{key}/{interval}/{to}/{from}` where the key format is `{EXCHANGE_PREFIX}|{NSE_FinInstrmId}|{DD-MM-YYYY_expiry}`. Interval SHALL be one of `1minute`, `30minute`, `day`. The system SHALL downsample 1-minute bars to 5-minute buckets (aligned on 09:15/09:20/…) before inserting into `intraday_candles`.

#### Scenario: Fetch real intraday for an expired weekly
- **WHEN** the system needs 5-min candles for NIFTY 24250 CE expiring 2026-09-01 on trade-date 2026-08-25
- **THEN** the system SHALL call `GET /v2/expired-instruments/historical-candle/NSE_FO%7C46995%7C01-09-2026/1minute/2026-08-25/2026-08-25`
- **AND** the response SHALL be 200 with ~375 one-minute candles
- **AND** the system SHALL bucket these into ~75 five-minute rows and INSERT into `intraday_candles`

### Requirement: Bhavcopy backfill also prefetches intraday
The bhavcopy backfill task SHALL, for each trading day and after daily rows are stored:
- Fetch and cache the day's 5-minute index intraday via `fetch_index_intraday(underlying, dt, "minutes", 5)`.
- Identify ATM from `UndrlygPric` and pick the two nearest expiries (relative to trade date).
- For each of those expiries, for strikes in `ATM ± STRIKE_WINDOW × strike_interval` (default `STRIKE_WINDOW = 5`), and for both CE and PE, call `fetch_expired_option_intraday` using the row's stored `nse_token` and insert the resulting 5-minute buckets into `intraday_candles`.
- Progress messages SHALL report `intraday cached: {ok} ok, {failed} skipped` per day.
- Any fetch failure counts as skipped; backtests will then fall back to BS with calibrated IV — no error is raised.

#### Scenario: Full day of pre-populated intraday
- **WHEN** bhavcopy backfill runs for a single NIFTY trading day
- **THEN** on completion the cache SHALL contain 5-min index intraday (~75 candles) plus 5-min intraday for `2 expiries × 11 strikes × 2 option_types = 44 contracts` (each ~77 candles), assuming no Upstox refusals
