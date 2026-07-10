#!/usr/bin/env python3
"""Re-register the Mastodon OAuth app with a web-client name.

Two-step flow:
  1. Run without --code → registers app, prints auth URL
  2. Visit URL, authorize, run with --code YOUR_CODE
"""

import argparse, json, sys, subprocess
from pathlib import Path
from urllib.parse import urlencode

INSTANCE = "dmv.community"
API = f"https://{INSTANCE}/api/v1"
TOKEN_FILE = Path.home() / ".hermes" / "secrets" / "mastodon_token"
APP_FILE = Path.home() / ".hermes" / "secrets" / "mastodon_app_reg.json"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
SCOPES = "read write follow push"
CLIENT_NAME = "Mastodon Web"


def sh(*args):
    """Run a command, return stdout, fail on non-zero exit."""
    r = subprocess.run(list(args), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ERROR: {' '.join(args)}", file=sys.stderr)
        print(r.stderr, file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()


def register_app():
    print(f"Registering new OAuth app on {INSTANCE} as '{CLIENT_NAME}'...")
    out = sh(
        "curl", "-sS", "-X", "POST", f"{API}/apps",
        "-F", f"client_name={CLIENT_NAME}",
        "-F", f"redirect_uris={REDIRECT_URI}",
        "-F", f"scopes={SCOPES}",
        "-F", f"website=https://{INSTANCE}",
    )
    return json.loads(out)


def exchange_code(app, code):
    print("Exchanging authorization code for access token...")
    out = sh(
        "curl", "-sS", "-X", "POST", f"https://{INSTANCE}/oauth/token",
        "-F", f"client_id={app['client_id']}",
        "-F", f"client_secret={app['client_secret']}",
        "-F", f"redirect_uri={REDIRECT_URI}",
        "-F", "grant_type=authorization_code",
        "-F", f"code={code}",
        "-F", f"scope={SCOPES}",
    )
    result = json.loads(out)
    if "access_token" not in result:
        print(f"ERROR: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)
    return result["access_token"]


def verify_token(token):
    print("Verifying token...")
    out = sh(
        "curl", "-sS",
        "-H", f"Authorization: Bearer {token}",
        f"{API}/accounts/verify_credentials",
    )
    acct = json.loads(out)
    if "error" in acct:
        print(f"ERROR: {acct['error']}", file=sys.stderr)
        sys.exit(1)
    print(f"  Verified as: @{acct['username']}@{INSTANCE}")


def main():
    p = argparse.ArgumentParser(description="Re-register Mastodon OAuth app")
    p.add_argument("--code", metavar="CODE", help="Authorization code from browser")
    args = p.parse_args()

    if args.code:
        if not APP_FILE.exists():
            print("ERROR: Run without --code first to register the app.", file=sys.stderr)
            sys.exit(1)
        app = json.loads(APP_FILE.read_text())
        token = exchange_code(app, args.code)
        verify_token(token)
        TOKEN_FILE.write_text(token)
        print(f"\nToken saved to {TOKEN_FILE}")
        print("Posts will now show 'via Mastodon Web' instead of 'via Hermes Agent'.")
        APP_FILE.rename(APP_FILE.with_suffix(".json.old"))
    else:
        app = register_app()
        APP_FILE.write_text(json.dumps(app, indent=2))
        auth_url = (
            f"https://{INSTANCE}/oauth/authorize?"
            + urlencode({
                "client_id": app["client_id"],
                "redirect_uri": REDIRECT_URI,
                "scope": SCOPES,
                "response_type": "code",
            })
        )
        print()
        print("=" * 60)
        print("Open this URL in your browser and authorize the app:")
        print()
        print(f"  {auth_url}")
        print()
        print("After authorizing, you'll get a code.")
        print("Then run:")
        print(f"  python3 {__file__} --code YOUR_CODE")
        print("=" * 60)


if __name__ == "__main__":
    main()
