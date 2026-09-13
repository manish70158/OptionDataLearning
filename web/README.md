# Options Strategy Backtester — Web App

A full-stack web application for backtesting NIFTY and BANKNIFTY option strategies against historical market data. Built with FastAPI (Python) backend and React (TypeScript) frontend.

Uses the **Upstox API** for fetching real historical option premiums. Falls back to Black-Scholes estimation when real data is unavailable.

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### 1. Install Python dependencies

```bash
cd web
pip3 install -r requirements.txt
```

Also install the parent project's dependencies (used by the pricing engine):

```bash
cd ..
pip3 install -r requirements.txt
```

### 2. Build the frontend

```bash
cd web/frontend
npm install
npm run build
cd ../..
```

### 3. Start the app

```bash
python3 -m web
```

This starts the server at **http://localhost:8000** and opens your browser automatically.

- App UI: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- Data sync status: http://localhost:8000/api/data/status

Use `python3 -m web --no-browser` to skip auto-opening the browser.

### Check Data Availability

Before running backtests, check what data is cached:

```bash
# Quick status check
curl http://localhost:8000/api/data/status | python3 -m json.tool

# Detailed database query
sqlite3 web/cache.db "SELECT instrument, COUNT(DISTINCT date) as days, MIN(date), MAX(date) FROM option_premiums GROUP BY instrument;"
```

### 4. (Optional) Development mode

For hot-reloading during development, run the backend and frontend separately:

**Terminal 1 — Backend:**
```bash
python3 -m web --reload --no-browser
```

**Terminal 2 — Frontend dev server:**
```bash
cd web/frontend
npm run dev
```

The Vite dev server runs at http://localhost:5173 and proxies `/api/*` requests to the backend on port 8000.

## Current Data Sync Status

**Active Sync:** A background data sync is currently running for NIFTY (Task ID: `6c8cc1cb`)

- **Date Range:** September 2025 - September 2026 (~248 trading days)
- **Status:** Check progress with `./monitor_sync.sh 6c8cc1cb`
- **Estimated Completion:** ~2 hours from start
- **Data Syncing:** ~19,840 option premiums (80 per day)

This will provide nearly a full year of real Upstox historical data including:
- ATM strikes
- ATM±1, ATM±2, ... ATM±20 (comprehensive strike coverage)
- Both CE and PE options
- Real OHLC premiums (not Black-Scholes estimates)

You can **start testing immediately** with the already-synced data (September 11, 2026) while the rest syncs in the background!

---

## Upstox API Setup

The app fetches historical option chain data from Upstox. You need valid API credentials.

### Get credentials

1. Create an app at https://api.upstox.com/
2. Complete the OAuth flow to get an access token

### Configure credentials

**Option A — Environment variables (recommended):**

```bash
export UPSTOX_API_KEY="your_api_key"
export UPSTOX_API_SECRET="your_api_secret"
export UPSTOX_ACCESS_TOKEN="your_access_token"
```

**Option B — Config file:**

Create `~/.upstox/config.json`:

```json
{
  "api_key": "your_api_key",
  "api_secret": "your_api_secret",
  "access_token": "your_access_token"
}
```

Environment variables take priority over the config file.

**Note:** The Upstox access token expires daily. You must refresh it via the Upstox OAuth flow each day you want to sync new data.

### Without credentials

The app works without Upstox credentials — the backtest engine uses **Black-Scholes estimation** for option premiums instead of real market data. You still need OHLCV index data in the cache (you can populate it manually or the engine will estimate from available data).

## How to Use

### Step 1 — Sync historical data

Before running backtests, you need historical data. The sync process fetches:
- **OHLCV data** for NIFTY/BANKNIFTY index
- **Option premiums** for all strikes within ATM ± 1000 points (NIFTY) or ATM ± 2000 points (BANKNIFTY)
  - Strike intervals: 50 points for NIFTY, 100 points for BANKNIFTY
  - Both CE and PE options
  - ~80 option contracts per trading day for NIFTY

**Via Web UI:**

1. Open the app at http://localhost:8000
2. In the left panel, find the **Data Status** section
3. Click **Sync Data** to fetch data for the selected underlying and date range
4. Wait for the sync to complete (progress bar shows status)

**Via API:**

```bash
# Sync 3 months of data (recommended for testing)
curl -X POST http://localhost:8000/api/data/sync \
  -H "Content-Type: application/json" \
  -d '{"underlying": "NIFTY", "start_date": "2026-06-13", "end_date": "2026-09-13"}'

# Sync 1 year of data (comprehensive backtesting)
curl -X POST http://localhost:8000/api/data/sync \
  -H "Content-Type: application/json" \
  -d '{"underlying": "NIFTY", "start_date": "2025-09-13", "end_date": "2026-09-13"}'
```

**Sync Time Estimates:**

| Date Range | Trading Days | Option Contracts | Estimated Time |
|---|---|---|---|
| 1 month | ~20 days | ~1,600 | 25-30 minutes |
| 3 months | ~60 days | ~4,800 | 1-1.5 hours |
| 6 months | ~120 days | ~9,600 | 2-3 hours |
| 1 year | ~250 days | ~20,000 | 4-5 hours |

**Monitor Sync Progress:**

```bash
# Get task ID from sync response, then:
curl http://localhost:8000/api/data/sync/{task_id}/status | python3 -m json.tool

# Or use the monitoring script:
./monitor_sync.sh {task_id}

# Check database directly:
sqlite3 web/cache.db "SELECT COUNT(DISTINCT date) FROM option_premiums WHERE instrument='NIFTY';"
```

**Important Notes:**

- **Incremental sync:** Re-running sync only fetches missing data
- **Background execution:** Sync continues even if you close the terminal
- **Rate limiting:** 250ms delay between API calls (Upstox requirement)
- **Test while syncing:** You can start backtesting with partial data while sync continues

### Step 2 — Build your strategy

In the **Strategy Builder** panel:

1. **Select underlying**: NIFTY or BANKNIFTY
2. **Select expiry type**: Weekly or Monthly
3. **Choose a preset** (optional): Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, Strangle, Short Straddle, Short Strangle
4. **Or build custom**: Click "Add Leg" and configure each leg:
   - **Position**: Buy or Sell
   - **Option Type**: CE (Call) or PE (Put)
   - **Strike**: Relative to ATM (e.g., ATM, ATM+100, ATM-200)
   - **Lots**: 1 to 50

You can add up to 8 legs per strategy.

### Step 3 — Configure backtest parameters

In the **Backtest Config** panel:

| Parameter | Default | Description |
|---|---|---|
| Date range | Last 2 years | Start and end dates for the backtest |
| Entry time | 09:20 IST | Time of day to enter positions |
| Exit time | 15:15 IST | Time of day to exit positions |
| Stop loss | 50% (enabled) | Exit when loss hits threshold (% of premium or points) |
| Target profit | Disabled | Exit when profit hits threshold |
| Trailing SL | Disabled | Move SL up as position gains (points) |
| VIX filter | None | Only trade on days within VIX range |
| Weekday filter | All days | Select which days of the week to trade |

### Step 4 — Run the backtest

Click **Run Backtest**. The results appear in the right panel:

- **Summary Statistics**: Total P&L, win rate, max drawdown, Sharpe ratio, profit factor, and more
- **Equity Curve**: Cumulative P&L over time (line chart)
- **Drawdown Chart**: Peak-to-trough drawdown (area chart)
- **Monthly Heatmap**: P&L by month with color intensity
- **Day of Week Breakdown**: Average P&L per weekday (bar chart)
- **Trade Log**: Sortable, searchable, paginated table of every trade

### Step 5 — Export & save

- **Export CSV**: Download the full trade log as a CSV file
- **Save**: The backtest is auto-saved with a unique ID for later retrieval

## Data Sync Tools

### Monitoring Script

Use the included monitoring script to track data sync progress:

```bash
./monitor_sync.sh {task_id}
```

The script displays:
- Current sync status and progress percentage
- Number of trading days synced
- Total option premiums in cache
- Date range coverage

Press Ctrl+C to stop monitoring (sync continues in background).

### Manual Progress Checks

```bash
# Check sync status
curl http://localhost:8000/api/data/sync/{task_id}/status

# Check cache status
curl http://localhost:8000/api/data/status | python3 -m json.tool

# Query database directly
sqlite3 web/cache.db "
SELECT
  instrument,
  COUNT(DISTINCT date) as trading_days,
  MIN(date) as first_date,
  MAX(date) as last_date,
  COUNT(*) as total_premiums
FROM option_premiums
GROUP BY instrument;"
```

### Data Sync Guide

See `DATA_SYNC_GUIDE.md` for comprehensive documentation on:
- Sync time estimates for different date ranges
- How to sync BANKNIFTY data
- Incremental sync behavior
- Cache management
- Troubleshooting sync issues

## API Reference

All endpoints are documented at http://localhost:8000/docs (Swagger UI).

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/backtest` | Start a backtest (returns task_id) |
| `GET` | `/api/backtest/{task_id}/status` | Poll backtest progress/results |
| `GET` | `/api/backtest/saved/{id}` | Retrieve a saved backtest |
| `POST` | `/api/data/sync` | Start historical data sync |
| `GET` | `/api/data/sync/{task_id}/status` | Poll sync progress |
| `GET` | `/api/data/status` | Cache status per underlying |
| `GET` | `/api/instruments/underlyings` | List supported underlyings |
| `GET` | `/api/instruments/{underlying}/expiries` | Available expiry dates |
| `GET` | `/api/instruments/{underlying}/strikes` | Available strikes for a date |

### Example: Run a backtest via API

```bash
curl -X POST http://localhost:8000/api/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": {
      "underlying": "NIFTY",
      "expiry_type": "weekly",
      "legs": [
        {"position": "buy", "option_type": "CE", "strike_offset": 0, "lots": 1},
        {"position": "sell", "option_type": "CE", "strike_offset": 100, "lots": 1}
      ]
    },
    "config": {
      "start_date": "2025-09-01",
      "end_date": "2026-09-01",
      "entry_time": "09:20",
      "exit_time": "15:15",
      "stop_loss_enabled": true,
      "stop_loss_mode": "percentage",
      "stop_loss_value": 50,
      "target_profit_enabled": false,
      "trailing_sl_enabled": false,
      "weekdays": [0, 1, 2, 3, 4]
    }
  }'
```

Then poll the status:

```bash
curl http://localhost:8000/api/backtest/{task_id}/status
```

## Supported Strategies

| Strategy | Legs | Profits When |
|---|---|---|
| Bull Call Spread | Buy ATM CE + Sell OTM CE | Market moves up |
| Bear Put Spread | Buy ATM PE + Sell OTM PE | Market moves down |
| Straddle | Buy ATM CE + Buy ATM PE | Large move in either direction |
| Strangle | Buy OTM CE + Buy OTM PE | Very large move in either direction |
| Iron Condor | Sell OTM CE/PE + Buy further OTM CE/PE | Market stays in a range |
| Iron Butterfly | Sell ATM CE/PE + Buy OTM CE/PE | Market stays near open price |
| Short Straddle | Sell ATM CE + Sell ATM PE | Market stays flat |
| Short Strangle | Sell OTM CE + Sell OTM PE | Market stays in a wider range |

You can also build **any custom multi-leg strategy** (up to 8 legs).

## Project Structure

```
web/
├── __main__.py              # Startup script (python -m web)
├── requirements.txt         # Python dependencies
├── cache.db                 # SQLite cache (auto-created, gitignored)
├── backend/
│   ├── main.py              # FastAPI app, CORS, static files
│   ├── schemas.py           # Pydantic request/response models
│   ├── tasks.py             # In-memory task registry
│   ├── routers/
│   │   ├── backtest.py      # POST /api/backtest, GET status/saved
│   │   ├── data.py          # POST /api/data/sync, GET status
│   │   └── instruments.py   # GET underlyings/expiries/strikes
│   ├── engine/
│   │   ├── pricing.py       # Real data lookup + Black-Scholes fallback
│   │   └── simulator.py     # Day-by-day backtest loop with SL/TP
│   └── data/
│       ├── models.py        # SQLite table definitions
│       ├── cache.py         # Async SQLite cache operations
│       └── upstox_fetcher.py # Upstox API v2 historical data
└── frontend/
    ├── package.json
    ├── vite.config.ts       # Dev proxy to backend
    └── src/
        ├── App.tsx
        ├── api/client.ts    # API client functions
        ├── hooks/useBacktest.ts
        ├── types/backtest.ts
        ├── pages/Backtest.tsx
        └── components/
            ├── StrategyBuilder/  # Leg builder, presets, summary
            ├── BacktestConfig/   # Date, time, SL/TP, filters
            └── ResultsDashboard/ # Charts, stats, trade log
```

## Data Storage

Historical data is cached in a local **SQLite database** (`web/cache.db`):

- **ohlcv_candles**: Daily OHLCV data for NIFTY and BANKNIFTY indices
- **option_premiums**: Historical option premiums (open/close/high/low) per strike/expiry
- **intraday_candles**: 5-minute candle data for intraday SL/TP simulation
- **sync_log**: Data sync history
- **saved_backtests**: Saved backtest configurations and results

The cache avoids redundant Upstox API calls. Subsequent syncs only fetch missing dates.

## Troubleshooting

| Issue | Solution |
|---|---|
| "Upstox credentials not configured" | Set env vars or create `~/.upstox/config.json` |
| "Access token expired" | Refresh the token via Upstox OAuth flow |
| "No historical data available" | Click "Sync Data" in the UI to fetch data first |
| Frontend shows blank page | Run `cd web/frontend && npm run build` |
| Port 8000 in use | Kill the existing process or change port in `__main__.py` |
| Backtest shows "estimated" pricing | Sync data for the date range to get real premiums |

## Implementation Notes

### Data Synced Per Trading Day

For each trading day, the system fetches:

**Index Data:**
- OHLCV candles for NIFTY 50 or BANKNIFTY index

**Option Premiums:**
- **NIFTY**: ATM ± 1000 points at 50-point intervals
  - Example: If spot is 23,400, fetches strikes from 22,400 to 24,400
  - ~40 strike pairs (CE/PE) = 80 option contracts per day
- **BANKNIFTY**: ATM ± 2000 points at 100-point intervals
  - Example: If spot is 51,000, fetches strikes from 49,000 to 53,000
  - ~40 strike pairs (CE/PE) = 80 option contracts per day

This provides comprehensive coverage including:
- ATM (at-the-money) strikes
- ATM+1, ATM+2, ... ATM+20 (out-of-the-money calls)
- ATM-1, ATM-2, ... ATM-20 (out-of-the-money puts)
- Real historical OHLC premiums (open, high, low, close)

### Upstox Instruments CSV Structure

The Upstox instruments master file uses:
- **Exchange**: `NSE_FO` (not `NFO`)
- **Instrument Type**: `OPTIDX` for index options
- **Option Type**: Separate `option_type` column with values `CE` or `PE`
- **Strike Column**: Named `strike` (not `strike_price`)

### Expiry Date Handling

NIFTY and BANKNIFTY option expiries are **not always on Thursdays**. Market holidays cause shifts to other weekdays (e.g., Tuesdays in September 2026). The app dynamically resolves expiries from the instruments master file rather than calculating them.

### Data Sync Behavior

When you run a data sync:
- **OHLCV data**: Fetched only for dates missing from cache (incremental)
- **Option premiums**: Always fetched for all trading days in the range, even if OHLCV exists

This ensures option premium data is populated even when re-syncing previously cached date ranges.

**Example:** If you have OHLCV for 248 days but only option data for 1 day, running sync will:
- Skip fetching 248 days of OHLCV (already cached)
- Fetch option premiums for all 248 days (~19,840 option contracts)
- Take ~2 hours due to API rate limiting
