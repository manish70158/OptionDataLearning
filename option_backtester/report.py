"""Report generation: Markdown, HTML, and CSV outputs."""
import os
import io
import base64
import pandas as pd
import numpy as np
from option_backtester.aggregator import (
    aggregate_results, aggregate_by_expiry, aggregate_by_vix_regime, flag_low_sample,
)
from option_backtester.config import FII_VIEWS, PRO_VIEWS


# --- Section generators ---

def generate_strategy_rankings(aggregated_df):
    """Generate ranked strategy tables per FII/PRO combination.

    Returns:
        dict mapping (fii_view, pro_view) -> DataFrame of strategies sorted by total_pnl desc
    """
    rankings = {}
    for (fii, pro), group in aggregated_df.groupby(['fii_view', 'pro_view']):
        ranked = group.sort_values('total_pnl', ascending=False).copy()
        ranked = ranked[['strategy_name', 'total_pnl', 'avg_daily_pnl', 'win_rate',
                         'max_single_day_loss', 'max_consecutive_drawdown',
                         'sharpe_ratio', 'day_count']].reset_index(drop=True)
        rankings[(fii, pro)] = ranked
    return rankings


def generate_summary_matrix(aggregated_df):
    """Generate 7×7 best-strategy summary matrix.

    Returns:
        DataFrame with FII views as index, PRO views as columns.
        Each cell: "Strategy (P&L: X, WR: Y%)" or "N/A"
    """
    # Find best strategy per FII/PRO combination
    best = aggregated_df.loc[
        aggregated_df.groupby(['fii_view', 'pro_view'])['total_pnl'].idxmax()
    ].copy()

    matrix = pd.DataFrame(index=FII_VIEWS, columns=PRO_VIEWS, dtype=str)
    matrix[:] = 'N/A'

    for _, row in best.iterrows():
        fii = row['fii_view']
        pro = row['pro_view']
        if fii in FII_VIEWS and pro in PRO_VIEWS:
            name = row['strategy_name']
            pnl = row['total_pnl']
            wr = row['win_rate']
            days = row['day_count']
            marker = '*' if days < 5 else ''
            matrix.loc[fii, pro] = f'{name}{marker} ({pnl:.0f}pts, {wr:.0f}%WR, {days}d)'

    return matrix


def generate_expiry_comparison(expiry_aggregated_df):
    """Identify combinations where best strategy differs between expiry and non-expiry.

    Returns:
        DataFrame with divergent combinations (both segments ≥3 days)
    """
    divergences = []

    for segment_type in ['expiry', 'non_expiry']:
        seg = expiry_aggregated_df[expiry_aggregated_df['segment'] == segment_type]
        if seg.empty:
            continue

    # Get best strategy per segment per combo
    results = {}
    for segment_type in ['expiry', 'non_expiry']:
        seg = expiry_aggregated_df[expiry_aggregated_df['segment'] == segment_type]
        if seg.empty:
            continue
        for (fii, pro), group in seg.groupby(['fii_view', 'pro_view']):
            best_idx = group['total_pnl'].idxmax()
            best_row = group.loc[best_idx]
            results.setdefault((fii, pro), {})[segment_type] = {
                'strategy': best_row['strategy_name'],
                'total_pnl': best_row['total_pnl'],
                'win_rate': best_row['win_rate'],
                'day_count': best_row['day_count'],
            }

    for (fii, pro), segs in results.items():
        if 'expiry' not in segs or 'non_expiry' not in segs:
            continue
        if segs['expiry']['day_count'] < 3 or segs['non_expiry']['day_count'] < 3:
            continue
        if segs['expiry']['strategy'] != segs['non_expiry']['strategy']:
            divergences.append({
                'fii_view': fii,
                'pro_view': pro,
                'expiry_strategy': segs['expiry']['strategy'],
                'expiry_pnl': segs['expiry']['total_pnl'],
                'expiry_win_rate': segs['expiry']['win_rate'],
                'expiry_days': segs['expiry']['day_count'],
                'non_expiry_strategy': segs['non_expiry']['strategy'],
                'non_expiry_pnl': segs['non_expiry']['total_pnl'],
                'non_expiry_win_rate': segs['non_expiry']['win_rate'],
                'non_expiry_days': segs['non_expiry']['day_count'],
            })

    return pd.DataFrame(divergences) if divergences else pd.DataFrame()


def generate_vix_regime_section(vix_aggregated_df, min_total_days=30):
    """Show optimal strategy per VIX regime for high-frequency combinations.

    Returns:
        dict mapping (fii_view, pro_view) -> DataFrame of VIX regimes with best strategy
    """
    # First find combos with enough total days
    total_days = vix_aggregated_df.groupby(
        ['fii_view', 'pro_view', 'strategy_name']
    )['day_count'].sum().reset_index()
    combo_days = total_days.groupby(['fii_view', 'pro_view'])['day_count'].first().reset_index()

    # Actually, we need total days per combo across all strategies (which is same per strategy)
    # Simpler: sum days per combo per regime
    combo_total = vix_aggregated_df.groupby(
        ['fii_view', 'pro_view']
    )['day_count'].sum().reset_index()
    # Each day appears 6 times (once per strategy), so divide by number of unique strategies
    n_strategies = vix_aggregated_df['strategy_name'].nunique()
    combo_total['actual_days'] = combo_total['day_count'] // max(n_strategies, 1)

    valid_combos = combo_total[combo_total['actual_days'] >= min_total_days]

    results = {}
    for _, combo_row in valid_combos.iterrows():
        fii = combo_row['fii_view']
        pro = combo_row['pro_view']
        combo_data = vix_aggregated_df[
            (vix_aggregated_df['fii_view'] == fii) &
            (vix_aggregated_df['pro_view'] == pro)
        ]

        regime_best = []
        for regime, regime_group in combo_data.groupby('vix_regime'):
            if regime_group.empty:
                continue
            best_idx = regime_group['total_pnl'].idxmax()
            best = regime_group.loc[best_idx]
            regime_best.append({
                'vix_regime': regime,
                'best_strategy': best['strategy_name'],
                'total_pnl': best['total_pnl'],
                'win_rate': best['win_rate'],
                'day_count': best['day_count'],
            })

        if regime_best:
            results[(fii, pro)] = pd.DataFrame(regime_best)

    return results


# --- Output writers ---

def _df_to_markdown(df, title=None):
    """Convert a DataFrame to GitHub-flavored Markdown table."""
    lines = []
    if title:
        lines.append(f'\n### {title}\n')

    # Header
    headers = '| ' + ' | '.join(str(c) for c in df.columns) + ' |'
    separator = '|' + '|'.join('---' for _ in df.columns) + '|'
    lines.append(headers)
    lines.append(separator)

    # Rows
    for _, row in df.iterrows():
        cells = []
        for val in row:
            if isinstance(val, float):
                cells.append(f'{val:.2f}')
            else:
                cells.append(str(val))
        lines.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join(lines)


def write_markdown_report(sections, output_path):
    """Compose all sections into a single GFM markdown report.

    Args:
        sections: dict with keys 'rankings', 'matrix', 'expiry_comparison',
                  'vix_regime', 'aggregated'
        output_path: Path to write the .md file
    """
    lines = ['# FII/PRO Option Strategy Profitability Report\n']
    lines.append('*Generated by option_backtester — Black-Scholes estimated premiums from VIX*\n')

    # Summary Matrix
    lines.append('## Summary Matrix — Best Strategy per FII/PRO Combination\n')
    matrix = sections['matrix']
    lines.append(_df_to_markdown(matrix.reset_index().rename(columns={'index': 'FII \\ PRO'})))
    lines.append('')

    # Strategy Rankings per combination
    lines.append('\n## Strategy Rankings by FII/PRO Combination\n')
    rankings = sections['rankings']
    for (fii, pro), df in sorted(rankings.items()):
        day_count = df['day_count'].iloc[0] if len(df) > 0 else 0
        lines.append(f'\n### {fii} × {pro} ({day_count} days)\n')
        lines.append(_df_to_markdown(df))
        lines.append('')

    # Expiry Comparison
    lines.append('\n## Expiry vs Non-Expiry Strategy Divergence\n')
    expiry_comp = sections.get('expiry_comparison')
    if expiry_comp is not None and len(expiry_comp) > 0:
        lines.append(_df_to_markdown(expiry_comp))
    else:
        lines.append('No divergent combinations found (or insufficient data).\n')

    # VIX Regime
    lines.append('\n## VIX Regime Analysis (Combinations with ≥30 days)\n')
    vix_data = sections.get('vix_regime', {})
    if vix_data:
        for (fii, pro), df in sorted(vix_data.items()):
            lines.append(f'\n### {fii} × {pro}\n')
            lines.append(_df_to_markdown(df))
            lines.append('')
    else:
        lines.append('No combinations with sufficient data for VIX regime analysis.\n')

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


def write_html_report(sections, charts, output_path):
    """Generate an HTML report with styled tables and embedded charts.

    Args:
        sections: dict with report sections
        charts: dict with chart names -> base64 PNG strings
        output_path: Path to write the .html file
    """
    html_parts = ['''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>FII/PRO Option Strategy Report</title>
<style>
body { font-family: -apple-system, Arial, sans-serif; margin: 40px; background: #f5f5f5; }
h1 { color: #1a1a2e; }
h2 { color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 8px; }
h3 { color: #533483; }
table { border-collapse: collapse; margin: 16px 0; width: 100%; background: white; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: right; }
th { background: #0f3460; color: white; }
tr:nth-child(even) { background: #f2f2f2; }
tr:hover { background: #e0e0e0; }
td:first-child, th:first-child { text-align: left; }
.chart { margin: 20px 0; text-align: center; }
.chart img { max-width: 100%; border: 1px solid #ddd; }
.note { color: #666; font-style: italic; }
</style></head><body>
<h1>FII/PRO Option Strategy Profitability Report</h1>
<p class="note">Generated by option_backtester — Black-Scholes estimated premiums from VIX</p>
''']

    # Summary Matrix
    html_parts.append('<h2>Summary Matrix — Best Strategy per FII/PRO Combination</h2>')
    matrix = sections['matrix']
    html_parts.append(matrix.reset_index().rename(columns={'index': 'FII \\ PRO'}).to_html(
        index=False, classes='matrix', escape=False,
    ))

    # Charts
    for name, b64 in charts.items():
        html_parts.append(f'<div class="chart"><h3>{name}</h3>')
        html_parts.append(f'<img src="data:image/png;base64,{b64}" alt="{name}"/></div>')

    # Rankings
    html_parts.append('<h2>Strategy Rankings by FII/PRO Combination</h2>')
    rankings = sections['rankings']
    for (fii, pro), df in sorted(rankings.items()):
        day_count = df['day_count'].iloc[0] if len(df) > 0 else 0
        html_parts.append(f'<h3>{fii} × {pro} ({day_count} days)</h3>')
        html_parts.append(df.to_html(index=False, float_format='%.2f'))

    # Expiry Comparison
    html_parts.append('<h2>Expiry vs Non-Expiry Strategy Divergence</h2>')
    expiry_comp = sections.get('expiry_comparison')
    if expiry_comp is not None and len(expiry_comp) > 0:
        html_parts.append(expiry_comp.to_html(index=False, float_format='%.2f'))
    else:
        html_parts.append('<p class="note">No divergent combinations found.</p>')

    # VIX Regime
    html_parts.append('<h2>VIX Regime Analysis</h2>')
    vix_data = sections.get('vix_regime', {})
    if vix_data:
        for (fii, pro), df in sorted(vix_data.items()):
            html_parts.append(f'<h3>{fii} × {pro}</h3>')
            html_parts.append(df.to_html(index=False, float_format='%.2f'))
    else:
        html_parts.append('<p class="note">No combinations with sufficient data.</p>')

    html_parts.append('</body></html>')

    with open(output_path, 'w') as f:
        f.write('\n'.join(html_parts))


def write_csv_export(sections, output_dir):
    """Write separate CSV files for each major table.

    Args:
        sections: dict with report sections
        output_dir: Directory to write CSV files
    """
    os.makedirs(output_dir, exist_ok=True)

    # Strategy rankings (all combos in one file)
    all_rankings = []
    for (fii, pro), df in sections['rankings'].items():
        ranked = df.copy()
        ranked.insert(0, 'fii_view', fii)
        ranked.insert(1, 'pro_view', pro)
        all_rankings.append(ranked)
    if all_rankings:
        pd.concat(all_rankings, ignore_index=True).to_csv(
            os.path.join(output_dir, 'strategy_rankings.csv'), index=False,
        )

    # Summary matrix
    matrix = sections['matrix']
    matrix.reset_index().rename(columns={'index': 'fii_view'}).to_csv(
        os.path.join(output_dir, 'summary_matrix.csv'), index=False,
    )

    # Expiry comparison
    expiry_comp = sections.get('expiry_comparison')
    if expiry_comp is not None and len(expiry_comp) > 0:
        expiry_comp.to_csv(
            os.path.join(output_dir, 'expiry_comparison.csv'), index=False,
        )
    else:
        pd.DataFrame(columns=['fii_view', 'pro_view', 'expiry_strategy',
                               'non_expiry_strategy']).to_csv(
            os.path.join(output_dir, 'expiry_comparison.csv'), index=False,
        )


def _generate_charts(sections):
    """Generate matplotlib charts as base64-encoded PNGs."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    charts = {}

    # Heatmap: best strategy P&L by FII/PRO combination
    try:
        aggregated = sections.get('aggregated')
        if aggregated is not None:
            best = aggregated.loc[
                aggregated.groupby(['fii_view', 'pro_view'])['total_pnl'].idxmax()
            ]
            pivot = best.pivot_table(
                index='fii_view', columns='pro_view', values='total_pnl',
                aggfunc='first',
            )
            # Reindex to standard order
            pivot = pivot.reindex(index=FII_VIEWS, columns=PRO_VIEWS)

            fig, ax = plt.subplots(figsize=(12, 8))
            im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto')
            ax.set_xticks(range(len(PRO_VIEWS)))
            ax.set_xticklabels(PRO_VIEWS, rotation=45, ha='right', fontsize=8)
            ax.set_yticks(range(len(FII_VIEWS)))
            ax.set_yticklabels(FII_VIEWS, fontsize=8)
            ax.set_title('Best Strategy Total P&L by FII/PRO Combination')
            plt.colorbar(im, label='Total P&L (points)')

            # Add text annotations
            for i in range(len(FII_VIEWS)):
                for j in range(len(PRO_VIEWS)):
                    val = pivot.values[i, j]
                    if not np.isnan(val):
                        ax.text(j, i, f'{val:.0f}', ha='center', va='center', fontsize=7)

            plt.tight_layout()
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            charts['P&L Heatmap'] = base64.b64encode(buf.read()).decode()
            plt.close(fig)
    except Exception:
        pass  # Charts are optional; don't fail the report

    return charts


def generate_full_report(results_df, output_format='md', output_dir='.'):
    """Generate the complete profitability report.

    Args:
        results_df: Raw backtest results DataFrame
        output_format: 'md', 'html', or 'csv'
        output_dir: Directory for output files
    """
    os.makedirs(output_dir, exist_ok=True)

    # Run all aggregations
    aggregated = flag_low_sample(aggregate_results(results_df))
    expiry_agg = aggregate_by_expiry(results_df)
    vix_agg = aggregate_by_vix_regime(results_df)

    # Generate sections
    sections = {
        'rankings': generate_strategy_rankings(aggregated),
        'matrix': generate_summary_matrix(aggregated),
        'expiry_comparison': generate_expiry_comparison(expiry_agg),
        'vix_regime': generate_vix_regime_section(vix_agg),
        'aggregated': aggregated,
    }

    if output_format == 'md':
        write_markdown_report(sections, os.path.join(output_dir, 'strategy_report.md'))
    elif output_format == 'html':
        charts = _generate_charts(sections)
        write_html_report(sections, charts, os.path.join(output_dir, 'strategy_report.html'))
    elif output_format == 'csv':
        write_csv_export(sections, output_dir)
