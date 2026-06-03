# New Music Digest

Weekly new-releases report for the listener's Last.fm top artists, cross-referenced with MusicBrainz release dates and Deezer metadata. Delivered as an HTML email with inline cover art.

## What it does

| Step | Source | Purpose |
|------|--------|---------|
| 1 | Last.fm | Fetch the user's top artists (1-month + 3-month windows, deduped) |
| 2 | MusicBrainz | Find release groups per artist, filter to last 30 days + next 90 days, full albums only |
| 3 | (dedup) | Drop duplicate artist/album pairs |
| 4 | Deezer | Enrich with cover art, fan count, genres, listen links |
| 5 | (validate) | Skip the email if both lists are empty |
| 6 | AgentMail | Send an HTML email with CID-attached cover art |

The output has two sections:
- **📀 Out Now** — albums released in the last 30 days
- **📅 Coming Soon** — albums releasing in the next 90 days

Singles, EPs, and compilations are deliberately excluded — full albums only.

## Setup

### Required env vars

```bash
LASTFM_API_KEY=...           # https://www.last.fm/api/account/create
LASTFM_USERNAME=...          # your Last.fm username
AGENTMAIL_API_KEY=...        # https://agentmail.to
AGENTMAIL_INBOX=...          # sender address (e.g. you@agentmail.to)
DIGEST_RECIPIENT=...         # where to send the digest (e.g. you@example.com)
```

Put these in `~/.hermes/.env` or export in your shell.

### MusicBrainz User-Agent

MusicBrainz requires a descriptive User-Agent with a real contact (their [policy](https://musicbrainz.org/doc/MusicBrainz_API/Rate_limiting)). The skill uses `NewMusicDigest/1.0 (contact@example.com)` by default — **edit this in the SKILL.md to your own contact** so MusicBrainz can reach you if your script misbehaves.

## Install

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/new-music-digest ~/.hermes/skills/
```

## Usage

Triggers on: "new music digest", "weekly music releases", "album release radar", "what's coming out this week".

Designed for a weekly cron (Friday morning is a good fit — last.fm windows line up well with Mon-Fri release weeks).

```python
cronjob(action="create", schedule="0 9 * * 5",
        prompt="Run the new-music-digest skill.")
```

## Why these three sources?

- **Last.fm** has the best "your artists" signal (your real listening history)
- **MusicBrainz** has the most reliable release-date data — Last.fm's `artist.getnewreleases` is broken
- **Deezer** has clean cover art and a permissive public API (no auth, no rate limit)

## Pitfalls

- **Do not use Last.fm's `artist.getnewreleases`** — it returns unreliable data
- **MusicBrainz will 429 you** if you skip the `time.sleep(0.35)` between calls
- **MusicBrainz needs a real User-Agent** — include a name and contact email
- **Always validate before sending** — never email an empty digest
- **Deezer covers come from the global chart cache first** — falls back to search if the artist isn't charting

## See also

- [agentmail](../agentmail/) — required for email delivery
- [deezer](../deezer/) — public Deezer API reference
