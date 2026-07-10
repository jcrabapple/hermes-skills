# Financial Document & Screenshot Analysis

## Revolut Securities Statement Layout

PDF statements from Revolut Securities (via DriveWealth) have these sections across 9 pages:

1. **Page 1 — Valuation Summary**: Beginning/ending account value, deposits, withdrawals, net change. Shows "This Period" and "This Year" columns.
2. **Pages 2-4 — Disclosures**: Legal text (skip).
3. **Page 5 — Balances**: Currency balances with trade date and settlement date balances.
4. **Page 6 — Holdings (Equity)**: Key section. Columns: Description, Symbol, Quantity, Unit Cost, Total Cost, Market Price, Market Value, Gain/(Loss).
5. **Pages 7-8 — Activity**: Transaction history. Columns: Trade Date, Settle Date, Currency, Activity Type, Symbol/Description, Quantity, Price, Amount.
6. **Page 8 — Sweep Activity**: Cash sweep transactions.
7. **Page 9 — Regulatory updates**: Tax lot disposition (FIFO default), program bank changes.

### Extraction

`pdftotext` works well for these text-based PDFs. The layout is columnar but not tabular — entries run together. Parse by looking for ticker symbols, BUY/SELL keywords, and dollar amounts.

## Revolut App Portfolio View (Mobile)

### Position Card Format

```
$[POSITION_VALUE]           ← shares × current_price (large text)
[shares] [TICKER] · $[PRICE]  ← current price per share (smaller text)
[🟢/🔴] [+/-XX.XX]%        ← gain/loss vs cost basis
```

### Reading Strategy

1. Extract all position cards from the screenshot
2. For each: grab ticker, shares, current price, gain %
3. Reverse-engineer cost: `cost_per_share = current_price / (1 + pct/100)`
4. Verify against any PDF statement data available

### Common Brokers

Same general pattern applies to Robinhood, Webull, Fidelity mobile, etc. — the detail line almost always shows current price, not cost. Always verify.

## Yahoo Finance API Quick Reference

Single quote (for portfolio tracking):
```
GET https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=1d
→ result[0].meta.regularMarketPrice = current price
→ result[0].meta.previousClose = yesterday's close
```

Batch quotes (v7) require auth — do NOT use. Use per-symbol chart endpoint instead.

Trending endpoint returns crypto/futures, not useful stock momentum.
