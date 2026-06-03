---
name: travelogue
description: Log travel experiences during trips — save photos, places visited, meals, activities, and memories as structured daily entries in Obsidian. User shares updates via Discord/Telegram with text and photos; agent organizes everything into a rich travel journal.
category: travel
---

# Travelogue

Capture and organize travel experiences into a rich, searchable Obsidian journal. The user sends updates during trips (text, photos, impressions) via Discord or Telegram; the agent logs everything as dated daily entries with structured metadata.

## Workflow

The user sends messages during their trip like:
- "We just arrived at the hotel, the oceanfront room is incredible"
- "Had lunch at [Restaurant] — the [dish] was amazing" [with photo]
- "Road to [destination] today — [Stop 1] was beautiful, but the water was brown from runoff" [with photos]
- "Sunset at [Beach] was unreal 🌅" [with photo]

The agent:
1. **Parses the update** — extracts date, location, activity, impressions
2. **Saves any photos** — stores in `~/.hermes/travelogue/<trip-name>/photos/`
3. **Writes/appends to Obsidian** — daily entry with structured format
4. **Confirms** — brief ack to the user

## Directory Structure

```
~/.hermes/travelogue/
├── {trip-slug}/
│   ├── photos/
│   │   ├── 2026-04-05-001.webp
│   │   ├── 2026-04-05-002.webp
│   │   ├── 2026-04-06-001.webp
│   │   └── ...
│   └── meta.json          # trip metadata (start/end dates, locations, etc.)
```

```
Obsidian Vault/
└── Travelogue/
    └── {Trip Name}/
        ├── 2026-04-05 — Departure & Arrival.md
        ├── 2026-04-06 — Day 1.md
        ├── 2026-04-07 — Day 2.md
        └── _Trip Index — {Trip Name}.md
```

## Entry Format

```markdown
---
date: 2026-04-06
trip: {trip-slug}
location: {location}
tags: [travel, {destination}, {year}]
---

# 2026-04-06 — {Brief Theme or Day N}

## 📍 Places Visited
- **{Place}** ({context, e.g. mile marker, neighborhood})
- **{Place}**

## 🍽️ Food & Drink
- **{Meal at Restaurant}** — {dish notes}
- **{Drink/Snack at Place}** ({flavor/notes})

## 📸 Photos
![[photos/2026-04-06-001.webp|{description}]]
![[photos/2026-04-06-002.webp|{description}]]
![[photos/2026-04-06-003.webp|{description}]]

## ✨ Highlights
- {What made the day memorable}
- {A specific moment or sight}

## 📝 Notes
- {Practical info, e.g. cash only, advisory in effect, hours}
- {Travel logistics}

## 🏨 Stay
- **{Hotel}** — {Room description}
- {Anything notable about the room or view}
```

## Photo Handling

When the user sends a photo:
1. **Save the photo** to `~/.hermes/travelogue/{trip}/photos/YYYY-MM-DD-NNN.webp`
   - Convert to WebP if needed: `magick input.jpg -quality 85 output.webp`
   - Or just save as-is if already compressed
2. **Reference in Obsidian** using `![[photos/YYYY-MM-DD-NNN.ext|description]]`
3. **Add the description** the user provided (or generate one from context)

For Discord/Telegram image attachments:
- Discord: Images arrive as URLs or attachments. Download with `curl -o path URL`
- Telegram: Images may be file IDs — use the Telegram file download endpoint
- If the user sends a MEDIA: path, it's already saved locally

## Trip Index Format

```markdown
---
trip: {trip-slug}
start: {YYYY-MM-DD}
end: {YYYY-MM-DD}
tags: [travel, {destination}, {year}]
---

# {Emoji + Trip Name} — {Date Range}

**Travelers:** {Names}
**Hotel:** {Hotel name}, {Room type}
**Car:** {Vehicle, rental company, confirmation #}
**Flights:** {Outbound flights}, {Return flights}

## 📅 Daily Entries
- [[{YYYY-MM-DD} — {Theme 1}]]
- [[{YYYY-MM-DD} — {Theme 2}]]
- [[{YYYY-MM-DD} — {Theme 3}]]

## 📊 Trip Stats
- Days: {N}
- Photos logged: {N}
- Restaurants tried: {N}
- Beaches visited: {N}
```

## Entry Naming

- Format: `YYYY-MM-DD — Brief Description.md`
- If it's the first entry of the day and user hasn't given a theme, use `YYYY-MM-DD — Day N.md`
- If the user mentions a specific activity, use that: `2026-04-06 — Road to Hana.md`
- If multiple updates come in for the same day, **append** to the existing entry

## Appending to Existing Day Entry

When a second update comes for the same day:
1. Find the existing entry for that date
2. Append a new section with a horizontal rule separator
3. Add the new photos, places, and notes under the relevant subheadings
4. Merge into existing sections (don't duplicate "Places Visited" — add new items to the list)

```markdown
---
# existing content above
---

## 📸 Additional Photos
![[photos/2026-04-06-004.webp|Sunset from hotel lanai]]

## ✨ More Highlights
- Caught an incredible sunset from the lanai around 6:30pm
```

## Obsidian Vault Path

Read from `OBSIDIAN_VAULT_PATH` env var, defaults to `~/Documents/Obsidian Vault`.
Always create the `Travelogue/{Trip Name}/` folder structure if it doesn't exist.

## Tips

- Be conversational when confirming — "Got it, logged the Road to Hana day with 3 photos"
- Don't over-process the user's words — preserve their voice in the entries
- If the user sends a photo without context, ask "What's this one?" or describe what you can see
- At the end of the trip, offer to generate a summary/trip recap
- Track running stats in the Trip Index (photos, restaurants, beaches, etc.)
- Use emojis as section headers for visual scanning in Obsidian
