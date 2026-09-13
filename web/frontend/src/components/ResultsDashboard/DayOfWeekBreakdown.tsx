import React, { useMemo } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import type { TradeRecord } from '../../types/backtest';

interface DayOfWeekBreakdownProps {
  trades: TradeRecord[];
}

const DayOfWeekBreakdown: React.FC<DayOfWeekBreakdownProps> = ({ trades }) => {
  const dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  // Prefer backend-provided pnl_inr; fall back to pnl_points × inferred lot size
  const lotSizeSample = trades.find((t) => t.pnl_points !== 0 && t.pnl_inr !== 0);
  const lotSize = lotSizeSample ? lotSizeSample.pnl_inr / lotSizeSample.pnl_points : 1;

  const dayData = useMemo(() => {
    const dayTotals: Record<string, { sum: number; count: number }> = {};

    trades.forEach((trade) => {
      if (!dayTotals[trade.day_of_week]) {
        dayTotals[trade.day_of_week] = { sum: 0, count: 0 };
      }
      dayTotals[trade.day_of_week].sum += trade.pnl_inr || trade.pnl_points * lotSize;
      dayTotals[trade.day_of_week].count += 1;
    });

    return dayOrder.map((day) => ({
      day,
      avgPnl: dayTotals[day] ? dayTotals[day].sum / dayTotals[day].count : 0,
      count: dayTotals[day] ? dayTotals[day].count : 0,
    }));
  }, [trades, lotSize]);

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#16213e',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '30px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
  };

  const titleStyle: React.CSSProperties = {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: '20px',
  };

  return (
    <div style={cardStyle}>
      <div style={titleStyle}>Day of Week Breakdown (Average P&L)</div>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={dayData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
          <XAxis
            dataKey="day"
            stroke="#a0a0a0"
            tick={{ fill: '#a0a0a0' }}
          />
          <YAxis
            stroke="#a0a0a0"
            tick={{ fill: '#a0a0a0' }}
            tickFormatter={(value) => `₹${value.toFixed(0)}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#16213e',
              border: '1px solid #2a2a4a',
              borderRadius: '4px',
              color: '#ffffff',
            }}
            formatter={(value: any) => {
              const numValue = typeof value === 'number' ? value : 0;
              return [`₹${numValue.toFixed(2)}`, 'Avg P&L'];
            }}
          />
          <Bar dataKey="avgPnl" name="Avg P&L" radius={[8, 8, 0, 0]}>
            {dayData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.avgPnl >= 0 ? '#4caf50' : '#f44336'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DayOfWeekBreakdown;
