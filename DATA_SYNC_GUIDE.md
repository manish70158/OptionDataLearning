# NIFTY Options Data Sync Guide

## Current Sync in Progress

**Task ID:** `6c8cc1cb`
**Date Range:** June 13 - September 13, 2026 (3 months)
**Estimated Time:** 25-30 minutes
**Status:** Check at http://localhost:8000/api/data/sync/6c8cc1cb/status

### Monitor Progress

```bash
# Option 1: Use the monitoring script
./monitor_sync.sh 6c8cc1cb

# Option 2: Check status manually
curl http://localhost:8000/api/data/sync/6c8cc1cb/status | python3 -m json.tool

# Option 3: Check database directly
sqlite3 web/cache.db "SELECT COUNT(DISTINCT date) as days, MIN(date), MAX(date) FROM option_premiums WHERE instrument='NIFTY';"
```

## What's Being Synced

For each trading day, the system fetches:
- **OHLCV data** for NIFTY index
- **Option premiums** for strikes: ATM ± 1000 points (50-point intervals)
  - Example: If NIFTY is at 23400, fetches strikes from 22400 to 24400
  - Both CE and PE for each strike
  - ~40 CE/PE pairs = 80 option contracts per day

This gives you **real historical Upstox data** for backtesting, not Black-Scholes estimates!

## Data Available for Testing

Even while the sync runs, you can test with already-synced dates:
- **September 11, 2026**: ✅ 80 option premiums available
- **More dates syncing**: Check progress with monitor script

## Sync Additional Data Later

### Last 6 months (faster)
```bash
curl -X POST http://localhost:8000/api/data/sync \
  -H "Content-Type: application/json" \
  -d '{
    "underlying": "NIFTY",
    "start_date": "2026-03-13",
    "end_date": "2026-09-13"
  }'
```

### Full 1 year (recommended for thorough backtesting)
```bash
curl -X POST http://localhost:8000/api/data/sync \
  -H "Content-Type: application/json" \
  -d '{
    "underlying": "NIFTY",
    "start_date": "2025-09-13",
    "end_date": "2026-09-13"
  }'
```
**Time:** 60-90 minutes

### Full 2 years (maximum available)
```bash
curl -X POST http://localhost:8000/api/data/sync \
  -H "Content-Type: application/json" \
  -d '{
    "underlying": "NIFTY",
    "start_date": "2024-09-13",
    "end_date": "2026-09-13"
  }'
```
**Time:** 2-3 hours

## Sync BANKNIFTY

To sync BANKNIFTY data (separate from NIFTY):

```bash
curl -X POST http://localhost:8000/api/data/sync \
  -H "Content-Type: application/json" \
  -d '{
    "underlying": "BANKNIFTY",
    "start_date": "2026-06-13",
    "end_date": "2026-09-13"
  }'
```

## Data Sync Behavior

- **Incremental:** Re-running sync only fetches missing data
- **OHLCV:** Fetched only once per date
- **Option premiums:** Always fetched (even if OHLCV exists) to ensure completeness
- **Cache location:** `web/cache.db` (SQLite database)

## Check Cache Status

```bash
# Summary
curl http://localhost:8000/api/data/status | python3 -m json.tool

# Detailed breakdown
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

## Troubleshooting

### Sync taking too long?
- Normal behavior: 250ms delay between API calls (rate limiting)
- ~60 trading days = ~25-30 minutes
- Sync continues even if you close terminal

### Check if sync is stuck:
```bash
curl http://localhost:8000/api/data/sync/<task_id>/status
```

If status is "failed", check the error field for details.

### Token expired error?
Upstox access tokens expire daily. Refresh at https://api.upstox.com/ and update:
```bash
export UPSTOX_ACCESS_TOKEN="new_token_here"
# Restart app
```

Or update `~/.upstox/config.json` and restart the app.

## Testing Tips

1. **Start small:** Use 1 month of data first
2. **Check pricing source:** Look for `"pricing_source": "real"` in backtest results
3. **Expand gradually:** Add more months as needed
4. **Background sync:** Let longer syncs run overnight

## Current Task

The 3-month sync (June-September 2026) is running now. Once complete, you'll have ~60 trading days of real NIFTY option data for testing your strategies! 🚀
