## Why

The existing option backtester is a CLI-only Python tool. Traders need a visual, interactive web interface (similar to algotest.in/backtest) where they can build custom multi-leg option strategies, configure risk parameters, and see backtest results with charts — all without touching the command line. Using Upstox API for real historical OHLCV data (last 2 years) replaces the current Black-Scholes estimation with actual market prices, producing more accurate backtest results.

## What Changes

- **New web application**: A full-stack web app with a React frontend and FastAPI backend that lets users visually build and backtest NIFTY/BANKNIFTY option strategies
- **Strategy Builder UI**: Interactive form to add/remove option legs (Buy/Sell, CE/PE, strike selection relative to ATM), set lots, choose underlying and expiry type
- **Backtest Configuration Panel**: Date range picker (up to 2 years), entry/exit time selection, stop loss and target profit settings (points or %), trailing SL, VIX filters, day-of-week filters
- **Results Dashboard**: Equity curve chart, drawdown chart, monthly P&L heatmap, trade log table, summary statistics (total P&L, win rate, max drawdown, Sharpe ratio, avg profit/loss per trade)
- **Upstox Historical Data Integration**: Backend service to fetch and cache 2 years of NIFTY/BANKNIFTY OHLCV and option chain data via Upstox API v2
- **Backtest Engine (web-adapted)**: Server-side engine that takes user-defined strategy legs plus configuration and simulates trades against historical data, returning structured results to the frontend

## Capabilities

### New Capabilities
- `web-ui/strategy-builder`: Interactive multi-leg option strategy builder with underlying selection, strike configuration (ATM-relative), position type, and lot sizing
- `web-ui/backtest-config`: Backtest parameter configuration — date range, entry/exit times, stop loss, target profit, trailing SL, VIX filter, weekday filter
- `web-ui/results-dashboard`: Backtest results visualization — equity curve, drawdown chart, monthly P&L heatmap, trade log, and summary statistics
- `api/backtest-engine`: REST API endpoint that accepts strategy definition + config, runs simulation against historical data, and returns structured results
- `api/historical-data`: Upstox API integration for fetching, caching, and serving 2 years of historical OHLCV and option chain data for NIFTY and BANKNIFTY
- `api/instrument-metadata`: Endpoints for available underlyings, expiry dates, and strike prices to populate the strategy builder dropdowns

### Modified Capabilities
<!-- None — this is a new web application built alongside the existing CLI tool. The CLI tool remains unchanged. -->

## Impact

- **New dependencies**: React (frontend), FastAPI + Uvicorn (backend), SQLite or file-based cache for historical data, Chart.js or Recharts for visualization
- **Upstox API**: Requires valid Upstox API credentials (api_key, api_secret, access_token) to fetch historical data. The existing `upstox_client.py` will be extended with historical candle and option chain endpoints
- **Existing code**: The existing `option_backtester/` CLI package is not modified. The new web app reuses pricing logic (`pricing.py`) and strategy definitions (`strategies.py`) but wraps them in a web-compatible backtest engine
- **Infrastructure**: Runs locally (localhost). No cloud deployment required. Frontend served by the FastAPI backend or a simple dev server
- **Data storage**: Historical data cached locally (SQLite or parquet files) to avoid repeated Upstox API calls. Cache covers ~500 trading days x multiple strikes per expiry

## Refinements & SENSEX (2026-09 follow-up)

Post-launch user testing surfaced correctness and usability gaps that are folded into this change:

- **INR currency formatting.** All user-facing money renders with `₹`, not `$`. Applies to trade log, summary tiles, chart axes/tooltips, and CSV export.
- **Days-to-expiry awareness.** Trade records carry `dte` (int) and `expiry_date` (str). Because the Upstox instruments master only lists live/future contracts, the engine infers the current weekly-expiry weekday from the modal weekday of near-term cached expiries and projects it forward — historical trades get realistic DTE (0 for expiry-day trades) even when the true historical expiry is not in the instruments cache.
- **Dashboard-level DTE filter.** A single `DTE: {All / 0 / 1 / 2 / 3+}` selector at the top of the Backtest Results page filters trades and rebuilds every derived metric (summary, equity curve, drawdown, monthly heatmap, day-of-week, cumulative P&L) client-side.
- **Intraday-aware entry/exit pricing.** For a user-configured entry_time (e.g. 09:20) the engine fetches 5-minute option candles via Upstox API v3 (`/v3/historical-candle/{key}/minutes/5/{to}/{from}`) and prices legs at that bar's open. Daily-open pricing is an incorrect approximation because it reflects the 09:15 opening tick, which for options is often distorted by opening-spread noise.
- **Real exit P&L.** Time-based exits compute P&L from real per-leg 5-minute exit prices, not Black-Scholes at spot_close. The trade log's Exit Premium column now shows `abs(exit_total)/lot_size` — matching the entry-side convention and the true intraday cache.
- **SENSEX (BSE) support.** SENSEX is added as a first-class underlying alongside NIFTY and BANKNIFTY. Instruments master parsing accepts `exchange = BSE_FO`, the index instrument key is `BSE_INDEX|SENSEX`, lot size is 20, strike interval is 100, and the sync range is ATM ± 2000 points. Weekly-expiry weekday is inferred (not hard-coded) because BSE has changed SENSEX expiry weekdays over time.

## Historical Data + Per-Leg SL + ATM-at-Entry (2026-09 second follow-up)

- **NIFTY lot size corrected to 65** (was 75). Reflected in backend `LOT_SIZES` and `/api/instruments/underlyings`.
- **Aggregate INR display.** Summary tiles (Total P&L, Max Drawdown, Avg Win, Avg Loss), Trade Log P&L / Cumulative P&L, Monthly Heatmap, Equity Curve, Day-of-Week Breakdown and Leg P&L all show values multiplied by lot size (INR) with a `NN pts` caption for the underlying points. Win-rate no longer double-multiplies by 100.
- **Drawdown chart** fixed to read `drawdown_pct` and render as a percentage (was reading a non-existent `drawdown` field and rendering as ₹).
- **Per-leg vs Combined Stop Loss** toggle in the UI. Default is per-leg — each leg exits at its own SL price using cached 5-min option candles when available, or BS-simulated intraday journey at index spot 5-min high/low otherwise. Combined mode keeps the previous whole-position semantics. Trailing SL is still combined-only.
- **ATM computed from spot at `entry_time`.** A new 5-minute index-intraday cache (`index_intraday` table) is populated on-demand from Upstox v3 for the index instrument key. ATM = `round(spot_at_entry_time / strike_interval) * strike_interval` — no more inheriting the 9:15 opening tick's spot when entry is later in the day.
- **Historical expiry calendar.** New rule table `WEEKLY_EXPIRY_WEEKDAY` per underlying with transition dates (NIFTY Thursday → Wednesday Nov 2024 → Thursday Apr 2025 → Tuesday Sep 2025; BANKNIFTY Thursday until Nov 2024 then discontinued; SENSEX Friday → Tuesday). Plus a `HOLIDAYS` set for 2024–2026. `historical_expiry(dt, underlying, expiry_type)` returns the correct historical expiry with holiday shift-back. This calendar wins over the live-master lookup so historical trades tag DTE against the real regime instead of the earliest live-master expiry.
- **NSE/BSE bhavcopy backfill** — new endpoint `POST /api/data/backfill-bhavcopy` and matching UI button. Downloads daily F&O bhavcopy CSVs (`nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_..._F_0000.csv.zip` and BSE equivalent), parses OHLC/vol/OI + underlying spot + `FinInstrmId` per contract, and writes to `option_premiums` with the correct historical expiry. Solves the "Upstox live master doesn't retain expired weeklies" problem for daily data.
- **Implied-volatility calibration** from bhavcopy close prices. New `iv_calibration.py` reverse-BS solves the observed close premium into a per-contract per-day IV; stored in `option_premiums.implied_vol` alongside `underlying_close`. Pricing engine prefers this calibrated IV over the coarse spot-range vix estimate when doing BS at a specific intraday time — giving realistic entry/exit premiums for any historical day without a full intraday cache.
- **Upstox expired-instruments endpoint for real 5-min intraday.** Confirmed working via `/v2/expired-instruments/historical-candle/{NSE_FO|<token>|<DD-MM-YYYY>}/{interval}/{to}/{from}`. Bhavcopy stores each contract's NSE token as `option_premiums.nse_token`; `_ensure_intraday_cached` falls back to the expired-instruments endpoint when the live-master lookup misses; 1-min bars are downsampled to 5-min buckets and inserted into `intraday_candles`. Per-leg SL and time-of-day pricing now use REAL intraday data for expired contracts, not just BS estimation.
- **Bhavcopy backfill also prefetches intraday.** For each backfilled day the task downloads the day's index 5-min bars plus the 5-min intraday for ATM ± 5 strikes × CE/PE across the two nearest expiries — so backtests read entirely from cache. Real-first with BS-with-calibrated-IV fallback only when Upstox refuses.
- **UI: full data-management panel.** Data Status shows all three underlyings with row-level "Catch up" buttons and a top-level "Catch up all". A collapsible "Fetch older…" panel offers preset ranges (Last 3m / 6m / 1y / 2y / 3y / 5y) plus a custom date-range picker and two actions: **Fetch (Upstox)** for live-master contracts and **Backfill (Bhavcopy)** for historical/expired contracts.
- **Old saved backtests purged** since their strike selections and P&L were computed pre-fix and would confuse users. The engine still supports loading saved backtests going forward.
