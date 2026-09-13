## Purpose

Upstox API client that fetches live NIFTY and BANKNIFTY option chain data for real-time strategy evaluation and daily recommendation generation.

## ADDED Requirements

### Requirement: Authentication with Upstox API
The system SHALL authenticate with the Upstox API using API key, API secret, and access token. Credentials SHALL be read from environment variables (`UPSTOX_API_KEY`, `UPSTOX_API_SECRET`, `UPSTOX_ACCESS_TOKEN`) or a local config file (`~/.upstox/config.json`). Environment variables SHALL take precedence over config file values.

#### Scenario: Successful authentication via environment variables
- **WHEN** `UPSTOX_API_KEY`, `UPSTOX_API_SECRET`, and `UPSTOX_ACCESS_TOKEN` are set
- **THEN** the system SHALL use these credentials to authenticate API requests

#### Scenario: Fallback to config file
- **WHEN** environment variables are not set but `~/.upstox/config.json` exists with valid credentials
- **THEN** the system SHALL read and use credentials from the config file

#### Scenario: Missing credentials
- **WHEN** neither environment variables nor config file provide valid credentials
- **THEN** the system SHALL raise a clear error message listing which credentials are missing and how to configure them

### Requirement: Fetch option chain data
The system SHALL fetch the full option chain for a given underlying (NIFTY or BANKNIFTY) and expiry date from the Upstox API. The fetched data SHALL include: strike price, call/put LTP (last traded price), call/put bid-ask spread, call/put open interest, call/put volume, and call/put Greeks (delta, gamma, theta, vega) when available.

#### Scenario: Fetch NIFTY weekly option chain
- **WHEN** the system requests the option chain for NIFTY with the nearest weekly expiry
- **THEN** it SHALL return a structured list of strike-level records containing LTP, OI, volume, and Greeks for both call and put at each strike

#### Scenario: API rate limiting
- **WHEN** the Upstox API returns a rate-limit response (HTTP 429)
- **THEN** the system SHALL wait for the duration specified in the Retry-After header (or 1 second default) and retry up to 3 times

#### Scenario: API unavailability
- **WHEN** the Upstox API is unreachable or returns HTTP 5xx
- **THEN** the system SHALL log the error and raise an exception with a descriptive message, without crashing the entire application

### Requirement: Expiry date resolution
The system SHALL determine the nearest weekly and monthly expiry dates for NIFTY and BANKNIFTY. It SHALL support fetching option chains for: the nearest weekly expiry, the nearest monthly expiry, or a specific user-provided expiry date.

#### Scenario: Auto-resolve nearest weekly expiry
- **WHEN** the system is asked for the "nearest weekly" option chain on a Monday
- **THEN** it SHALL resolve the expiry to the upcoming Thursday (NIFTY weekly expiry day) and fetch that chain

#### Scenario: User-specified expiry date
- **WHEN** the user provides a specific expiry date (e.g., "2026-09-24")
- **THEN** the system SHALL fetch the option chain for that exact expiry without auto-resolution

### Requirement: Option chain caching
The system SHALL cache fetched option chain data for a configurable duration (default: 5 minutes) to avoid redundant API calls within the same session. The cache SHALL be keyed by underlying symbol + expiry date.

#### Scenario: Cache hit within TTL
- **WHEN** the option chain for NIFTY 2026-09-17 was fetched 2 minutes ago and TTL is 5 minutes
- **THEN** the system SHALL return the cached data without making an API call

#### Scenario: Cache miss after TTL
- **WHEN** the option chain for NIFTY 2026-09-17 was fetched 6 minutes ago and TTL is 5 minutes
- **THEN** the system SHALL fetch fresh data from the API and update the cache
