# Retailer Site Scraping Workarounds

> Major appliance retailer sites (Lowe's, Home Depot, Best Buy) are frequently blocked or timeout with web_extract / Firecrawl. This reference documents the failures and reliable alternatives.

## Sites That Fail

| Site | Failure Mode | Notes |
|------|-------------|-------|
| **Lowe's** (`lowes.com/pd/*`) | Firecrawl 504 timeout | Product pages, review pages both fail consistently |
| **Home Depot** (`homedepot.com/p/*`) | Firecrawl 504 timeout | Review sub-pages especially prone to timeout |
| **Best Buy** (`bestbuy.com/site/reviews/*`) | Firecrawl 504 timeout | Product pages sometimes work; review pages almost never |
| **Amazon** (`amazon.com/dp/*` or `/product/*`) | CAPTCHA page returned | Product pages consistently return CAPTCHA when fetched via web_extract |
| **Better Housekeeping** (`betterhousekeeping.com`) | 403 Forbidden | Consistently blocks scrapers |
| **Reddit** (`reddit.com/r/*/comments/*`) | "Website Not Supported" | Firecrawl explicitly does not support Reddit |

## Workarounds (Use in this order)

1. **Search result snippets** — Use `web_search` with `site:lowes.com` or exact model numbers. The description/summary in search results often contains owner review excerpts and price info.
2. **Aggregate review sites** — ProductNotes, Consumer Reports (specs page), Reviewed.com, Wirecutter (NYT) scrape more reliably and carry expert analysis.
3. **Retailer mobile apps / in-store** — If search snippets are insufficient, ask the user to check Lowe's app or store for current sale prices. Appliance pricing is highly promotional.
4. **Browser tools** — `browser_navigate` can work for quick price checks if the environment has a working browser, but auto-launch can fail on headless/container setups. Use as fallback, not primary.
5. **YouTube** — Search result descriptions for review videos often contain owner comments with real-world complaints.
6. **Manufacturer direct sites** — Sites like `birdfy.com`, `wyze.com` are generally scrape-friendly and work reliably with `web_extract`. They often have better bundle options than Amazon (e.g. lifetime AI vs subscription), coupon codes (check footer for newsletter signup prompts), and detailed spec sheets. Always check the manufacturer's direct site after scanning retailers.
7. **Press coverage of sales events** — For historical Amazon pricing (Cyber Monday, Prime Day), search `"[product name]" "Amazon" "Prime Day"` or `"Cyber Monday"`. Sites like PopSci, Gizmodo, WIRED publish deal roundups with exact prices. Useful for knowing the floor price to watch for.

## Model-Specific Search Patterns That Work

When researching a specific model at a retailer:
- `"WM4000HWA" "Lowe's" review` — finds Reddit or Houzz threads with price context
- `"WM3400CW" vs "WM4000HWA" Reddit` — finds owner comparison threads with real buying decisions
- `"DLEX4000W" "sensor dry" problem` — surfaces specific complaint patterns
- `site:lowes.com "LG" "front load washer" under $1000` — surfaces collection pages even if product pages fail
