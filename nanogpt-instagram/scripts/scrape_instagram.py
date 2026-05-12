#!/usr/bin/env python3
"""
NanoGPT Instagram Post Scraper — convenience CLI.

Scrape Instagram profile posts or exact post URLs.

Usage:
  # Scrape profiles (detailed)
  ./scrape_instagram.py --profiles nasa,natgeo --posts 10

  # Scrape specific posts by URL
  ./scrape_instagram.py --urls "https://www.instagram.com/p/ABC123/"

  # Basic mode (cheaper, faster)
  ./scrape_instagram.py --profiles spacex --basic

  # Fresh posts only
  ./scrape_instagram.py --profiles nasa --after 2026-05-01 --skip-pinned

  # Output to file
  ./scrape_instagram.py --profiles nasa --output posts.json
"""

import json
import os
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
        "dataDetailLevel": "basicData" if args.get("basic") else "detailedData",
        "waitForFinishSecs": args.get("wait", 180),
        "resultLimit": args.get("results", 5000),
    }

    if args.get("profiles"):
        payload["usernames"] = [p.strip() for p in args["profiles"].split(",")]
    elif args.get("urls"):
        payload["usernames"] = [u.strip() for u in args["urls"].split(",")]

    payload["postsPerProfile"] = args.get("posts", 10)

    if args.get("after"):
        payload["onlyNewerThan"] = args["after"]
    if args.get("skip_pinned"):
        payload["skipPinnedPosts"] = True
    if args.get("max_charge"):
        payload["maxCharge"] = float(args["max_charge"])

    if args.get("additional"):
        try:
            payload["additionalJson"] = json.loads(args["additional"])
        except json.JSONDecodeError as e:
            print(f"ERROR: --additional must be valid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    return payload


def scrape_instagram(payload: dict, api_key: str) -> dict:
    """Call the NanoGPT Instagram scraper API and return the response."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{NANOGPT_BASE}/instagram/posts",
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


def pretty_print(data: dict):
    """Print results in a readable format."""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return

    posts = data.get("data", [])
    print(f"📸 Found {len(posts)} Instagram posts\n")

    for i, post in enumerate(posts, 1):
        print(f"{'='*60}")
        print(f"  #{i} — {post.get('url', 'No URL')}")
        print(f"{'='*60}")

        caption = post.get("caption", "") or ""
        if caption:
            print(f"  📝 Caption: {caption[:300]}")

        print(f"  ❤️ {post.get('likesCount', '?')}  💬 {post.get('commentsCount', '?')}")

        owner = post.get("ownerUsername", "")
        name = post.get("ownerFullName", "")
        if owner:
            print(f"  👤 @{owner}" + (f" ({name})" if name else ""))

        hashtags = post.get("hashtags", []) or []
        if hashtags:
            print(f"  #️⃣ {'  '.join(f'#{t}' for t in hashtags[:10])}")

        mentions = post.get("mentions", []) or []
        if mentions:
            print(f"  @️ {'  '.join(f'@{m}' for m in mentions[:5])}")

        ts = post.get("timestamp", "")
        if ts:
            print(f"  📅 {ts}")

        location = post.get("locationName", "")
        if location:
            print(f"  📍 {location}")

        is_video = post.get("isVideo", False)
        media_count = len(post.get("imageUrls", []) or [])
        media_info = "🎬 Video" if is_video else f"🖼️ {media_count} images" if media_count > 1 else "🖼️ 1 image"
        print(f"  {media_info}")

        print()

    usage = data.get("usage", {}) or {}
    if usage:
        print(f"📊 Cost: ${usage.get('totalCostUsd', '?')}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape Instagram posts via NanoGPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --profiles nasa,natgeo --posts 10
  %(prog)s --urls "https://www.instagram.com/p/ABC123/"
  %(prog)s --profiles spacex --basic
  %(prog)s --profiles nasa --after 2026-05-01 --skip-pinned
  %(prog)s --profiles nasa --output posts.json
        """,
    )

    # Source
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--profiles", help="Comma-separated Instagram usernames or profile URLs")
    source.add_argument("--urls", help="Comma-separated Instagram post URLs")

    # Options
    parser.add_argument("--posts", type=int, default=10, help="Posts per profile (default: 10)")
    parser.add_argument("--results", type=int, default=5000, help="Max total results (default: 5000)")
    parser.add_argument("--basic", action="store_true", help="Use basic data mode (cheaper, no comments/details)")
    parser.add_argument("--after", help="Only posts newer than ISO date (e.g. 2026-05-01)")
    parser.add_argument("--skip-pinned", action="store_true", help="Exclude pinned posts")
    parser.add_argument("--wait", type=int, default=180, help="Max wait seconds (default: 180)")
    parser.add_argument("--max-charge", type=float, help="Max cost in USD")
    parser.add_argument("--additional", help='Additional JSON for the scraper (e.g. \'{"key":"val"}\')')
    parser.add_argument("--output", "-o", help="Write raw JSON response to file")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON instead of formatted output")

    args = parser.parse_args()

    api_key = load_api_key()
    payload = build_payload(vars(args))

    detail = "basic" if args.basic else "detailed"
    print(f"🔍 Scraping Instagram ({detail} mode)... (waiting up to {args.wait}s)")
    data = scrape_instagram(payload, api_key)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved raw response to {args.output}")

    if args.raw:
        print(json.dumps(data, indent=2))
    else:
        pretty_print(data)


if __name__ == "__main__":
    main()
