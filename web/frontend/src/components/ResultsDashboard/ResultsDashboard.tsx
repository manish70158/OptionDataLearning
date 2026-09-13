import React, { useMemo, useState } from 'react';
import type {
  BacktestResult,
  BacktestSummary,
  DrawdownPoint,
  EquityCurvePoint,
  TradeRecord,
} from '../../types/backtest';
import SummaryStats from './SummaryStats';
import EquityCurve from './EquityCurve';
import DrawdownChart from './DrawdownChart';
import MonthlyHeatmap from './MonthlyHeatmap';
import TradeLog from './TradeLog';
import DayOfWeekBreakdown from './DayOfWeekBreakdown';

interface ResultsDashboardProps {
  result: BacktestResult | null;
  onSave?: (result: BacktestResult) => void;
}

type DteFilter = 'all' | '0' | '1' | '2' | '3plus';

function matchesDte(dte: number | undefined | null, filter: DteFilter): boolean {
  if (filter === 'all') return true;
  if (dte === undefined || dte === null) return false;
  if (filter === '3plus') return dte >= 3;
  return dte === Number(filter);
}

function maxConsecutive(values: number[], cond: (n: number) => boolean): number {
  let max = 0;
  let c = 0;
  for (const v of values) {
    if (cond(v)) {
      c += 1;
      if (c > max) max = c;
    } else {
      c = 0;
    }
  }
  return max;
}

function recomputeDerived(
  filtered: TradeRecord[],
  originalSummary: BacktestSummary,
): { summary: BacktestSummary; trades: TradeRecord[]; equity_curve: EquityCurvePoint[]; drawdown: DrawdownPoint[]; monthly_pnl: Record<string, number> } {
  // Rebuild cumulative P&L over the filtered subset
  let cum = 0;
  const trades: TradeRecord[] = filtered.map((t) => {
    cum += t.pnl_points;
    return { ...t, cumulative_pnl: Math.round(cum * 100) / 100 };
  });

  const pnls = trades.map((t) => t.pnl_points);
  const wins = pnls.filter((p) => p > 0);
  const losses = pnls.filter((p) => p <= 0);
  const total_pnl = pnls.reduce((a, b) => a + b, 0);
  const num_trades = trades.length;
  const win_rate = num_trades > 0 ? (wins.length / num_trades) * 100 : 0;

  let peak = 0;
  let max_dd = 0;
  let cumulative = 0;
  for (const p of pnls) {
    cumulative += p;
    if (cumulative > peak) peak = cumulative;
    const dd = cumulative - peak;
    if (dd < max_dd) max_dd = dd;
  }
  const max_dd_pct = peak > 0 ? (max_dd / peak) * 100 : 0;

  let sharpe = 0;
  if (pnls.length > 1) {
    const mean = total_pnl / pnls.length;
    const variance = pnls.reduce((a, p) => a + (p - mean) ** 2, 0) / pnls.length;
    const std = Math.sqrt(variance);
    sharpe = std > 0 ? (mean / std) * Math.sqrt(252) : 0;
  }

  const avg_win = wins.length > 0 ? wins.reduce((a, b) => a + b, 0) / wins.length : 0;
  const avg_loss = losses.length > 0 ? losses.reduce((a, b) => a + b, 0) / losses.length : 0;
  const gross_profit = wins.reduce((a, b) => a + b, 0);
  const gross_loss = Math.abs(losses.reduce((a, b) => a + b, 0));
  const profit_factor = gross_loss > 0 ? gross_profit / gross_loss : gross_profit > 0 ? 999.99 : 0;

  // Infer lot size from the original summary so total_pnl_inr stays consistent.
  const lotSize =
    originalSummary.total_pnl !== 0 && originalSummary.total_pnl_inr !== 0
      ? originalSummary.total_pnl_inr / originalSummary.total_pnl
      : 75;

  const summary: BacktestSummary = {
    total_pnl: Math.round(total_pnl * 100) / 100,
    total_pnl_inr: Math.round(total_pnl * lotSize * 100) / 100,
    num_trades,
    win_rate: Math.round(win_rate * 100) / 100,
    max_drawdown: Math.round(max_dd * 100) / 100,
    max_drawdown_pct: Math.round(max_dd_pct * 100) / 100,
    sharpe_ratio: Math.round(sharpe * 10000) / 10000,
    avg_win: Math.round(avg_win * 100) / 100,
    avg_loss: Math.round(avg_loss * 100) / 100,
    profit_factor: Math.round(Math.min(profit_factor, 999.99) * 100) / 100,
    max_consecutive_wins: maxConsecutive(pnls, (x) => x > 0),
    max_consecutive_losses: maxConsecutive(pnls, (x) => x <= 0),
  };

  const equity_curve: EquityCurvePoint[] = trades.map((t) => ({
    date: t.date,
    cumulative_pnl: t.cumulative_pnl,
  }));

  let peak2 = 0;
  const drawdown: DrawdownPoint[] = trades.map((t) => {
    if (t.cumulative_pnl > peak2) peak2 = t.cumulative_pnl;
    const dd_pct = peak2 > 0 ? ((t.cumulative_pnl - peak2) / peak2) * 100 : 0;
    return { date: t.date, drawdown_pct: Math.round(dd_pct * 100) / 100 };
  });

  const monthly_pnl: Record<string, number> = {};
  for (const t of trades) {
    const key = t.date.slice(0, 7);
    monthly_pnl[key] = (monthly_pnl[key] || 0) + t.pnl_points;
  }
  for (const k of Object.keys(monthly_pnl)) {
    monthly_pnl[k] = Math.round(monthly_pnl[k] * 100) / 100;
  }

  return { summary, trades, equity_curve, drawdown, monthly_pnl };
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ result, onSave }) => {
  const [dteFilter, setDteFilter] = useState<DteFilter>('all');

  const hasDteData = useMemo(
    () => (result?.trades ?? []).some((t) => t.dte !== undefined && t.dte !== null),
    [result],
  );

  const view = useMemo(() => {
    if (!result) return null;
    if (dteFilter === 'all' || !hasDteData) {
      return {
        summary: result.summary,
        trades: result.trades,
        equity_curve: result.equity_curve,
        drawdown: result.drawdown,
        monthly_pnl: result.monthly_pnl,
      };
    }
    const filtered = result.trades.filter((t) => matchesDte(t.dte, dteFilter));
    return recomputeDerived(filtered, result.summary);
  }, [result, dteFilter, hasDteData]);

  const containerStyle: React.CSSProperties = {
    backgroundColor: '#1a1a2e',
    minHeight: '100vh',
    padding: '40px',
    color: '#ffffff',
  };

  const headerStyle: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
    flexWrap: 'wrap',
    gap: '15px',
  };

  const titleStyle: React.CSSProperties = {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#ffffff',
  };

  const buttonContainerStyle: React.CSSProperties = {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
    flexWrap: 'wrap',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '12px 24px',
    backgroundColor: '#2196f3',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  };

  const emptyStateStyle: React.CSSProperties = {
    textAlign: 'center',
    padding: '60px',
    fontSize: '18px',
    color: '#a0a0a0',
  };

  const downloadCSV = () => {
    if (!view) return;

    const headers = [
      'Date',
      'Day',
      'DTE',
      'Entry Time',
      'Exit Time',
      'Entry Premium',
      'Exit Premium',
      'P&L',
      'Exit Reason',
      'Cumulative P&L',
      'VIX',
    ];

    const rows = view.trades.map((trade) => [
      trade.date,
      trade.day_of_week,
      trade.dte ?? '',
      trade.entry_time,
      trade.exit_time,
      trade.entry_premium.toFixed(2),
      trade.exit_premium.toFixed(2),
      trade.pnl_points.toFixed(2),
      trade.exit_reason,
      trade.cumulative_pnl.toFixed(2),
      (trade.vix ?? 0).toFixed(2),
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((row) => row.map((cell) => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `backtest_results_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSave = () => {
    if (result && onSave) {
      onSave(result);
    }
  };

  if (!result || !view) {
    return (
      <div style={containerStyle}>
        <div style={emptyStateStyle}>
          No backtest results to display. Run a backtest to see results here.
        </div>
      </div>
    );
  }

  const inferredLotSize =
    view.summary.total_pnl !== 0 && view.summary.total_pnl_inr !== 0
      ? view.summary.total_pnl_inr / view.summary.total_pnl
      : 1;

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <div style={titleStyle}>Backtest Results</div>
        <div style={buttonContainerStyle}>
          {hasDteData && (
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#ffffff', fontSize: '14px' }}>
              DTE:
              <select
                value={dteFilter}
                onChange={(e) => setDteFilter(e.target.value as DteFilter)}
                style={{
                  padding: '10px 12px',
                  backgroundColor: '#16213e',
                  border: '1px solid #2a2a4a',
                  borderRadius: '6px',
                  color: '#ffffff',
                  fontSize: '14px',
                  cursor: 'pointer',
                }}
              >
                <option value="all">All</option>
                <option value="0">0 DTE (Expiry Day)</option>
                <option value="1">1 DTE</option>
                <option value="2">2 DTE</option>
                <option value="3plus">3+ DTE</option>
              </select>
            </label>
          )}
          <button
            onClick={downloadCSV}
            style={buttonStyle}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#1976d2')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#2196f3')}
          >
            Export CSV
          </button>
          {onSave && (
            <button
              onClick={handleSave}
              style={{ ...buttonStyle, backgroundColor: '#4caf50' }}
              onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#388e3c')}
              onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#4caf50')}
            >
              Save Backtest
            </button>
          )}
        </div>
      </div>

      {dteFilter !== 'all' && hasDteData && (
        <div style={{
          backgroundColor: '#16213e',
          padding: '12px 16px',
          borderRadius: '6px',
          marginBottom: '20px',
          fontSize: '14px',
          color: '#ff9800',
          border: '1px solid #ff9800',
        }}>
          Filtered by DTE = {dteFilter === '3plus' ? '3+' : dteFilter}. Showing {view.trades.length} of {result.trades.length} trades. All metrics below are recomputed from this subset.
        </div>
      )}

      <SummaryStats summary={view.summary} />

      <EquityCurve data={view.equity_curve} lotSize={inferredLotSize} />

      <DrawdownChart data={view.drawdown} />

      <DayOfWeekBreakdown trades={view.trades} />

      <MonthlyHeatmap data={view.monthly_pnl} lotSize={inferredLotSize} />

      <TradeLog trades={view.trades} />
    </div>
  );
};

export default ResultsDashboard;
