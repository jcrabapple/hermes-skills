# tiktokLink VTT Discovery

The NanoGPT TikTok scraper's response includes `subtitleLinks[]`, each containing two URLs:
- `downloadLink` — Apify KVS URL (requires Apify API auth)
- `tiktokLink` — TikTok CDN URL (works without auth, returns WebVTT)

## The Trick

The `tiktokLink` URL looks like a TikTok video CDN endpoint:
```
https://v16m-webapp.tiktokcdn-us.com/<hash>/video/tos/useast8/...?mime_type=video_mp4&...
```

The `Content-Type` response header says `video/mp4`, and `file` command identifies it as "WebVTT subtitles, ASCII text."

**What's happening:** TikTok multiplexes video and subtitle tracks through the same CDN infrastructure using fragmented MP4. A GET request to the video URL returns the VTT subtitle data, not the video stream. The subtitle content is accessible because TikTok serves the subtitle track as a separate byte-range-accessible resource within the same file structure.

This is specific to TikTok's CDN implementation and may change without notice.

## Why It Matters

- **No additional auth needed** — unlike the Apify KVS URL, this works with a simple GET request
- **Free** — no NanoGPT billing for fetching the VTT (only the initial scrape costs)
- **Fast** — CDN hosted, typically responds in <1s
- **Full WebVTT** — includes timestamps, speaker diarization if present, and complete ASR output

## How to Use

```python
import urllib.request, re, json

# After getting the API response:
vtt_url = data["items"][0]["videoMeta"]["subtitleLinks"][0]["tiktokLink"]
vtt = urllib.request.urlopen(vtt_url).read().decode("utf-8")

# Parse VTT to plain text
lines = vtt.split("\n")
text_lines = []
for line in lines:
    line = line.strip()
    if not line or line.startswith("WEBVTT") or re.match(r"^\d{2}:\d{2}", line) or "-->" in line:
        continue
    text_lines.append(line)
transcript = " ".join(text_lines)
```

## Caveats

- **URLs may expire** — TikTok CDN URLs are typically valid for hours to days. Fetch immediately after scraping
- **Not all videos have ASR** — older videos, music-only content, or very short clips may lack subtitles. Fall back to the `text` (caption) field
- **Content-Type lies** — the header says `video/mp4` but the body is VTT. Don't filter by Content-Type
- **TikTok may change this** — this is an implementation detail of their CDN, not a documented API
