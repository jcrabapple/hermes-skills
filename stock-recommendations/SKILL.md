---
name: stock-recommendations
description: Weekly stock recommendation digest using mixed signals - trending tickers, fundamentals, and price momentum. Scans for stocks under $20 and delivers recommendations via email.
version: 1.1.0
author: Jason Crabtree
license: MIT
metadata:
  hermes:
    tags: [stocks, finance, investing, weekly-digest, cron]
    related_skills: []
---

# Stock Recommendations

Weekly stock scan using multiple data sources to identify investment opportunities under $20.

## Setup

### Finnhub API Key (Required)

1. Visit https://finnhub.io/register
2. Create free account
3. Store API key: `mkdir -p ~/.hermes/secrets && echo "YOUR_KEY" > ~/.hermes/secrets/finnhub_api_key`

## Data Sources

| Source | Purpose | Limit |
|--------|---------|-------|
| Yahoo Finance Trending | Momentum/trending tickers | None (be reasonable) |
| Yahoo Finance Chart | Price quotes, change % | None (be reasonable) |
| Finnhub | Fundamentals, metrics, profile | 60 calls/min free tier |

**Note:** Reddit r/wallstreetbets JSON scraping died in June 2026 (403 on all no-auth endpoints). Replaced with Yahoo Finance trending tickers as the momentum/sentiment signal.

## Filter Criteria

- Price under $20
- Market cap > $50M (avoid penny stocks)
- Common stock only (no ETFs/funds)
- Stocks appearing in both Yahoo trending AND the curated list are prioritized

## Cron Job Architecture

The weekly scan runs as a `no_agent=True` script-only cron job — no LLM is involved. The script (`~/.hermes/scripts/weekly_stock_scan.py`) runs the full pipeline: scan → format → email via AgentMail.

- **Schedule:** Sunday noon ET (`0 16 * * 0` in UTC = 16:00 UTC = 12:00 ET)
- **Delivery:** Telegram (summary) + email (full HTML report)
- **Model:** None (script-only, `no_agent=True`)

**For ad-hoc scans** (user asks "scan for stocks now"):
```bash
python3 ~/.hermes/scripts/weekly_stock_scan.py
```

**For modifying the scan logic:** Edit `~/.hermes/scripts/weekly_stock_scan.py` — this is the source of truth. The code below in this SKILL.md is reference documentation, not the running code.

## How the Scan Works

### 1. Yahoo Trending Tickers

Fetches `https://query1.finance.yahoo.com/v1/finance/trending/us` for the current list of trending US tickers. Filters out crypto (`BTC-USD`, `XRP-USD`), futures (`NQ=F`), forex, and indices (`^KS11`). These are the "momentum" candidates.

### 2. Curated Small-Cap List

A maintained list of known small-cap stocks historically under $20. Updated June 2026 to remove delisted tickers (NAKD→CENN, MULN delisted, CTRM merged). This list needs periodic review — tickers move above $20 or get delisted.

### 3. Price + Fundamentals Fetch

For each candidate ticker:
- **Yahoo v8 chart endpoint** — price, short name, day-over-day change
- **Finnhub metrics endpoint** — market cap, P/E ratio, 52-week range
- **Finnhub profile endpoint** — company name, sector

### 4. Filtering and Scoring

- Filter: price > $0 and ≤ $20, market cap ≥ $50M (Finnhub returns this in millions)
- Score: trending tickers get priority (`sources=2`), then sorted by market cap

## Key Functions

```python
def get_yahoo_quote(symbol):
    """Get quote from Yahoo Finance chart API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    meta = resp.json()['chart']['result'][0]['meta']
    price = meta.get('regularMarketPrice', 0)
    # CRITICAL: previousClose is None from this endpoint; use chartPreviousClose
    prev = meta.get('chartPreviousClose') or meta.get('previousClose') or price
    return {
        'symbol': symbol,
        'name': meta.get('shortName', symbol),
        'price': price,
        'change_pct': round(((price - prev) / prev * 100), 2) if prev and prev > 0 else 0
    }

def get_finnhub_metrics(symbol):
    """Get fundamentals from Finnhub. marketCapitalization is in MILLIONS."""
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={FINNHUB_KEY}"
    m = requests.get(url, timeout=10).json().get('metric', {})
    profile = requests.get(
        f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_KEY}",
        timeout=10
    ).json()
    return {
        'market_cap': m.get('marketCapitalization', 0),  # in MILLIONS
        'pe_ratio': m.get('peBasicExclExtraTTM'),
        'sector': profile.get('finnhubIndustry', 'Unknown'),
        'name': profile.get('name', symbol),
        '52w_high': m.get('52WeekHigh'),
        '52w_low': m.get('52WeekLow'),
    }
```

## Known Pitfalls

1. **Yahoo `previousClose` returns `None`** — the v8 chart endpoint does NOT populate `previousClose`. Use `chartPreviousClose` for change calculations. This was broken for months — every stock showed `+0.00%` change. Fixed June 2026.

2. **Reddit JSON endpoints return 403** — as of June 2026, `reddit.com/r/*/hot.json` blocks all unauthenticated requests. The `nanogpt_reddit_scraper` tool or Reddit API with auth (PRAW) are alternatives if sentiment data is needed again. Currently replaced with Yahoo Finance trending tickers.

3. **Finnhub `marketCapitalization` is in MILLIONS** — compare with `> 50` (meaning $50M), NOT `> 50_000_000`.

4. **Finnhub quote `c` field** often returns 0 for NASDAQ stocks — use Yahoo for price data.

5. **Yahoo batch quotes (v7)** requires auth (401) — use per-symbol chart endpoint (v8) instead.

6. **Yahoo trending includes crypto/futures** — filter out symbols containing `=`, `-USD`, or starting with `^`.

7. **Curated small-cap list goes stale** — tickers get delisted, merge, or move above $20. Prune periodically. Removed in June 2026 update: AMC (near bankruptcy), NAKD (became CENN in 2023), MULN (delisted from Nasdaq 2024), CTRM (merged), SQ (now Block, trades above $20), MRNA (trades above $100).

8. **Finnhub free tier** has no price-target or sentiment data — don't rely on those endpoints.

9. **Rate limiting on rapid scans** — running `scan()` twice in quick succession will get rate-limited by Finnhub (60 calls/min) and Yahoo (undocumented but strict). Space out manual runs by at least 60 seconds.

10. **SKILL.md code drifts from the running script** — The cron job runs `~/.hermes/scripts/weekly_stock_scan.py` as `no_agent=True`. The SKILL.md contains a reference copy of the key functions, but the script is the source of truth. When fixing bugs, edit the script first, then update the SKILL.md reference copy. The June 2026 review found the SKILL.md had a broken `previousClose` code example that the script also had — both needed fixing. Always check both files when modifying logic.

11. **Silent failures in bare `except` blocks** — The script uses bare `except Exception: pass` in several places. This means broken API fields (like `previousClose` returning `None`) fail silently and produce `0` or empty values rather than errors. When debugging "everything shows 0" issues, check each `except` block for swallowed errors.

## Portfolio Tracking

Track an existing brokerage portfolio (not just scan for new picks). Uses the same Yahoo Finance v8 chart endpoint for live prices.

### Workflow

1. **Extract holdings from PDF statement**: Use `pdftotext` for text-based broker statements (fast, no dependencies). For scanned/image PDFs, use pymupdf or marker per the `ocr-and-documents` skill.
2. **Read mobile app screenshots**: Use `vision_analyze` to extract holdings from brokerage app screenshots. **PITFALL** — see below.
3. **Build a tracking script**: Python script with hardcoded portfolio positions (ticker, shares, cost_basis). Fetches live prices, calculates P&L, formats a summary.
4. **Schedule via cron**: Weekday market close (e.g., `0 16 * * 1-5`) delivers updates to Discord/Telegram.

### Financial App Screenshot Reading Pitfall

Mobile brokerage apps (Revolut, Robinhood, etc.) display position cards with a specific format:

```
[Large number]          ← Total POSITION MARKET VALUE (shares × current price)
[quantity] TICKER · $[price]  ← shares, ticker, CURRENT MARKET PRICE per share
[arrow] [+/-XX.XX]%    ← Gain/loss from ACTUAL cost basis (NOT the price shown above)
```

**The "detail" price is the current market price, NOT the cost basis.** To recover the actual cost basis:
```python
cost_price = current_price / (1 + gain_pct / 100)
cost_basis = shares * cost_price
```

This is critical — treating the displayed price as cost basis produces wildly wrong P&L numbers.

### Price Fetching (reuse from scan function above)

```python
def fetch_price(ticker: str) -> float | None:
    """Single price from Yahoo Finance chart API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except Exception:
        return None
```

### Reference

- [references/portfolio-tracking.md](references/portfolio-tracking.md) — Full example script and Revolut statement layout details.

## Notes

- "Mixed signals" = stocks appearing in both Yahoo trending and the curated list
- Disclaimer: not financial advice
