## Why

We have 6 years of historical NIFTY data (1,484 trading days, 2020–2026) with FII/PRO view classifications and intraday movement patterns. The analysis in `FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md` proves that specific FII View × PRO View combinations reliably predict next-day directional moves (e.g., Mildly Bearish + Mildly Bearish = 100% Green, Bullish + Strong Bullish = only 36.5% Green). We need a system that backtests options strategies (Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, Strangle) against this historical data, mapping each FII/PRO combination to the optimal strategy, and produces a comprehensive profitability report. The system should also fetch live option chain data from the Upstox API for forward-looking daily strategy recommendations.

## What Changes

- **Add historical options strategy backtesting engine**: Simulate P&L for 6+ option strategies across all 47 FII/PRO view combinations using the existing CSV data (NIFTY OHLC, VIX, range %).
- **Add Upstox API integration**: Fetch real-time NIFTY option chain data (strikes, premiums, Greeks, expiry dates) to enable live strategy evaluation.
- **Add FII/PRO → strategy mapping logic**: Based on each combination's Green%, Avg Change%, dominant move pattern (Down to Up / Top to Down), and VIX level, determine which option strategy would have been most profitable.
- **Generate profitability report**: For each FII/PRO combination, output which strategy yielded the highest P&L, win rate, max drawdown, and risk-adjusted return — with expiry vs non-expiry breakdowns.
- **Add daily recommendation module**: Given today's FII view, PRO view, and VIX, recommend the optimal option strategy with specific strike selection and expected P&L range.

## Capabilities

### New Capabilities
- `option-strategy-backtester`: Core backtesting engine that simulates Iron Condor, Iron Butterfly, Bull Call Spread, Bear Put Spread, Straddle, and Strangle strategies using historical NIFTY OHLC data, VIX-derived implied volatility, and intraday range patterns.
- `upstox-option-data`: Upstox API client for fetching live NIFTY/BANKNIFTY option chain data including strikes, premiums, open interest, and Greeks.
- `fii-pro-strategy-report`: Report generator that maps each FII View × PRO View combination to strategy performance metrics and produces a ranked profitability analysis with visual summaries.

### Modified Capabilities
(none — greenfield project)

## Impact

- **New files**: Python modules for backtesting engine, Upstox API client, strategy definitions, report generator, and CLI entry point.
- **Dependencies**: `pandas`, `numpy` for data processing; `requests` or `upstox-python-sdk` for API access; `matplotlib`/`plotly` for report charts.
- **Data**: Reads existing `vix_fii_t1_intraday_daily_results.csv` (1,488 rows). No schema changes to existing data.
- **API**: Requires Upstox API credentials (API key, secret, access token) configured via environment variables or config file.
- **Output**: Markdown/HTML profitability report, CSV summary tables, optional chart images.
