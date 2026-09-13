"""Test script to debug option fetching."""
import asyncio
import sys
from datetime import date
sys.path.insert(0, "/Users/manishkumar/Documents/learning/OptionDataLearning")

from web.backend.data.upstox_fetcher import UpstoxHistoricalFetcher, STRIKE_INTERVALS, STRIKE_RANGES
import httpx

async def main():
    fetcher = UpstoxHistoricalFetcher()

    # Load instruments
    instruments = await fetcher.fetch_instruments_master()
    print(f"Loaded {len(instruments)} instruments\n")

    # Simulate sync logic for Sept 11
    underlying = "NIFTY"
    dt = date(2026, 9, 11)
    dt_str = dt.isoformat()
    spot = 23398.1  # From OHLCV

    # Calculate ATM and strikes
    strike_interval = STRIKE_INTERVALS[underlying]
    strike_range = STRIKE_RANGES[underlying]
    atm_strike = round(spot / strike_interval) * strike_interval
    print(f"Spot: {spot}, ATM Strike: {atm_strike}")

    # Compute strikes
    strikes = []
    s = atm_strike - strike_range
    while s <= atm_strike + strike_range:
        strikes.append(s)
        s += strike_interval
    print(f"Strikes to fetch: {len(strikes)} (from {strikes[0]} to {strikes[-1]})\n")

    # Find expiry
    expiry = fetcher._get_nearest_expiry(dt, underlying, "weekly")
    expiry_str = expiry.isoformat()
    print(f"Expiry: {expiry_str} ({expiry.strftime('%A')})\n")

    # Try to resolve some instrument keys
    test_strikes = [atm_strike - 100, atm_strike, atm_strike + 100]
    print("Testing instrument key resolution:")
    for strike in test_strikes:
        for opt_type in ["CE", "PE"]:
            inst_key = fetcher._resolve_instrument_key(underlying, strike, expiry_str, opt_type)
            print(f"  {strike} {opt_type}: {inst_key}")

    # Try to fetch one option contract
    print("\nTesting API fetch for ATM CE:")
    inst_key = fetcher._resolve_instrument_key(underlying, atm_strike, expiry_str, "CE")
    if inst_key:
        encoded_key = inst_key.replace("|", "%7C")
        url = f"https://api.upstox.com/v2/historical-candle/{encoded_key}/day/{dt_str}/{dt_str}"
        print(f"URL: {url}")

        async with httpx.AsyncClient(timeout=30) as client:
            result = await fetcher._request(client, "GET", url)
            if result:
                print(f"Success! Status: {result.get('status')}")
                candles = result.get("data", {}).get("candles", [])
                if candles:
                    print(f"Candle data: {candles[0]}")
                else:
                    print("No candles in response")
            else:
                print("Request returned None")
    else:
        print("Could not resolve instrument key")

if __name__ == "__main__":
    asyncio.run(main())
