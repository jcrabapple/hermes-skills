---
name: nanogpt-linkedin
description: Scrape LinkedIn profiles (name, title, company, email, education, etc.) through NanoGPT's API. Uses your existing NanoGPT API key.
---

# NanoGPT LinkedIn Scraper

Scrape LinkedIn profile data via NanoGPT's managed LinkedIn scraper (`POST /api/v1/linkedin/profile`). Extracts name, job title, company, location, industry, headline, education, email, phone, and more.

## Prerequisites

- NanoGPT API key in `~/.config/nanogpt/.env` (`NANOGPT_API_KEY=sk-nano-...`) or `NANOGPT_API_KEY` env var
- `curl` or `requests` Python library

## Script

A convenience CLI is at `scripts/scrape_linkedin.py` — handles API key loading, payload building, and formatted output.

```bash
# Single profile
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk

# Multiple profiles
./scripts/scrape_linkedin.py https://www.linkedin.com/in/satyanadella https://www.linkedin.com/in/jeffweiner08

# With cost cap
./scripts/scrape_linkedin.py https://www.linkedin.com/in/satyanadella --max-charge 0.05

# Save raw JSON
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk --output results.json

# Raw JSON output to stdout
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk --raw
```

## API Endpoint

```
POST https://nano-gpt.com/api/v1/linkedin/profile
Authorization: Bearer $NANOGPT_API_KEY
Content-Type: application/json
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `profileUrls` | string[] | **required** | LinkedIn profile URLs (e.g. `https://www.linkedin.com/in/username`) |
| `maxTotalChargeUsd` | float | — | Max cost in USD per request |
| `resultLimit` | integer | — | Max profiles to return |
| `waitForFinishSecs` | integer | 180 | How long to wait for scraping |

## Response Format

The API returns `items` (array of profile objects) and `usage` (billing info).

Each profile item contains:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Full name |
| `jobTitle` | string | Current job title |
| `company` | string | Current company |
| `location` | string | Geographic location |
| `industry` | string | Industry sector |
| `headline` | string | LinkedIn headline |
| `education` | string | Education background |
| `email` | string\|null | Email if available |
| `phone` | string\|null | Phone if available |
| `website` | string | Personal website |
| `linkedinUrl` | string | Profile URL |
| `verified` | string | Whether profile is verified |
| `scrapedAt` | string | ISO timestamp |
| `dataQuality` | string | Quality level (e.g. "professional") |

## Pricing

| Event | Cost (USD) |
|-------|-----------|
| Per profile scraped | ~$0.01 |

Billed through NanoGPT. Some profiles return empty items (very locked-down profiles) but still cost the per-event rate.

## Pitfalls

See `references/api-response-schema.md` for the full response structure, billing object, and tested profile behaviors.

- Very locked-down or private profiles may return empty items (0 results) but still incur the base Apify actor start cost
- Scraping runs on NanoGPT's infrastructure — wait time depends on job queue (30-80s typical)
- Only supports profile scraping currently (no posts, search, or company endpoints)
- Some profiles take longer to scrape than others — increase `waitForFinishSecs` for batches
- The API key lives at `~/.config/nanogpt/.env` — source it before running curl
- The actor (`unlimitedleadtestinbox/linkedin-profile-scraper-with-email-no-cookies`) does not require LinkedIn cookies
