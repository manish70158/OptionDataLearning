"""Test script to verify instruments parsing."""
import asyncio
import sys
sys.path.insert(0, "/Users/manishkumar/Documents/learning/OptionDataLearning")

from web.backend.data.upstox_fetcher import UpstoxHistoricalFetcher

async def main():
    fetcher = UpstoxHistoricalFetcher()
    print("Loading instruments master...")
    instruments = await fetcher.fetch_instruments_master()
    print(f"Total instruments loaded: {len(instruments)}")

    # Check for some specific NIFTY options
    test_keys = [
        ("NIFTY", 23400.0, "2026-09-15", "CE"),
        ("NIFTY", 23400.0, "2026-09-15", "PE"),
        ("NIFTY", 24000.0, "2026-09-15", "CE"),
    ]

    print("\nTest lookups:")
    for key in test_keys:
        result = instruments.get(key)
        print(f"  {key}: {result}")

    # Show some sample keys
    print("\nSample NIFTY Sept 2026 instruments:")
    count = 0
    for key, value in instruments.items():
        if key[0] == "NIFTY" and "2026-09" in key[2]:
            print(f"  {key}: {value}")
            count += 1
            if count >= 10:
                break

if __name__ == "__main__":
    asyncio.run(main())
