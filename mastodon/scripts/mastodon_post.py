#!/usr/bin/env python3
"""Mastodon posting helper for dmv.community.

Posts statuses, threads, media, and polls via the Mastodon API.
Token is read from ~/.hermes/secrets/mastodon_token.

Usage:
  python3 mastodon_post.py --status "Hello world!"
  python3 mastodon_post.py --status "With image" --media /path/to/img.png --alt "Description"
  python3 mastodon_post.py --thread --status "Part 1" --status "Part 2" --status "Part 3"
  python3 mastodon_post.py --status "Poll time" --poll "A" "B" "C" --poll-expires 86400
  python3 mastodon_post.py --status "Test" --dry-run
  python3 mastodon_post.py --status "CW post" --cw "Content warning"
  python3 mastodon_post.py --status "Unlisted" --visibility unlisted
"""

import argparse
import json
import mimetypes
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

INSTANCE = "dmv.community"
API_BASE = f"https://{INSTANCE}/api/v1"
TOKEN_FILE = os.path.expanduser("~/.hermes/secrets/mastodon_token")
MAX_CHARS = 1989
URL_RESERVED = 23


def load_token():
    try:
        return Path(TOKEN_FILE).read_text().strip()
    except FileNotFoundError:
        print(f"ERROR: Token file not found at {TOKEN_FILE}", file=sys.stderr)
        sys.exit(1)


# Browser-like User-Agent – avoids "via Hermes Agent" when the instance
# falls back to User-Agent for client identification.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
)


def api_request(endpoint, method="GET", data=None, fields=None):
    """Make an API request. If fields is provided, uses multipart form data."""
    import uuid
    import mimetypes

    url = f"{API_BASE}/{endpoint}"
    token = load_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
    }

    if fields:
        # Build multipart form data manually
        boundary = uuid.uuid4().hex
        body = b""
        for key, value in fields:
            if isinstance(value, tuple):
                # File upload: (filename, filedata, content_type)
                filename, filedata, content_type = value
                body += f"--{boundary}\r\n".encode()
                body += f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode()
                body += f"Content-Type: {content_type}\r\n\r\n".encode()
                body += filedata + b"\r\n"
            else:
                body += f"--{boundary}\r\n".encode()
                body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
                body += f"{value}\r\n".encode()
        body += f"--{boundary}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    elif data:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        return json.loads(error_body) if error_body else {"error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        print(f"URL Error: {e}", file=sys.stderr)
        return {"error": str(e)}


def count_chars(text):
    """Count characters with URL normalization (URLs = 23 chars)."""
    normalized = re.sub(r'https?://\S+', 'x' * URL_RESERVED, text)
    return len(normalized)


def upload_media(filepath, description=None):
    """Upload a media file and return its ID."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    mime_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    filedata = path.read_bytes()

    fields = [("file", (path.name, filedata, mime_type))]
    if description:
        fields.append(("description", description))

    result = api_request("media", method="POST", fields=fields)
    if "error" in result:
        print(f"Media upload failed: {result.get('error')}", file=sys.stderr)
        sys.exit(1)

    return result["id"]


def post_status(status, visibility="public", sensitive=False, spoiler_text=None,
                language="en", media_ids=None, in_reply_to_id=None,
                poll_options=None, poll_expires=None, poll_multiple=False,
                scheduled_at=None, dry_run=False):
    """Post a single status. Returns the response dict."""
    char_count = count_chars(status)
    if char_count > MAX_CHARS:
        print(f"ERROR: Status is {char_count} chars (max {MAX_CHARS})", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print(f"[DRY RUN] {char_count}/{MAX_CHARS} chars | visibility={visibility}")
        if spoiler_text:
            print(f"  CW: {spoiler_text}")
        if media_ids:
            print(f"  Media: {media_ids}")
        if poll_options:
            print(f"  Poll: {poll_options} (expires in {poll_expires}s)")
        if scheduled_at:
            print(f"  Scheduled: {scheduled_at}")
        if in_reply_to_id:
            print(f"  Reply to: {in_reply_to_id}")
        print(f"  Text: {status}")
        return {"id": "dry-run", "url": "[dry-run]"}

    fields = [
        ("status", status),
        ("visibility", visibility),
        ("sensitive", str(sensitive).lower()),
        ("language", language),
    ]

    if spoiler_text:
        fields.append(("spoiler_text", spoiler_text))
    if media_ids:
        for mid in media_ids:
            fields.append(("media_ids[]", mid))
    if in_reply_to_id:
        fields.append(("in_reply_to_id", in_reply_to_id))
    if poll_options:
        for opt in poll_options:
            fields.append(("poll[options][]", opt))
        fields.append(("poll[expires_in]", str(poll_expires or 86400)))
        fields.append(("poll[multiple]", str(poll_multiple).lower()))
    if scheduled_at:
        fields.append(("scheduled_at", scheduled_at))

    result = api_request("statuses", method="POST", fields=fields)

    if "error" in result:
        print(f"Post failed: {result.get('error')}", file=sys.stderr)
        sys.exit(1)

    return result


def post_thread(statuses, visibility="public", **kwargs):
    """Post a thread (chain of replies). Returns list of responses."""
    responses = []
    prev_id = None

    for i, status in enumerate(statuses, 1):
        print(f"Posting part {i}/{len(statuses)}...")
        result = post_status(status, visibility=visibility, in_reply_to_id=prev_id,
                             dry_run=kwargs.get("dry_run", False))
        responses.append(result)
        if "id" in result and result["id"] != "dry-run":
            prev_id = result["id"]
            print(f"  → {result.get('url', 'posted')}")
        elif result["id"] == "dry-run":
            prev_id = "dry-run"

    return responses


def delete_status(status_id):
    """Delete a status by ID."""
    result = api_request(f"statuses/{status_id}", method="DELETE")
    return result


def main():
    parser = argparse.ArgumentParser(description="Post to Mastodon (dmv.community)")
    parser.add_argument("--status", action="append", dest="statuses",
                        help="Status text (can be repeated for threads)")
    parser.add_argument("--status-file", action="append", dest="status_files",
                        help="Read status text from a UTF-8 file (can be repeated for threads)")
    parser.add_argument("--media", action="append", dest="media_files",
                        help="Media file path (can be repeated, max 4)")
    parser.add_argument("--alt", dest="alt_text",
                        help="Alt text for media (applies to first media)")
    parser.add_argument("--visibility", default="public",
                        choices=["public", "unlisted", "private", "direct"],
                        help="Post visibility (default: public)")
    parser.add_argument("--cw", dest="spoiler_text",
                        help="Content warning text")
    parser.add_argument("--sensitive", action="store_true",
                        help="Mark post as sensitive")
    parser.add_argument("--language", default="en",
                        help="Post language (default: en)")
    parser.add_argument("--poll", nargs="+", dest="poll_options",
                        help="Poll options (max 4, 50 chars each)")
    parser.add_argument("--poll-expires", type=int, default=86400,
                        help="Poll duration in seconds (default: 86400 = 24h)")
    parser.add_argument("--poll-multiple", action="store_true",
                        help="Allow multiple poll selections")
    parser.add_argument("--scheduled-at",
                        help="Schedule post (ISO 8601 UTC, min 5min future)")
    parser.add_argument("--thread", action="store_true",
                        help="Treat multiple --status as a thread")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without posting")
    parser.add_argument("--delete", metavar="STATUS_ID",
                        help="Delete a status by ID")

    args = parser.parse_args()

    statuses = list(args.statuses or [])
    for status_file in args.status_files or []:
        try:
            statuses.append(Path(status_file).read_text(encoding="utf-8").strip())
        except OSError as exc:
            parser.error(f"Cannot read --status-file {status_file}: {exc}")

    if args.delete:
        result = delete_status(args.delete)
        if "error" in result:
            print(f"Delete failed: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(f"Deleted status {args.delete}")
        return

    if not statuses:
        parser.error("At least one --status or --status-file is required (or use --delete)")

    # Upload media if provided
    media_ids = None
    if args.media_files:
        if len(args.media_files) > 4:
            print("ERROR: Max 4 media attachments", file=sys.stderr)
            sys.exit(1)
        media_ids = []
        for i, filepath in enumerate(args.media_files):
            alt = args.alt_text if i == 0 else None
            mid = upload_media(filepath, alt)
            media_ids.append(mid)
            print(f"Uploaded media: {filepath} → {mid}")

    # Single post
    if len(statuses) == 1 and not args.thread:
        result = post_status(
            statuses[0],
            visibility=args.visibility,
            sensitive=args.sensitive,
            spoiler_text=args.spoiler_text,
            language=args.language,
            media_ids=media_ids,
            poll_options=args.poll_options,
            poll_expires=args.poll_expires,
            poll_multiple=args.poll_multiple,
            scheduled_at=args.scheduled_at,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            print(f"Posted: {result.get('url', 'OK')}")
            print(f"ID: {result.get('id', 'N/A')}")
        return

    # Thread
    if args.thread or len(statuses) > 1:
        if media_ids:
            print("WARNING: Media only attaches to first post in thread", file=sys.stderr)
        if args.poll_options:
            print("WARNING: Polls not supported in threads, ignoring", file=sys.stderr)

        responses = post_thread(
            statuses,
            visibility=args.visibility,
            sensitive=args.sensitive,
            spoiler_text=args.spoiler_text,
            language=args.language,
            media_ids=media_ids,
            dry_run=args.dry_run,
        )
        if not args.dry_run and responses:
            print(f"\nThread posted! First post: {responses[0].get('url', 'N/A')}")


if __name__ == "__main__":
    main()
