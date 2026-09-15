#!/usr/bin/env python3
"""Refresh research/market_data.json: current LSE price/market-cap
snapshots plus daily share-price history (with a year-end rollup derived
from it), for the LSE-listed bank parents catalogued in
build_deliverable.py's PARENT_MARKET_DATA.

Meant to run periodically (e.g. a weekday cron job) ahead of
build_deliverable.py, which reads research/market_data.json at curate
time and merges it onto each mapped bank's page. Two free, keyless APIs:
the LSE's own instrument-data endpoint for the current snapshot, and
Yahoo Finance's chart endpoint for history (LSE tickers as SYMBOL.L).

Per CODING_STANDARDS.md's refresh conventions: idempotent, and a failed
fetch for one ticker must not clobber that ticker's already-good data
(the deliverable then just keeps showing the last successful snapshot -
the "when offline, show the latest data point we have" behaviour lives
here, as data staleness, not as fallback logic in the deliverable).

    python3 scripts/insights/fetch_market_data.py
"""
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_deliverable import PARENT_MARKET_DATA  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = ROOT / "research" / "market_data.json"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def _get_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def fetch_current(ticker):
    url = f"https://api.londonstockexchange.com/api/gw/lse/instruments/alldata/{ticker}"
    data = _get_json(url)
    price = data.get("midPrice") or data.get("bid")
    market_cap = data.get("marketcapitalization")
    if price is None or market_cap is None:
        raise ValueError(f"missing price/market cap in LSE response for {ticker}")
    return {
        "share_price_gbx": price,
        "market_cap_gbp": market_cap,
        "as_of": date.today().isoformat(),
        "source": url,
    }


def fetch_daily_history(ticker):
    """date (YYYY-MM-DD) -> closing share price (GBX), real daily
    resolution - a Yahoo/Google-Finance-style chart needs actual trading
    days, not one point a year. 20y at interval=1d is Yahoo's own cutoff
    for still honouring daily granularity (a literal range=max silently
    coarsens to ~quarterly instead); 20y comfortably covers every bank's
    earliest balance-sheet year in this project (2010)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}.L?range=20y&interval=1d"
    data = _get_json(url, timeout=30)
    result = ((data.get("chart") or {}).get("result")) or []
    if not result:
        raise ValueError(f"no chart data returned for {ticker}")
    r = result[0]
    timestamps = r.get("timestamp") or []
    closes = (((r.get("indicators") or {}).get("quote")) or [{}])[0].get("close") or []
    by_day = {}
    for ts, close in zip(timestamps, closes):
        if close is None:
            continue
        by_day[datetime.utcfromtimestamp(ts).date().isoformat()] = round(close, 2)
    return by_day


def yearly_rollup(daily):
    """Year -> last trading day's close seen that year (a year-end
    snapshot, not a smoothed average) - derived from the daily series so
    there's one fetch and one source of truth, not two independent calls
    that can silently drift apart."""
    by_year = {}
    for day in sorted(daily):
        by_year[day[:4]] = daily[day]
    return by_year


def main():
    tickers = sorted({meta["ticker"] for meta in PARENT_MARKET_DATA.values()})
    out = json.loads(OUT_PATH.read_text()) if OUT_PATH.exists() else {}
    failures = []
    for ticker in tickers:
        entry = dict(out.get(ticker, {}))
        try:
            entry["current"] = fetch_current(ticker)
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            failures.append(f"{ticker} current: {e}")
        try:
            # Merge, don't replace - a transient gap in one fetch must not
            # erase days already captured on a prior run.
            daily = {**entry.get("history_daily", {}), **fetch_daily_history(ticker)}
            entry["history_daily"] = daily
            entry["history"] = yearly_rollup(daily)
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            failures.append(f"{ticker} history: {e}")
        if entry:
            out[ticker] = entry
        time.sleep(0.5)  # polite pacing against two free, unauthenticated APIs

    tmp_path = OUT_PATH.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    tmp_path.replace(OUT_PATH)
    print(f"Wrote {len(out)} tickers to {OUT_PATH}")
    if failures:
        print(f"{len(failures)} fetch failures this run (prior data kept where available):")
        for f in failures:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
