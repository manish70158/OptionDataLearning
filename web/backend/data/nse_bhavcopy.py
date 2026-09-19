"""Historical F&O bhavcopy fetcher for NSE and BSE.

Upstox's live instruments master doesn't retain expired contracts, so we can't
recover their instrument_keys after they expire. NSE (and BSE) publish daily
bhavcopy CSVs that DO contain every contract traded that day — including its
open/high/low/close/settlement price — indexed by (symbol, expiry, strike,
option_type). We use those to populate option_premiums for historical dates.

NSE archive URL:
  https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip

BSE archive URL (equity derivatives incl. SENSEX options):
  https://www.bseindia.com/download/Bhavcopy/Derivative/BhavCopy_BSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip
"""
from __future__ import annotations

import csv
import io
import logging
import zipfile
from datetime import date, timedelta
from typing import Iterable, Optional

import httpx

logger = logging.getLogger(__name__)

_NSE_URL = "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{ymd}_F_0000.csv.zip"
_BSE_URL = "https://www.bseindia.com/download/Bhavcopy/Derivative/BhavCopy_BSE_FO_0_0_0_{ymd}_F_0000.csv.zip"

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def _url_for(exchange: str, dt: date) -> str:
    ymd = dt.strftime("%Y%m%d")
    if exchange == "BSE":
        return _BSE_URL.format(ymd=ymd)
    return _NSE_URL.format(ymd=ymd)


async def fetch_bhavcopy(exchange: str, dt: date) -> Optional[list[dict]]:
    """Download and parse one day's F&O bhavcopy. Returns None if unavailable
    (weekend / holiday / URL not published yet / origin blocked us).

    NSE archives can be picky about missing headers; a Referer sourced from
    nseindia.com plus a browser-like User-Agent unblocks most cloud hosts.
    """
    url = _url_for(exchange, dt)
    headers = {
        "User-Agent": _UA,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/all-reports-derivatives" if exchange == "NSE"
                   else "https://www.bseindia.com/",
    }
    try:
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
    except httpx.HTTPError as e:
        logger.warning(f"Bhavcopy fetch error {url}: {e}")
        return None
    if resp.status_code != 200 or not resp.content:
        logger.warning(f"Bhavcopy fetch {url} → HTTP {resp.status_code}")
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            name = zf.namelist()[0]
            raw = zf.read(name).decode("utf-8", errors="replace")
    except zipfile.BadZipFile:
        return None
    reader = csv.DictReader(io.StringIO(raw))
    return list(reader)


def parse_option_rows(rows: Iterable[dict], underlyings: set[str]) -> list[dict]:
    """Filter bhavcopy rows for option contracts on the given underlyings.

    Handles the NSE 2024+ column schema (BhavCopy_NSE_FO_..._F_0000.csv):
      TradDt, XpryDt, StrkPric, OptnTp, TckrSymb, FinInstrmTp,
      OpnPric, HghPric, LwPric, ClsPric, TtlTradgVol, OpnIntrst, ...

    Returns list of dicts with normalised fields:
      {trade_date, expiry, strike, option_type, open, high, low, close,
       volume, open_interest, underlying}.
    """
    out: list[dict] = []
    for row in rows:
        tkr = row.get("TckrSymb", "")
        if tkr not in underlyings:
            continue
        instr_tp = row.get("FinInstrmTp", "")
        if instr_tp not in ("IDO", "STO", "OPTIDX", "OPTSTK", "OPTFUT"):
            # NSE new schema uses IDO for index options; keep the older codes too
            continue
        opt_tp = row.get("OptnTp", "")
        if opt_tp not in ("CE", "PE"):
            continue
        try:
            strike = float(row.get("StrkPric", "0"))
            openp = float(row.get("OpnPric", "0") or 0)
            highp = float(row.get("HghPric", "0") or 0)
            lowp = float(row.get("LwPric", "0") or 0)
            closep = float(row.get("ClsPric", "0") or 0)
        except ValueError:
            continue
        expiry = row.get("XpryDt", "")[:10]
        trade_dt = row.get("TradDt", "")[:10]
        if not expiry or not trade_dt or strike <= 0:
            continue
        try:
            und = float(row.get("UndrlygPric", "0") or 0)
        except ValueError:
            und = 0.0
        # NSE FinInstrmId maps 1:1 to the numeric token in Upstox's instrument
        # key (NSE_FO|<token>). Persisting this lets us build the expired-
        # instruments key later: NSE_FO|<token>|<DD-MM-YYYY>.
        try:
            token = int(row.get("FinInstrmId", "0") or 0)
        except ValueError:
            token = 0
        out.append({
            "underlying": tkr,
            "trade_date": trade_dt,
            "expiry": expiry,
            "strike": strike,
            "option_type": opt_tp,
            "open": openp,
            "high": highp,
            "low": lowp,
            "close": closep,
            "underlying_close": und,
            "nse_token": token,
            "volume": int(float(row.get("TtlTradgVol", "0") or 0)),
            "open_interest": int(float(row.get("OpnIntrst", "0") or 0)),
        })
    return out


async def fetch_and_parse(dt: date, underlyings: set[str]) -> list[dict]:
    """Fetch bhavcopy for `dt` from whichever exchange serves the underlyings,
    parse, and return normalised option rows."""
    results: list[dict] = []
    # NSE covers NIFTY / BANKNIFTY / FINNIFTY / MIDCPNIFTY etc.
    if any(u in underlyings for u in ("NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY")):
        rows = await fetch_bhavcopy("NSE", dt)
        if rows:
            results.extend(parse_option_rows(rows, underlyings & {"NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"}))
    if "SENSEX" in underlyings:
        rows = await fetch_bhavcopy("BSE", dt)
        if rows:
            results.extend(parse_option_rows(rows, {"SENSEX"}))
    return results


def business_days(start: date, end: date) -> list[date]:
    """Return list of Mon–Fri dates in [start, end] (inclusive)."""
    out = []
    d = start
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out
