export type Position = 'buy' | 'sell';
export type OptionType = 'CE' | 'PE';
export type Underlying = 'NIFTY' | 'BANKNIFTY' | 'SENSEX';
export type ExpiryType = 'weekly' | 'monthly';
export type SLTPMode = 'percentage' | 'points';
export type SLScope = 'combined' | 'per_leg';

export interface StrategyLeg {
  position: Position;
  option_type: OptionType;
  strike_offset: number;
  lots: number;
}

export interface StrategyDefinition {
  underlying: Underlying;
  expiry_type: ExpiryType;
  legs: StrategyLeg[];
}

export interface BacktestConfig {
  start_date: string;
  end_date: string;
  entry_time: string;
  exit_time: string;
  stop_loss_enabled: boolean;
  stop_loss_mode: SLTPMode;
  stop_loss_value: number;
  sl_scope?: SLScope;
  target_profit_enabled: boolean;
  target_profit_mode: SLTPMode;
  target_profit_value: number;
  trailing_sl_enabled: boolean;
  trailing_sl_value: number;
  vix_min: number | null;
  vix_max: number | null;
  weekdays: number[];
}

export interface BacktestSummary {
  total_pnl: number;
  total_pnl_inr: number;
  num_trades: number;
  win_rate: number;
  max_drawdown: number;
  max_drawdown_pct: number;
  sharpe_ratio: number;
  avg_win: number;
  avg_loss: number;
  profit_factor: number;
  max_consecutive_wins: number;
  max_consecutive_losses: number;
}

export interface LegDetail {
  strike: number;
  option_type: string;
  position: string;
  lots: number;
  entry_premium: number;
  exit_premium: number;
  source: string;
}

export interface TradeRecord {
  date: string;
  day_of_week: string;
  entry_time: string;
  exit_time: string;
  entry_premium: number;
  exit_premium: number;
  pnl_points: number;
  pnl_inr: number;
  exit_reason: string;
  cumulative_pnl: number;
  vix: number | null;
  pricing_source: string;
  dte?: number;
  expiry_date?: string;
  legs?: LegDetail[];
}

export interface EquityCurvePoint {
  date: string;
  cumulative_pnl: number;
}

export interface DrawdownPoint {
  date: string;
  drawdown_pct: number;
}

export interface BacktestResult {
  summary: BacktestSummary;
  trades: TradeRecord[];
  equity_curve: EquityCurvePoint[];
  drawdown: DrawdownPoint[];
  monthly_pnl: Record<string, number>;
  backtest_id?: string;
}

export interface TaskStatus {
  task_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  result: BacktestResult | null;
  error: string | null;
}

export interface UnderlyingInfo {
  name: string;
  lot_size: number;
  strike_interval: number;
  trading_symbol: string;
}

export interface UnderlyingDataStatus {
  first_date: string | null;
  last_date: string | null;
  trading_days_count: number;
  last_sync_timestamp: string | null;
}

export interface DataStatus {
  NIFTY: UnderlyingDataStatus;
  BANKNIFTY: UnderlyingDataStatus;
  SENSEX?: UnderlyingDataStatus;
  cache_size_mb: number;
}

export interface BacktestRequest {
  strategy: StrategyDefinition;
  config: BacktestConfig;
}
