import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import type { EquityCurvePoint } from '../../types/backtest';

interface EquityCurveProps {
  data: EquityCurvePoint[];
  lotSize?: number;
}

const EquityCurve: React.FC<EquityCurveProps> = ({ data, lotSize = 1 }) => {
  const inrData = data.map((p) => ({ ...p, cumulative_pnl: p.cumulative_pnl * lotSize }));
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
      <div style={titleStyle}>Equity Curve</div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={inrData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
          <XAxis
            dataKey="date"
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
              return [`₹${numValue.toFixed(2)}`, 'P&L'];
            }}
          />
          <Line
            type="monotone"
            dataKey="cumulative_pnl"
            stroke="#2196f3"
            strokeWidth={2}
            dot={false}
            name="Cumulative P&L"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EquityCurve;
