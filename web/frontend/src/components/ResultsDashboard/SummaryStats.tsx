import React from 'react';
import type { BacktestSummary } from '../../types/backtest';

interface SummaryStatsProps {
  summary: BacktestSummary;
}

const SummaryStats: React.FC<SummaryStatsProps> = ({ summary }) => {
  // Backend summary reports P&L / drawdown / avg win/loss in *points* per lot.
  // Convert to INR using the ratio backend already exposes via total_pnl_inr.
  const lotSize =
    summary.total_pnl !== 0 && summary.total_pnl_inr !== 0
      ? summary.total_pnl_inr / summary.total_pnl
      : 1;
  const total_pnl_inr = summary.total_pnl_inr || summary.total_pnl * lotSize;
  const max_drawdown_inr = summary.max_drawdown * lotSize;
  const avg_win_inr = summary.avg_win * lotSize;
  const avg_loss_inr = summary.avg_loss * lotSize;

  const statCardStyle: React.CSSProperties = {
    backgroundColor: '#16213e',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
    boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '12px',
    color: '#a0a0a0',
    marginBottom: '8px',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  };

  const valueStyle: React.CSSProperties = {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#ffffff',
  };

  const getColoredValue = (value: number): React.CSSProperties => {
    const color = value >= 0 ? '#4caf50' : '#f44336';
    return {
      ...valueStyle,
      color,
    };
  };

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '20px',
      marginBottom: '30px',
    }}>
      <div style={statCardStyle}>
        <div style={labelStyle}>Total P&L</div>
        <div style={getColoredValue(total_pnl_inr)}>
          ₹{total_pnl_inr.toFixed(2)}
        </div>
        <div style={{ fontSize: '11px', color: '#a0a0a0', marginTop: '4px' }}>
          {summary.total_pnl.toFixed(2)} pts × {lotSize.toFixed(0)}
        </div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Total Trades</div>
        <div style={valueStyle}>{summary.num_trades}</div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Win Rate</div>
        <div style={valueStyle}>{summary.win_rate.toFixed(2)}%</div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Max Drawdown</div>
        <div style={{ ...valueStyle, color: '#f44336' }}>
          ₹{max_drawdown_inr.toFixed(2)}
        </div>
        <div style={{ fontSize: '11px', color: '#a0a0a0', marginTop: '4px' }}>
          {summary.max_drawdown.toFixed(2)} pts ({summary.max_drawdown_pct.toFixed(2)}%)
        </div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Sharpe Ratio</div>
        <div style={valueStyle}>{summary.sharpe_ratio.toFixed(3)}</div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Avg Win</div>
        <div style={{ ...valueStyle, color: '#4caf50' }}>
          ₹{avg_win_inr.toFixed(2)}
        </div>
        <div style={{ fontSize: '11px', color: '#a0a0a0', marginTop: '4px' }}>
          {summary.avg_win.toFixed(2)} pts
        </div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Avg Loss</div>
        <div style={{ ...valueStyle, color: '#f44336' }}>
          ₹{avg_loss_inr.toFixed(2)}
        </div>
        <div style={{ fontSize: '11px', color: '#a0a0a0', marginTop: '4px' }}>
          {summary.avg_loss.toFixed(2)} pts
        </div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Profit Factor</div>
        <div style={valueStyle}>{summary.profit_factor.toFixed(3)}</div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Max Consecutive Wins</div>
        <div style={{ ...valueStyle, color: '#4caf50' }}>
          {summary.max_consecutive_wins}
        </div>
      </div>

      <div style={statCardStyle}>
        <div style={labelStyle}>Max Consecutive Losses</div>
        <div style={{ ...valueStyle, color: '#f44336' }}>
          {summary.max_consecutive_losses}
        </div>
      </div>
    </div>
  );
};

export default SummaryStats;
