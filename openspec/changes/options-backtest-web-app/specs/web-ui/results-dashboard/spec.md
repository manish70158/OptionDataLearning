## Purpose

Backtest results visualization dashboard that displays the performance of a backtested strategy through charts, statistics, and a detailed trade log.

## ADDED Requirements

### Requirement: Summary statistics panel
The dashboard SHALL display a summary panel at the top with key metrics: total P&L (points), net P&L (INR, based on lot size), number of trades, win rate (%), max drawdown (points and %), Sharpe ratio, average profit per winning trade, average loss per losing trade, profit factor, and max consecutive wins/losses.

#### Scenario: Statistics displayed after backtest
- **WHEN** a backtest completes successfully
- **THEN** the summary panel SHALL display all key metrics calculated from the trade results

#### Scenario: Zero trades
- **WHEN** a backtest produces zero trades (all days filtered out)
- **THEN** the summary panel SHALL display "No trades matched the filter criteria" instead of metrics

### Requirement: Equity curve chart
The dashboard SHALL display a line chart showing cumulative P&L over time. The X-axis SHALL show dates, the Y-axis SHALL show cumulative P&L in points. The chart SHALL be interactive (hover to see date and P&L value).

#### Scenario: Equity curve rendering
- **WHEN** backtest results are loaded
- **THEN** an equity curve line chart SHALL render with one data point per trade day, showing cumulative P&L progression

#### Scenario: Hover on equity curve
- **WHEN** user hovers over a point on the equity curve
- **THEN** a tooltip SHALL show the date, day's P&L, and cumulative P&L at that point

### Requirement: Drawdown chart
The dashboard SHALL display a drawdown chart below the equity curve, showing peak-to-trough drawdown over time as a filled area chart (negative values, colored red).

#### Scenario: Drawdown visualization
- **WHEN** backtest results are loaded
- **THEN** a drawdown area chart SHALL render showing drawdown percentage from peak equity at each point in time

### Requirement: Monthly P&L heatmap
The dashboard SHALL display a heatmap table with months as columns and years as rows, showing the total P&L for each month. Green shading for profitable months, red for losing months. Intensity SHALL scale with magnitude.

#### Scenario: Heatmap rendering
- **WHEN** backtest spans multiple months
- **THEN** a monthly heatmap SHALL display with each cell showing the month's total P&L, colored from deep red (worst month) to deep green (best month)

#### Scenario: Single month backtest
- **WHEN** backtest spans less than one full month
- **THEN** the heatmap SHALL show a single cell for that partial month

### Requirement: Trade log table
The dashboard SHALL display a sortable, paginated table of all individual trades with columns: date, day of week, DTE (when trade records carry it), entry time, exit time, entry premium, exit premium, P&L (points), P&L (INR), exit reason (SL/TP/trailing SL/time exit), cumulative P&L, VIX at entry.

#### Scenario: Viewing trade log
- **WHEN** backtest results are loaded
- **THEN** a table SHALL display all trades with 20 rows per page and pagination controls

#### Scenario: Sorting trade log
- **WHEN** user clicks on the "P&L" column header
- **THEN** the table SHALL sort trades by P&L in descending order; clicking again SHALL reverse to ascending

#### Scenario: Filtering trade log
- **WHEN** user types in the search/filter box
- **THEN** the table SHALL filter trades matching the search text across date, exit reason, or day of week columns

### Requirement: Day of week breakdown
The dashboard SHALL display a bar chart showing average P&L grouped by day of the week (Monday through Friday).

#### Scenario: Day breakdown rendering
- **WHEN** backtest results are loaded
- **THEN** a bar chart SHALL display average P&L per weekday, with positive bars in green and negative in red

### Requirement: Export results
The dashboard SHALL allow exporting backtest results as a CSV file containing the full trade log.

#### Scenario: CSV export
- **WHEN** user clicks "Export CSV"
- **THEN** the browser SHALL download a CSV file containing all trade records with all columns from the trade log

### Requirement: Share/save backtest
The dashboard SHALL allow saving a backtest configuration and results with a unique identifier, so the user can return to view results later.

#### Scenario: Save backtest
- **WHEN** user clicks "Save"
- **THEN** the system SHALL persist the strategy configuration, backtest parameters, and results, and display a unique backtest ID

#### Scenario: Load saved backtest
- **WHEN** user navigates to a saved backtest URL or enters a backtest ID
- **THEN** the system SHALL load and display the saved results and configuration

### Requirement: INR (₹) currency formatting
Every user-facing money value in the dashboard — summary tiles (Total P&L, Max Drawdown, Avg Win, Avg Loss), chart axes (Equity Curve, Drawdown, Day-of-Week Breakdown Y-axis), chart tooltips, monthly heatmap cells, and every price cell in the Trade Log (Entry Premium, Exit Premium, P&L, Cumulative P&L, expanded per-leg Entry/Exit/Leg P&L) — SHALL be rendered with the Indian Rupee sign `₹` (U+20B9). No user-visible `$` prefix SHALL appear for currency values.

#### Scenario: Trade log currency
- **WHEN** the trade log renders any row
- **THEN** the Entry Premium, Exit Premium, P&L and Cumulative P&L cells SHALL be prefixed with `₹`

#### Scenario: Chart tooltip currency
- **WHEN** the user hovers on the Equity Curve or Drawdown chart
- **THEN** the tooltip SHALL show the numeric value prefixed with `₹`

### Requirement: Dashboard-level DTE filter
The Backtest Results page SHALL expose a DTE filter dropdown in the header with options `All / 0 DTE (Expiry Day) / 1 DTE / 2 DTE / 3+ DTE`. The filter SHALL be visible only when at least one trade record carries a `dte` field. When the selection is not `All`, the frontend SHALL:
- Filter `result.trades` by the selected DTE bucket (0-DTE = exactly 0, 1/2 = exact match, 3+ = `dte >= 3`).
- Rebuild `cumulative_pnl` from the filtered trades in order.
- Recompute the summary (total_pnl, num_trades, win_rate, max_drawdown, max_drawdown_pct, sharpe_ratio, avg_win, avg_loss, profit_factor, max_consecutive_wins, max_consecutive_losses) using formulas that match the backend's `_compute_summary`, so metrics stay consistent whether the same subset were run server-side.
- Recompute equity_curve, drawdown, and monthly_pnl series from the filtered trades.
- Re-render SummaryStats, EquityCurve, DrawdownChart, DayOfWeekBreakdown, MonthlyHeatmap, and TradeLog against these filtered/derived values.
- Display a visible banner: "Filtered by DTE = X. Showing N of M trades. All metrics below are recomputed from this subset."

The filter SHALL NOT be duplicated inside the Trade Log component; the Trade Log's own search box remains but its DTE selector is removed.

#### Scenario: Filter to 0 DTE
- **WHEN** a user picks "0 DTE (Expiry Day)" on a backtest that includes 5 Tuesday trades out of 30 total
- **THEN** all six chart/table components SHALL redraw showing only those 5 trades, with the summary tiles reflecting metrics computed from those 5 rows

#### Scenario: Saved backtest without DTE data
- **WHEN** a legacy backtest (missing `dte` on all trades) is loaded
- **THEN** the DTE filter dropdown SHALL NOT render, and the dashboard SHALL behave as before

#### Scenario: total_pnl_inr scales with lot size
- **WHEN** a DTE filter narrows trades to a subset and metrics are recomputed
- **THEN** `total_pnl_inr` SHALL equal `filtered_total_pnl * inferred_lot_size`, where `inferred_lot_size = original_summary.total_pnl_inr / original_summary.total_pnl` when non-zero

### Requirement: CSV export honours filter and includes DTE
The CSV export SHALL export the currently-visible filtered trades (not the full raw set) and SHALL include a `DTE` column alongside the existing columns.

#### Scenario: Filtered CSV
- **WHEN** the DTE filter is set to "0 DTE" and the user clicks Export CSV
- **THEN** the downloaded file SHALL contain only the 0-DTE rows and a DTE column with value `0` on each row

### Requirement: All P&L values displayed in INR (points × lot_size)
Summary tiles for Total P&L, Max Drawdown, Avg Win, and Avg Loss SHALL display the aggregated INR value (points × lot_size). Each SHALL show a small caption underneath with the underlying points reading. Win Rate SHALL be rendered as `summary.win_rate` (already a percentage) — NOT multiplied by 100 again. Trade Log P&L column SHALL show `pnl_inr` with a `NN pts` caption; Cumulative P&L SHALL show `cumulative_pnl * lotSize` with the pts caption; Leg P&L (inside Leg Details) SHALL multiply per-leg points × lot_size × leg.lots. Equity Curve and Monthly Heatmap SHALL scale their point values × lot size before rendering.

Lot size SHALL be inferred from `summary.total_pnl_inr / summary.total_pnl` when both are non-zero, so the same behaviour applies to filtered subsets that recompute derived series client-side.

#### Scenario: Total P&L tile
- **WHEN** a backtest returns `total_pnl = 76.15 points` for NIFTY (lot=65)
- **THEN** the Total P&L tile SHALL show `₹4,949.75` with a `76.15 pts × 65` caption underneath

#### Scenario: Trade log P&L cell
- **WHEN** a trade record has `pnl_points = 127.85` and `pnl_inr = 8310.25`
- **THEN** the P&L cell SHALL show `₹8,310.25` with a `127.85 pts` caption

#### Scenario: Win rate
- **WHEN** `summary.win_rate = 62.96` (already a percentage)
- **THEN** the Win Rate tile SHALL show `62.96%`, NOT `6296.00%`

### Requirement: Drawdown chart reads drawdown_pct and renders as percentage
The drawdown area chart SHALL bind its `dataKey` to `drawdown_pct` (matching the backend `DrawdownPoint` schema). Both Y-axis ticks and tooltip formatter SHALL render values as percentages (e.g. `-3.42%`), not as ₹.

#### Scenario: Drawdown renders correctly
- **WHEN** the backend returns `drawdown_pct = -3.42` at some date
- **THEN** the chart's area SHALL plot -3.42 at that x-value, the Y-axis tick nearest SHALL read `-3.4%`, and hovering SHALL show `−3.42%` in the tooltip
