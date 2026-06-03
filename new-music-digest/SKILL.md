---
name: new-music-digest
description: >
  Build a weekly new releases digest for the user's favorite artists using
  Last.fm (top artists), MusicBrainz (release dates), and Deezer (album art,
  genres, popularity). Triggers on: new music digest, weekly music releases,
  music release report, album release radar.
---

# New Music Digest

Build a weekly new releases report from the user's Last.fm top artists, cross-referenced with MusicBrainz release dates and Deezer metadata.

## Data Sources

| Source | Purpose | Auth |
|--------|---------|------|
| Last.fm | Top artists from listening history | API key |
| MusicBrainz | Release dates, album types | None (User-Agent only) |
| Deezer | Cover art, genres, fan counts | None |

## Required Environment Variables

Set these before running (e.g. in `~/.hermes/.env`):

```bash
LASTFM_API_KEY=...           # https://www.last.fm/api/account/create
LASTFM_USERNAME=...          # your Last.fm username
AGENTMAIL_API_KEY=...        # https://agentmail.to
AGENTMAIL_INBOX=...          # sender address, e.g. you@agentmail.to
DIGEST_RECIPIENT=...         # where to send the digest, e.g. you@example.com
```

## Workflow

### Step 1 — Get top artists from Last.fm

```python
import os, requests

LASTFM_KEY = os.environ["LASTFM_API_KEY"]
BASE_URL = "https://ws.audioscrobbler.com/2.0/"
USERNAME = os.environ["LASTFM_USERNAME"]

def get_top_artists(period, limit=25):
    params = {
        "method": "user.gettopartists",
        "user": USERNAME,
        "api_key": LASTFM_KEY,
        "period": period,
        "limit": limit,
        "format": "json"
    }
    r = requests.get(BASE_URL, params=params)
    return r.json().get("topartists", {}).get("artist", [])

one_month = get_top_artists("1month", 25)
three_month = get_top_artists("3month", 25)
seen, artists = set(), []
for a in one_month + three_month:
    if a["name"] not in seen:
        seen.add(a["name"])
        artists.append(a["name"])
```

### Step 2 — Fetch releases from MusicBrainz

MusicBrainz has reliable `first-release-date` data. Last.fm's `artist.getnewreleases` **does not work** — do not use it.

```python
import time, requests
from datetime import datetime, timedelta

MB_BASE = "https://musicbrainz.org/ws/2/"
# MusicBrainz requires a descriptive User-Agent (their policy).
# Use something like "NewMusicDigest/1.0 (your-email@example.com)"
HEADERS = {"User-Agent": "NewMusicDigest/1.0 (contact@example.com)"}
now = datetime.now()

def parse_date(d):
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(d.strip(), fmt)
        except:
            pass
    return None

def get_mb_releases(artist_name):
    # Search for artist MBID
    resp = requests.get(f"{MB_BASE}artist/",
        params={"query": f'artist:"{artist_name}"', "fmt": "json", "limit": 1},
        headers=HEADERS, timeout=10)
    artists = resp.json().get("artists", [])
    if not artists:
        return [], []
    mbid = artists[0]["id"]
    time.sleep(0.35)  # MusicBrainz: 1 req/sec limit

    # Fetch all release groups (paginated)
    all_rgs, offset = [], 0
    while True:
        resp = requests.get(f"{MB_BASE}release-group",
            params={"artist": mbid, "fmt": "json", "limit": 100, "offset": offset,
                    "type": "album|ep|single|compilation"},
            headers=HEADERS, timeout=10)
        d = resp.json()
        rgs = d.get("release-groups", [])
        if not rgs:
            break
        all_rgs.extend(rgs)
        offset += len(rgs)
        if offset >= d.get("release-group-count", 0):
            break

    out, coming = [], []
    for rg in all_rgs:
        first_rel = rg.get("first-release-date")
        if not first_rel:
            continue
        rel_date = parse_date(first_rel)
        if not rel_date:
            continue
        item = {
            "artist": artist_name,
            "album": rg.get("title", ""),
            "date": first_rel,
            "type": rg.get("primary-type", ""),
            "mbid": rg.get("id", "")
        }
        if now - timedelta(days=30) <= rel_date <= now and item["type"] == "album":
            out.append(item)
        elif now < rel_date <= now + timedelta(days=90) and item["type"] == "album":
            coming.append(item)
    return out, coming

all_out, all_coming = [], []
lookup_count = 0
for i, artist in enumerate(artists):
    out, coming = get_mb_releases(artist)
    all_out.extend(out)
    all_coming.extend(coming)
    lookup_count += 1
    if (i+1) % 10 == 0:
        print(f"  Processed {i+1}/{len(artists)} artists...")
    time.sleep(0.1)
```

### Step 3 — Deduplicate and filter

```python
def dedup(releases):
    seen, result = set(), []
    for item in sorted(releases, key=lambda x: x["date"], reverse=True):
        key = f"{item['artist']}|{item['album'].lower()}"
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

out_now = dedup(all_out)[:12]
coming_soon = dedup(all_coming)[:10]
```

### Step 4 — Enrich with Deezer

Deezer has no rate limit on public endpoints. Try chart match first, then album search.

```python
import requests

DEEZER_BASE = "https://api.deezer.com/"

def extract_deezer_data(a):
    return {
        "cover": a.get("cover_big") or a.get("cover_medium"),
        "link": a.get("link"),
        "fans": a.get("fans", 0),
        "genres": [g["name"] for g in a.get("genres", {}).get("data", [])]
    }

def enrich_deezer(artist, album, chart_albums):
    album_lower = album.lower()
    # 1. Try chart match (fast path for popular releases)
    for a in chart_albums:
        a_title = a.get("title", "").lower()
        if album_lower in a_title or a_title in album_lower:
            if artist.lower() == a.get("artist", {}).get("name", "").lower():
                return extract_deezer_data(a)
    # 2. Search Deezer for the album (no auth needed)
    search_url = f"{DEEZER_BASE}search/album"
    r = requests.get(search_url, params={"q": f"{artist} {album}", "limit": 3})
    if r.ok:
        for result in r.json().get("data", []):
            result_artist = result.get("artist", {}).get("name", "").lower()
            if artist.lower() in result_artist or result_artist in artist.lower():
                return extract_deezer_data(result)
    return None

# Fetch chart albums once (used as fast-match cache)
deezer_chart = requests.get(f"{DEEZER_BASE}chart/0/albums",
    params={"limit": 50}).json().get("data", [])

for item in out_now + coming_soon:
    enriched = enrich_deezer(item["artist"], item["album"], deezer_chart)
    item["cover"] = enriched["cover"] if enriched else None
    item["link"] = enriched["link"] if enriched else None
    item["fans"] = enriched["fans"] if enriched else 0
    item["genres"] = enriched["genres"] if enriched else []
```

### Step 5 — Validate before sending

```python
if not out_now and not coming_soon:
    print("WARNING: No releases found. Skipping email send.")
    print(f"Artists scanned: {len(artists)}")
    print(f"MusicBrainz lookups: {lookup_count}")
    # Exit early — don't send an empty email
else:
    print(f"Found: {len(out_now)} out now, {len(coming_soon)} coming soon")
```

### Step 6 — Send HTML email via AgentMail

**Inline images:** Download Deezer covers, base64-encode them, attach with CID, reference as `cid:` in HTML. This ensures images display even when external images are blocked.

```python
import os, tempfile, base64, hashlib
from agentmail import AgentMail
from datetime import datetime

client = AgentMail(api_key=os.environ["AGENTMAIL_API_KEY"])
today = datetime.now().strftime("%B %d, %Y")

def fmt_date(d):
    try:
        return datetime.strptime(d[:10], "%Y-%m-%d").strftime("%b %d, %Y")
    except:
        return d

# Build HTML first, collecting cover URLs for download
html_parts = []
cover_attachments = []  # list of (cid, local_path)

def make_cover(item, size="120"):
    """Download cover to a temp file and prepare an inline attachment."""
    url = item.get("cover")
    if not url:
        return ""
    # Stable CID from artist+album (safe for filename and HTML)
    cid = hashlib.md5(f"{item['artist']}|{item['album']}".encode()).hexdigest()[:12]
    try:
        import requests as _r
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.write(_r.get(url, timeout=10).content)
        tmp.close()
        cover_attachments.append((cid, tmp.name))
        return f'<img src="cid:{cid}" width="{size}" style="border-radius: 6px;" />'
    except Exception:
        return ""

html = f"""<html><body style="font-family: -apple-system, sans-serif; max-width: 700px; margin: auto;">
<h2 style="border-bottom: 1px solid #eee; padding-bottom: 10px;">🎵 New Music Digest — {today}</h2>
"""

if out_now:
    html += "<h3 style="color: #d63031;">📀 Out Now</h3><ul style="list-style: none; padding: 0;">"
    for item in out_now:
        cover_tag = make_cover(item, "120")
        fans_str = f" ({item['fans']:,} fans)" if item.get("fans", 0) > 0 else ""
        genres_str = f" · {', '.join(item['genres'][:2])}" if item.get("genres") else ""
        link = item.get("link") or f"https://www.last.fm/music/{item['artist'].replace(' ', '+')}/{item['album'].replace(' ', '+')}"
        html += f"""<li style="margin-bottom: 20px; display: flex; gap: 15px;">
  <div style="min-width: 120px;">{cover_tag}</div>
  <div>
    <strong>{item['artist']}</strong> — {item['album']}<br/>
    <span style="color: #888; font-size: 12px;">{fmt_date(item['date'])}{fans_str}{genres_str}</span><br/>
    <a href="{link}" style="color: #0984e3; font-size: 12px;">▶ Listen</a>
  </div>
</li>"""
    html += "</ul>"

if coming_soon:
    html += "<h3 style="color: #00b894; margin-top: 30px;">📅 Coming Soon</h3><ul style="list-style: none; padding: 0;">"
    for item in coming_soon:
        cover_tag = make_cover(item, "80")
        link = item.get("link") or f"https://www.last.fm/music/{item['artist'].replace(' ', '+')}/{item['album'].replace(' ', '+')}"
        html += f"""<li style="margin-bottom: 16px; display: flex; gap: 15px;">
  <div style="min-width: 80px;">{cover_tag}</div>
  <div>
    <strong>{item['artist']}</strong> — {item['album']}<br/>
    <span style="color: #00b894; font-size: 13px;">Drops {fmt_date(item['date'])}</span>
    <br/><a href="{link}" style="color: #0984e3; font-size: 12px;">▶ Listen</a>
  </div>
</li>"""
    html += "</ul>"

if not out_now and not coming_soon:
    html += "<p>No new releases found for your top artists this week.</p>"

html += "<hr style="border: none; border-top: 1px solid #eee; margin-top: 30px;"><p style="color: #aaa; font-size: 11px;">Sources: Last.fm, MusicBrainz, Deezer</p></body></html>"

text = f"New Music Digest — {today}\n\n"
for item in out_now:
    text += f"📀 {item['artist']} — {item['album']} ({fmt_date(item['date'])})\n"
for item in coming_soon:
    text += f"📅 {item['artist']} — {item['album']} (Drops {fmt_date(item['date'])})\n"
if not out_now and not coming_soon:
    text += "No new releases found."

# Build inline attachments
attachments = []
from agentmail.attachments import SendAttachment
for cid, path in cover_attachments:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    attachments.append(SendAttachment(
        filename=f"{cid}.jpg",
        content_type="image/jpeg",
        content_disposition="inline",
        content_id=cid,
        content=b64,
    ))
    os.unlink(path)  # clean up temp file

client.inboxes.messages.send(
    inbox_id=os.environ["AGENTMAIL_INBOX"],
    to=[os.environ["DIGEST_RECIPIENT"]],
    subject=f"New Music Digest — {today}",
    text=text,
    html=html,
    attachments=attachments if attachments else None,
)
print("Email sent successfully.")
```

## Key Rules

- **MusicBrainz for dates only** — `artist.getnewreleases` on Last.fm does NOT work
- **Out Now = last 30 days, full albums only** — skip singles, EPs, compilations
- **Coming Soon = next 90 days** — full albums only
- **MusicBrainz rate limit: 0.35s sleep** between calls or you'll get a 429
- **Deezer: no rate limit on public endpoints** — use freely for enrichment
- **Always validate before sending** — if both lists are empty, skip the email and log
- **MusicBrainz User-Agent policy** — include a real contact (name/email). Anonymous UAs get throttled or blocked

## Deezer API Quick Reference

```bash
# Album chart (global, no auth)
curl "https://api.deezer.com/chart/0/albums?limit=50"

# Album search (no auth)
curl "https://api.deezer.com/search/album?q=Artist+Album+Name&limit=3"

# Album detail (no auth — has release_date, genres, cover, fans)
curl "https://api.deezer.com/album/{album_id}"
```

## References

- [references/endpoints.md](./references/endpoints.md) — Full Last.fm endpoint reference
