# Concert Monitor

Weekly digest of upcoming concerts in your metro area. Searches Ticketmaster, StubHub, and venue-specific sites to compile a clean, scannable list of shows — delivered via email, Telegram, or Discord.

## Features

- **Multi-platform search**: Ticketmaster, StubHub, SeatGeek, venue sites
- **Configurable metro areas**: works for any city — just edit the config
- **Venue-specific tracking**: monitors the venues you care about
- **Multiple delivery methods**: email, Telegram, Discord, or local file
- **Clean output**: grouped by area and date, with prices and links
- **Cron-ready**: designed for weekly automated runs

## Quick Start

### 1. Configure your area

```bash
cd concert-monitor
cp config.example.yaml config.yaml
```

Edit `config.yaml` — set your metro areas, venues, and delivery method:

```yaml
metro_areas:
  - name: "Austin, TX"
    venues:
      - name: "Stubb's BBQ"
      - name: "Emo's Austin"
      - name: "Mohawk Austin"
      - name: "ACL Live at The Moody Theater"

delivery:
  method: email
  target: "you@example.com"
```

### 2. Run it

From within [Hermes Agent](https://hermes-agent.nousresearch.com):

> "Load the concert-monitor skill and run the weekly concert digest."

Or set it up as a cron job:

```bash
hermes cron add --name "concert-monitor" \
  --schedule "0 9 * * 1" \
  --prompt "Load the concert-monitor skill, read ~/.hermes/skills/leisure/concert-monitor/config.yaml, and run the weekly concert digest for the configured metro areas and venues."
```

This runs every Monday at 9am.

## Configuration

`config.example.yaml` contains a full annotated template. Key sections:

### Metro Areas

```yaml
metro_areas:
  - name: "City, ST"
    venues:
      - name: "Main Venue"
      - name: "Another Venue"
        aliases: ["Short Name"]  # optional alternative names
```

Add as many metro areas as you want. Each area gets its own section in the output.

### Delivery

```yaml
delivery:
  method: email          # email | telegram | discord | local
  target: "you@example.com"  # email address, chat ID, or file path
```

- **Email**: uses AgentMail (requires AgentMail setup)
- **Telegram**: `target` is your Telegram chat ID
- **Discord**: `target` is `discord:CHANNEL_ID`
- **Local**: `target` is a file path (e.g. `/tmp/concerts.md`)

### Lookahead

```yaml
weeks_ahead: 2  # how many weeks of shows to include
```

## How It Works

1. Reads your `config.yaml` for metro areas and venues
2. For each area, searches web for upcoming concerts
3. Searches each venue individually for their event calendars
4. Cross-references with Ticketmaster, StubHub, and SeatGeek
5. Deduplicates and sorts by date
6. Formats into a clean digest
7. Delivers via your configured method

## Example Output

```
🎵 Concert Monitor — May 12–25, 2026

📍 WASHINGTON, DC

📅 Fri May 16
• LCD Soundsystem @ The Anthem — 8pm — $65–$95
• Local Natives @ 9:30 Club — 8pm — $40

📅 Sat May 17
• Khruangbin @ Merriweather Post Pavilion — 7pm — $45–$85

📅 Tue May 20
• Waxahatchee @ Black Cat — 8pm — $30

📍 BALTIMORE, MD

📅 Fri May 16
• Turnstile @ Baltimore Soundstage — 7pm — $35

📅 Sat May 17
• Goose @ CFG Bank Arena — 8pm — $55–$120
```

## Included Venue Presets

The example config ships with venues for:
- **Washington, DC** — 9:30 Club, The Anthem, Black Cat, Merriweather, etc.
- **Baltimore, MD** — Soundstage, Nevermore Hall, Ottobar, CFG Bank Arena

Commented-out examples for **Austin, TX** and **Nashville, TN** are also included.

## Pitfalls

- **Don't hallucinate shows.** Only list concerts actually found via search.
- **Date format.** Always include day of week: "Fri May 2" not just "May 2".
- **Venue disambiguation.** Many cities have similarly-named venues — verify you have the right one.
- **Sold out shows.** Mark them clearly.
- **Timezones.** Show times are local to the venue.
- **Small venues.** Some clubs don't list on major platforms — check their websites directly.

## License

MIT

## Using with Hermes Agent

```bash
# Install
git clone https://github.com/jcrabapple/hermes-skills.git /tmp/hermes-skills
cp -r /tmp/hermes-skills/concert-monitor ~/.hermes/skills/leisure/concert-monitor
rm -rf /tmp/hermes-skills

# Configure
cp ~/.hermes/skills/leisure/concert-monitor/config.example.yaml \
   ~/.hermes/skills/leisure/concert-monitor/config.yaml
# Edit config.yaml with your metro areas and venues
```

Once installed, Hermes loads the skill when concerts are mentioned. Example prompts:

> "Load the concert-monitor skill and run the weekly digest."
> "What concerts are coming up in Austin this month?"
