# Appliance Price Comparison Session Notes

## Session: 2026-05-24
### Context: User comparing LG WM4000HWA + DLEX4000W vs. alternatives at Lowe's / Home Depot
### Budget: Under $1,000/piece, total under $2,200 with delivery/install/haul-away/plan

---

## Pricing Snapshots (memorial for pattern recognition)

### LG 4000 Series (benchmark)
- **WM4000HWA washer**: ~$900–$1,000
- **DLEX4000W dryer**: ~$900–$1,000
- **Pair total**: ~$1,800–$2,000 before add-ons
- **With delivery/install/haul-away/plan**: $2,200+ at Lowe's

### LG 3400 Series (budget fallback)
- **WM3400CW washer**: ~$700–$800
- **DLE3400W dryer**: ~$700–$800
- **Pair total**: ~$1,400–$1,600
- Same mechanical platform as 4000 series. No TurboWash, steam, WiFi.

### GE UltraFresh 550 Series (value winner)
- **GFW550SSNWW washer**: $799 (Home Depot sale, was $1,099)
- **GFD55ESSNWW dryer**: ~$649–$799 individually
- **Home Depot bundle**: **$1,448/pair** (was $2,198) — saves $750 vs. individual MSRP
- **Lowe's**: Listed as "Top Deal" with same $2,198 crossed-out reference price
- Key differentiator: UltraFresh Vent + Microban gasket (mold prevention)

### Samsung B6300 Series (feature-rich, reliability-caveated)
- **WF45B6300AW washer**: $799–$940
- **DVE45B6300W dryer**: $799–$940
- **Pair total**: ~$1,600–$1,700
- Super Speed 28-min cycle comparable to LG TurboWash
- Samsung CR reliability trails LG/GE

---

## Bundle Pricing Pattern

Home Depot in particular shows "Price for 2 Appliances" that is substantially below the sum of individual prices. This is critical to check even if the user only needs one piece — the bundle may still be cheaper.

- GE GFW550 + GFD55: individual MSRP ~$1,898, bundle $1,448 (24% off)
- Always search `[retailer] [model] bundle` or `[model] collection` to find bundle pages

## Cross-Retailer Check Priority

For major appliances in the US, check in this order:
1. **Home Depot** — strongest bundle discounts, explicit "Price for 2 Appliances"
2. **Lowe's** — price-match guarantee, "Top Deal" / "Flash Sale" tags
3. **Best Buy** — competitive on Samsung/LG smart bundles, Geek Squad plans
4. **AJ Madison / Abt** — lower on some high-end models, verify delivery area first

## Scraper Fallback Validation

Both Lowe's and Home Depot product pages returned 504/403 with Firecrawl during this session. Confirmed workaround: `web_search` with `site:lowes.com [model]` or `site:homedepot.com [model]` surfaces current pricing and sale flags from search index.
