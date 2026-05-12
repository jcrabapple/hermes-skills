---
name: nanogpt-instagram
description: Scrape Instagram profile posts or exact post URLs with captions, metrics, media, comments, tags, and metadata through NanoGPT's API. Uses your existing NanoGPT API key.
---

# NanoGPT Instagram Post Scraper

Scrape Instagram posts via NanoGPT's managed Instagram scraper (`POST /api/v1/instagram/posts`). Supports scraping by username/profile URL or direct post URLs.

## Prerequisites

- NanoGPT API key in `~/.config/nanogpt/.env` (`NANOGPT_API_KEY=sk-nano-...`) or `NANOGPT_API_KEY` env var
- `curl` or `requests` Python library

## API Endpoint

```
POST https://nano-gpt.com/api/v1/instagram/posts
Authorization: Bearer $NANOGPT_API_KEY
Content-Type: application/json
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `usernames` | string[] | — | Instagram usernames, profile URLs, or post URLs to scrape |
| `postsPerProfile` | integer | 10 | How many posts to fetch per profile |
| `dataDetailLevel` | string | `"detailedData"` | One of: `"basicData"`, `"detailedData"` |
| `onlyNewerThan` | string | — | ISO date string — skip posts older than this |
| `maxCharge` | float | — | Max cost in USD for this run |
| `skipPinnedPosts` | boolean | false | Exclude pinned/highlighted posts |
| `waitForFinishSecs` | integer | 180 | How long to wait for scraping to complete |
| `resultLimit` | integer | 5000 | Max total results to return |
| `additionalJson` | object | — | Extra JSON fields passed through to the underlying scraper |

## Usage Examples

### Scrape a profile's recent posts
```bash
curl -s -X POST https://nano-gpt.com/api/v1/instagram/posts \
  -H "Authorization: Bearer $NANOGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["nasa", "natgeo"],
    "postsPerProfile": 10,
    "dataDetailLevel": "detailedData",
    "skipPinnedPosts": true,
    "waitForFinishSecs": 180
  }' | jq '.'
```

### Scrape specific post URLs
```bash
curl -s -X POST https://nano-gpt.com/api/v1/instagram/posts \
  -H "Authorization: Bearer $NANOGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["https://www.instagram.com/p/ABC123/"],
    "dataDetailLevel": "detailedData",
    "waitForFinishSecs": 60
  }' | jq '.'
```

### Basic data only (cheaper, faster)
```bash
curl -s -X POST https://nano-gpt.com/api/v1/instagram/posts \
  -H "Authorization: Bearer $NANOGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["nasa"],
    "postsPerProfile": 20,
    "dataDetailLevel": "basicData",
    "waitForFinishSecs": 120,
    "resultLimit": 20
  }' | jq '.'
```

### Fresh posts only (with date filter)
```bash
curl -s -X POST https://nano-gpt.com/api/v1/instagram/posts \
  -H "Authorization: Bearer $NANOGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["spacex"],
    "postsPerProfile": 50,
    "dataDetailLevel": "detailedData",
    "onlyNewerThan": "2026-05-01",
    "skipPinnedPosts": true,
    "waitForFinishSecs": 180
  }' | jq '.'
```

## Python Integration

```python
import os, json, urllib.request

# Load NanoGPT API key
nanogpt_key = os.environ.get("NANOGPT_API_KEY")
if not nanogpt_key:
    with open(os.path.expanduser("~/.config/nanogpt/.env")) as f:
        for line in f:
            if line.startswith("NANOGPT_API_KEY="):
                nanogpt_key = line.strip().split("=", 1)[1]
                break

payload = json.dumps({
    "usernames": ["nasa"],
    "postsPerProfile": 10,
    "dataDetailLevel": "detailedData",
    "waitForFinishSecs": 180,
}).encode()

req = urllib.request.Request(
    "https://nano-gpt.com/api/v1/instagram/posts",
    data=payload,
    headers={
        "Authorization": f"Bearer {nanogpt_key}",
        "Content-Type": "application/json",
    }
)

with urllib.request.urlopen(req, timeout=300) as resp:
    data = json.loads(resp.read().decode())
    print(json.dumps(data, indent=2))
```

## Pricing

Charged through NanoGPT billing. Per-event pricing:
- Post scraped: $0.00187
- Post details (detailed mode): $0.00110

Estimate: ~$0.03 for a basic profile scrape with 10 posts, ~$0.06 for detailed mode.

## Response Format (Detailed)

Returns a JSON object with:
- `object`: `"instagram.posts.scraper"`
- `actor`: `"apify/instagram-post-scraper"`
- `data`: Array of post objects containing:
  - `id` — Post ID
  - `url` — Post permalink
  - `caption` — Post caption text
  - `hashtags` — Extracted hashtags
  - `mentions` — @mentioned usernames
  - `commentsCount` — Number of comments
  - `likesCount` — Number of likes
  - `timestamp` — ISO date string
  - `ownerUsername` — Poster's username
  - `ownerFullName` — Poster's display name
  - `imageUrls` — Array of image URLs (for carousels)
  - `videoUrl` — Video URL (if video post)
  - `isVideo` — Boolean
  - `locationName` — Location tag (if any)
  - `comments` — Array of comment objects (when detail level allows)

## Pitfalls

- Instagram may rate-limit or require login for heavy scraping — results depend on current Instagram anti-bot measures
- Detailed mode costs more per post but gives you comments, full captions, and richer metadata
- The underlying actor is Apify's Instagram Post Scraper — some fields depend on Instagram's current DOM structure
- For username-only input, don't include the `@` symbol
- `waitForFinishSecs` may need to be higher for profiles with many posts (>50)
- The API key lives at `~/.config/nanogpt/.env` — source it with `export $(grep NANOGPT_API_KEY ~/.config/nanogpt/.env | xargs)` before running curl commands
- Basic data mode is much faster/cheaper if you just need captions, metrics, and media URLs without comments
