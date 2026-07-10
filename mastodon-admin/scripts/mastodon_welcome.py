#!/usr/bin/env python3
"""Mastodon new user welcome bot for dmv.community.

Finds newly approved local accounts that haven't been welcomed yet,
sends them a personalized DM with the welcome message from Jason's
Obsidian vault, and tracks welcomed users in a state file to avoid
duplicate messages.

Exit codes: always 0 (never blocks the cron job)
Output: JSON on stdout
"""

import json
import os
import time
import urllib.request
import urllib.error
import uuid
from datetime import datetime, timezone
from pathlib import Path

INSTANCE = "dmv.community"
API_BASE = f"https://{INSTANCE}/api/v1"
TOKEN_FILE = os.path.expanduser("~/.hermes/secrets/mastodon_token")
STATE_FILE = os.path.expanduser("~/.hermes/state/mastodon_welcomed.json")
ADMIN_ACCOUNT_ID = os.environ.get("MASTODON_ADMIN_ID", "")  # Set to your account ID - skip welcoming yourself

# Only welcome accounts created within this many days.
# Prevents sending belated welcomes to old accounts that were never tracked.
MAX_ACCOUNT_AGE_DAYS = 7

WELCOME_MESSAGE = """@{username} Welcome to DMV.Community! Glad to have you here!

Check out the About page at https://dmv.community/about, and the wiki at https://wiki.dmv.community!

If you are new to Mastodon, I recommend reading Roma's Mastodon Starter Pack: https://blog.kizu.dev/my-mastodon-starter-pack/

Also check out my pinned posts on my profile for regional accounts to follow, and follow @FediFollows@social.growyourown.services and @FediTips@social.growyourown.services for more accounts to follow and tips on making the most of Mastodon and the fediverse!

(This is an automated welcome message from your instance admin 😊)"""


def load_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()


def api_request(endpoint, method="GET", fields=None):
    url = f"{API_BASE}/{endpoint}"
    token = load_token()
    headers = {"Authorization": f"Bearer {token}"}

    if fields:
        boundary = uuid.uuid4().hex
        body = b""
        for key, value in fields:
            body += f"--{boundary}\r\n".encode()
            body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
            body += f"{value}\r\n".encode()
        body += f"--{boundary}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode()), resp.status
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            return json.loads(error_body), e.code
        except json.JSONDecodeError:
            return {"error": error_body[:500]}, e.code
    except Exception as e:
        return {"error": str(e)}, 0


def load_welcomed():
    """Load the set of account IDs that have already been welcomed."""
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        with open(STATE_FILE) as f:
            data = json.load(f)
            return set(data.get("welcomed", []))
    except (json.JSONDecodeError, IOError):
        return set()


def save_welcomed(welcomed_ids):
    """Save the set of welcomed account IDs to the state file."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({
            "welcomed": sorted(welcomed_ids),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)


def send_welcome_dm(username, account_id):
    """Send a welcome DM to a newly approved user."""
    message = WELCOME_MESSAGE.format(username=username)

    resp, code = api_request("statuses", method="POST", fields=[
        ("status", message),
        ("visibility", "direct"),
        ("language", "en"),
    ])

    return code, resp


def main():
    # Fetch recently approved local accounts
    # Using admin/accounts endpoint with status=active (approved) and origin=local
    accounts_data, code = api_request(
        "admin/accounts?origin=local&status=active&limit=40"
    )

    if code != 200 or not isinstance(accounts_data, list):
        print(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": f"Failed to fetch accounts: HTTP {code}",
            "total_active": 0,
            "new_welcomed": 0,
            "already_welcomed": 0,
            "skipped": 0,
            "details": [],
        }, indent=2))
        return

    # Load state
    welcomed = load_welcomed()
    details = []
    new_welcomed = 0
    already_welcomed = 0
    skipped = 0

    for account in accounts_data:
        account_id = account.get("id", "")
        username = account.get("username", "unknown")
        approved = account.get("approved", False)

        # Skip if not approved yet
        if not approved:
            skipped += 1
            continue

        # Skip accounts older than MAX_ACCOUNT_AGE_DAYS
        # (prevents belated welcomes to old accounts not in state file)
        created_at = account.get("created_at", "")
        if created_at:
            try:
                created_dt = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                )
                age_days = (datetime.now(timezone.utc) - created_dt).days
                if age_days > MAX_ACCOUNT_AGE_DAYS:
                    skipped += 1
                    continue
            except (ValueError, TypeError):
                pass  # If we can't parse the date, don't skip

        # Skip admin account
        if account_id == ADMIN_ACCOUNT_ID:
            skipped += 1
            continue

        # Skip if already welcomed
        if account_id in welcomed:
            already_welcomed += 1
            continue

        # Send welcome DM
        time.sleep(2)  # Rate limit
        dm_code, dm_resp = send_welcome_dm(username, account_id)

        if dm_code == 200:
            welcomed.add(account_id)
            new_welcomed += 1
            details.append({
                "username": username,
                "account_id": account_id,
                "action": "welcomed",
                "dm_id": dm_resp.get("id", ""),
                "dm_url": dm_resp.get("url", ""),
            })
        else:
            details.append({
                "username": username,
                "account_id": account_id,
                "action": "failed",
                "error": str(dm_resp.get("error", f"HTTP {dm_code}")),
            })

    # Save updated state
    save_welcomed(welcomed)

    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_active": len(accounts_data),
        "new_welcomed": new_welcomed,
        "already_welcomed": already_welcomed,
        "skipped": skipped,
        "details": details,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()