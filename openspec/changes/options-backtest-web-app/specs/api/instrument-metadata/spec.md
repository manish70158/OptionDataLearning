## Purpose

API endpoints that provide available underlyings, expiry dates, and strike prices to populate the strategy builder's dropdown menus and validate user inputs.

## ADDED Requirements

### Requirement: List available underlyings
The API SHALL expose GET `/api/instruments/underlyings` returning the list of supported underlyings with their metadata (name, lot size, strike interval, trading symbol).

#### Scenario: Get underlyings
- **WHEN** GET `/api/instruments/underlyings` is called
- **THEN** the API SHALL return JSON array with entries for NIFTY (lot_size=65, strike_interval=50), BANKNIFTY (lot_size=30, strike_interval=100), and SENSEX (lot_size=20, strike_interval=100)

### Requirement: Data status includes historical + intraday coverage
The system SHALL expose per-underlying historical data coverage via `/api/data/status`, showing the first/last cached dates and count of trading days for the daily option premium cache. The UI SHALL render this alongside a freshness label that considers weekdays only (a cache ending on Friday when today is Sunday SHALL read "current", not "2 days behind").

#### Scenario: Weekend-aware freshness label
- **WHEN** today is Sunday and the underlying's `last_date` is the previous Friday
- **THEN** the freshness label SHALL read "current" — the intervening weekend is not counted as trading days behind

### Requirement: List expiry dates
The API SHALL expose GET `/api/instruments/{underlying}/expiries` returning available expiry dates for the given underlying within the cached data range. The response SHALL distinguish weekly and monthly expiries.

#### Scenario: Get NIFTY expiries
- **WHEN** GET `/api/instruments/NIFTY/expiries` is called
- **THEN** the API SHALL return a JSON object with `weekly` (array of Thursday dates) and `monthly` (array of last-Thursday-of-month dates) within the available data range

#### Scenario: No data available
- **WHEN** no historical data has been synced for the requested underlying
- **THEN** the API SHALL return HTTP 200 with empty arrays and a `data_available: false` flag

### Requirement: List available strikes
The API SHALL expose GET `/api/instruments/{underlying}/strikes` returning available strike prices for a given date and expiry. Query parameters: `date` (trading date) and `expiry_date`.

#### Scenario: Get strikes for a date
- **WHEN** GET `/api/instruments/NIFTY/strikes?date=2026-01-15&expiry_date=2026-01-16` is called
- **THEN** the API SHALL return an array of available strike prices sorted ascending, along with the ATM strike for that date

#### Scenario: Date not in cache
- **WHEN** the requested date is not in the historical data cache
- **THEN** the API SHALL return HTTP 404 with "No data available for the requested date"

### Requirement: Data availability status
The API SHALL expose GET `/api/data/status` returning the current state of the historical data cache: date ranges available per underlying, total trading days cached, last sync time, and cache size.

#### Scenario: Check data status
- **WHEN** GET `/api/data/status` is called
- **THEN** the API SHALL return JSON with per-underlying entries showing first_date, last_date, trading_days_count, last_sync_timestamp, and cache_size_mb

#### Scenario: Empty cache
- **WHEN** no data has been synced
- **THEN** the API SHALL return JSON with empty entries and a message "No data synced. Call POST /api/data/sync to fetch historical data."
