# Travelogue

Capture and organize travel experiences into a rich, searchable Obsidian journal. Send updates during trips via Discord or Telegram; the agent logs everything as dated daily entries with structured metadata.

## What it does

- **Parses ad-hoc updates** — text, photos, impressions — into a clean journal
- **Saves photos** to a structured `~/.hermes/travelogue/{trip}/photos/` directory
- **Writes daily Obsidian entries** with consistent emoji-sectioned structure
- **Appends** to existing entries when more updates come in for the same day
- **Maintains a Trip Index** with travelers, hotel, flights, rental, and running stats
- **Generates recaps** on request at the end of the trip

## Entry structure

Each day's entry follows a consistent template:

- `## 📍 Places Visited` — places by name with context
- `## 🍽️ Food & Drink` — meals and notable drinks
- `## 📸 Photos` — Obsidian image embeds with descriptions
- `## ✨ Highlights` — what made the day memorable
- `## 📝 Notes` — practical info and travel logistics
- `## 🏨 Stay` — hotel and room details

The structure is opinionated for scannability. Skip a section if it's empty rather than writing `None`.

## Setup

### Required

- **Obsidian vault** — set `OBSIDIAN_VAULT_PATH` in `~/.hermes/.env` (defaults to `~/Documents/Obsidian Vault`)
- A `Travelogue/` folder at the vault root (created automatically on first use)
- A way to receive updates: Discord channel, Telegram chat, or direct message

### Optional

- **ImageMagick** (`magick` command) for converting photos to WebP
- A cron or reminder to send the agent a brief update each day of the trip

## Install

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/travelogue ~/.hermes/skills/travel/
```

## Usage

Triggers on: "log this to travelogue", "save this to my trip", "add to the journal", or any photo + text combo during a known trip period.

Typical flow:
1. User: "Just checked into the hotel, room has an amazing ocean view" [photo]
2. Agent: saves the photo, creates/updates today's entry, replies briefly
3. User: "Had poke for lunch at Foodland" [photo]
4. Agent: appends to today's entry, merges into existing Food & Drink section

## Tips

- **Preserve user voice** — don't rewrite their descriptions into formal prose
- **Be conversational** when confirming — "Got it, logged the Road to Hana day with 3 photos"
- **Ask about context-less photos** — "What's this one?" beats guessing
- **Update Trip Index stats** as days go by (photo count, restaurants, beaches, etc.)
- **End-of-trip recap** — offer to write a summary post-trip with the highlights

## Pitfalls

See [SKILL.md](./SKILL.md) for the full workflow. Key ones:
- **Don't duplicate sections** — if "Places Visited" exists, append items to it, don't create a second "Places Visited" header
- **Trip slug matters** — pick a stable one at trip start (`{destination}-{year}` works) and use it consistently in the directory and frontmatter
- **Photo filenames** — `YYYY-MM-DD-NNN.ext` with a counter that resets each day
- **Time zones** — for cross-time-zone trips, use local time at destination, not the sender's time zone

## See also

- [obsidian](../obsidian/) — broader Obsidian vault patterns
- [flight-tracker](../flight-tracker/) — track flight status alongside trip logging
