import { useState, useCallback, useRef } from 'react';
import type {
  StrategyDefinition,
  BacktestConfig,
  BacktestResult,
  DataStatus,
} from '../types/backtest';
import {
  runBacktest,
  pollBacktestStatus,
  getDataStatus,
  syncData,
  pollSyncStatus,
  backfillBhavcopy,
} from '../api/client';

const POLL_INTERVAL = 1000;

const defaultStrategy: StrategyDefinition = {
  underlying: 'NIFTY',
  expiry_type: 'weekly',
  legs: [
    { position: 'buy', option_type: 'CE', strike_offset: 0, lots: 1 },
    { position: 'buy', option_type: 'PE', strike_offset: 0, lots: 1 },
  ],
};

const today = new Date();
const twoYearsAgo = new Date(today);
twoYearsAgo.setFullYear(today.getFullYear() - 2);

const defaultConfig: BacktestConfig = {
  start_date: twoYearsAgo.toISOString().split('T')[0],
  end_date: today.toISOString().split('T')[0],
  entry_time: '09:20',
  exit_time: '15:15',
  stop_loss_enabled: true,
  stop_loss_mode: 'percentage',
  stop_loss_value: 50,
  sl_scope: 'per_leg',
  target_profit_enabled: false,
  target_profit_mode: 'percentage',
  target_profit_value: 50,
  trailing_sl_enabled: false,
  trailing_sl_value: 20,
  vix_min: null,
  vix_max: null,
  weekdays: [0, 1, 2, 3, 4],
};

export function useBacktest() {
  const [strategy, setStrategy] = useState<StrategyDefinition>(defaultStrategy);
  const [config, setConfig] = useState<BacktestConfig>(defaultConfig);
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [dataStatus, setDataStatus] = useState<DataStatus | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncProgress, setSyncProgress] = useState(0);
  const [syncingUnderlying, setSyncingUnderlying] = useState<string | null>(null);
  // Data source for the "Catch up" flow. Bhavcopy is the default because it
  // works for expired weeklies too and doesn't need a live Upstox token; the
  // Upstox live-master path is retained as an opt-in for edge cases.
  const [dataSource, setDataSource] = useState<'bhavcopy' | 'upstox'>(() => {
    const saved = typeof window !== 'undefined' ? window.localStorage.getItem('dataSource') : null;
    return saved === 'upstox' ? 'upstox' : 'bhavcopy';
  });
  const updateDataSource = useCallback((src: 'bhavcopy' | 'upstox') => {
    setDataSource(src);
    if (typeof window !== 'undefined') window.localStorage.setItem('dataSource', src);
  }, []);
  const pollRef = useRef<number | null>(null);

  const fetchDataStatus = useCallback(async () => {
    try {
      const status = await getDataStatus();
      setDataStatus(status);
    } catch (e) {
      console.error('Failed to fetch data status:', e);
    }
  }, []);

  const startBacktest = useCallback(async () => {
    setIsRunning(true);
    setError(null);
    setProgress(0);
    setResult(null);

    try {
      const { task_id } = await runBacktest({ strategy, config });

      // Poll for results
      const poll = async () => {
        try {
          const status = await pollBacktestStatus(task_id);
          setProgress(status.progress);

          if (status.status === 'completed' && status.result) {
            setResult(status.result as BacktestResult);
            setIsRunning(false);
            return;
          }
          if (status.status === 'failed') {
            setError(status.error || 'Backtest failed');
            setIsRunning(false);
            return;
          }
          // Continue polling
          pollRef.current = window.setTimeout(poll, POLL_INTERVAL);
        } catch (e) {
          setError(e instanceof Error ? e.message : 'Polling failed');
          setIsRunning(false);
        }
      };
      poll();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start backtest');
      setIsRunning(false);
    }
  }, [strategy, config]);

  const syncRange = useCallback(async (underlying: string, startDate: string, endDate: string): Promise<void> => {
    setIsSyncing(true);
    setSyncingUnderlying(underlying);
    setSyncProgress(0);

    return new Promise((resolve, reject) => {
      const finish = (err?: unknown) => {
        setIsSyncing(false);
        setSyncingUnderlying(null);
        fetchDataStatus();
        if (err) reject(err);
        else resolve();
      };

      syncData(underlying, startDate, endDate).then(({ task_id }) => {
        const poll = async () => {
          try {
            const status = await pollSyncStatus(task_id);
            setSyncProgress(status.progress);
            if (status.status === 'completed') return finish();
            if (status.status === 'failed') {
              setError(status.error || `Sync failed for ${underlying}`);
              return finish(new Error(status.error || 'sync failed'));
            }
            pollRef.current = window.setTimeout(poll, POLL_INTERVAL);
          } catch (e) {
            setError(e instanceof Error ? e.message : 'Sync polling failed');
            finish(e);
          }
        };
        poll();
      }).catch((e) => {
        setError(e instanceof Error ? e.message : `Failed to start sync for ${underlying}`);
        finish(e);
      });
    });
  }, [fetchDataStatus]);

  // Backwards-compatible entry used by the old Sync/Update buttons
  const startSync = useCallback((underlying: string, startDate: string, endDate: string) => {
    return syncRange(underlying, startDate, endDate).catch(() => {});
  }, [syncRange]);

  const startBhavcopyBackfill = useCallback(async (
    underlying: string, startDate: string, endDate: string,
  ) => {
    setIsSyncing(true);
    setSyncingUnderlying(underlying);
    setSyncProgress(0);
    try {
      const { task_id } = await backfillBhavcopy(underlying, startDate, endDate);
      await new Promise<void>((resolve) => {
        const poll = async () => {
          try {
            const status = await pollSyncStatus(task_id);
            setSyncProgress(status.progress);
            if (status.status === 'completed' || status.status === 'failed') {
              if (status.status === 'failed') {
                setError(status.error || 'Bhavcopy backfill failed');
              }
              setIsSyncing(false);
              setSyncingUnderlying(null);
              await fetchDataStatus();
              resolve();
              return;
            }
            pollRef.current = window.setTimeout(poll, POLL_INTERVAL);
          } catch (e) {
            setError(e instanceof Error ? e.message : 'Bhavcopy polling failed');
            setIsSyncing(false);
            setSyncingUnderlying(null);
            resolve();
          }
        };
        poll();
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start bhavcopy backfill');
      setIsSyncing(false);
      setSyncingUnderlying(null);
    }
  }, [fetchDataStatus]);

  const catchUpUnderlying = useCallback(async (underlying: string) => {
    const status = await getDataStatus();
    setDataStatus(status);
    const entry = (status as unknown as Record<string, { last_date?: string | null } | undefined>)[underlying];
    const today = new Date().toISOString().split('T')[0];
    let start: string;
    if (entry?.last_date) {
      const next = new Date(entry.last_date);
      next.setDate(next.getDate() + 1);
      start = next.toISOString().split('T')[0];
    } else {
      const d = new Date();
      d.setDate(d.getDate() - 30);
      start = d.toISOString().split('T')[0];
    }
    if (start > today) return; // already up to date
    if (dataSource === 'bhavcopy') {
      await startBhavcopyBackfill(underlying, start, today);
    } else {
      await syncRange(underlying, start, today);
    }
  }, [syncRange, startBhavcopyBackfill, dataSource]);

  const catchUpAll = useCallback(async () => {
    for (const u of ['NIFTY', 'BANKNIFTY', 'SENSEX']) {
      try {
        await catchUpUnderlying(u);
      } catch {
        // continue to next underlying even if one fails; error is already surfaced
      }
    }
  }, [catchUpUnderlying]);

  const saveBacktest = useCallback(async () => {
    if (result?.backtest_id) {
      return result.backtest_id;
    }
    return null;
  }, [result]);

  return {
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
    dataSource,
    setDataSource: updateDataSource,
    startBacktest,
    startSync,
    startBhavcopyBackfill,
    catchUpUnderlying,
    catchUpAll,
    fetchDataStatus,
    saveBacktest,
  };
}
