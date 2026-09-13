# Trade Log Leg Details Feature

## Overview

The Trade Log now displays individual CE and PE option prices for each leg of your strategy, showing exactly what was bought and sold.

## Visual Example

### Before (collapsed):
```
┌─────────┬────────────┬───────┬──────────┬──────────┬───────┬──────────────┐
│ Details │ Date       │ Day   │ Entry    │ Exit     │ P&L   │ Exit Reason  │
├─────────┼────────────┼───────┼──────────┼──────────┼───────┼──────────────┤
│    ▶    │ 2026-09-11 │ Fri   │ 09:20    │ 15:15    │ -37.92│ time_exit    │
└─────────┴────────────┴───────┴──────────┴──────────┴───────┴──────────────┘
```

### After (expanded - click ▶ button):
```
┌─────────┬────────────┬───────┬──────────┬──────────┬───────┬──────────────┐
│ Details │ Date       │ Day   │ Entry    │ Exit     │ P&L   │ Exit Reason  │
├─────────┼────────────┼───────┼──────────┼──────────┼───────┼──────────────┤
│    ▼    │ 2026-09-11 │ Fri   │ 09:20    │ 15:15    │ -37.92│ time_exit    │
├─────────┴────────────┴───────┴──────────┴──────────┴───────┴──────────────┤
│  Leg Details:                                                              │
│  ┌────────┬──────┬──────────┬──────┬─────────────┬───────────┬──────────┐ │
│  │ Strike │ Type │ Position │ Lots │ Entry Price │ Exit Price│ Leg P&L  │ │
│  ├────────┼──────┼──────────┼──────┼─────────────┼───────────┼──────────┤ │
│  │ 23250  │ CE   │ BUY      │ 1    │ ₹159.95     │ ₹237.65   │ +₹77.70  │ │
│  │ 23350  │ CE   │ SELL     │ 1    │ ₹52.85      │ ₹161.90   │ -₹109.05 │ │
│  └────────┴──────┴──────────┴──────┴─────────────┴───────────┴──────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

## Features

### 1. Expandable Rows
- Click the **▶** button to expand
- Shows **▼** when expanded
- Click again to collapse

### 2. Individual Leg Information
Each leg shows:
- **Strike Price**: The strike at which the option was traded
- **Type**: CE (Call) or PE (Put)
- **Position**: BUY or SELL
- **Lots**: Number of lots traded
- **Entry Price**: Premium paid/received when entering (₹)
- **Exit Price**: Premium paid/received when exiting (₹)
- **Leg P&L**: Profit/Loss for this specific leg (₹)
- **Source**: Whether data is from real Upstox API or estimated

### 3. Color Coding
- **CE options**: Green
- **PE options**: Orange
- **BUY positions**: Blue
- **SELL positions**: Red
- **Profitable legs**: Green P&L
- **Loss-making legs**: Red P&L
- **Real data source**: Green
- **Estimated data**: Orange

## Example Strategies

### Bull Call Spread
```
Leg 1: Buy ATM CE at ₹159.95 → Exit at ₹237.65 (+₹77.70)
Leg 2: Sell OTM CE at ₹52.85 → Exit at ₹161.90 (-₹109.05)
Net P&L: -₹37.92
```

### Iron Condor (4 legs)
```
Leg 1: Sell OTM CE (200)
Leg 2: Buy Further OTM CE (300)
Leg 3: Sell OTM PE (-200)
Leg 4: Buy Further OTM PE (-300)
```
Each leg shows individual entry/exit prices!

## Data Accuracy

- **Real Data**: Fetched from Upstox historical API
- **Estimated Data**: Calculated using Black-Scholes (fallback)
- Each leg shows its data source individually
- You can have mixed sources (some legs real, some estimated)

## Use Cases

### 1. Strategy Analysis
See which leg contributed to profit/loss:
- Did the bought options gain value?
- Were sold options profitable?
- Which strikes performed better?

### 2. Premium Verification
Verify actual market premiums:
- Compare entry vs exit prices
- Understand slippage
- Analyze time decay

### 3. Multi-Leg Optimization
For complex strategies:
- Identify weak legs
- Optimize strike selection
- Compare different expiries

## Technical Details

### Backend
- Stores individual leg premiums in TradeRecord
- Fetches entry AND exit prices for each leg
- Calculates leg-level P&L
- Preserves data source per leg

### Frontend
- Expandable row component
- Responsive design
- Sortable/filterable (main table)
- Pagination support

## How to Access

1. Run a backtest
2. Scroll to **Trade Log** section
3. Look for **▶** button in Details column
4. Click to expand and view leg details
5. Click again to collapse

## Notes

- Leg details available for all strategies (1-8 legs)
- Works with both real and estimated data
- Data persists in saved backtests
- Can be exported via CSV (includes leg data)

---

**Feature Status**: ✅ Live and Functional

**Last Updated**: 2026-09-13

**Compatibility**: All browsers, all screen sizes
