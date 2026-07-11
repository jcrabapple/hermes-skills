---
name: deezer-playlist-creator
description: >-
  Create Deezer playlists programmatically from any query — similar artists,
  genre mixes, festival lineups, mood-based collections. Three-tier data
  pipeline: Deezer public REST API for discovery, GQL Pipe API for smart
  mixes and playlist creation, web search for subjective curation.
  Uses ARL cookie auth — no OAuth app required.
triggers:
  - make me a deezer playlist
  - create a deezer playlist
  - deezer playlist from
  - build playlist on deezer
  - generate deezer playlist
  - artists similar to
  - playlist of artists like
  - top tracks by
related_skills:
  - deezer
  - infisical-secrets
  - soundiiz
metadata:
  hermes:
    tags: [deezer, playlist, music, creation, curation]
prerequisites:
  commands: [python3.14, pip]
  python_packages: [deezer-python-gql]
  secrets:
    - name: DEEZER_ARL
      stored_in: Environment variable, Infisical, or secrets file
      description: Your Deezer ARL cookie (192-char hex string from browser DevTools)
      how_to_get: |
        1. Go to deezer.com and log in
        2. F12 → Application → Cookies → deezer.com
        3. Copy the 'arl' cookie value
      valid_for: ~3 months, then re-extract
---

# Deezer Playlist Creator

End-to-end Deezer playlist creation. Three data sources, one pipeline: discover tracks → build tracklist → push to Deezer.

## Data Pipeline Architecture

Every playlist request flows through a three-tier data sourcing strategy:

### Tier 1: Deezer Public REST API (no auth)

Primary source for structured music discovery. Fast, rate-limited to ~50 req/5s, no credentials needed.
Load the `deezer` skill before using these endpoints — it has the full reference.

| Query type | API call | Returns |
|---|---|---|
| "Artists similar to X" | `GET /artist/{id}/related` | Up to 100 related artists with IDs |
| "Top tracks by X" | `GET /artist/{id}/top?limit=N` | Ranked top tracks (max 50) |
| "Discography of X" | `GET /artist/{id}/albums` | All albums by artist |
| "What's trending" | `GET /chart/0/tracks` | Worldwide chart |
| "New releases" | `GET /editorial/0/releases` | This week's new albums |
| "Genre exploration" | `GET /genre/{id}/artists` | Artists in a genre |
| "Search anything" | `GET /search?q=QUERY&order=RANKING` | Tracks, albums, artists |
| "Album tracklist" | `GET /album/{id}/tracks` | All tracks in an album |

**Full workflow example: "playlist of artists similar to Nirvana"**

```
1. Public API: GET /search/artist?q=Nirvana          → artist ID: 543
2. Public API: GET /artist/543/related                → [Pearl Jam, Soundgarden, Alice in Chains, ...]
3. Public API: GET /artist/{id}/top?limit=3           → top 3 tracks per related artist
4. Build JSON tracklist from all those tracks
5. Pipe to deezer_create_playlist.py                  → playlist URL
```

Every step uses the public REST API for discovery. The GQL API only enters at the final step to create the playlist.

### Tier 2: Deezer GQL Pipe API (ARL auth)

Adds algorithmic personalization. Use these when the public API can't answer the question.

| Method | What it gives | Use when |
|---|---|---|
| `get_artist_mix(artist_id)` | Algorithmic mix based on artist | "Deep cuts similar to X" |
| `get_track_mix(track_id)` | Mix from a seed track | "Songs like this one" |
| `get_similar_tracks(track_id)` | Similar to one track | "More tracks in this vein" |
| `get_recommendations()` | Personalized "you might like" | "Surprise me" |
| `get_flow()` | Deezer's infinite Flow radio | "Put on something I'll like" |
| `get_charts()` | Current chart data | "What's hot right now" |
| `search(query)` | Authenticated search | Better results than public API |

**Common genre IDs for public API:** `0`=All, `132`=Pop, `116`=Rap/Hip Hop, `152`=Rock, `113`=Dance, `129`=Jazz, `98`=Classical, `85`=Alternative, `106`=Electro

### Tier 3: Web search (last resort)

For subjective or human-curated questions APIs can't answer:

- "Best deep cuts by The Cure"
- "Underrated 90s shoegaze albums"
- "Songs that feel like autumn in New England"
- Festival lineups, music blog picks, Reddit threads

Always prefer Tier 1 or Tier 2 first — web search is for when the API endpoints don't exist for the question being asked.

## Script: `deezer_create_playlist.py`

Located at `scripts/deezer_create_playlist.py` in this skill directory.

The final step in every pipeline. Takes a JSON tracklist, searches Deezer for each track, creates a playlist, and populates it.

### Usage

```bash
# With env var (simplest)
DEEZER_ARL="your-arl-cookie" python3.14 scripts/deezer_create_playlist.py < playlist.json

# With Infisical (if you use it)
echo '{"title":"Name","description":"","tracks":[...]}' | \
  infisical run --projectId <YOUR_PROJECT_ID> --env dev -- \
  python3.14 scripts/deezer_create_playlist.py

# From a file
python3.14 scripts/deezer_create_playlist.py --input /tmp/playlist.json
```

### Input format

```json
{
  "title": "Playlist name",
  "description": "Optional description",
  "tracks": [
    {"title": "Track Title", "artist": "Artist Name"},
    ...
  ]
}
```

### Output

```json
{
  "playlist_url": "https://www.deezer.com/playlist/15515468061",
  "playlist_id": "15515468061",
  "matched": 15,
  "missed": 2,
  "missed_tracks": [{"title": "...", "artist": "..."}],
  "tracks": [{"title": "...", "artist": "...", "link": "..."}]
}
```

### How it works

1. **Search** — Each track searched via GQL `search()`, returns up to 20 candidates
2. **Score** — Python `SequenceMatcher` (0.7 title + 0.3 artist weight), score ≥ 0.5 = match
3. **Create** — `create_playlist()` → public, non-collaborative
4. **Populate** — `add_tracks_to_playlist()` in batches of 50

### Match scoring details

- Extracts artist via `contributors.edges[].node.name` (not a flat `artists` array)
- Sorts all candidates by score, takes the highest
- Score < 0.5 → track is skipped and reported in `missed_tracks`

## Full Workflow Examples

### "Make me a playlist of artists similar to Nirvana"

```
1. Load deezer skill
2. GET /search/artist?q=Nirvana → artist ID 543
3. GET /artist/543/related → [Pearl Jam, Soundgarden, Alice in Chains, ...]
4. For each related artist: GET /artist/{id}/top?limit=3
5. Build JSON: {title: "Artists Like Nirvana", tracks: [...]}
6. Pipe to deezer_create_playlist.py
```

### "Make me a 90s trip-hop playlist"

```
1. GET /search?q=trip-hop 90s&order=RANKING&limit=50 (public API)
2. Filter results for quality/relevance
3. For top artists found: GET /artist/{id}/top?limit=3
4. Build JSON and pipe to script
```

### "What's trending in electronic music right now?"

```
1. GET /genre/106/artists (electronic genre)
2. For each artist: GET /artist/{id}/top?limit=2
3. OR: GET /chart/0/tracks (worldwide chart, filter by genre)
4. Build JSON and pipe
```

### "Surprise me with something I'll like"

```
1. Use GQL get_recommendations() or get_flow()
2. Extract tracks
3. Build JSON and pipe
```

## Decision Tree

When the user asks for a playlist, follow this order:

1. **Can the public REST API answer this directly?** (similar artists, top tracks, genre, charts, search) → Use Tier 1
2. **Does it need algorithmic smarts?** (track-based mixes, personal recommendations, flow) → Use Tier 2
3. **Is it subjective or requires human cultural knowledge?** (vibes, deep cuts, "best of" lists, festival lineups) → Use Tier 3 (web search)

Never use web search when the public API has a direct endpoint for the query. Never use the GQL API for simple searches the public API handles faster.

## Pitfalls

- **ARL expires ~3 months**. If auth fails, re-extract from browser and update your DEEZER_ARL.
- **Null nodes in search edges** — Some GQL track search results contain `edge.node = None`. The script skips these silently, but if all edges for a query are null the track is reported as missed. This is a Deezer API quirk, not a script bug.
- **0.5 scoring threshold is generous** — It catches nearly everything (103/103 in testing) but produces false matches on ambiguous track names. Raise the threshold near line 117 in `deezer_create_playlist.py` if you prefer fewer false matches at the cost of more misses.
- **Search errors in stderr** — The GQL API logs non-critical errors (album not found, playlist owner access denied) but search still returns results. Ignore the noise; check for actual data, not error messages.
- **`contributors` not `artists`** — Track nodes use `contributors.edges[].node.name`, not a flat `artists` array
- **`create_playlist` returns `{playlist: {id}}`** — Need `result.playlist.id`, not `result.id`
- **Requires python3.14** — The script uses asyncio features from Python 3.14
- **Rate limiting** — 0.2s delay between searches. Large playlists (50+ tracks) take a few minutes.
- **Public API limit is 50 req/5s** — Add delays in bulk artist/track fetching loops
- **Some tracks won't match** — ~5-10% miss rate is normal. Less common tracks, regional releases, or tracks with special characters in the title are the usual culprits.
- **Genre IDs are Deezer-specific** — Use the list above; don't guess
- **`/radio/top` is unreliable** — Use `/radio/genres` + `/radio/lists` instead

## Troubleshooting

| Issue | Fix |
|---|---|
| `DEEZER_ARL not found` | Export the env var or use your secrets manager |
| All tracks return "No match found" | ARL may be expired; re-extract from browser |
| `Object of type ... is not JSON serializable` | Check `.playlist.id` extraction and track ID types |
| GQL search returns 0 results | Fall back to public REST API search (`deezer` skill) |
| Public API returns 0 for related artists | Some artists have empty related lists; try web search |
| Playlist created but empty | `add_tracks_to_playlist` may have failed silently; check stderr |
| Tracks matching wrong artists | Raise score threshold in the script; 0.5 is tuned for recall, 0.8+ for precision |
