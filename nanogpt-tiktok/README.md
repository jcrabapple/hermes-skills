# NanoGPT TikTok Scraper

Scrape TikTok hashtags, profiles, keyword searches, and video URLs — with full ASR transcripts — through [NanoGPT](https://nano-gpt.com) billing.

## Features

- **4 source modes**: hashtags, profiles, keyword search, direct video URLs
- **Full transcripts**: extracts ASR (automatic speech recognition) subtitles as clean text via TikTok's CDN — no additional auth needed
- **Engagement metrics**: likes, views, comments, shares, collect counts
- **Rich metadata**: creator info, hashtags, music track, duration, location
- **Comment fetching**: pull comments alongside video data
- **Media downloads**: optionally download videos, covers, and avatars
- **Filters**: date range, min/max hearts, proxy country

## Prerequisites

- A [NanoGPT](https://nano-gpt.com) account with API credits
- Your NanoGPT API key set as the `NANOGPT_API_KEY` environment variable:

```bash
export NANOGPT_API_KEY=sk-nano-your-key-here
```

Or in a `.env` file (the CLI auto-detects it):

```bash
echo 'NANOGPT_API_KEY=sk-nano-your-key-here' >> ~/.config/nanogpt/.env
```

- Python 3.8+ (for the CLI script)
- `curl` (for raw API usage)

## Installation

Clone the repo and make the script executable:

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cd hermes-skills/nanogpt-tiktok
chmod +x scripts/scrape_tiktok.py
```

Or just grab the script directly:

```bash
curl -O https://raw.githubusercontent.com/jcrabapple/hermes-skills/main/nanogpt-tiktok/scripts/scrape_tiktok.py
chmod +x scrape_tiktok.py
```

## Quick Start

```bash
# Scrape a single video by URL (with transcript)
./scripts/scrape_tiktok.py --urls "https://www.tiktok.com/t/ZTkngGoyg/" --show-transcript

# Search by hashtag
./scripts/scrape_tiktok.py --hashtags ai,python --results 20

# Search by keyword
./scripts/scrape_tiktok.py --search "machine learning" --min-hearts 1000 --after 2026-01-01

# Get profile videos
./scripts/scrape_tiktok.py --profiles nba --results 10

# Save raw JSON response
./scripts/scrape_tiktok.py --hashtags ai --output results.json
```

## CLI Reference

```
usage: scrape_tiktok.py [-h] [--hashtags HASHTAGS | --search SEARCH | --profiles PROFILES | --urls URLS]
                        [--related] [--results RESULTS] [--per-source PER_SOURCE] [--min-hearts MIN_HEARTS]
                        [--max-hearts MAX_HEARTS] [--after AFTER] [--before BEFORE] [--comments COMMENTS]
                        [--proxy PROXY] [--download-videos] [--download-covers] [--download-avatars]
                        [--transcribe {never,download,missing,all}] [--show-transcript]
                        [--max-charge MAX_CHARGE] [--wait WAIT] [--output OUTPUT] [--raw]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--hashtags` | — | Comma-separated hashtags to search (no #) |
| `--search` | — | Comma-separated keyword queries |
| `--profiles` | — | Comma-separated profile usernames (no @) |
| `--urls` | — | Comma-separated TikTok video URLs |
| `--related` | false | Also scrape related videos (with `--urls`) |
| `--results` | 10 | Max total results |
| `--per-source` | 10 | Videos per source |
| `--min-hearts` | — | Minimum like count filter |
| `--max-hearts` | — | Maximum like count filter |
| `--after` | — | Only results after ISO date (e.g. 2026-01-01) |
| `--before` | — | Only results before ISO date |
| `--comments` | 0 | Comments to fetch per post |
| `--proxy` | None | Proxy country code |
| `--download-videos` | false | Download video files |
| `--download-covers` | false | Download cover images |
| `--download-avatars` | false | Download author avatars |
| `--transcribe` | never | Subtitle option: never, download, missing, all |
| `--show-transcript` | false | Fetch and display subtitle text inline |
| `--max-charge` | — | Max cost in USD (required with --transcribe, min $0.60) |
| `--wait` | 180 | Max seconds to wait for scraping |
| `--output` / `-o` | — | Save raw JSON response to file |
| `--raw` | false | Print raw JSON instead of formatted output |

## Subtitles & Transcription

The `--transcribe` flag controls subtitle handling:

| Value | Behavior | Cost |
|-------|----------|------|
| `never` | Don't fetch subtitles | Cheapest |
| `download` | Download existing ASR subtitles | Low |
| `missing` | Download existing + transcribe missing | Medium |
| `all` | Transcribe all videos from scratch | Most expensive |

**How transcripts work:** TikTok generates ASR subtitles for videos. The API response includes a URL (`subtitleLinks[].tiktokLink`) that serves the full WebVTT file. The `--show-transcript` flag downloads this, strips timestamps, and returns clean plain text. No additional authentication is needed.

```bash
# Get metadata + full transcript
./scripts/scrape_tiktok.py --urls "https://www.tiktok.com/t/ZTkngGoyg/" --show-transcript
```

The `tiktokLink` URL looks like a video CDN endpoint but actually returns WebVTT subtitle content. Fetch it immediately after scraping as CDN URLs may expire.

## Raw API Usage

If you prefer `curl`:

```bash
curl -s -X POST https://nano-gpt.com/api/v1/tiktok \
  -H "Authorization: Bearer $NANOGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "hashtags": ["ai", "python"],
    "resultsPerPage": 10,
    "downloadSubtitlesOptions": "DOWNLOAD_SUBTITLES",
    "maxTotalChargeUsd": 0.60,
    "waitForFinishSecs": 180
  }' | jq '.'
```

### Extract transcript from raw API response

```bash
curl -s -X POST https://nano-gpt.com/api/v1/tiktok \
  -H "Authorization: Bearer $NANOGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "postURLs": ["https://www.tiktok.com/t/ZTkngGoyg/"],
    "downloadSubtitlesOptions": "DOWNLOAD_SUBTITLES",
    "maxTotalChargeUsd": 0.60,
    "waitForFinishSecs": 60
  }' | python3 -c "
import json,sys,urllib.request
d=json.load(sys.stdin)
sl=d['items'][0]['videoMeta']['subtitleLinks'][0]
vtt=urllib.request.urlopen(sl['tiktokLink']).read().decode()
lines=[l for l in vtt.split('\n') if l.strip() and not l.startswith('WEBVTT') and '-->' not in l and not l[0].isdigit()]
print(' '.join(lines))
"
```

## Pricing

Charged through your NanoGPT account. Per-event pricing:

| Event | Cost |
|-------|------|
| Result (video metadata) | $0.00360 |
| Video download | $0.00120 |
| Comment | $0.00120 |
| Transcription minute | $0.04920 |
| Actor start | $0.00120 |
| Filter/popularity applied | $0.00120 each |

**Estimates:** ~$0.005 for a single video URL scrape. ~$0.60 for 10 hashtag results with no downloads.

## API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hashtags` | string[] | — | Hashtag names (no #) |
| `profiles` | string[] | — | Usernames (no @) |
| `searchQueries` | string[] | — | Search keywords |
| `postURLs` | string[] | — | TikTok video URLs |
| `scrapeRelatedVideos` | boolean | false | Also scrape related (with postURLs) |
| `resultsPerPage` | integer | 10 | Videos per source |
| `resultLimit` | integer | 10 | Max total results |
| `publishedAfter` | string | — | ISO date filter |
| `publishedBefore` | string | — | ISO date filter |
| `minHearts` | integer | — | Minimum like count |
| `maxHearts` | integer | — | Maximum like count |
| `commentsPerPost` | integer | 0 | Comments per video |
| `proxyCountryCode` | string | None | Proxy country code |
| `downloadVideos` | boolean | false | Download video files |
| `downloadCovers` | boolean | false | Download cover images |
| `downloadAvatars` | boolean | false | Download author avatars |
| `downloadSubtitlesOptions` | string | NEVER_DOWNLOAD_SUBTITLES | Subtitle handling |
| `maxTotalChargeUsd` | float | — | Max cost in USD (min $0.60 for transcription) |
| `waitForFinishSecs` | integer | 180 | Max wait time |
| `additionalJson` | object | — | Extra JSON for the scraper |

## Response Format

The API returns:

```
POST /api/v1/tiktok

{
  "object": "tiktok.scrape",
  "actor": "clockworks/tiktok-scraper",
  "status": "SUCCEEDED",
  "items": [ ... ],        // ← video array (key is "items", not "data")
  "usage": {
    "actualCostUsd": 0.0012,
    "chargedEventCounts": { ... }
  }
}
```

Each video item contains:

| Field | Description |
|-------|-------------|
| `id` | TikTok video ID |
| `text` | Video caption/description |
| `webVideoUrl` | Share URL |
| `createTimeISO` | ISO timestamp |
| `diggCount` | Like count |
| `playCount` | View count |
| `commentCount` | Comment count |
| `shareCount` | Share count |
| `collectCount` | Bookmark count |
| `authorMeta` | Creator: name, nickName, fans, signature, avatar |
| `hashtags` | Array of `{id, name, title}` |
| `musicMeta` | Track: musicName, musicAuthor, playUrl |
| `videoMeta` | Duration, resolution, coverUrl, subtitleLinks |
| `locationCreated` | Country code |
| `submittedVideoUrl` | The URL that was submitted |

## Full API Documentation

See NanoGPT's official documentation:
- [TikTok Scraper Application](https://nano-gpt.com/applications/tiktok)
- [Pricing & API](https://nano-gpt.com/api/v1/tiktok)

## License

MIT
