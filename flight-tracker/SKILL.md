---
name: flight-tracker
description: Track flights using AviationStack API — real-time status, gate changes, delays, terminal info. Parse airline booking emails to auto-discover flights. Cron monitoring on travel days.
category: travel
---

# Flight Tracker

Track flights in real-time: status, gates, terminals, delays, baggage claims. Auto-discovers flights by parsing airline confirmation emails. Monitors upcoming flights on travel days via cron.

## Prerequisites

1. AviationStack API key (free tier: 500 req/month) — sign up at [aviationstack.com](https://aviationstack.com/)
2. AgentMail inbox for receiving forwarded booking confirmations
3. `curl` installed

## Configuration

**API Key**: Set `AVIATIONSTACK_API_KEY` in `~/.hermes/.env` or export it in your shell. Never hardcode the key into scripts or commit it to source control.

**AgentMail Inbox**: Set `AGENTMAIL_INBOX` to the address where you'll forward airline booking confirmations. The skill polls this inbox for new itineraries.

## AviationStack API Endpoints

### Base URL
```
https://api.aviationstack.com/v1/flights
```

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `access_key` | API key (required) | (your key) |
| `flight_iata` | Flight number (IATA) | `UA123` |
| `flight_icao` | Flight number (ICAO) | `UAL123` |
| `dep_iata` | Departure airport | `SFO` |
| `arr_iata` | Arrival airport | `OGG` |
| `dep_icao` | Departure airport (ICAO) | `KSFO` |
| `arr_icao` | Arrival airport (ICAO) | `PHOG` |
| `airline_iata` | Airline code | `UA` |
| `flight_status` | Filter by status | `active`, `landed`, `scheduled`, `cancelled` |
| `date` | Flight date | `2026-04-05` |

### Example Calls

```bash
# Track a specific flight
curl -s "https://api.aviationstack.com/v1/flights?access_key=$AVIATIONSTACK_API_KEY&flight_iata=UA1749"

# All flights SFO → OGG today
curl -s "https://api.aviationstack.com/v1/flights?access_key=$AVIATIONSTACK_API_KEY&dep_iata=SFO&arr_iata=OGG"

# All United flights today
curl -s "https://api.aviationstack.com/v1/flights?access_key=$AVIATIONSTACK_API_KEY&airline_iata=UA&date=2026-04-05"

# Active flights only
curl -s "https://api.aviationstack.com/v1/flights?access_key=$AVIATIONSTACK_API_KEY&flight_iata=UA1749&flight_status=active"
```

### Response Structure

Key fields in the response:
- `flight_status`: `scheduled`, `active`, `landed`, `cancelled`, `diverted`, `incident`
- `departure.gate`, `departure.terminal`, `departure.delay` (minutes)
- `arrival.gate`, `arrival.terminal`, `arrival.baggage`, `arrival.delay`
- `aircraft.registration` — tail number
- `flight.codeshared` — if this is a codeshare, the actual operating flight
- `departure.scheduled`, `departure.estimated`, `departure.actual` — ISO timestamps

### Free Tier Limitations
- 500 requests per month
- HTTP only (no HTTPS) — use `http://` not `https://` for the API
- No live position data (use OpenSky Network for that)
- Limited to current day + near-future schedules

## Email Parsing

When an airline confirmation email arrives in your AgentMail inbox:

1. Use AgentMail tools to list threads/messages in the inbox
2. Look for emails with subjects like:
   - "Your itinerary" / "Flight confirmation" / "Booking confirmed"
   - "Change to your trip" / "Gate change" / "Flight schedule update"
3. Extract:
   - **Flight numbers** (e.g., UA 1234, UA 5678)
   - **Dates** (departure and return)
   - **Airports** (origin and destination, IATA codes)
   - **Confirmation code / PNR** (6-character alphanumeric)
   - **Times** (scheduled departure/arrival)

## Typical Workflow

### On-Demand Flight Check

```bash
curl -s "https://api.aviationstack.com/v1/flights?access_key=$AVIATIONSTACK_API_KEY&flight_iata=UA1749" | \
python3 -c "
import json, sys
data = json.load(sys.stdin)
for f in data.get('data', []):
    dep = f['departure']
    arr = f['arrival']
    status = f['flight_status']
    print(f\"{f['flight']['iata']} — {status}\")
    print(f\"  Departure: {dep['airport']} ({dep['iata']})\")
    print(f\"    Terminal: {dep.get('terminal', 'N/A')}, Gate: {dep.get('gate', 'N/A')}\")
    print(f\"    Scheduled: {dep['scheduled']}\")
    if dep.get('delay'): print(f\"    Delay: {dep['delay']} min\")
    print(f\"  Arrival: {arr['airport']} ({arr['iata']})\")
    print(f\"    Terminal: {arr.get('terminal', 'N/A')}, Gate: {arr.get('gate', 'N/A')}\")
    print(f\"    Scheduled: {arr['scheduled']}\")
    if arr.get('baggage'): print(f\"    Baggage: {arr['baggage']}\")
    if arr.get('delay'): print(f\"    Delay: {arr['delay']} min\")
    # Handle codeshare info
    cs = f.get('flight', {}).get('codeshared')
    if cs:
        print(f\"  Operated as: {cs['airline_iata']}{cs['flight_number']} ({cs['airline_name']})\")
    print()
"
```

### Cron Monitoring on Travel Day

Create a cron job that:
1. Checks all upcoming flights for the user (stored list or from recent emails)
2. Compares current gate/delay status to last known state
3. Alerts only on **changes** (gate change, new delay, status change)

Polling frequency: every 30 minutes from 4 hours before departure until wheels up. The free tier is 500 requests/month — plan polling carefully.

### Suggested Route File Format

For personal tracking, keep a small file (e.g. `~/.hermes/travelogue/<trip>/flights.json`) with the routes you care about:

```json
[
  { "date": "2026-04-05", "flight": "UA1749", "from": "SFO", "to": "OGG" },
  { "date": "2026-04-12", "flight": "UA1746", "from": "OGG", "to": "SFO" }
]
```

The cron prompt can read this file to know what to poll.

## Common IATA Airport Codes

| Code | Airport | City |
|------|---------|------|
| SFO | San Francisco International | San Francisco, CA |
| LAX | Los Angeles International | Los Angeles, CA |
| SEA | Seattle-Tacoma International | Seattle, WA |
| DEN | Denver International | Denver, CO |
| OGG | Kahului Airport | Maui, HI |
| HNL | Daniel K. Inouye Intl | Honolulu, Oahu, HI |
| KOA | Kona International | Big Island, HI |
| LIH | Lihue Airport | Kauai, HI |
| IAD | Dulles International | Washington DC area |
| EWR | Newark Liberty | New Jersey |
| ORD | O'Hare International | Chicago, IL |

## Common Airline IATA Codes

| Code | Airline |
|------|---------|
| UA | United Airlines |
| HA | Hawaiian Airlines |
| AS | Alaska Airlines |
| WN | Southwest Airlines |
| DL | Delta Air Lines |
| AA | American Airlines |
| B6 | JetBlue |
| NK | Spirit Airlines |

## Pitfalls

1. **HTTP only** — AviationStack free tier requires `http://`, not `https://`. Using HTTPS returns auth errors.
2. **Codeshares** — The API returns both the marketed flight and the actual operating flight. Always check `flight.codeshared` for the real flight number.
3. **Rate limits** — 500 req/month on free tier. Don't poll more than every 30 min on travel days.
4. **Time zones** — All timestamps are UTC. Convert to the relevant local time zone (HST = UTC-10 for Hawaii, PT = UTC-8, ET = UTC-5, etc.).
5. **Gate null values** — Gates may be null until 2-3 hours before departure. This is normal — don't alert on it.
6. **Historical data** — Free tier doesn't support historical flight lookups beyond scheduled data.
