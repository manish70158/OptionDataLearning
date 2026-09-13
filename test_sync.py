"""Test script to debug sync logic."""
import asyncio
import sys
from datetime import date
sys.path.insert(0, "/Users/manishkumar/Documents/learning/OptionDataLearning")

from web.backend.data.upstox_fetcher import UpstoxHistoricalFetcher

async def main():
    fetcher = UpstoxHistoricalFetcher()

    # Load instruments first
    instruments = await fetcher.fetch_instruments_master()
    print(f"Total instruments loaded: {len(instruments)}")

    # Test expiry calculation
    test_date = date(2026, 9, 11)
    expiry = fetcher._get_nearest_expiry(test_date, "NIFTY", "weekly")
    print(f"\nTest date: {test_date} ({test_date.strftime('%A')})")
    print(f"Calculated expiry: {expiry} ({expiry.strftime('%A') if expiry else 'None'})")
    print(f"\nTotal instruments loaded: {len(instruments)}")

    # Check if instruments exist for calculated expiry
    expiry_str = expiry.isoformat()
    matching = [(k, v) for k, v in instruments.items()
                if k[0] == "NIFTY" and k[2] == expiry_str and 23000 <= k[1] <= 24000]
    print(f"\nInstruments for NIFTY {expiry_str} (strikes 23000-24000):")
    for k, v in matching[:5]:
        print(f"  {k}: {v}")

    # Check what expiries exist near September 11
    sept_expiries = set()
    for k in instruments.keys():
        if k[0] == "NIFTY" and "2026-09" in k[2]:
            sept_expiries.add(k[2])
    print(f"\nAll NIFTY September 2026 expiries in instruments:")
    for exp in sorted(sept_expiries):
        exp_date = date.fromisoformat(exp)
        print(f"  {exp} ({exp_date.strftime('%A')})")

if __name__ == "__main__":
    asyncio.run(main())
