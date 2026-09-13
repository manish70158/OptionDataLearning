## Context

The project has 1,488 rows of historical NIFTY data (2020–2026) in CSV format with OHLC prices, VIX, FII/PRO view classifications, and intraday movement metrics. See proposal.md for full motivation. There is no existing code — this is greenfield Python development. The CSV columns relevant to backtesting are: `nifty_open`, `nifty_high`, `nifty_low`, `nifty_close`, `vix_open`, `vix_close`, `is_nifty_expiry`, `fii_view`, `pro_view`, and `actual_range_pct`.

Historical NIFTY option chain data is not available. Premiums must be estimated from VIX using Black-Scholes. This is an approximation — real option premiums are affected by skew, term structure, and market microstructure — but VIX is a reasonable proxy for ATM implied volatility on NIFTY index options.

## Goals / Non-Goals

**Goals:**
- Produce a complete profitability report showing which option strategy works best for each FII/PRO combination
- Estimate realistic option premiums from VIX using Black-Scholes
- Support 6 standard option strategies with configurable strikes
- Integrate with Upstox API for live option chain data
- Generate daily strategy recommendations based on current FII/PRO view

**Non-Goals:**
- Real-time auto-execution of trades (this is analysis/recommendation only)
- Multi-leg margin calculation (out of scope for this iteration)
- Tick-by-tick intraday simulation (we use OHLC bars only)
- BANKNIFTY or stock options backtesting (NIFTY only for now, though architecture supports extension)
- Greeks-based hedging or dynamic adjustment during the day

## Decisions

### 1. Python with pandas for data processing
**Choice**: Python 3.10+ with pandas, numpy, scipy

**Rationale**: pandas naturally fits the CSV-based tabular data. numpy/scipy provide Black-Scholes math (norm.cdf). The user's existing analysis workflow is data-science oriented.

**Alternatives considered**:
- JavaScript/Node.js: Less natural for financial math and dataframe operations
- Jupyter notebook only: Harder to automate and produce repeatable reports

### 2. Black-Scholes premium estimation from VIX
**Choice**: Use `vix_open` as annualized IV for entry premiums, `vix_close` for exit premiums. Apply standard Black-Scholes formula with NIFTY strike interval of 50 points.

**Rationale**: We lack historical option chain data. VIX represents the market's implied volatility expectation for NIFTY options. While VIX is a weighted average of OTM option IVs (not a single strike's IV), it provides a reasonable approximation for ATM and near-OTM strikes. For deep OTM strikes used in Iron Condor wings, we apply a simple skew adjustment (multiply IV by a configurable skew factor, default 1.1 for puts, 0.95 for calls).

**Alternatives considered**:
- Flat premium assumption (e.g., fixed % of spot): Too unrealistic, ignores VIX regime changes
- Historical option chain data from NSE archives: Not available in structured format for 6 years
- Upstox historical data API: Only provides limited history, not sufficient for 6-year backtest

### 3. Entry at open, exit at close
**Choice**: Each day, the system enters all strategy legs at market open (using `nifty_open` + `vix_open`) and exits at market close (using `nifty_close` + `vix_close`). No intraday adjustments.

**Rationale**: The CSV data provides OHLC at daily granularity. The FII/PRO view data is available before market open (T-1 data published after market close). This models a trader who checks the signal before open, enters at open, and exits at close — matching the "daily basis" testing requirement.

**Alternatives considered**:
- Hold till expiry: More realistic for premium sellers but makes comparison across strategies harder and requires multi-day tracking
- Entry at a fixed time (e.g., 9:30 AM): No intraday timestamp data available

### 4. Module structure
**Choice**: Flat Python package with clear module separation:

```
option_backtester/
├── __init__.py
├── strategies.py        # Strategy definitions (leg structures, payoff functions)
├── pricing.py           # Black-Scholes pricing, premium estimation
├── backtester.py        # Core backtest loop, daily simulation
├── aggregator.py        # Group by FII/PRO, compute metrics
├── upstox_client.py     # Upstox API integration
├── recommender.py       # Daily recommendation engine
├── report.py            # Report generation (MD/HTML/CSV)
├── config.py            # Configuration, defaults, strike parameters
└── cli.py               # CLI entry point (argparse)
```

**Rationale**: Simple flat structure for a focused project. Each module has a single responsibility. No need for nested packages at this scale.

**Alternatives considered**:
- Single monolithic script: Hard to test and maintain
- Class-heavy OOP architecture: Over-engineering for a data pipeline

### 5. Upstox SDK vs raw HTTP
**Choice**: Use `requests` with direct REST API calls rather than the `upstox-python-sdk`.

**Rationale**: The official SDK has version compatibility issues and adds a heavy dependency. We only need 2-3 API endpoints (auth token refresh, option chain, market quotes). Raw HTTP with requests is simpler, more maintainable, and easier to debug.

**Alternatives considered**:
- `upstox-python-sdk`: Adds dependency risk, SDK may lag behind API changes
- `httpx` with async: Unnecessary complexity — we make sequential API calls, not concurrent

### 6. Report visualization
**Choice**: matplotlib for static charts in HTML reports, plain Markdown tables for MD output.

**Rationale**: matplotlib is the standard Python charting library, produces publication-quality static images. For HTML reports, we embed charts as base64 PNG images. Markdown reports use plain text tables (GitHub-flavored).

**Alternatives considered**:
- plotly: Interactive but heavier, requires browser rendering
- seaborn: Good for statistical plots but adds another dependency on top of matplotlib

## Risks / Trade-offs

**[VIX-based premium estimation is approximate]** → The Black-Scholes model with VIX as IV will overestimate premiums for deep OTM options and underestimate for high-skew regimes. Mitigation: Apply configurable skew adjustments and clearly document that absolute P&L numbers are estimates — the relative ranking of strategies across FII/PRO combinations is what matters.

**[No bid-ask spread in historical simulation]** → Real trades incur slippage. Mitigation: Add a configurable "slippage" parameter (default: 2 NIFTY points per leg) that is deducted from each trade's P&L. This makes absolute returns more conservative.

**[OHLC doesn't capture intraday path]** → We know the high and low but not when they occurred. An Iron Condor might have been stopped out intraday even if the close was within range. Mitigation: Use the max adverse excursion (high/low) to compute worst-case intraday P&L as a separate "intraday risk" metric alongside close-to-close P&L.

**[Upstox API token expiry]** → Upstox access tokens expire daily and require manual OAuth flow. Mitigation: Document the token refresh process. The system SHALL gracefully degrade — backtest and report features work without Upstox; only the live recommendation needs it.

**[Small sample sizes for rare combinations]** → Some FII/PRO combos have 1-3 days. Statistical significance is questionable. Mitigation: Flag combinations with <5 days in reports, assign "Low" confidence rating, and focus analysis narrative on combinations with ≥30 days.

## Open Questions

- Should we add a "hold overnight" mode for multi-day strategies in a future iteration, or keep it strictly intraday?
- For the Upstox integration, should we support BANKNIFTY option chains in addition to NIFTY from day one, or defer to a follow-up change?
