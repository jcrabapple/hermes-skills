---
name: nanogpt-tiktok
description: Scrape TikTok hashtags, profiles, searches, video URLs, comments, and media metadata through NanoGPT's API. Supports full ASR transcript extraction. Use when the user shares a TikTok link or asks about TikTok content.
version: 1.0.0
author: Jason Crabtree
license: MIT
metadata:
  hermes:
    tags: [tiktok, social-media, scraping, nlp, transcript]
    related_skills: [deep-research, obsidian, pico-sh]
---

# NanoGPT TikTok Scraper

Scrape TikTok content via NanoGPT's managed TikTok scraper (`POST /api/v1/tiktok`). Supports four source modes: hashtags, profiles, keyword search, and direct video URLs.

## When to Use

- User shares a TikTok URL and wants you to understand its contents
- User asks for TikTok trend research by hashtag or keyword
- User wants engagement metrics, creator info, or comments from a TikTok video
- User needs a full transcript of a TikTok's spoken content
- User wants to research topics mentioned in a TikTok video

**Don't use for:** Scraping other platforms (use platform-specific tools), bypassing TikTok's ToS, or downloading copyrighted content without permission.

## Prerequisites

- `NANOGPT_API_KEY` env var set in `~/.hermes/.env` or loaded from `~/.config/nanogpt/.env`
- Python 3.8+ (for the CLI script)

## Overview

This skill wraps NanoGPT's TikTok scraping API endpoint. It handles API key loading, payload construction, and parsing of the response. The key feature is **ASR transcript extraction** — the API returns subtitle links from TikTok's CDN that serve full WebVTT files, which this skill parses into clean text.

### Quick Usage (CLI)

```bash
# Scrape a video URL with transcript
cd ~/.hermes/skills/social-media/nanogpt-tiktok
python3 scripts/scrape_tiktok.py --urls "https://www.tiktok.com/t/ZTkngGoyg/" --show-transcript

# Search by hashtag
python3 scripts/scrape_tiktok.py --hashtags ai,python --results 20 --comments 3

# Save raw response
python3 scripts/scrape_tiktok.py --hashtags ai --output /tmp/tiktok_data.json
```

### Agent Usage (within Hermes)

When a user gives you a TikTok URL, load this skill and run:

```python
import subprocess, json

result = subprocess.run([
    "python3",
    os.path.expanduser("~/.hermes/skills/social-media/nanogpt-tiktok/scripts/scrape_tiktok.py"),
    "--urls", tiktok_url,
    "--show-transcript",
    "--raw"
], capture_output=True, text=True, timeout=180)

data = json.loads(result.stdout)
```

Then extract the transcript and metadata from the response for further processing.

## Workflow: TikTok URL → Research

When a user shares a TikTok link:

1. **Scrape** the URL with `postURLs` and `DOWNLOAD_SUBTITLES`
2. **Extract transcript** from `items[0].videoMeta.subtitleLinks[0].tiktokLink` (fetches and parses WebVTT)
3. **Read** the `text` field for the caption/description
4. **Analyze** the content — identify claims, topics, people, and questions raised
5. **Research** using `deep-research`, `web_search`, or other skills
6. **Save** to Obsidian or blog if the user requests it

### Transcript Extraction

The `subtitleLinks[].tiktokLink` URL in the API response serves full WebVTT content even though the Content-Type header says `video/mp4`. Fetch it and parse:

```python
import urllib.request, re

vtt_url = data["items"][0]["videoMeta"]["subtitleLinks"][0]["tiktokLink"]
response = urllib.request.urlopen(vtt_url)
vtt_text = response.read().decode("utf-8")

lines = vtt_text.split("\n")
text_lines = []
for line in lines:
    line = line.strip()
    if not line or line.startswith("WEBVTT") or re.match(r"^\d{2}:\d{2}", line) or "-->" in line:
        continue
    text_lines.append(line)
transcript = " ".join(text_lines)
```

## CLI Reference

### Source Modes

| Flag | Description |
|------|-------------|
| `--hashtags` | Comma-separated hashtag names (no #) |
| `--search` | Comma-separated keyword queries |
| `--profiles` | Comma-separated usernames (no @) |
| `--urls` | Comma-separated TikTok video URLs |

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--related` | false | Also scrape related videos (with --urls) |
| `--results` | 10 | Max total results |
| `--per-source` | 10 | Videos per source |
| `--min-hearts` | — | Minimum like count filter |
| `--max-hearts` | — | Maximum like count filter |
| `--after` | — | Only results after ISO date |
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

## Pricing

Charged through NanoGPT billing. Per-event pricing:

| Event | Cost |
|-------|------|
| Result (video metadata) | $0.00360 |
| Video download | $0.00120 |
| Comment | $0.00120 |
| Transcription minute | $0.04920 |
| Actor start | $0.00120 |

**Estimates:** ~$0.005 for a single video URL scrape. ~$0.60 for 10 hashtag results.

## Common Pitfalls

1. **`tiktokLink` URL looks like video but returns VTT** — Don't skip it because of the URL or Content-Type header. The URL serves WebVTT subtitles. Fetch it and parse.

2. **CDN URLs may expire** — Fetch the VTT from `tiktokLink` immediately after scraping. Don't store the URL for later use.

3. **`maxTotalChargeUsd` required for transcription** — When using `--transcribe all` or `--transcribe missing`, you must set `--max-charge` to at least `0.60`. Without it, the API returns an error.

4. **Response uses `items` key, not `data`** — The API returns `{"items": [...]}`, NOT `{"data": [...]}`. Access items via `response["items"]`.

5. **Apify KVS URL requires auth** — The `subtitleLinks[].downloadLink` goes to Apify's key-value store and requires Apify API auth (NanoGPT's internal account). Use `tiktokLink` instead.

6. **Always set `waitForFinishSecs` appropriately** — Scraping runs on NanoGPT's infrastructure. For large result sets (50+ videos) or media downloads, allow 300+ seconds.

7. **Comments are in a separate dataset** — The `commentsDatasetUrl` in the response links to an Apify dataset. When you request comments, they aren't in the main response body.

8. **Rate limiting** — Results may be limited by TikTok's anti-scraping measures and your NanoGPT account balance.

## Related Skills

- `deep-research` — Fact-check claims found in TikTok videos
- `obsidian` — Save TikTok research to your knowledge base
- `pico-sh` — Publish blog posts about TikTok research
- `weekly-blog` — Incorporate TikTok trends into weekly content
