"""SQLite table definitions for historical data cache."""

TABLES = {
    "ohlcv_candles": """
        CREATE TABLE IF NOT EXISTS ohlcv_candles (
            instrument TEXT NOT NULL,
            date TEXT NOT NULL,
            interval TEXT NOT NULL DEFAULT 'day',
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER DEFAULT 0,
            PRIMARY KEY (instrument, date, interval)
        )
    """,
    "option_premiums": """
        CREATE TABLE IF NOT EXISTS option_premiums (
            instrument TEXT NOT NULL,
            date TEXT NOT NULL,
            expiry TEXT NOT NULL,
            strike REAL NOT NULL,
            option_type TEXT NOT NULL,
            open_premium REAL,
            close_premium REAL,
            high_premium REAL,
            low_premium REAL,
            implied_vol REAL,
            underlying_close REAL,
            nse_token INTEGER,
            PRIMARY KEY (instrument, date, expiry, strike, option_type)
        )
    """,
    "intraday_candles": """
        CREATE TABLE IF NOT EXISTS intraday_candles (
            instrument TEXT NOT NULL,
            date TEXT NOT NULL,
            strike REAL NOT NULL,
            option_type TEXT NOT NULL,
            expiry TEXT NOT NULL,
            time TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            PRIMARY KEY (instrument, date, strike, option_type, expiry, time)
        )
    """,
    "index_intraday": """
        CREATE TABLE IF NOT EXISTS index_intraday (
            instrument TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            PRIMARY KEY (instrument, date, time)
        )
    """,
    "sync_log": """
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            synced_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'completed'
        )
    """,
    "saved_backtests": """
        CREATE TABLE IF NOT EXISTS saved_backtests (
            id TEXT PRIMARY KEY,
            strategy_config TEXT NOT NULL,
            backtest_config TEXT NOT NULL,
            results TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """,
    "upstox_credentials": """
        CREATE TABLE IF NOT EXISTS upstox_credentials (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            access_token TEXT NOT NULL,
            refresh_token TEXT,
            expires_at TEXT,
            updated_at TEXT NOT NULL
        )
    """,
}

INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_ohlcv_instrument_date ON ohlcv_candles(instrument, date)",
    "CREATE INDEX IF NOT EXISTS idx_option_premiums_lookup ON option_premiums(instrument, date, strike, option_type)",
    "CREATE INDEX IF NOT EXISTS idx_option_premiums_expiry ON option_premiums(instrument, date, expiry)",
    "CREATE INDEX IF NOT EXISTS idx_intraday_lookup ON intraday_candles(instrument, date, strike, option_type, expiry)",
    "CREATE INDEX IF NOT EXISTS idx_sync_log_instrument ON sync_log(instrument, start_date, end_date)",
    "CREATE INDEX IF NOT EXISTS idx_saved_backtests_created ON saved_backtests(created_at)",
]
