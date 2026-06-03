# Flight Tracker

Track flights in real-time using the [AviationStack](https://aviationstack.com/) API. Auto-discovers flights by parsing airline confirmation emails forwarded to an AgentMail inbox. Polls upcoming flights on travel days and alerts on changes (gate, delay, status).

## What it does

- **Real-time status** — scheduled, active, landed, cancelled, diverted, incident
- **Gate/terminal/baggage info** as it becomes available
- **Codeshare detection** — surfaces the actual operating flight, not the marketed one
- **Email-driven discovery** — parses booking confirmations to find new flights
- **Cron-based monitoring** — polls every 30 min on travel days, alerts on deltas only

## Setup

### Required

1. **AviationStack API key** — sign up at [aviationstack.com](https://aviationstack.com/) (free tier: 500 req/month)
2. **AgentMail inbox** — set up an inbox to receive forwarded airline booking emails
3. **`AVIATIONSTACK_API_KEY`** in `~/.hermes/.env`
4. **`AGENTMAIL_INBOX`** env var (e.g. `your-inbox@agentmail.to`)

### Optional but recommended

- A small `flights.json` file listing the flights you want monitored (see SKILL.md for format)
- A cron job that runs every 30 minutes on travel days, polling AviationStack and diffing against the last known state

## Install

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/flight-tracker ~/.hermes/skills/travel/
```

## Usage

Triggers on: "track flight", "flight status", "is my flight on time", "gate change", "what terminal", "is flight delayed".

For travel-day monitoring, set up a cron job:

```python
cronjob(action="create", schedule="*/30 4-23 * * *",
        prompt="Run the flight-tracker skill: check all flights in flights.json against AviationStack, alert on any change from last known state.")
```

## Example output

```
UA1749 — active
  Departure: San Francisco International (SFO)
    Terminal: 3, Gate: E12
    Scheduled: 2026-04-05T15:30:00.000Z
    Estimated: 2026-04-05T15:42:00.000Z
    Delay: 12 min
  Arrival: Kahului Airport (OGG)
    Terminal: 1, Gate: N/A
    Scheduled: 2026-04-05T18:55:00.000Z
    Baggage: 5

🔔 Change detected: gate changed from E10 to E12, now delayed 12 minutes.
```

## Pitfalls

See [SKILL.md](./SKILL.md) for the full list. Key ones:
- **Use `http://` not `https://`** on the AviationStack free tier (HTTPS returns auth errors)
- **Watch for codeshares** — the API returns both the marketed and operating flights
- **500 req/month is tight** — don't poll more than every 30 min on travel days
- **Timestamps are UTC** — convert to the local time zone for the user-facing message
- **Gate null is normal** until 2-3 hours before departure — don't alert on it

## See also

- [travelogue](../travelogue/) — log trip activities, photos, and meals alongside flight tracking
- [agentmail](../agentmail/) — required for the email-parsing side of flight discovery
