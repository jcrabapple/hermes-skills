---
name: concert-monitor
description: "Weekly concert digest for any metro area. Searches multiple ticket platforms, compiles upcoming shows with dates, venues, artists, and prices, and delivers a curated list via email or messaging. Configurable for any city with customizable venue lists."
tags: [concerts, music, live-music, events, cron, local]
---

# Concert Monitor

Weekly digest of upcoming concerts in your area. Searches multiple ticket platforms and compiles a clean, scannable list of shows.

## Configuration

Copy `config.example.yaml` to `config.yaml` and customize for your metro area:

```bash
cp config.example.yaml config.yaml
```

The config file defines:
- **Metro areas** you want to monitor (e.g. "Washington DC", "Austin TX")
- **Key venues** to check in each area
- **Delivery method** (email, Telegram, Discord)
- **How many weeks ahead** to look

See `config.example.yaml` for the full format.

## Search Strategy

For each metro area in your config, run these searches:

### Primary Searches (web_search)
1. `"concerts [METRO AREA]" upcoming [MONTH] [YEAR]`
2. `site:ticketmaster.com concerts [METRO AREA]`
3. `site:stubhub.com concerts [METRO AREA]`
4. `"VENUE NAME" upcoming shows [MONTH]` (for each venue in config)

### Venue-Specific Searches
Search each venue from your config individually:
- `"VENUE NAME" upcoming concerts [MONTH]`
- `site:ticketmaster.com VENUE NAME`

### Ticket Platforms
- Ticketmaster
- StubHub
- SeatGeek
- AXS
- Venue direct sites

## Output Format

```
🎵 Concert Monitor — [DATE RANGE]

📍 [METRO AREA 1]

📅 Fri [DATE]
• [Artist] @ [Venue] — [Time] — [Price or "Check tickets"]
• [Artist] @ [Venue] — [Time] — [Price]

📅 Sat [DATE]
• [Artist] @ [Venue] — [Time] — [Price]

📅 Mon–Thu [DATES]
• [Artist] @ [Venue] — [Date, Day, Time] — [Price]

📍 [METRO AREA 2]
[etc.]
```

## Rules

- Focus on the next 2 weeks of shows (configurable)
- Include: date, day of week, start time, artist(s), venue, ticket price
- Group by metro area, then by date (soonest first)
- Only include shows with confirmed dates — don't guess
- Mark sold out shows
- If price unavailable, say "Check tickets" with a link
- Sort by date ascending

## Delivery

Supports multiple delivery methods:
- **Email**: via AgentMail or any SMTP
- **Telegram**: via Hermes send_message
- **Discord**: via Hermes send_message
- **Local file**: save to disk

Configure in `config.yaml`.

## Pitfalls

- **Don't hallucinate shows.** Only list concerts you actually found via search. If nothing comes up for a venue, skip it.
- **Date format consistency.** Always include the day of week: "Fri May 2" not just "May 2"
- **Venue accuracy.** Many cities have venues with similar names — double-check you have the right one.
- **Price ranges.** If you find a range ($30-$60), list the range. If only resale available, note "Resale from $X".
- **Don't list festivals unless music-focused.** A food festival with a band isn't a concert.
- **Keep it scannable.** The whole point is to quickly see what's coming up.
- **Some venues don't list on major platforms.** Check venue websites directly for smaller clubs.
- **Timezone awareness.** Show times are local to the venue — note the timezone if delivering to a different one.

## Cron Setup

Run weekly via Hermes cron:

```
Schedule: "0 9 * * 1"  (every Monday at 9am)
```

Or use the Hermes CLI:
```bash
hermes cron add --name "concert-monitor" --schedule "0 9 * * 1" --prompt "Load the concert-monitor skill and run the weekly concert digest."
```
