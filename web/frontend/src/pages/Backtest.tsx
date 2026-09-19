import { useEffect, useState } from 'react';
import { StrategyBuilder } from '../components/StrategyBuilder';
import BacktestConfig from '../components/BacktestConfig';
import ResultsDashboard from '../components/ResultsDashboard/ResultsDashboard';
import { useBacktest } from '../hooks/useBacktest';

const styles = {
  container: {
    display: 'flex',
    gap: '20px',
    padding: '20px',
    minHeight: '100vh',
    backgroundColor: '#0f0f1a',
    color: '#e0e0e0',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  } as React.CSSProperties,
  leftPanel: {
    flex: '0 0 420px',
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '16px',
    maxHeight: '100vh',
    overflowY: 'auto' as const,
  } as React.CSSProperties,
  rightPanel: {
    flex: 1,
    minWidth: 0,
    maxHeight: '100vh',
    overflowY: 'auto' as const,
  } as React.CSSProperties,
  header: {
    padding: '16px 20px',
    backgroundColor: '#16213e',
    borderRadius: '8px',
    marginBottom: '4px',
  } as React.CSSProperties,
  title: {
    margin: 0,
    fontSize: '20px',
    fontWeight: 700,
    color: '#fff',
  } as React.CSSProperties,
  subtitle: {
    margin: '4px 0 0',
    fontSize: '13px',
    color: '#888',
  } as React.CSSProperties,
  dataStatus: {
    padding: '12px 16px',
    backgroundColor: '#16213e',
    borderRadius: '8px',
    fontSize: '13px',
  } as React.CSSProperties,
  syncBtn: {
    padding: '6px 14px',
    backgroundColor: '#3b82f6',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
    marginLeft: '8px',
  } as React.CSSProperties,
  syncBtnDisabled: {
    padding: '6px 14px',
    backgroundColor: '#555',
    color: '#999',
    border: 'none',
    borderRadius: '4px',
    fontSize: '12px',
    marginLeft: '8px',
    cursor: 'not-allowed',
  } as React.CSSProperties,
  placeholder: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '400px',
    backgroundColor: '#16213e',
    borderRadius: '8px',
    color: '#666',
    fontSize: '16px',
  } as React.CSSProperties,
  errorBanner: {
    padding: '12px 16px',
    backgroundColor: '#3b1111',
    border: '1px solid #f87171',
    borderRadius: '8px',
    color: '#f87171',
    fontSize: '13px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  } as React.CSSProperties,
  progressBar: {
    height: '4px',
    backgroundColor: '#1e293b',
    borderRadius: '2px',
    overflow: 'hidden' as const,
    marginTop: '8px',
  } as React.CSSProperties,
  progressFill: {
    height: '100%',
    backgroundColor: '#3b82f6',
    transition: 'width 0.3s ease',
  } as React.CSSProperties,
};

export default function Backtest() {
  const {
    strategy,
    setStrategy,
    config,
    setConfig,
    result,
    isRunning,
    progress,
    error,
    setError,
    dataStatus,
    isSyncing,
    syncProgress,
    syncingUnderlying,
    startBacktest,
    startSync,
    startBhavcopyBackfill,
    catchUpUnderlying,
    catchUpAll,
    dataSource,
    setDataSource,
    fetchDataStatus,
    saveBacktest,
  } = useBacktest();

  // Custom-range fetch panel state
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
  const twoYearsAgo = new Date();
  twoYearsAgo.setFullYear(twoYearsAgo.getFullYear() - 2);
  const [customUnderlying, setCustomUnderlying] = useState<'NIFTY' | 'BANKNIFTY' | 'SENSEX'>('NIFTY');
  const [customStart, setCustomStart] = useState<string>(twoYearsAgo.toISOString().split('T')[0]);
  const [customEnd, setCustomEnd] = useState<string>(oneYearAgo.toISOString().split('T')[0]);
  const [showCustom, setShowCustom] = useState<boolean>(false);

  useEffect(() => {
    fetchDataStatus();
  }, [fetchDataStatus]);

  const underlyings: Array<keyof NonNullable<typeof dataStatus>> = ['NIFTY', 'BANKNIFTY', 'SENSEX'];
  const today = new Date().toISOString().split('T')[0];
  const rowsToShow = underlyings.filter((u) => u in (dataStatus ?? {}));

  return (
    <div style={styles.container}>
      <div style={styles.leftPanel}>
        <div style={styles.header}>
          <h1 style={styles.title}>Options Strategy Backtester</h1>
          <p style={styles.subtitle}>Build, test, and analyze option strategies</p>
        </div>

        {/* Data sync status */}
        <div style={styles.dataStatus}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', gap: '8px', flexWrap: 'wrap' }}>
            <div style={{ fontWeight: 600, color: '#fff' }}>Data Status</div>
            <div style={{ display: 'flex', gap: '6px' }}>
              <a
                href="/api/auth/upstox/authorize"
                target="_blank"
                rel="noreferrer"
                style={{ ...styles.syncBtn, textDecoration: 'none', backgroundColor: '#0ea5e9', display: 'inline-block' }}
                title="Grant the deployed app a fresh Upstox access token (needs to be redone daily)"
              >
                Authorise Upstox
              </a>
            <button
              style={isSyncing ? styles.syncBtnDisabled : styles.syncBtn}
              onClick={catchUpAll}
              disabled={isSyncing}
              title="Sync every underlying from its last cached date up to today"
            >
              {isSyncing ? `Syncing ${syncingUnderlying ?? ''} ${syncProgress}%…` : 'Catch up all'}
            </button>
            </div>
          </div>
          {rowsToShow.map((u) => {
            const s = (dataStatus as unknown as Record<string, { first_date?: string | null; last_date?: string | null; trading_days_count?: number } | undefined>)[u];
            const lastDate = s?.last_date ?? null;
            // Count weekdays (Mon–Fri) strictly between lastDate and today. Weekends
            // never carry data, so cache ending on Friday is "current" through Sun.
            const tradingDaysBehind = (() => {
              if (!lastDate) return null;
              const start = new Date(lastDate);
              const end = new Date(today);
              start.setDate(start.getDate() + 1);
              let n = 0;
              while (start <= end) {
                const day = start.getDay();
                if (day !== 0 && day !== 6) n += 1;
                start.setDate(start.getDate() + 1);
              }
              return n;
            })();
            const upToDate = tradingDaysBehind !== null && tradingDaysBehind === 0;
            const behindLabel = lastDate
              ? tradingDaysBehind === 0
                ? 'current'
                : `${tradingDaysBehind} trading day${tradingDaysBehind === 1 ? '' : 's'} behind`
              : 'no data';
            return (
              <div key={u} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '4px 0', borderTop: '1px solid #1e2a4a' }}>
                <div>
                  <span style={{ fontWeight: 600 }}>{u}: </span>
                  {s?.first_date ? (
                    <span>{s.first_date} → {s.last_date} <span style={{ color: '#888' }}>({s.trading_days_count}d)</span></span>
                  ) : (
                    <span style={{ color: '#f59e0b' }}>no cache</span>
                  )}
                  <span style={{ marginLeft: '8px', color: upToDate ? '#4ade80' : '#f59e0b', fontSize: '11px' }}>
                    {behindLabel}
                  </span>
                </div>
                <button
                  style={isSyncing ? styles.syncBtnDisabled : styles.syncBtn}
                  disabled={isSyncing}
                  onClick={() => catchUpUnderlying(u as string)}
                  title={lastDate ? `Sync ${u} from ${lastDate} to ${today}` : `Sync last 30 days of ${u}`}
                >
                  {isSyncing && syncingUnderlying === u ? `${syncProgress}%` : (lastDate ? 'Catch up' : 'Sync 30d')}
                </button>
              </div>
            );
          })}
          <div style={{ marginTop: '6px', color: '#94a3b8', fontSize: '11px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>Cache: {dataStatus?.cache_size_mb ?? 0} MB</span>
              <span style={{ color: '#4b5563' }}>·</span>
              <span>Source:</span>
              <label style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="data-source"
                  checked={dataSource === 'bhavcopy'}
                  onChange={() => setDataSource('bhavcopy')}
                  disabled={isSyncing}
                />
                Bhavcopy
              </label>
              <label style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="data-source"
                  checked={dataSource === 'upstox'}
                  onChange={() => setDataSource('upstox')}
                  disabled={isSyncing}
                />
                Upstox
              </label>
            </div>
            <button
              style={{ ...styles.syncBtn, marginLeft: 0, backgroundColor: showCustom ? '#334155' : '#3b82f6' }}
              onClick={() => setShowCustom((v) => !v)}
              disabled={isSyncing}
            >
              {showCustom ? 'Hide' : 'Fetch older…'}
            </button>
          </div>

          {showCustom && (
            <div style={{ marginTop: '10px', padding: '10px', backgroundColor: '#0f172a', borderRadius: '6px', border: '1px solid #1e2a4a' }}>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '8px' }}>
                Pull a custom date range for one underlying. Useful for backfilling months or years of history.
              </div>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', alignItems: 'center', marginBottom: '8px' }}>
                <select
                  value={customUnderlying}
                  onChange={(e) => setCustomUnderlying(e.target.value as 'NIFTY' | 'BANKNIFTY' | 'SENSEX')}
                  style={{ padding: '4px 8px', backgroundColor: '#16213e', color: '#fff', border: '1px solid #2a2a4a', borderRadius: '4px', fontSize: '12px' }}
                  disabled={isSyncing}
                >
                  <option value="NIFTY">NIFTY</option>
                  <option value="BANKNIFTY">BANKNIFTY</option>
                  <option value="SENSEX">SENSEX</option>
                </select>
                <input
                  type="date"
                  value={customStart}
                  onChange={(e) => setCustomStart(e.target.value)}
                  disabled={isSyncing}
                  style={{ padding: '4px 6px', backgroundColor: '#16213e', color: '#fff', border: '1px solid #2a2a4a', borderRadius: '4px', fontSize: '12px' }}
                />
                <span style={{ color: '#94a3b8' }}>→</span>
                <input
                  type="date"
                  value={customEnd}
                  onChange={(e) => setCustomEnd(e.target.value)}
                  disabled={isSyncing}
                  style={{ padding: '4px 6px', backgroundColor: '#16213e', color: '#fff', border: '1px solid #2a2a4a', borderRadius: '4px', fontSize: '12px' }}
                />
                <button
                  style={isSyncing ? styles.syncBtnDisabled : styles.syncBtn}
                  disabled={isSyncing || !customStart || !customEnd || customStart >= customEnd}
                  onClick={() => startBhavcopyBackfill(customUnderlying, customStart, customEnd)}
                  title="Load daily OHLC for every option contract that traded in the range — includes already-expired weeklies (via NSE/BSE bhavcopy). Recommended."
                >
                  Fetch (Bhavcopy)
                </button>
                <button
                  style={isSyncing ? styles.syncBtnDisabled : { ...styles.syncBtn, backgroundColor: '#475569' }}
                  disabled={isSyncing || !customStart || !customEnd || customStart >= customEnd}
                  onClick={() => startSync(customUnderlying, customStart, customEnd)}
                  title="Fetch via Upstox live-instruments master. Only covers the current-forward weekly for historical dates."
                >
                  Fetch (Upstox)
                </button>
              </div>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {[
                  { label: '3m', months: 3 },
                  { label: '6m', months: 6 },
                  { label: '1y', months: 12 },
                  { label: '2y', months: 24 },
                  { label: '3y', months: 36 },
                  { label: '5y', months: 60 },
                ].map(({ label, months }) => (
                  <button
                    key={label}
                    disabled={isSyncing}
                    style={{
                      padding: '4px 10px',
                      backgroundColor: isSyncing ? '#334155' : '#1e293b',
                      color: '#e2e8f0',
                      border: '1px solid #334155',
                      borderRadius: '4px',
                      cursor: isSyncing ? 'not-allowed' : 'pointer',
                      fontSize: '11px',
                    }}
                    onClick={() => {
                      const end = new Date();
                      const start = new Date();
                      start.setMonth(start.getMonth() - months);
                      const s = start.toISOString().split('T')[0];
                      const e = end.toISOString().split('T')[0];
                      setCustomStart(s);
                      setCustomEnd(e);
                      // Presets honour the active data source preference.
                      if (dataSource === 'bhavcopy') {
                        startBhavcopyBackfill(customUnderlying, s, e);
                      } else {
                        startSync(customUnderlying, s, e);
                      }
                    }}
                    title={`Fetch last ${label} of ${customUnderlying} via ${dataSource === 'bhavcopy' ? 'bhavcopy' : 'Upstox'}`}
                  >
                    Last {label}
                  </button>
                ))}
              </div>
              <div style={{ marginTop: '8px', color: '#64748b', fontSize: '10px' }}>
                {dataSource === 'bhavcopy'
                  ? 'Bhavcopy (default): pulls all strikes’ daily OHLC per contract + real 5-min intraday for ATM ± 5 across the two nearest expiries. Works for expired contracts. Only needs Upstox for intraday step.'
                  : 'Upstox live-master: only fetches the current-forward weekly for each day (ATM ± 2 strikes). Fast but historical dates roll to the wrong expiry — use bhavcopy for anything older than a week.'}
              </div>
            </div>
          )}

          {isSyncing && (
            <div style={styles.progressBar}>
              <div style={{ ...styles.progressFill, width: `${syncProgress}%` }} />
            </div>
          )}
        </div>

        {error && (
          <div style={styles.errorBanner}>
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              style={{ background: 'none', border: 'none', color: '#f87171', cursor: 'pointer', fontSize: '16px' }}
            >
              ×
            </button>
          </div>
        )}

        <StrategyBuilder strategy={strategy} onChange={setStrategy} />
        <BacktestConfig
          config={config}
          onChange={setConfig}
          onSubmit={startBacktest}
          isRunning={isRunning}
        />

        {isRunning && (
          <div style={styles.dataStatus}>
            <div style={{ color: '#3b82f6', fontWeight: 600 }}>
              Running backtest... {progress}%
            </div>
            <div style={styles.progressBar}>
              <div style={{ ...styles.progressFill, width: `${progress}%` }} />
            </div>
          </div>
        )}
      </div>

      <div style={styles.rightPanel}>
        {result ? (
          <ResultsDashboard result={result} onSave={saveBacktest} />
        ) : (
          <div style={styles.placeholder}>
            Configure a strategy and click "Run Backtest" to see results
          </div>
        )}
      </div>
    </div>
  );
}
