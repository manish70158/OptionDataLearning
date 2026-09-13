"""CLI entry point for the option backtester."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog='option_backtester',
        description='Backtest option strategies based on FII/PRO view combinations',
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # backtest subcommand
    bt_parser = subparsers.add_parser('backtest', help='Run backtest on historical data')
    bt_parser.add_argument(
        '--csv', default='vix_fii_t1_intraday_daily_results.csv',
        help='Path to the CSV data file (default: vix_fii_t1_intraday_daily_results.csv)',
    )
    bt_parser.add_argument(
        '--output', default='backtest_results.csv',
        help='Path for output results CSV (default: backtest_results.csv)',
    )
    bt_parser.add_argument(
        '--stop-loss', choices=['on', 'off'], default='on',
        help='Enable/disable stop loss (default: on). Uses per-strategy SL thresholds from config.',
    )
    bt_parser.add_argument(
        '--rr-ratio', type=float, default=None,
        help='Risk:Reward ratio for take profit. E.g., 1.0 means TP = SL (1:1). Default: no TP.',
    )
    bt_parser.add_argument(
        '--move-exit', type=float, default=None,
        help='Exit when NIFTY moves this %% from open. E.g., 0.5 = exit at 0.5%% move. Default: off.',
    )

    # report subcommand
    rpt_parser = subparsers.add_parser('report', help='Generate profitability report')
    rpt_parser.add_argument(
        '--output-format', choices=['md', 'html', 'csv'], default='md',
        help='Report output format (default: md)',
    )
    rpt_parser.add_argument(
        '--output-dir', default='.',
        help='Directory for report output (default: current directory)',
    )
    rpt_parser.add_argument(
        '--backtest-results', default='backtest_results.csv',
        help='Path to backtest results CSV (default: backtest_results.csv)',
    )

    # recommend subcommand
    rec_parser = subparsers.add_parser('recommend', help='Get daily strategy recommendation')
    rec_parser.add_argument('--fii-view', required=True, help='Current FII view')
    rec_parser.add_argument('--pro-view', required=True, help='Current PRO view')
    rec_parser.add_argument('--vix', required=True, type=float, help='Current VIX level')
    rec_parser.add_argument('--nifty-spot', type=float, help='Current NIFTY spot price')
    rec_parser.add_argument(
        '--backtest-results', default='backtest_results.csv',
        help='Path to backtest results CSV (default: backtest_results.csv)',
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == 'backtest':
        from option_backtester.backtester import load_data, run_backtest, compute_days_to_expiry
        from option_backtester.strategies import get_all_strategies
        from option_backtester import config

        print(f'Loading data from {args.csv}...')
        df = load_data(args.csv)
        print(f'Loaded {len(df)} trading days')

        df = compute_days_to_expiry(df)
        strategies = get_all_strategies()
        sl_pct = config.STOP_LOSS_PCT if args.stop_loss == 'on' else None
        rr_ratio = args.rr_ratio
        move_exit = args.move_exit
        sl_status = 'ON (%-based)' if sl_pct else 'OFF'
        tp_status = f'ON (1:{rr_ratio})' if rr_ratio else 'OFF'
        move_status = f'ON ({move_exit}% NIFTY move)' if move_exit else 'OFF'
        print(f'Running backtest with {len(strategies)} strategies...')
        print(f'  SL: {sl_status} | TP: {tp_status} | Move exit: {move_status}')
        if sl_pct:
            for name, pct in sl_pct.items():
                tp_info = f', TP at {pct * rr_ratio}%' if rr_ratio else ''
                print(f'  {name}: SL at {pct}%{tp_info}')
        results = run_backtest(df, strategies, config, stop_loss_pct=sl_pct,
                               rr_ratio=rr_ratio, move_exit_pct=move_exit)
        results.to_csv(args.output, index=False)
        sl_count = int(results['sl_hit'].sum()) if 'sl_hit' in results.columns else 0
        tp_count = int(results['tp_hit'].sum()) if 'tp_hit' in results.columns else 0
        move_count = int(results['move_exit'].sum()) if 'move_exit' in results.columns else 0
        close_count = len(results) - sl_count - tp_count - move_count
        total = len(results)
        print(f'Backtest complete. Results saved to {args.output}')
        print(f'Total result rows: {total}')
        print(f'Exit breakdown:')
        if move_exit:
            print(f'  Move exit: {move_count} ({move_count/total*100:.1f}%)')
        if rr_ratio:
            print(f'  TP hit:    {tp_count} ({tp_count/total*100:.1f}%)')
        print(f'  SL hit:    {sl_count} ({sl_count/total*100:.1f}%)')
        print(f'  Close:     {close_count} ({close_count/total*100:.1f}%)')

    elif args.command == 'report':
        import pandas as pd
        from option_backtester.report import generate_full_report

        print(f'Loading backtest results from {args.backtest_results}...')
        results_df = pd.read_csv(args.backtest_results)
        print(f'Generating {args.output_format} report...')
        generate_full_report(results_df, args.output_format, args.output_dir)
        print('Report generation complete.')

    elif args.command == 'recommend':
        import pandas as pd
        from option_backtester.recommender import get_recommendation, format_recommendation

        results_df = pd.read_csv(args.backtest_results)
        rec = get_recommendation(args.fii_view, args.pro_view, args.vix, results_df)
        output = format_recommendation(rec, nifty_spot=args.nifty_spot)
        print(output)
