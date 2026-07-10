---
name: cross-border-shopping
description: >-
  Research and evaluate gray-market / cross-border products not officially
  sold in the user's region. Covers import smartphone and electronics
  purchasing: brand availability, carrier band compatibility checks, Global
  vs. regional ROM verification, reputable gray-market retailers, financing
  options, warranty realities, and pricing benchmarks. Also covers website
  legitimacy evaluation — vetting unfamiliar e-commerce sites for scam risk
  before purchase. Triggers on: import phone, buy [Xiaomi/Oppo/Vivo/Realme/Redmi]
  in US, gray market, international phone, will this phone work on [carrier],
  where to buy [product] not sold here, import electronics, is [website] legit,
  is [website] a scam, can I trust [website], open-ear earbuds alternatives,
  import earbuds, Huawei FreeClip, buy [product] outside [region].
---

# Cross-Border Shopping Skill

## Purpose
Help users buy products — especially electronics and smartphones — that are not officially distributed in their region. Covers availability research, technical compatibility verification, retailer vetting, pricing, financing, and the risks/ tradeoffs of gray-market imports.

## Scope
- Smartphones: Xiaomi, Oppo, Vivo, Realme, OnePlus (non-US models), Sony (Japan variants), etc.
- Other electronics: cameras, audio gear (earbuds, headphones, speakers), wearables, anything with regional distribution gaps
- Region focus: US-centric (T-Mobile / AT&T / Verizon band compatibility), but principles transfer

## Core Workflow

### 0. Website Legitimacy Check (Prerequisite)

**Before recommending any purchase from an unfamiliar retailer, run a structured vetting pass.** This applies to gray-market import stores AND any retailer the user found that you haven't verified before.

#### Step-by-Step Vetting Pipeline

| Check | Tool / Source | Pass Condition |
|-------|--------------|----------------|
| **Scam scoring** | [ScamAdviser](https://www.scamadviser.com/check-website/) — punch in the URL | "Very Likely Safe" or "Good Trust Score" (80%+). "Low Trust" or "Caution" = red alert. |
| **ScamDoc** | [scamdoc.com](https://www.scamdoc.com/) — secondary validation | 90%+ trust score supports legitimacy; below 70% is high risk. |
| **Domain age** | ScamAdviser or WHOIS lookup | Registered >1 year is positive signal (scam domains rarely renew). Multiple years = stronger positive. |
| **SSL validity** | ScamAdviser or browser padlock | Valid SSL certificate = baseline requirement. Missing SSL is automatic disqualification. |
| **Customer reviews** | Trustpilot (site: trustpilot.com), Reddit (site:reddit.com "SITENAME" experience/trust/scam), social media | Mixed is normal. Pattern of 1-star reports about "never received," "no refund," or "fake product" = walk away. Overwhelmingly 5-star on Trustpilot with <50 reviews and no 3-4 star reviews = probably fake. |
| **About Us / Contact** | Visit /aboutus, /contact directly | Real physical address, phone number, working contact form. Missing or vague = flag. |
| **Return policy** | Check /returns, /warranty, /shipping | Clear policy with timelines. "No returns" on expensive imports = risk. |
| **Payment methods** | At checkout | Credit card or PayPal = consumer protection. Wire transfer / crypto only = automatic hard no. |

#### Common Red Flags

- **Product not yet released** being sold as "pre-order" on a no-name import site (the FreeClip 2 listing on Microless had this issue)
- **Spec discrepancies** — listing claims Bluetooth 6.0, standard not ratified yet. If the listing gets a basic fact wrong, reliability of the entire transaction is suspect.
- **Too cheap** — significantly below MSRP from official channels in launched regions
- **"Global shipping" with no stated origin** — if origin warehouse is unclear, returns become impossible

#### When Import Is Too Risky → Find Domestic Alternatives

If the user's goal is a specific product that's not officially sold in their region AND the available import sources fail the vetting above (or the user just wants less hassle):

1. **Identify the category** — What class of product is it? (open-ear earbuds, flagship phone, etc.)
2. **Search for US-available top-tier alternatives** — For each major brand in that category, check:
   - Current model lineup + MSRP
   - Availability at Amazon / Best Buy / B&H
   - Backed by US warranty, easy returns
3. **Compare on the dimensions that mattered** in the original choice (sound quality, battery life, comfort, specific features)
4. **Present a ranked comparison** with prices and where to buy, plus honest trade-offs vs. the original import

Example from this session: Huawei FreeClip 2 (import-only) → alternatives were Bose Ultra Open ($209, Amazon), Shokz OpenDots ONE ($199, Amazon), Sony LinkBuds Clip ($229), Soundcore AeroClip ($150). All beat the FreeClip 2 on warranty/support convenience; some beat it on sound quality or battery.

### 1. Identify the Exact Product & Variant
- **Model number matters more than marketing name.** Example: Xiaomi 15 Ultra has variants `25010PN30G` (Global) vs. `25010PN30C` (China).
- Ask or verify: Is the user looking at the **Global / International** version or a China-specific variant?
- **Chinese-market devices** typically lack US LTE/5G bands, have no Google Play, and run China ROM. They are much cheaper but often unusable in the US.
- **Global ROM** devices: Google Play pre-installed, broader band support, typically English + local languages.

### 2. Carrier Band Compatibility Check

**The canonical tool:** [Kimovil](https://www.kimovil.com/en/frequency-checker)
- Enter device name → select "USA" → see band overlap with T-Mobile / AT&T / Verizon
- **T-Mobile** is the most import-friendly US carrier (relies heavily on n41, n71, B2, B4, B12, B66, B71 which Global phones often include)
- **Verizon** is the least compatible (requires specific CDMA-less certification and bands many imports lack)
- **AT&T** is middle ground; may allow registration but block some 5G bands

**What "Global coverage" looks like in practice:**
- Excellent: 12+ of 15 T-Mobile 5G bands, 10+ of 13 4G bands
- Good: 8-11 of 15 5G bands, 8-10 of 13 4G bands (urban coverage fine, rural gaps possible)
- Poor: <8 5G bands or missing B71/n71 (rural T-Mobile dead zones)

**Red flags to mention:**
- No B71/n71 support = poor rural T-Mobile coverage
- No carrier aggregation support = slower real-world speeds even when connected
- China-only variant = likely missing most US bands entirely

### 3. Rural Coverage Check (Critical for US Users)

This is the #1 reason import phones get returned. Band compatibility on paper means nothing if the user's local tower broadcasts a band the phone lacks.

**Action:** Ask if the user lives in a rural area. If yes or uncertain:
- Direct them to [CellMapper](https://cellmapper.net) or T-Mobile's coverage map for their specific address
- Cross-reference which bands serve their area (often B71, n71, B12)
- Verify the import device covers *those specific bands*, not just "most" bands
- If the import lacks B71/n71 and the user is rural, **steer them to a domestic alternative** (e.g., OnePlus 13 for Hasselblad cameras, Samsung S Ultra for best hardware) rather than letting them discover dead zones after purchase

See `references/chinese-smartphone-imports.md` for detailed rural coverage guidance and domestic alternatives.

### 4. Research Latest Model Lineup

For Chinese smartphone brands, search by brand:
- **Xiaomi:** Xiaomi [number] Ultra, Xiaomi [number] Pro, Redmi Note [number] Pro+, Poco [model]
- **Oppo:** Find X[number] Pro, Find X[number], Reno [number] Pro
- **Vivo:** X[number] Pro, X[number], Y[number], V[number]
- **OnePlus:** [number] Pro, [number] (Global versions often sold officially in US; verify)
- **Realme:** GT [number] Pro, GT Neo [number]

**Information hierarchy:**
1. Official brand global sites (oppo.com/en, vivo.com/en, mi.com/global) for official specs
2. GSMArena for full band/spec sheets
3. TechRadar, PhoneArena, CNET for reviews and real-world testing
4. Reddit (r/Xiaomi, r/Oppo, r/Vivo) for US user reports on actual carrier performance
5. Kimovil for compatibility matrix

### 4. Find Reputable Retailers

#### Tier 1 (Recommended)
| Retailer | Region | Notes | Financing |
|----------|--------|-------|-----------|
| **Swiftronics** | US/Canada | Domestic shipping, explicit Global versions, real returns | Sezzle (Pay in 4), Shop Pay |
| **TradingShenzhen** | EU (Germany) | Best prices, hardware-tested before ship, 1yr warranty | Klarna, PayPal, Apple/Google Pay |
| **Wonda Mobile** | HK | Long track record, Xiaomi/Oppo/Vivo specialists | PayPal only (use PayPal Credit if eligible) |

#### Tier 2 (Use with Caution)
| Retailer | Notes |
|----------|-------|
| **AliExpress** | Multiple sellers; high variance. Look for "Choice"/"Plus" badges, 95%+ ratings, explicit "Global Version" in title. No centralized warranty. |
| **Microless** | UAE-based general importer (microless.com / global.microless.com). Legit per ScamAdviser (93% trust score), domain 3+ years, valid SSL, but mixed Trustpilot reviews — some report non-delivery and refund hassles. Sells Huawei (and other brands banned in US) alongside common products. Best for users comfortable with UAE→US shipping timelines and gray-market risk. Run the vetting pipeline above before committing. |
| **eBay** | Buyer protection helps, but warranty/service varies wildly by seller. Check seller history and return policy. |
| **Etoren** | Works but less community-discussed than Swiftronics/Wonda. |

#### Pricing Benchmark
- TradingShenzhen is usually cheapest (€800-900 for Xiaomi 15 Ultra 16/512)
- Swiftronics is ~$100-150 more but domestic shipping + easier returns
- AliExpress can match or beat prices but with higher risk

### 5. Financing Reality Check

**No traditional 0% APR financing** exists for gray-market imports. Options:
- **Sezzle** (Swiftronics): Pay in 4, no hard credit check
- **Klarna** (TradingShenzhen): Pay in 4 or longer terms
- **PayPal Credit / Pay in 4** (Wonda Mobile, some AliExpress sellers): If you have it
- **Credit card installment plans** (Chase, Amex, etc.): Many cards offer "Plan It" or similar post-purchase installment

**Never offer Apple Card / Samsung Financing / carrier financing** for gray-market devices — these only apply to officially sold products.

### 6. Set Expectations on Warranty & Service

| Reality | What to Tell the User |
|---------|----------------------|
| No US warranty | Manufacturer warranty is void or requires shipping back to Asia/EU |
| 30-day retailer warranty | Swiftronics offers this; TradingShenzhen offers 1yr but EU-based |
| Repair logistics | TradingShenzhen has EU partners (~1 week) or China (~3-6 weeks, free loaner) |
| Returns | Buyer usually pays return shipping for international orders (~$30-60) |
| Restocking fees | 15-25% common if device shows any use |
| Wall adapter | International chargers included; EU/UK adapter may be bundled |

### 7. Output Format

When user asks "Should I buy X?" or "Where can I buy X?", structure response as:

```
## Latest Model Overview
[Short paragraph on top current models]

## US Availability
[Xiaomi/Oppo/Vivo: No official US sales. Available via gray-market import.]

## T-Mobile / Carrier Compatibility
[Kimovil summary, band coverage, caveats]

## Where to Buy (Global Version)
| Store | Price | Financing | Shipping | Warranty |

## Key Risks
- No official US warranty
- No eSIM on some brands (notably Vivo)
- Possible carrier aggregation gaps
- Software: verify Global ROM, not China ROM with custom ROM flashed
- Rural coverage: verify local tower bands via CellMapper before buying
```

## Pitfalls

1. **"Global ROM" vs "Global Version"** — Some sellers flash a custom Global ROM onto a China-hardware device. This blocks OTA updates and may contain malware. Stick to sellers who guarantee official firmware (TradingShenzhen is explicit about this).
2. **Model number mix-ups** — `25010PN30G` (Global) vs `25010PN30C` (China). Always verify the suffix.
3. **eSIM** — Many Chinese flagships omit eSIM entirely. Users on T-Mobile who rely on eSIM will need a physical SIM.
4. **Android Auto** — Some Xiaomi/Vivo devices list "No" for Android Auto compatibility in official specs. Check if this matters for the user.
5. **Language limits** — Official Global ROM supports English + major languages; China ROM is English/Chinese only.
6. **Overpromising financing** — Don't suggest Apple Card, Samsung Financing, or carrier installment plans. These don't work for gray-market devices.
7. **Verizon** — Almost always a no-go for Chinese imports. Don't entertain it unless the user explicitly confirms the device is whitelisted.
8. **Rural band blindness** — An import can show 10+ supported bands but still fail where the user lives if it's missing the one band their local tower uses. Always ask about rural location.
9. **Domestic alternative audio bugs** — When a user is switching flagships to escape audio/Bluetooth bugs (e.g., Pixel → Samsung), verify the target device isn't experiencing the same class of issues. Audio subsystem problems can affect multiple brands simultaneously. See `references/chinese-smartphone-imports.md` for Samsung S26 audio issue details.
10. **T-Mobile vs. MVNO confusion** — Users often say "T-Mobile" when they're on Google Fi, Mint, or Cricket. These MVNOs use T-Mobile's network but may have slightly different band/certification requirements. Clarify actual carrier before declaring compatibility.

## Session-Specific References

See `references/chinese-smartphone-imports.md` for detailed product research from May 2026 sessions, including specific model specs, retailer prices, and user-reported US carrier experiences.

See `references/audio-gear-imports-and-alternatives.md` for audio/earbud import research from May 2026, including Huawei FreeClip 2 importers and US-available open-ear earbud alternatives with pricing and trade-offs.
