"""Aggregation of backtest results by FII/PRO view combinations."""
import pandas as pd
import numpy as np
from option_backtester.config import VIX_REGIME_THRESHOLDS, LOW_SAMPLE_THRESHOLD


def _compute_max_consecutive_drawdown(pnl_series):
    """Compute maximum drawdown over consecutive losing days."""
    max_dd = 0.0
    current_dd = 0.0
    for pnl in pnl_series:
        if pnl < 0:
            current_dd += pnl
            max_dd = min(max_dd, current_dd)
        else:
            current_dd = 0.0
    return max_dd


def _compute_group_metrics(group):
    """Compute all metrics for a group of daily P&L values."""
    pnl_values = group['daily_pnl']
    day_count = len(pnl_values)
    total_pnl = pnl_values.sum()
    avg_daily_pnl = pnl_values.mean()
    win_rate = (pnl_values > 0).mean() * 100 if day_count > 0 else 0.0
    max_single_day_loss = pnl_values.min() if day_count > 0 else 0.0
    max_consecutive_drawdown = _compute_max_consecutive_drawdown(pnl_values.values)
    std = pnl_values.std()
    sharpe_ratio = avg_daily_pnl / std if std > 0 else 0.0

    return pd.Series({
        'total_pnl': total_pnl,
        'avg_daily_pnl': avg_daily_pnl,
        'win_rate': win_rate,
        'max_single_day_loss': max_single_day_loss,
        'max_consecutive_drawdown': max_consecutive_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'day_count': day_count,
    })


def aggregate_results(results_df):
    """Aggregate backtest results by FII View × PRO View × Strategy.

    Args:
        results_df: DataFrame from run_backtest with daily_pnl column

    Returns:
        DataFrame with aggregated metrics per group
    """
    grouped = results_df.groupby(['fii_view', 'pro_view', 'strategy_name'])
    aggregated = grouped.apply(_compute_group_metrics, include_groups=False).reset_index()
    aggregated['day_count'] = aggregated['day_count'].astype(int)
    return aggregated


def aggregate_by_expiry(results_df):
    """Aggregate results with expiry vs non-expiry segmentation.

    Produces three sets per group: combined, expiry-only, non-expiry-only.

    Returns:
        DataFrame with an additional 'segment' column ('combined', 'expiry', 'non_expiry')
    """
    segments = []

    # Combined
    combined = aggregate_results(results_df)
    combined['segment'] = 'combined'
    segments.append(combined)

    # Expiry only
    expiry_df = results_df[results_df['is_expiry'] == 1]
    if len(expiry_df) > 0:
        expiry_agg = aggregate_results(expiry_df)
        expiry_agg['segment'] = 'expiry'
        segments.append(expiry_agg)

    # Non-expiry only
    non_expiry_df = results_df[results_df['is_expiry'] == 0]
    if len(non_expiry_df) > 0:
        non_expiry_agg = aggregate_results(non_expiry_df)
        non_expiry_agg['segment'] = 'non_expiry'
        segments.append(non_expiry_agg)

    return pd.concat(segments, ignore_index=True)


def _classify_vix_regime(vix_value):
    """Classify a VIX value into a regime."""
    for regime, (low, high) in VIX_REGIME_THRESHOLDS.items():
        if low <= vix_value < high:
            return regime
    return 'High'  # Fallback


def aggregate_by_vix_regime(results_df, thresholds=None):
    """Aggregate results by VIX regime in addition to FII/PRO.

    Args:
        results_df: DataFrame from run_backtest
        thresholds: Optional custom thresholds dict (default: from config)

    Returns:
        DataFrame grouped by (fii_view, pro_view, strategy_name, vix_regime)
    """
    df = results_df.copy()
    df['vix_regime'] = df['vix_open'].apply(_classify_vix_regime)

    grouped = df.groupby(['fii_view', 'pro_view', 'strategy_name', 'vix_regime'])
    aggregated = grouped.apply(_compute_group_metrics, include_groups=False).reset_index()
    aggregated['day_count'] = aggregated['day_count'].astype(int)
    return aggregated


def flag_low_sample(aggregated_df, min_days=LOW_SAMPLE_THRESHOLD):
    """Add low_sample boolean flag to aggregated results.

    Args:
        aggregated_df: DataFrame with day_count column
        min_days: Minimum days threshold (default: from config)

    Returns:
        DataFrame with added 'low_sample' column
    """
    df = aggregated_df.copy()
    df['low_sample'] = df['day_count'] < min_days
    return df
