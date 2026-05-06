#!/usr/bin/env python3
"""
NanoGPT TikTok Scraper — convenience CLI.

Scrape TikTok by hashtag, profile, keyword search, or direct video URLs.

Usage:
  # By hashtag
  ./scrape_tiktok.py --hashtags ai,python --results 20 --comments 3

  # By keyword search
  ./scrape_tiktok.py --search "machine learning tutorial" --min-hearts 1000

  # By profile
  ./scrape_tiktok.py --profiles nba,cnn --results 5

  # By video URLs
  ./scrape_tiktok.py --urls "https://www.tiktok.com/@user/video/123"

  # With transcription (requires --max-charge 0.60+)
  ./scrape_tiktok.py --urls "https://www.tiktok.com/t/ZTkngGoyg/" --transcribe all --max-charge 0.60

  # Fetch subtitle content after scraping
  ./scrape_tiktok.py --urls "https://www.tiktok.com/t/ZTkngGoyg/" --show-transcript

  # Output to file
  ./scrape_tiktok.py --hashtags ai --output results.json
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error

NANOGPT_BASE = "https://nano-gpt.com/api/v1"
ENV_FILE = os.path.expanduser("~/.config/nanogpt/.env")


def load_api_key() -> str:
    """Load NanoGPT API key from env var or ~/.config/nanogpt/.env."""
    key = os.environ.get("NANOGPT_API_KEY")
    if key:
        return key
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NANOGPT_API_KEY="):
                    return line.split("=", 1)[1]
    print("ERROR: NANOGPT_API_KEY not found. Set it as an env var or in ~/.config/nanogpt/.env", file=sys.stderr)
    sys.exit(1)


def build_payload(args: dict) -> dict:
    """Build the request payload from CLI args."""
    payload = {
        "waitForFinishSecs": args.get("wait", 180),
        "resultLimit": args.get("results", 10),
    }

    # Source type handling
    if args.get("hashtags"):
        payload["hashtags"] = [h.strip() for h in args["hashtags"].split(",")]
        payload["resultsPerPage"] = args.get("per_source", 10)
    elif args.get("search"):
        payload["searchQueries"] = [s.strip() for s in args["search"].split(",")]
        payload["resultsPerPage"] = args.get("per_source", 10)
    elif args.get("profiles"):
        payload["profiles"] = [p.strip() for p in args["profiles"].split(",")]
        payload["resultsPerPage"] = args.get("per_source", 10)
    elif args.get("urls"):
        payload["postURLs"] = [u.strip() for u in args["urls"].split(",")]
        payload["resultsPerPage"] = 1  # Videos per URL doesn't apply
        if args.get("related"):
            payload["scrapeRelatedVideos"] = True

    # Optional filters
    if args.get("min_hearts"):
        payload["minHearts"] = int(args["min_hearts"])
    if args.get("max_hearts"):
        payload["maxHearts"] = int(args["max_hearts"])
    if args.get("after"):
        payload["publishedAfter"] = args["after"]
    if args.get("before"):
        payload["publishedBefore"] = args["before"]
    if args.get("comments"):
        payload["commentsPerPost"] = int(args["comments"])
    if args.get("proxy"):
        payload["proxyCountryCode"] = args["proxy"]

    # Downloads
    if args.get("download_videos"):
        payload["downloadVideos"] = True
    if args.get("download_covers"):
        payload["downloadCovers"] = True
    if args.get("download_avatars"):
        payload["downloadAvatars"] = True

    # Subtitles / transcription
    transcribe = args.get("transcribe", "never")
    sub_options = {
        "never": "NEVER_DOWNLOAD_SUBTITLES",
        "download": "DOWNLOAD_SUBTITLES",
        "missing": "DOWNLOAD_AND_TRANSCRIBE_MISSING_SUBTITLES",
        "all": "TRANSCRIBE_ALL_VIDEOS",
    }
    payload["downloadSubtitlesOptions"] = sub_options.get(transcribe, "NEVER_DOWNLOAD_SUBTITLES")

    # Max charge (required when transcription is enabled, min $0.60)
    if args.get("max_charge"):
        payload["maxTotalChargeUsd"] = float(args["max_charge"])
    elif transcribe != "never":
        payload["maxTotalChargeUsd"] = 0.60

    # Additional JSON passthrough
    if args.get("additional"):
        try:
            payload["additionalJson"] = json.loads(args["additional"])
        except json.JSONDecodeError as e:
            print(f"ERROR: --additional must be valid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    return payload


def scrape_tiktok(payload: dict, api_key: str) -> dict:
    """Call the NanoGPT TikTok scraper API and return the response."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{NANOGPT_BASE}/tiktok",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=payload.get("waitForFinishSecs", 180) + 30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        return {"error": f"HTTP {e.code}: {body_text}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def try_fetch_transcript(video: dict) -> dict:
    """Fetch subtitle/transcript content from TikTok's CDN.

    The subtitleLinks[].tiktokLink URL serves WebVTT content even though
    the response headers say video/mp4 — TikTok multiplexes subtitles and
    video through the same CDN endpoint. A byte-range request to this URL
    returns the full VTT file.

    Returns dict of {language: plain_text} for successfully fetched subtitles.
    """
    import re

    meta = video.get("videoMeta", {}) or {}
    subs = meta.get("subtitleLinks", []) or []
    results = {}

    for link in subs:
        lang = link.get("language", "unknown")
        url = link.get("tiktokLink", "") or link.get("downloadLink", "")

        if not url:
            continue

        # Skip plain video URLs that lack subtitle path indicators.
        # The tiktokLink usually works; check it first.
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                if "WEBVTT" in body:
                    lines = body.split("\n")
                    text_lines = []
                    for line in lines:
                        line = line.strip()
                        if (not line or line.startswith("WEBVTT")
                                or re.match(r"^\d{2}:\d{2}", line) or "-->" in line):
                            continue
                        text_lines.append(line)
                    results[lang] = " ".join(text_lines)
                elif len(body) > 20:
                    results[lang] = body
        except Exception:
            pass

    return results


def pretty_print(data: dict, show_transcript: bool = False):
    """Print results in a readable format."""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return

    # API returns items under 'items' key (not 'data')
    videos = data.get("items", data.get("data", []))
    cost = "?"
    usage = data.get("usage", {}) or {}
    if usage:
        cost = f"${usage.get('actualCostUsd', '?')}"

    print(f"🎬 Found {len(videos)} TikTok videos  |  Cost: {cost}\n")

    for i, video in enumerate(videos, 1):
        # Core identifiers
        vid_id = video.get("id", "")
        web_url = video.get("webVideoUrl", "") or video.get("url", "")
        text = video.get("text", "") or video.get("description", "")
        print(f"{'='*65}")
        print(f"  #{i} — {vid_id}")
        print(f"{'='*65}")

        if text:
            print(f"  📝 {text[:300]}")

        # Engagement
        likes = video.get("diggCount", "?")
        views = video.get("playCount", "?")
        comments = video.get("commentCount", "?")
        shares = video.get("shareCount", "?")
        collects = video.get("collectCount", 0)
        print(f"  ❤️ {likes:,}  👁️ {views:,}  💬 {comments:,}  🔄 {shares:,}  📌 {collects:,}")

        # Author
        author = video.get("authorMeta", {}) or video.get("author", {}) or {}
        author_name = author.get("name", "") or "unknown"
        followers = author.get("fans", author.get("followers", "?"))
        print(f"  👤 @{author_name}  ({followers:,} followers)")

        # Hashtags
        hashtags = video.get("hashtags", []) or []
        if hashtags:
            tags = [h.get("name", "") for h in hashtags if isinstance(h, dict)]
            if tags:
                print(f"  #️⃣ {'  '.join(f'#{t}' for t in tags)}")

        # Duration & date
        meta = video.get("videoMeta", {}) or {}
        duration = meta.get("duration", video.get("duration"))
        if duration:
            mins, secs = divmod(int(duration), 60)
            print(f"  ⏱️ {mins}m{secs}s")
        created = video.get("createTimeISO", "") or video.get("createdAt", "")
        if created:
            print(f"  📅 {created}")

        # Music
        music = video.get("musicMeta", {}) or {}
        if music.get("musicName"):
            print(f"  🎵 {music['musicName']}  —  {music.get('musicAuthor', '')}")

        # Location
        loc = video.get("locationCreated", "")
        if loc:
            print(f"  📍 {loc}")

        # Subtitles info
        subs = (meta.get("subtitleLinks", []) or
                video.get("subtitleLinks", []) or [])
        if subs:
            langs = set()
            for s in subs:
                lang = s.get("language", "?")
                src = s.get("source", "")
                langs.add(f"{lang} ({src})")
            print(f"  🎤 Subtitles: {', '.join(langs)}")
            for s in subs:
                dl = s.get("downloadLink", "")
                if dl and "apify" in dl:
                    print(f"     📥 Apify KVS: {dl}")

        # Try fetching transcript content
        if show_transcript:
            tx = try_fetch_transcript(video)
            if tx:
                for lang, content in tx.items():
                    print(f"\n  📝 Transcript ({lang}):")
                    print(f"     {content[:500]}")
                    if len(content) > 500:
                        print(f"     ... ({len(content)} chars total)")
            else:
                # Show the text description as fallback
                if text:
                    print(f"\n  📝 Text caption (available as transcript fallback):")
                    print(f"     {text[:300]}")

        # Comments (if fetched)
        if video.get("commentCount", 0) > 0 and show_transcript:
            pass  # Comments are in a separate dataset URL

        # URL
        if web_url:
            print(f"  🔗 {web_url}")

        print()

    # Usage summary
    if usage and cost != "?":
        events = usage.get("chargedEventCounts", {})
        if events:
            detail = " + ".join(f"{k}={v}" for k, v in events.items() if v)
            print(f"📊 Cost: {cost}  |  {detail}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape TikTok via NanoGPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --hashtags ai,python --results 20
  %(prog)s --search "machine learning" --min-hearts 1000
  %(prog)s --profiles nba --results 10 --comments 5
  %(prog)s --urls "https://www.tiktok.com/@user/video/123"
  %(prog)s --urls "https://www.tiktok.com/t/ZTkngGoyg/" --transcribe all --max-charge 0.60
  %(prog)s --urls "https://www.tiktok.com/t/ZTkngGoyg/" --show-transcript
  %(prog)s --hashtags python --output results.json
        """,
    )

    # Source
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--hashtags", help="Comma-separated hashtags (no #)")
    source.add_argument("--search", help="Comma-separated keyword queries")
    source.add_argument("--profiles", help="Comma-separated profile usernames (no @)")
    source.add_argument("--urls", help="Comma-separated TikTok video URLs (tiktok.com/t/ or /@user/video/)")

    # Video URL options
    parser.add_argument("--related", action="store_true", help="Also scrape related videos (only with --urls)")

    # Pagination
    parser.add_argument("--results", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--per-source", type=int, default=10, help="Videos per source (default: 10)")

    # Filters
    parser.add_argument("--min-hearts", type=int, help="Minimum likes")
    parser.add_argument("--max-hearts", type=int, help="Maximum likes")
    parser.add_argument("--after", help="Published after (ISO date, e.g. 2026-01-01)")
    parser.add_argument("--before", help="Published before (ISO date)")
    parser.add_argument("--comments", type=int, default=0, help="Comments to fetch per post")
    parser.add_argument("--proxy", help="Proxy country code")

    # Media
    parser.add_argument("--download-videos", action="store_true", help="Download video files")
    parser.add_argument("--download-covers", action="store_true", help="Download cover images")
    parser.add_argument("--download-avatars", action="store_true", help="Download avatar images")

    # Transcription
    parser.add_argument("--transcribe", choices=["never", "download", "missing", "all"],
                        default="never",
                        help="Subtitle option (default: never). "
                             "'all' = transcribe all, 'download' = download existing only")
    parser.add_argument("--show-transcript", action="store_true",
                        help="Attempt to fetch and display subtitle content inline")
    parser.add_argument("--max-charge", type=float,
                        help="Max cost in USD (required for transcription, min $0.60 with --transcribe)")

    # Other
    parser.add_argument("--wait", type=int, default=180, help="Max wait seconds (default: 180)")
    parser.add_argument("--additional", help='Additional JSON object for the scraper (e.g. \'{"key":"val"}\')')
    parser.add_argument("--output", "-o", help="Write raw JSON response to file")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON instead of formatted output")

    args = parser.parse_args()

    # Validate at least one source
    if not any([args.hashtags, args.search, args.profiles, args.urls]):
        parser.error("Specify one of --hashtags, --search, --profiles, or --urls")

    api_key = load_api_key()
    payload = build_payload(vars(args))

    mode = "transcribe" if args.transcribe != "never" else "scrape"
    max_charge = payload.get("maxTotalChargeUsd", "default")
    print(f"🔍 {mode.title()} TikTok... (waiting up to {args.wait}s, max charge ${max_charge})")
    data = scrape_tiktok(payload, api_key)

    if "error" in data:
        print(f"\n❌ Error: {data['error']}")
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved raw response to {args.output}")

    if args.raw:
        print(json.dumps(data, indent=2))
    else:
        pretty_print(data, show_transcript=args.show_transcript)


if __name__ == "__main__":
    main()
