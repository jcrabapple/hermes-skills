# NanoGPT LinkedIn Scraper

Scrape LinkedIn profile data — name, job title, company, location, industry, headline, education, email, phone, and more — through [NanoGPT](https://nano-gpt.com) billing.

## Features

- **Profile extraction**: name, job title, company, location, industry, headline
- **Contact info**: email and phone when available
- **Education & background**: education field, personal website
- **Quality indicators**: data quality level, verification status
- **No cookies needed**: uses Apify actor that doesn't require LinkedIn login
- **Batch scraping**: multiple profiles in a single request

## Prerequisites

- A [NanoGPT](https://nano-gpt.com) account with API credits
- Your NanoGPT API key set as the `NANOGPT_API_KEY` environment variable:

```bash
export NANOGPT_API_KEY=sk-nan...here
```

Or in a `.env` file (the CLI auto-detects it):

```bash
echo 'NANOGPT_API_KEY=sk-nan...here' >> ~/.config/nanogpt/.env
```

- Python 3.8+ (for the CLI script)
- `curl` (for raw API usage)

## Installation

Clone the repo and make the script executable:

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cd hermes-skills/nanogpt-linkedin
chmod +x scripts/scrape_linkedin.py
```

Or just grab the script directly:

```bash
curl -O https://raw.githubusercontent.com/jcrabapple/hermes-skills/main/nanogpt-linkedin/scripts/scrape_linkedin.py
chmod +x scrape_linkedin.py
```

## Quick Start

```bash
# Scrape a single profile
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk

# Scrape multiple profiles
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk https://www.linkedin.com/in/satyanadella

# With cost cap
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk --max-charge 0.05

# Save raw JSON
./scripts/scrape_linkedin.py https://www.linkedin.com/in/elonmusk --output results.json
```

## CLI Reference

```
usage: scrape_linkedin.py [-h] [--max-charge MAX_CHARGE] [--results RESULTS]
                          [--wait WAIT] [--output OUTPUT] [--raw]
                          urls [urls ...]
```

| Flag | Default | Description |
|------|---------|-------------|
| positional `urls` | — | One or more LinkedIn profile URLs |
| `--max-charge` | — | Max cost in USD per request |
| `--results` | — | Max profiles to return |
| `--wait` | 180 | Max seconds to wait for scraping |
| `--output` / `-o` | — | Save raw JSON response to file |
| `--raw` | false | Print raw JSON instead of formatted output |

## Raw API Usage

If you prefer `curl`:

```bash
curl -s -X POST https://nano-gpt.com/api/v1/linkedin/profile \
  -H "Authorization: Bearer sk-nan...here" \
  -H "Content-Type: application/json" \
  -d '{
    "profileUrls": ["https://www.linkedin.com/in/elonmusk"],
    "waitForFinishSecs": 180
  }' | jq '.items[0]'
```

### With cost cap

```bash
curl -s -X POST https://nano-gpt.com/api/v1/linkedin/profile \
  -H "Authorization: Bearer sk-nan...here" \
  -H "Content-Type: application/json" \
  -d '{
    "profileUrls": [
      "https://www.linkedin.com/in/elonmusk",
      "https://www.linkedin.com/in/satyanadella"
    ],
    "maxTotalChargeUsd": 0.05,
    "waitForFinishSecs": 180
  }' | jq '.'
```

## Pricing

Charged through your NanoGPT account:

| Event | Cost |
|-------|------|
| Per profile scraped | ~$0.01 |

The actor (`unlimitedleadtestinbox/linkedin-profile-scraper-with-email-no-cookies`) does not require LinkedIn cookies or login.

## API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `profileUrls` | string[] | **required** | LinkedIn profile URLs |
| `maxTotalChargeUsd` | float | — | Max cost in USD per request |
| `resultLimit` | integer | — | Max profiles to return |
| `waitForFinishSecs` | integer | 180 | Max wait time |

## Response Format

The API returns:

```json
{
  "object": "linkedin.profile.scrape",
  "actor": "unlimitedleadtestinbox/linkedin-profile-scraper-with-email-no-cookies",
  "status": "SUCCEEDED",
  "items": [ ... ],
  "usage": {
    "actualCostUsd": 0.010266,
    "chargedEventCounts": { "apify-default-dataset-item": 1 }
  },
  "metadata": {
    "estimatedProfiles": 1,
    "resultLimit": 1
  }
}
```

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
| `email` | string\|null | Email (when available) |
| `phone` | string\|null | Phone (when available) |
| `website` | string | Personal website |
| `linkedinUrl` | string | Profile URL |
| `verified` | string | Verification status (string, not boolean) |
| `dataQuality` | string | Quality level (e.g. "professional") |
| `scrapedAt` | string | ISO timestamp |

## Pitfalls

- **Locked-down profiles** may return empty `items[]` — very private profiles (Bill Gates, Satya Nadella) don't return data even though the scraper runs
- **Scrape time** varies: 30-80 seconds per request depending on profile accessibility
- **Only profile scraping** is currently available — no posts, search, or company endpoints exist yet
- **No cookies needed** — the Apify actor works without LinkedIn authentication
- **`verified` is a string** (`"true"`) not a boolean — handle accordingly in code

## Full API Documentation

- [LinkedIn Profile Scraper Application](https://nano-gpt.com/applications/linkedin/profile)

## License

MIT

## Using with Hermes Agent

This skill can be loaded directly into [Hermes Agent](https://hermes-agent.nousresearch.com) so your AI agent can scrape LinkedIn profiles and research people autonomously.

### Installation

```bash
# From anywhere in your Hermes environment:
git clone https://github.com/jcrabapple/hermes-skills.git /tmp/hermes-skills
cp -r /tmp/hermes-skills/nanogpt-linkedin ~/.hermes/skills/social-media/nanogpt-linkedin
rm -rf /tmp/hermes-skills
```

Or symlink to keep it updated:

```bash
git clone https://github.com/jcrabapple/hermes-skills.git ~/hermes-skills
ln -s ~/hermes-skills/nanogpt-linkedin ~/.hermes/skills/social-media/nanogpt-linkedin
```

### Configure API Key

Add your NanoGPT API key to Hermes' environment file:

```bash
echo 'NANOGPT_API_KEY=sk-nan...here' >> ~/.hermes/.env
```

### Usage Within Hermes

Once installed, Hermes Agent can load the skill with `skill_view(name='nanogpt-linkedin')` and invoke the CLI or raw API to:

- Scrape a LinkedIn profile and return structured data
- Pull contact info (email, phone) for outreach
- Research companies and industries via employee profiles
- Feed scraped profiles into research workflows

Example agent prompt:

> "Load the nanogpt-linkedin skill and scrape the profiles of the leadership team at Acme Corp."

### How It Works in Hermes

The `SKILL.md` file in the skill directory is a Hermes-native skill definition. When loaded, it makes the tool surface available to the agent — the agent can call the Python CLI, make curl requests, or use the data extraction logic automatically based on your instructions.

The skill is designed to be composable: you can chain it with other skills like `deep-research` (for company research), `obsidian` (for saving contact notes), or `job-search` (for recruiting workflows).
