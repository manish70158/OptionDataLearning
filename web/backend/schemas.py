"""Pydantic models for request/response validation."""
from datetime import date, time
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


class Position(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OptionType(str, Enum):
    CE = "CE"
    PE = "PE"


class Underlying(str, Enum):
    NIFTY = "NIFTY"
    BANKNIFTY = "BANKNIFTY"
    SENSEX = "SENSEX"


class ExpiryType(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class SLTPMode(str, Enum):
    PERCENTAGE = "percentage"
    POINTS = "points"


class SLScope(str, Enum):
    COMBINED = "combined"
    PER_LEG = "per_leg"


# --- Request models ---

class StrategyLeg(BaseModel):
    position: Position
    option_type: OptionType
    strike_offset: int = Field(description="Points relative to ATM")
    lots: int = Field(ge=1, le=50, default=1)


class StrategyDefinition(BaseModel):
    underlying: Underlying = Underlying.NIFTY
    expiry_type: ExpiryType = ExpiryType.WEEKLY
    legs: list[StrategyLeg] = Field(min_length=1, max_length=8)


class BacktestConfig(BaseModel):
    start_date: date
    end_date: date
    entry_time: time = Field(default=time(9, 20))
    exit_time: time = Field(default=time(15, 15))
    stop_loss_enabled: bool = True
    stop_loss_mode: SLTPMode = SLTPMode.PERCENTAGE
    stop_loss_value: float = Field(default=50.0, ge=0)
    sl_scope: SLScope = Field(
        default=SLScope.PER_LEG,
        description="'combined' = SL on net strategy P&L; 'per_leg' = each leg has its own SL.",
    )
    target_profit_enabled: bool = False
    target_profit_mode: SLTPMode = SLTPMode.PERCENTAGE
    target_profit_value: float = Field(default=50.0, ge=0)
    trailing_sl_enabled: bool = False
    trailing_sl_value: float = Field(default=20.0, ge=0)
    vix_min: Optional[float] = None
    vix_max: Optional[float] = None
    weekdays: list[int] = Field(
        default=[0, 1, 2, 3, 4],
        description="0=Mon, 1=Tue, ..., 4=Fri",
    )

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        diff = (self.end_date - self.start_date).days
        if diff > 730:
            raise ValueError("Maximum backtest period is 2 years (730 days)")
        return self

    @model_validator(mode="after")
    def validate_times(self):
        if self.entry_time >= self.exit_time:
            raise ValueError("exit_time must be after entry_time")
        return self


class BacktestRequest(BaseModel):
    strategy: StrategyDefinition
    config: BacktestConfig


class SyncRequest(BaseModel):
    underlying: Underlying
    start_date: date
    end_date: date


# --- Response models ---

class BacktestSummary(BaseModel):
    total_pnl: float
    total_pnl_inr: float = 0.0
    num_trades: int
    win_rate: float
    max_drawdown: float
    max_drawdown_pct: float
    sharpe_ratio: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    max_consecutive_wins: int
    max_consecutive_losses: int


class LegDetail(BaseModel):
    strike: float
    option_type: str
    position: str
    lots: int
    entry_premium: float
    exit_premium: float
    source: str = "estimated"


class TradeRecord(BaseModel):
    date: str
    day_of_week: str
    entry_time: str
    exit_time: str
    entry_premium: float
    exit_premium: float
    pnl_points: float
    pnl_inr: float = 0.0
    exit_reason: str
    cumulative_pnl: float
    vix: Optional[float] = None
    pricing_source: str = "estimated"
    dte: int = 0
    expiry_date: str = ""
    legs: Optional[list[LegDetail]] = None  # Individual leg details


class EquityCurvePoint(BaseModel):
    date: str
    cumulative_pnl: float


class DrawdownPoint(BaseModel):
    date: str
    drawdown_pct: float


class BacktestResult(BaseModel):
    summary: BacktestSummary
    trades: list[TradeRecord]
    equity_curve: list[EquityCurvePoint]
    drawdown: list[DrawdownPoint]
    monthly_pnl: dict[str, float]


class TaskStatus(BaseModel):
    task_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: int = 0  # 0-100
    result: Optional[Any] = None
    error: Optional[str] = None


class DataStatus(BaseModel):
    NIFTY: dict
    BANKNIFTY: dict
    SENSEX: Optional[dict] = None
    cache_size_mb: float


class UnderlyingInfo(BaseModel):
    name: str
    lot_size: int
    strike_interval: int
    trading_symbol: str
