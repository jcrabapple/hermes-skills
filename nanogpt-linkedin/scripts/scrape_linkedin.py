#!/usr/bin/env python3
"""
NanoGPT LinkedIn Scraper — convenience CLI.

Scrape LinkedIn profile data by URL (name, title, company, email, education, etc.).

Usage:
  # Single profile
  ./scrape_linkedin.py https://www.linkedin.com/in/elonmusk

  # Multiple profiles
  ./scrape_linkedin.py https://www.linkedin.com/in/satyanadella https://www.linkedin.com/in/jeffweiner08

  # With cost cap
  ./scrape_linkedin.py https://www.linkedin.com/in/satyanadella --max-charge 0.05

  # Save raw JSON
  ./scrape_linkedin.py https://www.linkedin.com/in/elonmusk --output results.json

  # Raw JSON to stdout
  ./scrape_linkedin.py https://www.linkedin.com/in/elonmusk --raw
"""

import json
import os
import sys
import urllib.request
import urllib.error

NANOGPT_BASE = "https://nano-gpt.com/api/v1"
ENV_FILE = os.path.expanduser("~/.config/nanogpt/.env")


def load_api_key() -> str:
    """Load NanoGPT API key from env var or ~/.config/nanogpt/.env."""
    key = os.environ.get("NANOGPT_API_KEY")
    if key:
        return key
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NANOGPT_API_KEY="):
                    return line.split("=", 1)[1]
    print("ERROR: NANOGPT_API_KEY not found. Set it as an env var or in ~/.config/nanogpt/.env", file=sys.stderr)
    sys.exit(1)


def scrape_linkedin(profile_urls: list[str], api_key: str,
                    max_charge: float = None, result_limit: int = None,
                    wait: int = 180) -> dict:
    """Call the NanoGPT LinkedIn scraper API and return the response."""
    payload = {
        "profileUrls": profile_urls,
        "waitForFinishSecs": wait,
    }
    if max_charge is not None:
        payload["maxTotalChargeUsd"] = max_charge
    if result_limit is not None:
        payload["resultLimit"] = result_limit

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{NANOGPT_BASE}/linkedin/profile",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=wait + 30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")
        return {"error": f"HTTP {e.code}: {err_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def pretty_print(data: dict):
    """Print results in a readable format."""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return

    items = data.get("items", [])
    usage = data.get("usage", {}) or {}
    cost = f"${usage.get('actualCostUsd', '?')}"

    print(f"🔗 Found {len(items)} LinkedIn profile(s)  |  Cost: {cost}\n")

    for i, profile in enumerate(items, 1):
        print(f"{'='*65}")
        name = profile.get("name", "Unknown")
        headline = profile.get("headline", "")
        print(f"  #{i} — {name}")
        print(f"{'='*65}")

        if headline:
            print(f"  📝 {headline}")

        title = profile.get("jobTitle", "")
        company = profile.get("company", "")
        if title and company and company != "Not specified":
            print(f"  💼 {title} @ {company}")
        elif title:
            print(f"  💼 {title}")

        location = profile.get("location", "")
        if location and location != "Not specified":
            print(f"  📍 {location}")

        industry = profile.get("industry", "")
        if industry and industry != "Not specified":
            print(f"  🏢 {industry}")

        education = profile.get("education", "")
        if education and education != "Not specified":
            print(f"  🎓 {education}")

        email = profile.get("email")
        if email:
            print(f"  📧 {email}")

        phone = profile.get("phone")
        if phone:
            print(f"  📞 {phone}")

        website = profile.get("website", "")
        if website:
            print(f"  🌐 {website}")

        linkedin_url = profile.get("linkedinUrl", "")
        if linkedin_url:
            print(f"  🔗 {linkedin_url}")

        quality = profile.get("dataQuality", "")
        if quality:
            print(f"  ⭐ Data quality: {quality}")

        scraped = profile.get("scrapedAt", "")
        if scraped:
            print(f"  📅 Scraped: {scraped}")

        print()

    # Usage summary
    if usage:
        events = usage.get("chargedEventCounts", {})
        preflight = usage.get("preflightEventPricesUsd", {})
        event_prices = usage.get("eventPricesUsd", {})
        if events:
            detail = " + ".join(f"{k}={v}" for k, v in events.items() if v)
            print(f"📊 Cost: {cost}  |  {detail}")
        estimated = usage.get("estimatedMaxChargeUsd")
        if estimated:
            print(f"   Estimated max: ${estimated}")

    # Metadata
    metadata = data.get("metadata", {})
    if metadata:
        est = metadata.get("estimatedProfiles")
        if est:
            print(f"   Profiles requested: {est}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape LinkedIn profiles via NanoGPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://www.linkedin.com/in/elonmusk
  %(prog)s https://www.linkedin.com/in/satyanadella https://www.linkedin.com/in/jeffweiner08
  %(prog)s https://www.linkedin.com/in/elonmusk --max-charge 0.05
  %(prog)s https://www.linkedin.com/in/elonmusk --output results.json
        """,
    )

    parser.add_argument("urls", nargs="+", help="LinkedIn profile URLs")
    parser.add_argument("--max-charge", type=float, help="Max cost in USD")
    parser.add_argument("--results", type=int, help="Max profiles to return")
    parser.add_argument("--wait", type=int, default=180, help="Max wait seconds (default: 180)")
    parser.add_argument("--output", "-o", help="Write raw JSON response to file")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON instead of formatted output")

    args = parser.parse_args()

    # Validate URLs
    for u in args.urls:
        if "linkedin.com/in/" not in u:
            print(f"WARNING: '{u}' doesn't look like a LinkedIn profile URL", file=sys.stderr)

    api_key = load_api_key()

    print(f"🔍 Scraping {len(args.urls)} LinkedIn profile(s)... (waiting up to {args.wait}s)")
    data = scrape_linkedin(
        args.urls,
        api_key,
        max_charge=args.max_charge,
        result_limit=args.results,
        wait=args.wait,
    )

    if "error" in data:
        print(f"\n❌ Error: {data['error']}")
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved raw response to {args.output}")

    if args.raw:
        print(json.dumps(data, indent=2))
    else:
        pretty_print(data)


if __name__ == "__main__":
    main()
