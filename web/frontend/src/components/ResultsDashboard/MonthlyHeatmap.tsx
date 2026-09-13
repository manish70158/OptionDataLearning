import React from 'react';

interface MonthlyHeatmapProps {
  data: Record<string, number>;
  lotSize?: number;
}

const MonthlyHeatmap: React.FC<MonthlyHeatmapProps> = ({ data, lotSize = 1 }) => {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // Backend monthly_pnl values are per-lot points; multiply by lot_size for INR.
  const yearMonthData: Record<string, Record<number, number>> = {};
  let minValue = 0;
  let maxValue = 0;

  Object.entries(data).forEach(([key, rawValue]) => {
    const value = rawValue * lotSize;
    const [year, month] = key.split('-');
    const monthIndex = parseInt(month, 10) - 1;

    if (!yearMonthData[year]) {
      yearMonthData[year] = {};
    }
    yearMonthData[year][monthIndex] = value;

    minValue = Math.min(minValue, value);
    maxValue = Math.max(maxValue, value);
  });

  const years = Object.keys(yearMonthData).sort();

  const getColorForValue = (value: number | undefined): string => {
    if (value === undefined) return '#1a1a2e';

    if (value === 0) return '#2a2a4a';

    const absMax = Math.max(Math.abs(minValue), Math.abs(maxValue));
    const intensity = Math.abs(value) / absMax;

    if (value > 0) {
      // Green for positive
      const alpha = Math.min(intensity * 0.8 + 0.2, 1);
      return `rgba(76, 175, 80, ${alpha})`;
    } else {
      // Red for negative
      const alpha = Math.min(intensity * 0.8 + 0.2, 1);
      return `rgba(244, 67, 54, ${alpha})`;
    }
  };

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

  const tableStyle: React.CSSProperties = {
    width: '100%',
    borderCollapse: 'collapse',
  };

  const cellStyle: React.CSSProperties = {
    padding: '12px',
    textAlign: 'center',
    fontSize: '12px',
    border: '1px solid #2a2a4a',
    color: '#ffffff',
  };

  const headerCellStyle: React.CSSProperties = {
    ...cellStyle,
    backgroundColor: '#1a1a2e',
    fontWeight: 'bold',
  };

  return (
    <div style={cardStyle}>
      <div style={titleStyle}>Monthly P&L Heatmap</div>
      <div style={{ overflowX: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={headerCellStyle}>Year</th>
              {months.map((month) => (
                <th key={month} style={headerCellStyle}>{month}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {years.map((year) => (
              <tr key={year}>
                <td style={headerCellStyle}>{year}</td>
                {months.map((_, monthIndex) => {
                  const value = yearMonthData[year][monthIndex];
                  return (
                    <td
                      key={monthIndex}
                      style={{
                        ...cellStyle,
                        backgroundColor: getColorForValue(value),
                        fontWeight: value !== undefined ? 'bold' : 'normal',
                      }}
                    >
                      {value !== undefined ? `₹${value.toFixed(0)}` : '-'}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MonthlyHeatmap;
