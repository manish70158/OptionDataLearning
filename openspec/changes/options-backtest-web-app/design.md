## Context

The project has an existing CLI-based option backtester (`option_backtester/`) that uses Black-Scholes estimation for pricing. It has well-structured modules for strategies (8 defined), pricing, backtesting, and an Upstox API client (currently only for live option chain data). See proposal.md for full motivation.

The new web app lives alongside the existing CLI tool in a separate `web/` directory, reusing core pricing and strategy logic via Python imports.

## Goals / Non-Goals

**Goals:**
- Single-command local startup (`python -m web` or similar) for both backend and frontend
- Interactive strategy builder with visual feedback matching algotest.in's UX
- Real historical option premiums from Upstox API (not Black-Scholes estimates) for the last 2 years
- Sub-10-second backtest execution for 1 year of daily trades on a typical strategy
- All data stays local — no cloud services, no accounts beyond Upstox API

**Non-Goals:**
- Multi-user authentication or user accounts
- Live/paper trading execution
- Real-time streaming data or WebSocket feeds
- Mobile-responsive design (desktop-first)
- Cloud deployment or Docker packaging
- Options Greeks visualization or payoff diagrams (future enhancement)

## Decisions

### Decision 1: FastAPI + React (Vite) monorepo

**Choice**: FastAPI backend serving a React (Vite-built) SPA. Backend serves the built frontend as static files in production; Vite dev server with proxy in development.

**Why over alternatives:**
- **vs Django**: FastAPI's async support handles data-sync tasks better. Pydantic models give typed request/response contracts for free. Lighter weight.
- **vs Flask**: No native async, no built-in request validation. FastAPI is the modern choice for API-first apps.
- **vs Next.js full-stack**: Would require rewriting the Python backtest engine in JavaScript/TypeScript, losing the existing `strategies.py` and `pricing.py` code. Python backend lets us import and reuse them directly.
- **vs Streamlit/Gradio**: Too limited for the custom interactive strategy builder UI needed. No fine-grained control over chart interactions or form layout.

**Structure:**
```
web/
├── backend/
│   ├── main.py              # FastAPI app, CORS, static file mounting
│   ├── routers/
│   │   ├── backtest.py      # POST /api/backtest, GET /api/backtest/{id}
│   │   ├── data.py          # POST /api/data/sync, GET /api/data/status
│   │   └── instruments.py   # GET /api/instruments/*
│   ├── engine/
│   │   ├── simulator.py     # Web-adapted backtest loop
│   │   └── pricing.py       # Wraps option_backtester.pricing + real data lookup
│   ├── data/
│   │   ├── upstox_fetcher.py  # Historical data fetcher (extends upstox_client.py)
│   │   ├── cache.py         # SQLite cache layer
│   │   └── models.py        # SQLAlchemy/raw SQL models for cache tables
│   └── schemas.py           # Pydantic models for request/response
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   └── Backtest.tsx     # Main backtest page (builder + config + results)
│   │   ├── components/
│   │   │   ├── StrategyBuilder/ # Leg management, presets, summary
│   │   │   ├── BacktestConfig/  # Date, time, SL, TP, filters
│   │   │   └── ResultsDashboard/ # Charts, stats, trade log
│   │   ├── hooks/
│   │   │   └── useBacktest.ts   # API calls, state management
│   │   └── types/
│   │       └── backtest.ts      # TypeScript interfaces matching Pydantic schemas
│   ├── package.json
│   └── vite.config.ts
├── cache.db                 # SQLite database (gitignored)
└── requirements.txt         # Python deps for web app
```

### Decision 2: SQLite for historical data cache

**Choice**: SQLite database with tables for OHLCV candles, option premiums, and sync metadata.

**Why over alternatives:**
- **vs Parquet files**: SQLite gives indexed lookups by (instrument, date, strike) which is the exact query pattern the backtest engine needs. Parquet is better for bulk scans but worse for random access by date+strike.
- **vs PostgreSQL**: Overkill for a single-user local app. SQLite requires zero setup.
- **vs In-memory dict**: Data must persist across server restarts. 2 years of option data across all strikes could be 500MB+; too large for RAM-only.

**Tables:**
- `ohlcv_candles`: instrument, date, interval, open, high, low, close, volume
- `option_premiums`: instrument, date, expiry, strike, option_type, open_premium, close_premium, high_premium, low_premium
- `intraday_candles`: instrument, date, strike, option_type, expiry, time, open, high, low, close
- `sync_log`: instrument, start_date, end_date, synced_at, status

### Decision 3: Hybrid pricing — real data with Black-Scholes fallback

**Choice**: Use actual historical option premiums from Upstox when available. Fall back to the existing Black-Scholes estimation (from `pricing.py`) when strike/date data is missing.

**Why**: Upstox may not have option chain data for all historical dates (especially far-OTM strikes or dates >1 year ago). A hard failure on missing data would make the tool unusable for extended backtests. The fallback is clearly marked in results so users know which trades used estimated vs real premiums.

### Decision 4: Background task execution for backtests and data sync

**Choice**: Use FastAPI's `BackgroundTasks` for short operations (<30s). For longer operations (2-year data sync, large backtests), use Python `asyncio.create_task` with an in-memory task registry. No external task queue (Celery, Redis).

**Why over alternatives:**
- **vs Celery + Redis**: Requires running additional services. This is a single-user local app; in-process task management is sufficient.
- **vs synchronous execution**: A 2-year data sync involves thousands of API calls with rate limiting — could take minutes. Blocking the HTTP request is not viable.

**Task registry**: In-memory dict mapping `task_id` → `{status, progress, result}`. Tasks lost on server restart (acceptable for local tool — user can re-trigger).

### Decision 5: Recharts for chart visualization

**Choice**: Recharts (React charting library built on D3).

**Why over alternatives:**
- **vs Chart.js (react-chartjs-2)**: Recharts is more React-idiomatic (declarative JSX components). Better for the interactive hover tooltips and responsive layouts we need.
- **vs Plotly**: Heavier bundle size (~3MB). Recharts is ~300KB. Overkill for the chart types we need (line, area, bar, heatmap).
- **vs Lightweight-charts (TradingView)**: Great for candlestick/financial charts but doesn't cover heatmaps or bar charts for the results dashboard.

### Decision 6: Single-page layout for backtest workflow

**Choice**: One page (`/backtest`) with three panels — Strategy Builder (left), Config (left below builder), Results (right/below). Results panel appears after running a backtest, replacing a placeholder.

**Why**: Matches algotest.in's UX pattern where configuration and results are on the same page. Avoids page navigation that breaks the user's flow. React state management keeps everything in sync without routing complexity.

### Decision 7: Upstox historical candles API for data fetching

**Choice**: Use Upstox API v2 `/historical-candle/{instrumentKey}/{interval}/{to_date}/{from_date}` endpoint for index OHLCV and `/historical-candle/{instrumentKey}/{interval}/{to_date}` for individual option contracts.

**Constraints from Upstox API:**
- Historical candles are free but rate-limited (~250 requests/min)
- Option instrument keys need to be resolved from the instruments master list
- Access token expires daily — user must refresh via OAuth
- Maximum date range per call varies by interval (1 day for minute candles, 1 year for daily)

**Fetch strategy**: For each trading day in the range, resolve the relevant expiry, compute ATM from index close, fetch option premiums for ATM +/- 1000pts (NIFTY) or +/- 2000pts (BANKNIFTY) at relevant strikes. Batch requests with 250ms delay between calls.

## Risks / Trade-offs

**[Upstox data availability for historical options]** → Upstox may not have option chain historical data going back 2 full years, or data may be sparse for far-OTM strikes. **Mitigation**: Hybrid pricing with Black-Scholes fallback. UI indicates which trades used real vs estimated premiums.

**[Token expiry friction]** → Upstox access tokens expire daily. Users must re-authenticate via browser OAuth flow. **Mitigation**: Clear error message with link to Upstox OAuth page. Consider adding a `/api/auth/upstox` endpoint that initiates OAuth redirect if feasible.

**[Large initial data sync]** → Syncing 2 years of option data for all strikes is thousands of API calls. **Mitigation**: Progress reporting in UI. Incremental sync (only fetch missing dates). Background execution. User can start backtesting with partial data while sync continues.

**[Single-user task registry]** → In-memory task state is lost on server restart. **Mitigation**: Acceptable for local dev tool. Saved backtests persist in SQLite. Task results can be refetched by re-running.

**[Bundle size]** → React + Recharts + date picker libraries add frontend weight. **Mitigation**: Vite tree-shaking and code splitting. The app is local-only so initial load time is not critical.

## Implementation Findings & Corrections

### Upstox Instruments Master CSV Structure (Resolved)

The Upstox instruments master file at `https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz` uses the following structure for option contracts:

**Correct column names:**
- `instrument_key`: e.g., "NSE_FO|47293"
- `exchange`: "NSE_FO" (not "NFO")
- `instrument_type`: "OPTIDX" for index options
- `option_type`: "CE" or "PE" (separate column, not in instrument_type)
- `strike`: Strike price as float (column name is `strike`, not `strike_price`)
- `expiry`: Expiry date in "YYYY-MM-DD" format
- `name`: "NIFTY" or "BANKNIFTY"

**Filtering logic:**
```python
if exchange == "NSE_FO" and instrument_type == "OPTIDX" and option_type in ("CE", "PE"):
    if name in ("NIFTY", "BANKNIFTY"):
        lookup[(name, strike, expiry, option_type)] = instrument_key
```

### Expiry Date Resolution (Resolved)

Expiry dates are **not consistently on Thursdays**. Market holidays cause expiries to shift to Tuesdays or other days. Example: NIFTY September 2026 expiries are all on Tuesdays (15th, 22nd, 29th), not Thursdays.

**Correct approach:** Dynamically resolve expiries from the instruments master by:
1. Extracting all unique expiry dates for the underlying from instruments cache
2. For weekly expiries: finding the nearest expiry >= current date within 14 days
3. For monthly expiries: finding the nearest expiry >= current date with day >= 20

**Do not hardcode** Thursday calculations using `(3 - dt.weekday()) % 7`.

### Data Sync Logic (Resolved)

The sync process must handle OHLCV and option premiums independently:

1. **OHLCV sync**: Fetch only missing dates (checked via `get_missing_dates()`)
2. **Option premium sync**: Always fetch for ALL trading days in the requested range, even if OHLCV already exists

This is necessary because:
- Option premium data may be missing even when OHLCV exists
- Users may sync OHLCV first, then later want to populate options
- Re-running sync should fetch missing option data without re-fetching OHLCV

### Bug Fixes Applied

Five critical bugs were fixed in the Upstox integration:

1. **CSV column name**: Changed `row.get("strike_price")` → `row.get("strike")`
2. **Exchange filter**: Changed `exchange != "NFO"` → `exchange != "NSE_FO"`
3. **Instrument type check**: Changed `instrument_type not in ("CE", "PE")` → separate checks for `instrument_type != "OPTIDX"` and `option_type not in ("CE", "PE")`
4. **Expiry calculation**: Replaced static Thursday calculation with dynamic lookup from instruments master
5. **Sync iteration**: Changed loop from `for dt_str in missing_dates` → `for dt_str in all_dates` to always fetch options

These fixes enable successful fetching of real historical option premium data from Upstox API.

## Open Questions

- **VIX historical data source**: Upstox may or may not provide India VIX historical data. If not, we may need to source it from NSE or use the existing CSV data for VIX filtering. This does not change the architecture — just the data pipeline for that one field. *(Currently using estimated VIX from daily price range)*
