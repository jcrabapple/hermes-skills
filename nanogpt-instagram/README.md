# NanoGPT Instagram Scraper

Scrape Instagram posts — captions, likes, comments, media URLs, hashtags, mentions, and more — through [NanoGPT](https://nano-gpt.com) billing.

## Features

- **Profile scraping**: fetch recent posts from any public Instagram profile
- **Direct post URLs**: scrape specific posts by permalink
- **Two detail modes**: basic (cheap, fast) or detailed (comments, full metadata)
- **Date filtering**: only fetch posts newer than a given date
- **Rich metadata**: captions, hashtags, mentions, likes, comments, location, media URLs
- **Video support**: detects video posts and returns video URLs

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

## Installation

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cd hermes-skills/nanogpt-instagram
chmod +x scripts/scrape_instagram.py
```

Or grab the script directly:

```bash
curl -O https://raw.githubusercontent.com/jcrabapple/hermes-skills/main/nanogpt-instagram/scripts/scrape_instagram.py
chmod +x scrape_instagram.py
```

## Quick Start

```bash
# Scrape a profile's recent posts (detailed mode)
./scripts/scrape_instagram.py --profiles nasa,natgeo --posts 10

# Scrape specific post URLs
./scripts/scrape_instagram.py --urls "https://www.instagram.com/p/ABC123/"

# Basic mode — cheaper, faster, no comments
./scripts/scrape_instagram.py --profiles spacex --basic

# Only posts from the last month
./scripts/scrape_instagram.py --profiles nasa --after 2026-05-01 --skip-pinned

# Save raw JSON
./scripts/scrape_instagram.py --profiles nasa --output posts.json
```

## CLI Reference

```
usage: scrape_instagram.py [-h] (--profiles PROFILES | --urls URLS)
                           [--posts POSTS] [--results RESULTS] [--basic]
                           [--after AFTER] [--skip-pinned] [--wait WAIT]
                           [--max-charge MAX_CHARGE] [--additional ADDITIONAL]
                           [--output OUTPUT] [--raw]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--profiles` | — | Comma-separated usernames or profile URLs |
| `--urls` | — | Comma-separated Instagram post URLs |
| `--posts` | 10 | Posts per profile |
| `--results` | 5000 | Max total results |
| `--basic` | false | Use basic data mode (cheaper, no comments) |
| `--after` | — | Only posts newer than ISO date |
| `--skip-pinned` | false | Exclude pinned/highlighted posts |
| `--wait` | 180 | Max seconds to wait |
| `--max-charge` | — | Max cost in USD |
| `--output` / `-o` | — | Save raw JSON to file |
| `--raw` | false | Print raw JSON instead of formatted output |

## Raw API Usage

```bash
# Detailed profile scrape
curl -s -X POST https://nano-gpt.com/api/v1/instagram/posts \
  -H "Authorization: Bearer sk-nan...here" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["nasa", "natgeo"],
    "postsPerProfile": 10,
    "dataDetailLevel": "detailedData",
    "skipPinnedPosts": true,
    "waitForFinishSecs": 180
  }' | jq '.data | length'
```

## Pricing

| Mode | Cost per post |
|------|--------------|
| Basic | ~$0.002 |
| Detailed | ~$0.003 |

Estimate: ~$0.03 for 10 posts (basic), ~$0.06 for 10 posts (detailed).

## API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `usernames` | string[] | **required** | Usernames, profile URLs, or post URLs |
| `postsPerProfile` | integer | 10 | Posts per profile |
| `dataDetailLevel` | string | `detailedData` | `basicData` or `detailedData` |
| `onlyNewerThan` | string | — | ISO date filter |
| `skipPinnedPosts` | boolean | false | Exclude pinned posts |
| `maxCharge` | float | — | Max cost in USD |
| `waitForFinishSecs` | integer | 180 | Max wait time |
| `resultLimit` | integer | 5000 | Max total results |

## Response Format

Each post item contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Post ID |
| `url` | string | Post permalink |
| `caption` | string | Full caption text |
| `hashtags` | string[] | Extracted hashtags |
| `mentions` | string[] | @mentioned usernames |
| `likesCount` | integer | Like count |
| `commentsCount` | integer | Comment count |
| `timestamp` | string | ISO date |
| `ownerUsername` | string | Poster's username |
| `ownerFullName` | string | Poster's display name |
| `imageUrls` | string[] | Image URLs (carousels have multiple) |
| `videoUrl` | string | Video URL (if video post) |
| `isVideo` | boolean | Whether it's a video |
| `locationName` | string | Location tag |

## Pitfalls

- Don't include `@` in usernames
- Detailed mode costs more but gives comments and richer metadata
- Some fields depend on Instagram's current DOM structure (Apify actor)
- Heavy scraping may trigger Instagram rate limits
- Increase `waitForFinishSecs` for profiles with many posts
- Basic mode is much faster/cheaper if you just need captions and metrics

## License

MIT

## Using with Hermes Agent

```bash
# Install
git clone https://github.com/jcrabapple/hermes-skills.git /tmp/hermes-skills
cp -r /tmp/hermes-skills/nanogpt-instagram ~/.hermes/skills/social-media/nanogpt-instagram
rm -rf /tmp/hermes-skills

# Set API key
echo 'NANOGPT_API_KEY=sk-nan...here' >> ~/.hermes/.env
```

Once installed, Hermes loads the skill automatically when Instagram scraping is needed. Example prompt:

> "Load the nanogpt-instagram skill and scrape the last 10 posts from @nasa."
