import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import type { DrawdownPoint } from '../../types/backtest';

interface DrawdownChartProps {
  data: DrawdownPoint[];
}

const DrawdownChart: React.FC<DrawdownChartProps> = ({ data }) => {
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
      <div style={titleStyle}>Drawdown</div>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
          <XAxis
            dataKey="date"
            stroke="#a0a0a0"
            tick={{ fill: '#a0a0a0' }}
          />
          <YAxis
            stroke="#a0a0a0"
            tick={{ fill: '#a0a0a0' }}
            tickFormatter={(value) => `${value.toFixed(1)}%`}
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
              return [`${numValue.toFixed(2)}%`, 'Drawdown'];
            }}
          />
          <Area
            type="monotone"
            dataKey="drawdown_pct"
            stroke="#f44336"
            fill="#f44336"
            fillOpacity={0.6}
            name="Drawdown"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DrawdownChart;
