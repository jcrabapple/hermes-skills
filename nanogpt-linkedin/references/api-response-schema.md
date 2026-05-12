# LinkedIn Profile Scraper — API Response Schema

## Endpoint

```
POST https://nano-gpt.com/api/v1/linkedin/profile
Authorization: Bearer $NANOGPT_API_KEY
Content-Type: application/json
```

## Request Body

```json
{
  "profileUrls": ["https://www.linkedin.com/in/username"],
  "maxTotalChargeUsd": 0.05,
  "resultLimit": 5,
  "waitForFinishSecs": 180
}
```

**Required:** `profileUrls` (array of LinkedIn profile URLs)
**Optional:** `maxTotalChargeUsd`, `resultLimit`, `waitForFinishSecs`

No `startUrls` — only `profileUrls` is accepted.

## Response Structure

```json
{
  "object": "linkedin.profile.scrape",
  "actor": "unlimitedleadtestinbox/linkedin-profile-scraper-with-email-no-cookies",
  "name": "LinkedIn Profile Scraper",
  "model": "linkedin-profile-scraper",
  "status": "SUCCEEDED",
  "runId": "rA1dzZrsVnQi7oJoX",
  "defaultDatasetId": "xOMsgD0VRBiuWvMqy",
  "items": [ ... ],
  "usage": { ... },
  "metadata": { ... }
}
```

## Profile Item Fields

| Field | Type | Example |
|-------|------|---------|
| `name` | string | `"Elon Musk"` |
| `jobTitle` | string | `"Investor, entrepreneur, and CEO"` |
| `company` | string | `"Not specified"` (when unavailable) |
| `location` | string | `"Not specified"` (when unavailable) |
| `industry` | string | `"Venture capital & private equity"` |
| `headline` | string | `"Investor, entrepreneur, and CEO focused on..."` |
| `education` | string | `"Not specified"` (when unavailable) |
| `email` | string\|null | `null` (when unavailable) |
| `phone` | string\|null | `null` (when unavailable) |
| `website` | string | `""` (empty when unavailable) |
| `linkedinUrl` | string | `"https://www.linkedin.com/in/elonmusk"` |
| `verified` | string | `"true"` (string, not boolean) |
| `scrapedAt` | string | `"2026-05-12T19:58:29.527Z"` |
| `source` | string | `"unlimited-leads-linkedin"` |
| `leadId` | string | `"linkedin_1778615909527_2"` |
| `profileIndex` | integer | `2` |
| `dataQuality` | string | `"professional"` |

## Usage / Billing Object

```json
{
  "chargedEventCounts": { "apify-default-dataset-item": 1 },
  "eventPricesUsd": { "apify-default-dataset-item": 0.010267 },
  "preflightEventPricesUsd": { "apify-default-dataset-item": 0.011 },
  "estimatedMaxChargeUsd": 0.05,
  "actualCostUsd": 0.010266,
  "uncappedActualCostUsd": 0.010266,
  "chargedAmount": 0.010266,
  "paymentSource": "USD",
  "exceededPreflightEstimate": false
}
```

## Metadata Object

```json
{
  "estimatedProfiles": 2,
  "isEstimateBounded": true,
  "resultLimit": 2,
  "resultOffset": 0
}
```

## Tested Behaviors

- **Bill Gates** (`williamhgates`): Returned empty `items[]`, cost $0 — very locked-down profile
- **Satya Nadella** (`satyanadella`): Returned empty `items[]`, cost $0 — also locked down
- **Elon Musk** (`elonmusk`): Returned 1 item with full data, cost $0.010266
- **Jeff Weiner** (`jeffweiner08`): Returned empty `items[]`, cost $0

Locked-down profiles return empty items but still incur the Apify actor start cost (~$0.001). The $0 actual cost for empty results suggests NanoGPT may not charge when 0 items are returned, but the preflight estimate still applies.

## Error Response

```json
{
  "error": {
    "message": "Provide at least one LinkedIn profile URL.",
    "code": "invalid_request"
  }
}
```

HTTP 400 when `profileUrls` is missing or empty. HTTP 404 for non-existent endpoints (`/api/v1/linkedin/posts`, `/api/v1/linkedin/search` — only `/profile` exists).
