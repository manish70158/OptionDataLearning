"""Upstox API historical data fetcher.

Fetches historical OHLCV candles and option chain data from Upstox API v2,
stores them in the SQLite cache for backtest consumption.
"""
import asyncio
import gzip
import io
import csv
import json
import logging
import os
import time
from datetime import date, datetime, timedelta
from typing import Callable, Optional

import httpx

from web.backend.data import cache

logger = logging.getLogger(__name__)

UPSTOX_BASE_URL = "https://api.upstox.com/v2"
INSTRUMENTS_URL = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"

# Instrument key mappings
INDEX_KEYS = {
    "NIFTY": "NSE_INDEX|Nifty 50",
    "BANKNIFTY": "NSE_INDEX|Nifty Bank",
    "SENSEX": "BSE_INDEX|SENSEX",
}

# Strike intervals
STRIKE_INTERVALS = {"NIFTY": 50, "BANKNIFTY": 100, "SENSEX": 100}
# Number of strikes to sync on either side of ATM (so ATM ± N contracts × 2 sides
# × CE/PE = 4N + 2 option calls per trading day). Kept small on purpose to make
# the sync fast; the backtest engine falls back to Black-Scholes for strikes
# outside this window.
STRIKE_WINDOW = 2

# Exchange each underlying's option contracts live on in the instruments master
UNDERLYING_EXCHANGES = {
    "NIFTY": "NSE_FO",
    "BANKNIFTY": "NSE_FO",
    "SENSEX": "BSE_FO",
}

# Rate limiting
REQUEST_DELAY_MS = 250
MAX_RETRIES = 3


class UpstoxAuthError(Exception):
    """Raised when Upstox credentials are missing or invalid."""
    pass


class UpstoxHistoricalFetcher:
    """Fetches historical data from Upstox API v2."""

    def __init__(self):
        self.api_key: Optional[str] = None
        self.api_secret: Optional[str] = None
        self.access_token: Optional[str] = None
        self._instruments_cache: Optional[dict] = None
        self._load_credentials()

    def _load_credentials(self):
        """Load credentials from env vars or config file.

        Deployed setups (Render, etc.) should set ``UPSTOX_API_KEY`` and
        ``UPSTOX_API_SECRET`` as env vars; the access token is stored in the
        DB via the OAuth callback and refreshed by ``reload_access_token()``.
        """
        self.api_key = os.environ.get("UPSTOX_API_KEY")
        self.api_secret = os.environ.get("UPSTOX_API_SECRET")
        self.access_token = os.environ.get("UPSTOX_ACCESS_TOKEN")

        if self.api_key and self.api_secret and self.access_token:
            return

        config_path = os.path.expanduser("~/.upstox/config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                self.api_key = self.api_key or config.get("api_key")
                self.api_secret = self.api_secret or config.get("api_secret")
                self.access_token = self.access_token or config.get("access_token")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to read Upstox config: {e}")

    async def reload_access_token(self) -> bool:
        """Pull the latest access token from the DB (set by the OAuth callback).
        Returns True if a token was loaded, False if none is persisted."""
        from web.backend.data import cache
        row = await cache.get_upstox_credentials()
        if row and row.get("access_token"):
            self.access_token = row["access_token"]
            return True
        return False

    def is_authenticated(self) -> bool:
        """Check if credentials are available."""
        return bool(self.api_key and self.api_secret and self.access_token)

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

    async def _request(self, client: httpx.AsyncClient, method: str, url: str,
                       **kwargs) -> Optional[dict]:
        """Make HTTP request with retry logic."""
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = await client.request(
                    method, url, headers=self._get_headers(), **kwargs
                )
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 2))
                    if attempt < MAX_RETRIES:
                        logger.warning(f"Rate limited, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    return None

                if response.status_code == 401:
                    raise UpstoxAuthError("Access token expired. Please refresh via Upstox OAuth flow.")

                if response.status_code >= 500:
                    if attempt < MAX_RETRIES:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return None

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Upstox API {response.status_code}: {response.text[:200]}")
                    return None

            except httpx.ConnectError as e:
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"Upstox API unreachable: {e}") from e

        return None

    async def fetch_index_ohlcv(self, instrument_key: str, from_date: str,
                                 to_date: str, interval: str = "day") -> list[dict]:
        """Fetch historical OHLCV candles for an index.

        Args:
            instrument_key: e.g. 'NSE_INDEX|Nifty 50'
            from_date: 'YYYY-MM-DD'
            to_date: 'YYYY-MM-DD'
            interval: 'day', '1minute', '5minute', etc.

        Returns:
            List of {date, open, high, low, close, volume} dicts.
        """
        if not self.is_authenticated():
            raise UpstoxAuthError("Upstox credentials not configured")

        # Upstox URL format: /historical-candle/{instrumentKey}/{interval}/{to_date}/{from_date}
        encoded_key = instrument_key.replace("|", "%7C")
        url = f"{UPSTOX_BASE_URL}/historical-candle/{encoded_key}/{interval}/{to_date}/{from_date}"

        async with httpx.AsyncClient(timeout=30) as client:
            result = await self._request(client, "GET", url)

        if not result or result.get("status") != "success":
            return []

        candles = result.get("data", {}).get("candles", [])
        records = []
        for candle in candles:
            # Candle format: [timestamp, open, high, low, close, volume, oi]
            if len(candle) >= 6:
                ts = candle[0]
                dt = ts[:10] if isinstance(ts, str) else datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                records.append({
                    "date": dt,
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": int(candle[5]) if candle[5] else 0,
                })
        return records

    async def fetch_option_historical(self, instrument_key: str, from_date: str,
                                       to_date: str, interval: str = "day") -> list[dict]:
        """Fetch historical candles for an individual option contract.

        Same format as fetch_index_ohlcv but for option instrument keys.
        """
        return await self.fetch_index_ohlcv(instrument_key, from_date, to_date, interval)

    async def fetch_index_intraday(self, underlying: str, dt: str,
                                    unit: str = "minutes",
                                    interval: int = 5) -> list[dict]:
        """Fetch intraday index (spot) candles for a single date via v3.

        Returns [{time: 'HH:MM', open, high, low, close}, ...].
        """
        index_key = INDEX_KEYS.get(underlying)
        if not index_key:
            return []
        return await self.fetch_option_intraday(index_key, dt, unit, interval)

    async def fetch_expired_option_intraday(self, exchange_prefix: str, token: int,
                                              expiry: str, dt: str,
                                              interval: str = "1minute") -> list[dict]:
        """Fetch intraday candles for an already-expired option contract.

        Uses Upstox's dedicated ``expired-instruments`` endpoint which accepts
        the key format ``NSE_FO|<token>|<DD-MM-YYYY>``. Interval must be one
        of the v2 set: ``1minute``, ``30minute``, ``day``.
        """
        if not self.is_authenticated():
            raise UpstoxAuthError("Upstox credentials not configured")
        # expiry incoming as YYYY-MM-DD; endpoint wants DD-MM-YYYY
        try:
            y, m, d = expiry.split("-")
            exp_ddmmyyyy = f"{d}-{m}-{y}"
        except Exception:
            return []
        key = f"{exchange_prefix}|{token}|{exp_ddmmyyyy}"
        enc = key.replace("|", "%7C")
        url = f"{UPSTOX_BASE_URL}/expired-instruments/historical-candle/{enc}/{interval}/{dt}/{dt}"
        async with httpx.AsyncClient(timeout=30) as client:
            result = await self._request(client, "GET", url)
        if not result or result.get("status") != "success":
            return []
        candles = result.get("data", {}).get("candles", [])
        records = []
        for c in candles:
            if len(c) < 6:
                continue
            ts = c[0]
            time_str = ts[11:16] if isinstance(ts, str) and len(ts) >= 16 else ""
            if not time_str:
                continue
            records.append({
                "time": time_str,
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
            })
        records.sort(key=lambda r: r["time"])
        return records

    async def fetch_option_intraday(self, instrument_key: str, dt: str,
                                     unit: str = "minutes",
                                     interval: int = 5) -> list[dict]:
        """Fetch intraday option candles for a single date via Upstox API v3.

        v3 supports smaller minute intervals than v2 (v2 only allowed 1minute/30minute).
        Valid units and intervals per Upstox docs: minutes (1,2,3,5,10,15,30),
        hours (1,2,3,4), days (1).

        Returns list of {time: 'HH:MM', open, high, low, close} dicts.
        """
        if not self.is_authenticated():
            raise UpstoxAuthError("Upstox credentials not configured")

        encoded_key = instrument_key.replace("|", "%7C")
        # v3 endpoint: /v3/historical-candle/{key}/{unit}/{interval}/{to}/{from}
        url = (
            f"https://api.upstox.com/v3/historical-candle/{encoded_key}"
            f"/{unit}/{interval}/{dt}/{dt}"
        )

        async with httpx.AsyncClient(timeout=30) as client:
            result = await self._request(client, "GET", url)

        if not result or result.get("status") != "success":
            return []

        candles = result.get("data", {}).get("candles", [])
        records = []
        for c in candles:
            if len(c) < 6:
                continue
            ts = c[0]
            # Upstox timestamps look like "2026-09-11T09:15:00+05:30"
            time_str = ts[11:16] if isinstance(ts, str) and len(ts) >= 16 else ""
            if not time_str:
                continue
            records.append({
                "time": time_str,
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
            })
        # API returns candles newest-first; sort ascending for cache consumers
        records.sort(key=lambda r: r["time"])
        return records

    async def fetch_instruments_master(self) -> dict:
        """Download and parse Upstox instruments master file.

        Returns:
            Dict mapping (underlying, strike, expiry, option_type) -> instrument_key
        """
        if self._instruments_cache is not None:
            return self._instruments_cache

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(INSTRUMENTS_URL)
            if response.status_code != 200:
                logger.error(f"Failed to fetch instruments: {response.status_code}")
                return {}

        # Parse gzipped CSV
        decompressed = gzip.decompress(response.content)
        reader = csv.DictReader(io.StringIO(decompressed.decode("utf-8")))

        lookup = {}
        for row in reader:
            # Accept NSE_FO (NIFTY/BANKNIFTY) and BSE_FO (SENSEX) index options
            exchange = row.get("exchange", "")
            instrument_type = row.get("instrument_type", "")
            option_type = row.get("option_type", "")
            if instrument_type != "OPTIDX":
                continue
            if option_type not in ("CE", "PE"):
                continue

            underlying = row.get("name", "")
            expected_exchange = UNDERLYING_EXCHANGES.get(underlying)
            if not expected_exchange or exchange != expected_exchange:
                continue

            strike = float(row.get("strike", 0))
            expiry = row.get("expiry", "")[:10]  # YYYY-MM-DD
            instrument_key = row.get("instrument_key", "")

            if instrument_key and strike > 0:
                key = (underlying, strike, expiry, option_type)
                lookup[key] = instrument_key

        self._instruments_cache = lookup
        logger.info(f"Loaded {len(lookup)} option instrument keys")
        return lookup

    def _resolve_instrument_key(self, underlying: str, strike: float,
                                 expiry: str, option_type: str) -> Optional[str]:
        """Look up an option's instrument key from the master."""
        if self._instruments_cache is None:
            return None
        return self._instruments_cache.get((underlying, strike, expiry, option_type))

    def _get_nearest_expiry(self, dt: date, underlying: str, expiry_type: str = "weekly") -> Optional[date]:
        """Find the nearest available expiry date from instruments master.

        Looks up actual expiries in the instruments cache rather than calculating,
        since expiry days can vary (e.g., Tuesday vs Thursday due to holidays).
        """
        if self._instruments_cache is None:
            return None

        # Extract all unique expiry dates for this underlying
        expiries = set()
        for key in self._instruments_cache.keys():
            if key[0] == underlying:
                expiries.add(key[2])

        if not expiries:
            return None

        # Convert to date objects and filter by type
        expiry_dates = sorted([date.fromisoformat(exp) for exp in expiries])

        if expiry_type == "weekly":
            # Find the nearest expiry >= current date within next 14 days
            for exp in expiry_dates:
                if exp >= dt and (exp - dt).days <= 14:
                    return exp
        else:  # monthly
            # Find the nearest expiry at month end (>= 20 days into month)
            for exp in expiry_dates:
                if exp >= dt and exp.day >= 20:
                    return exp

        # Fallback: return nearest future expiry
        for exp in expiry_dates:
            if exp >= dt:
                return exp

        return None

    async def sync_data(self, underlying: str, start_date: str, end_date: str,
                         progress_callback: Optional[Callable[[int, int, str], None]] = None):
        """Orchestrate full data sync for an underlying.

        1. Fetch index OHLCV for the date range
        2. For each trading day: compute ATM, resolve strikes, fetch option premiums
        3. Store everything in SQLite cache
        4. Log sync completion

        Args:
            underlying: 'NIFTY' or 'BANKNIFTY'
            start_date: 'YYYY-MM-DD'
            end_date: 'YYYY-MM-DD'
            progress_callback: fn(current, total, message) for progress updates
        """
        if not self.is_authenticated():
            raise UpstoxAuthError("Upstox credentials not configured")

        # Get all trading days in range (for option premium sync)
        from datetime import date as date_cls
        start_dt = date_cls.fromisoformat(start_date)
        end_dt = date_cls.fromisoformat(end_date)
        all_dates = []
        current = start_dt
        while current <= end_dt:
            if current.weekday() < 5:  # Monday-Friday
                all_dates.append(current.isoformat())
            current += timedelta(days=1)

        # Check which dates need OHLCV syncing
        missing_ohlcv_dates = await cache.get_missing_dates(underlying, start_date, end_date)

        total_steps = len(all_dates) + 1  # +1 for index OHLCV
        current_step = 0

        def report(msg: str):
            nonlocal current_step
            current_step += 1
            if progress_callback:
                pct = int(current_step / total_steps * 100)
                progress_callback(pct, 100, msg)

        # Step 1: Fetch index OHLCV (only for missing dates)
        if missing_ohlcv_dates:
            index_key = INDEX_KEYS.get(underlying)
            if not index_key:
                raise ValueError(f"Unknown underlying: {underlying}")

            report(f"Fetching {underlying} index OHLCV data...")
            candles = await self.fetch_index_ohlcv(index_key, start_date, end_date)

            if candles:
                ohlcv_rows = [
                    {
                        "instrument": underlying,
                        "date": c["date"],
                        "interval": "day",
                        "open": c["open"],
                        "high": c["high"],
                        "low": c["low"],
                        "close": c["close"],
                        "volume": c["volume"],
                    }
                    for c in candles
                ]
                await cache.insert_ohlcv_batch(ohlcv_rows)

        # Step 2: Load instruments master
        instruments = await self.fetch_instruments_master()

        # Step 3: For each trading day, fetch option premiums
        strike_interval = STRIKE_INTERVALS[underlying]

        async with httpx.AsyncClient(timeout=30) as client:
            for dt_str in all_dates:
                dt = date.fromisoformat(dt_str)
                report(f"Fetching options for {dt_str}...")

                # Find the spot price for this date from OHLCV
                ohlcv = await cache.get_ohlcv(underlying, dt_str)
                if not ohlcv:
                    continue

                spot = ohlcv["close"]
                atm_strike = round(spot / strike_interval) * strike_interval

                # Compute relevant strikes: ATM ± STRIKE_WINDOW steps
                strikes = [
                    atm_strike + i * strike_interval
                    for i in range(-STRIKE_WINDOW, STRIKE_WINDOW + 1)
                ]

                # Find the nearest expiry for this date
                expiry = self._get_nearest_expiry(dt, underlying, "weekly")
                if not expiry:
                    logger.warning(f"No expiry found for {underlying} on {dt_str}")
                    continue
                expiry_str = expiry.isoformat()

                # Fetch option premiums for each strike
                premium_rows = []
                for strike in strikes:
                    for opt_type in ["CE", "PE"]:
                        inst_key = self._resolve_instrument_key(
                            underlying, strike, expiry_str, opt_type
                        )
                        if not inst_key:
                            continue

                        # Fetch daily candle for this option contract
                        encoded_key = inst_key.replace("|", "%7C")
                        url = f"{UPSTOX_BASE_URL}/historical-candle/{encoded_key}/day/{dt_str}/{dt_str}"

                        result = await self._request(client, "GET", url)
                        await asyncio.sleep(REQUEST_DELAY_MS / 1000)

                        if result and result.get("status") == "success":
                            opt_candles = result.get("data", {}).get("candles", [])
                            if opt_candles:
                                c = opt_candles[0]
                                premium_rows.append({
                                    "instrument": underlying,
                                    "date": dt_str,
                                    "expiry": expiry_str,
                                    "strike": strike,
                                    "option_type": opt_type,
                                    "open_premium": float(c[1]),
                                    "close_premium": float(c[4]),
                                    "high_premium": float(c[2]),
                                    "low_premium": float(c[3]),
                                })

                if premium_rows:
                    await cache.insert_option_premiums_batch(premium_rows)

        await cache.log_sync(underlying, start_date, end_date, "completed")
        if progress_callback:
            progress_callback(100, 100, "Sync complete")
