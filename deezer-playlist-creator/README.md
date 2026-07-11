# Deezer Playlist Creator

Create Deezer playlists programmatically from any query — similar artists, genre mixes, festival lineups, or mood-based collections.

## What it does

| Capability | Description |
|---|---|
| Artist-similar playlists | Given a seed artist, pulls related artists + their top tracks |
| Genre/chart playlists | Pulls from Deezer charts, genre pages, or new releases |
| Smart algorithmic mixes | Uses Deezer's GQL Pipe API for personalized recommendations |
| Full creation pipeline | Searches for every track, creates playlist, adds all matches |
| Match scoring | Fuzzy title + artist matching with configurable threshold |

## Setup

### Required

- Python 3.14+
- `pip install deezer-python-gql`
- A Deezer account (free or premium)

### Authentication

This skill uses your Deezer **ARL cookie** — no OAuth app registration needed.

1. Go to [deezer.com](https://www.deezer.com) and log in
2. Open DevTools (`F12`) → **Application** → **Cookies** → `deezer.com`
3. Copy the `arl` cookie value (192-character hex string)
4. Export it as an environment variable:

```bash
export DEEZER_ARL="your-arl-cookie-here"
```

The ARL cookie expires after approximately 3 months. Re-extract when auth fails.

If you use Infisical or another secrets manager, store it there and inject via `infisical run --` or equivalent.

## Install

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/deezer-playlist-creator ~/.hermes/skills/leisure/
pip install deezer-python-gql
```

## Usage

Triggers on: "make me a Deezer playlist", "create a Deezer playlist", "artists similar to", "top tracks by", "build playlist on Deezer".

The agent uses a three-tier data pipeline:

1. **Deezer Public REST API** (no auth) — similar artists, top tracks, charts, genres
2. **Deezer GQL Pipe API** (ARL auth) — algorithmic mixes, recommendations, Flow
3. **Web search** (fallback) — subjective curation, festival lineups, human-curated lists

### Example: "Make me a playlist of artists similar to Sleep Token"

```bash
# The agent will:
# 1. GET /search/artist?q=Sleep+Token → artist ID
# 2. GET /artist/{id}/related → Bad Omens, Spiritbox, Dayseeker, ...
# 3. GET /artist/{id}/top?limit=3 → top tracks for each related artist
# 4. Build JSON tracklist
# 5. Pipe to scripts/deezer_create_playlist.py
```

### Running the script directly

```bash
echo '{
  "title": "My Playlist",
  "tracks": [
    {"title": "Get Lucky", "artist": "Daft Punk"},
    {"title": "Enjoy the Silence", "artist": "Depeche Mode"}
  ]
}' | DEEZER_ARL="$DEEZER_ARL" python3.14 scripts/deezer_create_playlist.py
```

### Output

```json
{
  "playlist_url": "https://www.deezer.com/playlist/15515468061",
  "playlist_id": "15515468061",
  "matched": 95,
  "missed": 5,
  "missed_tracks": [{"title": "...", "artist": "..."}],
  "tracks": [{"title": "...", "artist": "...", "link": "..."}]
}
```

## Pitfalls

- **ARL expires ~3 months.** Re-extract and re-export when auth fails.
- **0.5 scoring threshold is generous.** It catches nearly everything but produces occasional false matches on ambiguous track names. Raise the threshold in `scripts/deezer_create_playlist.py` for better precision.
- **Requires Python 3.14.** The script uses 3.14 asyncio features.
- **~5-10% miss rate is normal.** Regional releases and uncommon tracks may not match.
- **Large playlists take time.** 0.2s delay between searches — a 100-track playlist takes ~2-3 minutes.

## See also

- [new-music-digest](../new-music-digest/) — Weekly new release tracking across favorite artists
- [concert-monitor](../concert-monitor/) — Find upcoming concerts in your area
