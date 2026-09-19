import React, { useState, useMemo } from 'react';
import type { TradeRecord } from '../../types/backtest';

interface TradeLogProps {
  trades: TradeRecord[];
}

type SortField = keyof TradeRecord;
type SortDirection = 'asc' | 'desc';

const TradeLog: React.FC<TradeLogProps> = ({ trades }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortField, setSortField] = useState<SortField>('date');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedTrades, setExpandedTrades] = useState<Set<number>>(new Set());

  const hasDteData = trades.some((t) => t.dte !== undefined && t.dte !== null);

  // Infer lot size so cumulative_pnl (a points running total) can be displayed
  // in INR. pnl_inr is per-trade INR from the backend; cumulative_pnl is in
  // points and does not have a paired INR field on the record.
  const lotSizeSample = trades.find((t) => t.pnl_points !== 0 && t.pnl_inr !== 0);
  const lotSize = lotSizeSample ? lotSizeSample.pnl_inr / lotSizeSample.pnl_points : 1;

  const itemsPerPage = 20;

  const toggleTradeExpansion = (index: number) => {
    const newExpanded = new Set(expandedTrades);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedTrades(newExpanded);
  };

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
    setCurrentPage(1);
  };

  const filteredAndSortedTrades = useMemo(() => {
    let filtered = trades;

    // Filter by search term
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter((trade) => {
        return (
          trade.date.toLowerCase().includes(searchLower) ||
          trade.day_of_week.toLowerCase().includes(searchLower) ||
          trade.exit_reason.toLowerCase().includes(searchLower) ||
          trade.pnl_points.toString().includes(searchLower)
        );
      });
    }

    // Sort
    const sorted = [...filtered].sort((a, b) => {
      const aValue = a[sortField];
      const bValue = b[sortField];

      // Handle null/undefined values
      if ((aValue === null || aValue === undefined) && (bValue === null || bValue === undefined)) return 0;
      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });

    return sorted;
  }, [trades, searchTerm, sortField, sortDirection]);

  const totalPages = Math.ceil(filteredAndSortedTrades.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentTrades = filteredAndSortedTrades.slice(startIndex, endIndex);

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

  const searchInputStyle: React.CSSProperties = {
    width: '100%',
    padding: '10px',
    marginBottom: '20px',
    backgroundColor: '#1a1a2e',
    border: '1px solid #2a2a4a',
    borderRadius: '4px',
    color: '#ffffff',
    fontSize: '14px',
  };

  const tableStyle: React.CSSProperties = {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '13px',
  };

  const thStyle: React.CSSProperties = {
    padding: '12px 8px',
    textAlign: 'left',
    backgroundColor: '#1a1a2e',
    color: '#ffffff',
    fontWeight: 'bold',
    cursor: 'pointer',
    userSelect: 'none',
    borderBottom: '2px solid #2a2a4a',
  };

  const tdStyle: React.CSSProperties = {
    padding: '12px 8px',
    borderBottom: '1px solid #2a2a4a',
    color: '#ffffff',
  };

  const paginationStyle: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '10px',
    marginTop: '20px',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '8px 16px',
    backgroundColor: '#2196f3',
    color: '#ffffff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  };

  const disabledButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#2a2a4a',
    cursor: 'not-allowed',
  };

  return (
    <div style={cardStyle}>
      <div style={titleStyle}>Trade Log</div>

      <input
        type="text"
        placeholder="Search trades..."
        value={searchTerm}
        onChange={(e) => {
          setSearchTerm(e.target.value);
          setCurrentPage(1);
        }}
        style={searchInputStyle}
      />

      <div style={{ overflowX: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Details</th>
              <th style={thStyle} onClick={() => handleSort('date')}>
                Date {sortField === 'date' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('day_of_week')}>
                Day {sortField === 'day_of_week' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              {hasDteData && (
                <th style={thStyle} onClick={() => handleSort('dte' as SortField)}>
                  DTE {sortField === 'dte' && (sortDirection === 'asc' ? '▲' : '▼')}
                </th>
              )}
              <th style={thStyle} onClick={() => handleSort('entry_time')}>
                Entry Time {sortField === 'entry_time' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('exit_time')}>
                Exit Time {sortField === 'exit_time' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('entry_premium')}>
                Entry Premium {sortField === 'entry_premium' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('exit_premium')}>
                Exit Premium {sortField === 'exit_premium' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('pnl_points')}>
                P&L {sortField === 'pnl_points' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('exit_reason')}>
                Exit Reason {sortField === 'exit_reason' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('cumulative_pnl')}>
                Cum. P&L {sortField === 'cumulative_pnl' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
              <th style={thStyle} onClick={() => handleSort('vix')}>
                VIX {sortField === 'vix' && (sortDirection === 'asc' ? '▲' : '▼')}
              </th>
            </tr>
          </thead>
          <tbody>
            {currentTrades.map((trade, index) => {
              const globalIndex = startIndex + index;
              const isExpanded = expandedTrades.has(globalIndex);
              const hasLegs = trade.legs && trade.legs.length > 0;

              return (
                <React.Fragment key={index}>
                  <tr>
                    <td style={tdStyle}>
                      {hasLegs && (
                        <button
                          onClick={() => toggleTradeExpansion(globalIndex)}
                          style={{
                            background: 'none',
                            border: 'none',
                            color: '#2196f3',
                            cursor: 'pointer',
                            fontSize: '16px',
                            padding: '0 8px',
                          }}
                          title="Show leg details"
                        >
                          {isExpanded ? '▼' : '▶'}
                        </button>
                      )}
                    </td>
                    <td style={tdStyle}>{trade.date}</td>
                    <td style={tdStyle}>{trade.day_of_week}</td>
                    {hasDteData && (
                      <td style={{
                        ...tdStyle,
                        color: trade.dte === 0 ? '#ff9800' : '#ffffff',
                        fontWeight: trade.dte === 0 ? 'bold' : 'normal',
                      }}>
                        {trade.dte ?? '-'}
                      </td>
                    )}
                    <td style={tdStyle}>{trade.entry_time}</td>
                    <td style={tdStyle}>{trade.exit_time}</td>
                    <td style={tdStyle}>₹{trade.entry_premium.toFixed(2)}</td>
                    <td style={tdStyle}>₹{trade.exit_premium.toFixed(2)}</td>
                    <td style={{
                      ...tdStyle,
                      color: trade.pnl_points >= 0 ? '#4caf50' : '#f44336',
                      fontWeight: 'bold',
                    }}>
                      ₹{(trade.pnl_inr || trade.pnl_points * lotSize).toFixed(2)}
                      <div style={{ fontSize: '10px', color: '#888', fontWeight: 'normal' }}>
                        {trade.pnl_points.toFixed(2)} pts
                      </div>
                    </td>
                    <td style={tdStyle}>{trade.exit_reason}</td>
                    <td style={{
                      ...tdStyle,
                      color: trade.cumulative_pnl >= 0 ? '#4caf50' : '#f44336',
                    }}>
                      ₹{(trade.cumulative_pnl * lotSize).toFixed(2)}
                      <div style={{ fontSize: '10px', color: '#888' }}>
                        {trade.cumulative_pnl.toFixed(2)} pts
                      </div>
                    </td>
                    <td style={tdStyle}>{trade.vix !== null ? trade.vix.toFixed(2) : 'N/A'}</td>
                  </tr>
                  {isExpanded && hasLegs && (
                    <tr>
                      <td colSpan={hasDteData ? 12 : 11} style={{ ...tdStyle, backgroundColor: '#1a1a2e', padding: '16px' }}>
                        <div style={{ fontSize: '12px', color: '#aaaaaa' }}>
                          <strong style={{ color: '#ffffff', marginBottom: '8px', display: 'block' }}>
                            Leg Details:
                          </strong>
                          <table style={{ width: '100%', marginTop: '8px' }}>
                            <thead>
                              <tr>
                                <th style={{ textAlign: 'left', padding: '4px 8px', color: '#aaaaaa' }}>Strike</th>
                                <th style={{ textAlign: 'left', padding: '4px 8px', color: '#aaaaaa' }}>Type</th>
                                <th style={{ textAlign: 'left', padding: '4px 8px', color: '#aaaaaa' }}>Position</th>
                                <th style={{ textAlign: 'right', padding: '4px 8px', color: '#aaaaaa' }}>Lots</th>
                                <th style={{ textAlign: 'right', padding: '4px 8px', color: '#aaaaaa' }}>Entry Price</th>
                                <th style={{ textAlign: 'right', padding: '4px 8px', color: '#aaaaaa' }}>Exit Price</th>
                                <th style={{ textAlign: 'right', padding: '4px 8px', color: '#aaaaaa' }}>Leg P&L</th>
                                <th style={{ textAlign: 'center', padding: '4px 8px', color: '#aaaaaa' }}>Source</th>
                              </tr>
                            </thead>
                            <tbody>
                              {trade.legs!.map((leg, legIndex) => {
                                const grossPoints = leg.position === 'buy'
                                  ? (leg.exit_premium - leg.entry_premium) * leg.lots
                                  : (leg.entry_premium - leg.exit_premium) * leg.lots;
                                // Backend deducts 2 pts × lot_size per leg as slippage
                                // (independent of leg.lots). Reflect that here so the
                                // sum of Leg P&L ties out to the trade's total P&L.
                                const SLIPPAGE_POINTS_PER_LEG = 2;
                                const legPnlPoints = grossPoints - SLIPPAGE_POINTS_PER_LEG;
                                const legPnlInr = legPnlPoints * lotSize;

                                return (
                                  <tr key={legIndex}>
                                    <td style={{ padding: '4px 8px', color: '#ffffff' }}>{leg.strike}</td>
                                    <td style={{ padding: '4px 8px', color: leg.option_type === 'CE' ? '#4caf50' : '#ff9800' }}>
                                      {leg.option_type}
                                    </td>
                                    <td style={{ padding: '4px 8px', color: leg.position === 'buy' ? '#2196f3' : '#f44336' }}>
                                      {leg.position.toUpperCase()}
                                    </td>
                                    <td style={{ padding: '4px 8px', textAlign: 'right', color: '#ffffff' }}>{leg.lots}</td>
                                    <td style={{ padding: '4px 8px', textAlign: 'right', color: '#ffffff' }}>
                                      ₹{leg.entry_premium.toFixed(2)}
                                    </td>
                                    <td style={{ padding: '4px 8px', textAlign: 'right', color: '#ffffff' }}>
                                      ₹{leg.exit_premium.toFixed(2)}
                                    </td>
                                    <td style={{
                                      padding: '4px 8px',
                                      textAlign: 'right',
                                      color: legPnlInr >= 0 ? '#4caf50' : '#f44336',
                                      fontWeight: 'bold'
                                    }}>
                                      ₹{legPnlInr.toFixed(2)}
                                      <div style={{ fontSize: '10px', color: '#888', fontWeight: 'normal' }}>
                                        {grossPoints.toFixed(2)} pts − 2 slp
                                      </div>
                                    </td>
                                    <td style={{
                                      padding: '4px 8px',
                                      textAlign: 'center',
                                      color: leg.source === 'real' ? '#4caf50' : '#ff9800'
                                    }}>
                                      {leg.source}
                                    </td>
                                  </tr>
                                );
                              })}
                            </tbody>
                          </table>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>

      <div style={paginationStyle}>
        <button
          onClick={() => setCurrentPage(1)}
          disabled={currentPage === 1}
          style={currentPage === 1 ? disabledButtonStyle : buttonStyle}
        >
          First
        </button>
        <button
          onClick={() => setCurrentPage(currentPage - 1)}
          disabled={currentPage === 1}
          style={currentPage === 1 ? disabledButtonStyle : buttonStyle}
        >
          Previous
        </button>
        <span style={{ color: '#ffffff' }}>
          Page {currentPage} of {totalPages} ({filteredAndSortedTrades.length} trades)
        </span>
        <button
          onClick={() => setCurrentPage(currentPage + 1)}
          disabled={currentPage === totalPages}
          style={currentPage === totalPages ? disabledButtonStyle : buttonStyle}
        >
          Next
        </button>
        <button
          onClick={() => setCurrentPage(totalPages)}
          disabled={currentPage === totalPages}
          style={currentPage === totalPages ? disabledButtonStyle : buttonStyle}
        >
          Last
        </button>
      </div>
    </div>
  );
};

export default TradeLog;
