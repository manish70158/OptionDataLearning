import type {
  BacktestRequest,
  BacktestResult,
  TaskStatus,
  DataStatus,
  UnderlyingInfo,
} from '../types/backtest';

const BASE_URL = '/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    const body = await response.text();
    let detail = `HTTP ${response.status}`;
    try {
      const json = JSON.parse(body);
      detail = json.detail || detail;
    } catch { /* ignore */ }
    throw new Error(detail);
  }
  return response.json();
}

export async function runBacktest(request: BacktestRequest): Promise<{ task_id: string }> {
  return fetchJSON(`${BASE_URL}/backtest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
}

export async function pollBacktestStatus(taskId: string): Promise<TaskStatus> {
  return fetchJSON(`${BASE_URL}/backtest/${taskId}/status`);
}

export async function getSavedBacktest(id: string): Promise<BacktestResult> {
  return fetchJSON(`${BASE_URL}/backtest/saved/${id}`);
}

export async function backfillBhavcopy(
  underlying: string,
  startDate: string,
  endDate: string,
): Promise<{ task_id: string }> {
  return fetchJSON(`${BASE_URL}/data/backfill-bhavcopy`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ underlying, start_date: startDate, end_date: endDate }),
  });
}

export async function syncData(
  underlying: string,
  startDate: string,
  endDate: string,
): Promise<{ task_id: string }> {
  return fetchJSON(`${BASE_URL}/data/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      underlying,
      start_date: startDate,
      end_date: endDate,
    }),
  });
}

export async function pollSyncStatus(taskId: string): Promise<TaskStatus> {
  return fetchJSON(`${BASE_URL}/data/sync/${taskId}/status`);
}

export async function getDataStatus(): Promise<DataStatus> {
  return fetchJSON(`${BASE_URL}/data/status`);
}

export async function getUnderlyings(): Promise<UnderlyingInfo[]> {
  return fetchJSON(`${BASE_URL}/instruments/underlyings`);
}

export async function getExpiries(underlying: string): Promise<{
  weekly: string[];
  monthly: string[];
  data_available: boolean;
}> {
  return fetchJSON(`${BASE_URL}/instruments/${underlying}/expiries`);
}

export async function getStrikes(
  underlying: string,
  date: string,
  expiryDate: string,
): Promise<{ strikes: number[]; atm_strike: number }> {
  return fetchJSON(
    `${BASE_URL}/instruments/${underlying}/strikes?date=${date}&expiry_date=${expiryDate}`,
  );
}
