"""Upstox API client for fetching live option chain data."""
import os
import json
import time
import logging
from datetime import datetime, timedelta
import requests
from option_backtester.config import UPSTOX_CACHE_TTL

logger = logging.getLogger(__name__)

UPSTOX_BASE_URL = 'https://api.upstox.com/v2'


class UpstoxAuthError(Exception):
    """Raised when Upstox credentials are missing or invalid."""
    pass


class UpstoxClient:
    """Client for the Upstox REST API."""

    def __init__(self):
        """Initialize with credentials from env vars or config file."""
        self.api_key = None
        self.api_secret = None
        self.access_token = None
        self._cache = {}  # key -> (timestamp, data)

        self._load_credentials()

    def _load_credentials(self):
        """Load credentials from env vars (priority) or config file."""
        # Try environment variables first
        self.api_key = os.environ.get('UPSTOX_API_KEY')
        self.api_secret = os.environ.get('UPSTOX_API_SECRET')
        self.access_token = os.environ.get('UPSTOX_ACCESS_TOKEN')

        if self.api_key and self.api_secret and self.access_token:
            return

        # Fallback to config file
        config_path = os.path.expanduser('~/.upstox/config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                self.api_key = self.api_key or config.get('api_key')
                self.api_secret = self.api_secret or config.get('api_secret')
                self.access_token = self.access_token or config.get('access_token')
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f'Failed to read Upstox config: {e}')

        # Check if we have all required credentials
        missing = []
        if not self.api_key:
            missing.append('UPSTOX_API_KEY')
        if not self.api_secret:
            missing.append('UPSTOX_API_SECRET')
        if not self.access_token:
            missing.append('UPSTOX_ACCESS_TOKEN')

        if missing:
            raise UpstoxAuthError(
                f'Missing Upstox credentials: {", ".join(missing)}\n'
                f'Set them as environment variables or in ~/.upstox/config.json\n'
                f'Example config.json:\n'
                f'{{\n'
                f'  "api_key": "your_api_key",\n'
                f'  "api_secret": "your_api_secret",\n'
                f'  "access_token": "your_access_token"\n'
                f'}}'
            )

    def _get_headers(self):
        """Return authorization headers."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
        }

    def _request_with_retry(self, method, url, max_retries=3, **kwargs):
        """Make HTTP request with retry logic for 429 and 5xx."""
        for attempt in range(max_retries + 1):
            try:
                response = requests.request(method, url, headers=self._get_headers(), **kwargs)

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    if attempt < max_retries:
                        logger.warning(f'Rate limited, retrying in {retry_after}s (attempt {attempt + 1})')
                        time.sleep(retry_after)
                        continue
                    response.raise_for_status()

                if response.status_code >= 500:
                    if attempt < max_retries:
                        wait = 2 ** attempt
                        logger.warning(f'Server error {response.status_code}, retrying in {wait}s')
                        time.sleep(wait)
                        continue
                    logger.error(f'Upstox API error: {response.status_code} {response.text}')
                    response.raise_for_status()

                response.raise_for_status()
                return response.json()

            except requests.ConnectionError as e:
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f'Upstox API unreachable: {e}') from e

        return None

    def fetch_option_chain(self, underlying, expiry_date):
        """Fetch option chain for a given underlying and expiry.

        Args:
            underlying: Symbol like 'NSE_INDEX|Nifty 50' or 'NSE_INDEX|Nifty Bank'
            expiry_date: Expiry date string 'YYYY-MM-DD'

        Returns:
            List of dicts with strike-level data
        """
        cache_key = f'{underlying}|{expiry_date}'
        cached = self._cache.get(cache_key)
        if cached:
            ts, data = cached
            if time.time() - ts < UPSTOX_CACHE_TTL:
                return data

        url = f'{UPSTOX_BASE_URL}/option/chain'
        params = {
            'instrument_key': underlying,
            'expiry_date': expiry_date,
        }

        result = self._request_with_retry('GET', url, params=params)

        if result and result.get('status') == 'success':
            chain_data = result.get('data', [])
            parsed = self._parse_chain(chain_data)
            self._cache[cache_key] = (time.time(), parsed)
            return parsed

        return []

    def _parse_chain(self, chain_data):
        """Parse raw option chain API response into structured records."""
        records = []
        for item in chain_data:
            record = {
                'strike_price': item.get('strike_price'),
                'expiry': item.get('expiry'),
            }
            for side in ['call_options', 'put_options']:
                opt = item.get(side, {})
                prefix = 'call' if 'call' in side else 'put'
                market = opt.get('market_data', {})
                greeks = opt.get('option_greeks', {})
                record[f'{prefix}_ltp'] = market.get('ltp')
                record[f'{prefix}_bid'] = market.get('bid_price')
                record[f'{prefix}_ask'] = market.get('ask_price')
                record[f'{prefix}_oi'] = market.get('oi')
                record[f'{prefix}_volume'] = market.get('volume')
                record[f'{prefix}_delta'] = greeks.get('delta')
                record[f'{prefix}_gamma'] = greeks.get('gamma')
                record[f'{prefix}_theta'] = greeks.get('theta')
                record[f'{prefix}_vega'] = greeks.get('vega')
            records.append(record)
        return records

    @staticmethod
    def resolve_nearest_expiry(underlying='NIFTY', expiry_type='weekly'):
        """Calculate the nearest weekly or monthly expiry date.

        NIFTY weekly expiry: Thursday
        Monthly expiry: Last Thursday of the month

        Returns:
            date string 'YYYY-MM-DD'
        """
        today = datetime.now().date()

        if expiry_type == 'weekly':
            # Thursday = weekday 3
            days_ahead = (3 - today.weekday()) % 7
            if days_ahead == 0 and datetime.now().hour >= 15:
                # Past 3:30 PM on Thursday, next week
                days_ahead = 7
            if days_ahead == 0:
                next_expiry = today
            else:
                next_expiry = today + timedelta(days=days_ahead)
            return next_expiry.strftime('%Y-%m-%d')

        elif expiry_type == 'monthly':
            # Last Thursday of current month
            import calendar
            year, month = today.year, today.month
            # Find last Thursday
            last_day = calendar.monthrange(year, month)[1]
            last_date = datetime(year, month, last_day).date()
            while last_date.weekday() != 3:  # Thursday
                last_date -= timedelta(days=1)

            if last_date < today or (last_date == today and datetime.now().hour >= 15):
                # Move to next month
                if month == 12:
                    year += 1
                    month = 1
                else:
                    month += 1
                last_day = calendar.monthrange(year, month)[1]
                last_date = datetime(year, month, last_day).date()
                while last_date.weekday() != 3:
                    last_date -= timedelta(days=1)

            return last_date.strftime('%Y-%m-%d')

        else:
            raise ValueError(f"expiry_type must be 'weekly' or 'monthly', got '{expiry_type}'")
