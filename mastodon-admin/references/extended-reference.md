# Extended Reference: Cron Jobs

This file contains detailed material moved from `SKILL.md` for progressive disclosure. Load it when the task needs one of the sections listed below.

## Cron Jobs

Three hourly cron jobs use the scripts in this skill:

| Job | Script | Job ID | Schedule | Deliver |
|-----|--------|--------|----------|---------|
| Report Monitor | `mastodon_reports.py` | `eee50a40770f` | `0 * * * *` | Discord (origin) |
| Signup Monitor | `mastodon_signups.py` | `e5a5c0362182` | `0 * * * *` | Discord (origin) |
| Welcome Bot | `mastodon_welcome.py` | `bc88499f661a` | `0 * * * *` | Discord (origin) |

All three use Gemini 2.5 Flash (cheap, fast for JSON formatting) and the
`terminal` toolset. All go `[SILENT]` when there's nothing to report.

## Pitfalls

- **CRITICAL: Cron script paths.** Cron jobs look for scripts in `~/.hermes/scripts/`, NOT in the skill's `scripts/` directory. When creating or updating a script in this skill, ALWAYS copy it to both locations:
  ```bash
  cp ~/.hermes/skills/social-media/mastodon-admin/scripts/mastodon_reports.py ~/.hermes/scripts/mastodon_reports.py
  ```
  Failure to do this causes "Script not found" errors at runtime.

- **write_file tool mangles expanduser lines.** The `skill_manage(action='write_file')` tool sometimes truncates `os.path.expanduser("~/.hermes/secrets/mastodon_token")` to `os.path.expanduser("~/.hermes/secrets/mastodon_tok` or similar. Always verify scripts after writing by running `python3 -c "import ast; ast.parse(open('path').read())"` or executing the script with `--help`. Fix any mangled lines with `patch` before relying on the script.

- **Shell quoting with `$(cat)`.** The token subshell expansion breaks inside nested python3 `-c` strings. Always pipe curl to a temp file, then parse separately. Alternatively, write a standalone Python script that reads the token file directly with `open()`.

- **Approve endpoint returns 403 for already-approved accounts.** The `/admin/accounts/{id}/approve` endpoint returns `403 {"error": "This action is not allowed"}` when the account is already approved. This is NOT a permission error — treat 403 on approve as "already done" (success). The same applies to the reject endpoint for already-rejected accounts.

- **Rate limiting on bulk operations.** When approving/rejecting many accounts in sequence, space calls 2+ seconds apart. Without delays, the API returns cascading 403s. The `mastodon_signups.py` script handles this with `time.sleep(2)` between actions and retry logic.

- **Accounts with `approved=True` still appear in `status=pending` results.** Mastodon 4.6 returns already-approved accounts in the pending list. The `approved` field must be checked **before classification**, not just before the approve API call — otherwise already-approved accounts that look like spam (non-DMV location, disposable email) will be re-reported as rejections or escalations every cron cycle. The `mastodon_signups.py` script now skips any account with `approved=True` at the top of the loop, before `classify_account()` runs. If you edit the script, preserve this early-skip pattern.

- **Welcome bot must filter by account age, not just state file.** The welcome bot fetches *all* active local accounts and welcomes anyone not in the state file. Accounts that joined before the bot existed will never be in the state file and will get belated welcomes (e.g., a user from September 2025 got a welcome DM in June 2026). The `mastodon_welcome.py` script now skips accounts where `created_at` is older than `MAX_ACCOUNT_AGE_DAYS` (7 days). If you edit the script, preserve this age check.

- **Signup classifier must cover non-DMV US locations, not just international.** The `NON_DMV_LOCATIONS` list originally only had international locations (UK, Germany, etc.). Spam accounts mentioning "San Diego" or "New York" fell through to "escalate" instead of being auto-rejected. The list now includes all 50 US states (with abbreviations) and major cities outside the DMV area. When adding new locations, ensure they don't collide with DMV-area place names (e.g., "Portland" alone is ambiguous — use "Portland ME" for Maine).

- **Email domain spam check must use substring matching, not just exact set membership.** The original `SPAM_EMAIL_DOMAINS` set only caught exact domain matches. Disposable email services have many variants (e.g., `cc.spammail.free.nf` contains "spammail" but isn't in the set). The `SPAM_EMAIL_DOMAIN_SUBSTRINGS` list checks for spam keywords anywhere in the domain. When you encounter a new disposable domain that was missed, add both the specific domain AND any recognizable substring to the respective lists.

- **Distinguishing auto-rejected from escalated in cron responses.** The signup monitor's output uses emoji prefixes: 🚫 = auto-rejected (script already called the reject API), ⚠️ = escalated (needs Jason's decision). When Jason replies "Reject" to a 🚫 message, the account is already rejected — confirm this and suggest adding the email domain to the blocklist instead of calling the reject API again. When Jason replies "Reject" to a ⚠️ message, call the reject API manually with the account ID from the admin URL.

- **Always patch both script copies.** The signup script lives in two places: `~/.hermes/scripts/mastodon_signups.py` (what the cron job runs) and `~/.hermes/skills/social-media/mastodon-admin/scripts/mastodon_signups.py` (the skill source). When adding domains, fixing bugs, or changing logic, update both. The skill copy is the canonical source; the scripts copy is the runtime copy.

- **Username as location signal — design tradeoffs (see `references/username-signal-design.md`).** The signup classifier accepts `DMV_USERNAME_PATTERNS` matches (e.g. `vegan_baltimore`, `nova_writer`, `arlington_dev`) as approval signal when invite text is silent. Spammer-gameable by design, so the token list is intentionally conservative: full city names only, no state abbreviations (`md`/`va`/`dc`), no common surnames (`fairfax`, `shaw`, `bowie`, `richmond`, `norfolk`, `vienna`). Order of precedence matters: non-DMV location in invite text still rejects even if username is DMV, because invite text reflects stated intent. When adding tokens, follow the rules-of-thumb documented in the source comment above `DMV_USERNAME_PATTERNS` AND summarized in `references/username-signal-design.md`.

- **Always unit-test classifier changes before deploying.** When editing `mastodon_signups.py` (new tokens, new reject paths, new approval logic), run a Python import + at least 6 representative test cases before declaring done. Pattern:
  ```python
  import importlib.util, os
  spec = importlib.util.spec_from_file_location("ms", os.path.expanduser("~/.hermes/scripts/mastodon_signups.py"))
  ms = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(ms)
  
  test_cases = [
      ("description", {"id": "...", "username": "...", "email": "...", "invite_request": "..."}, "expected_action"),
      # ...
  ]
  for desc, acct, expected in test_cases:
      result = ms.classify_account(acct)
      assert result["action"] == expected, f"{desc}: got {result['action']}, expected {expected}"
  ```
  Cover at minimum: (1) the canonical case that triggered the change, (2) the spam-rejection path, (3) the non-DMV-text-overrides-username path, (4) the disposable-email-overrides-username path, (5) a legitimate non-DMV domain (gmail.com) NOT flagged, (6) an ambiguous-name domain (e.g. `moneymutual.com`) NOT flagged by the new TLD substring rule. This pattern caught the `write_file` mangling bug and the pre-existing `\bin\b`/`\bhi\b` false positives during the 2026-07-09 username-signal work.

- **Email/word collisions in `NON_DMV_LOCATIONS`.** The list contains entries like `\bin\b` (Indiana) and `\bhi\b` (Hawaii) that match common English words ("in the area", "Hi all"). Pre-existing limitation, separate from the username-classifier work. Symptom: a signup whose only matching token is a 2-letter state abbreviation in their invite text gets auto-rejected with reason `Non-DMV location: in` etc. Likely fix: tighten patterns to `(?<![a-z])\bin(?![a-z])` style or move 2-letter state abbreviations into a separate "weak signals" tier that doesn't block username approval.

- **Suspend is severe.** Mastodon suspension deletes the user's posts and is only reversible within ~30 days. Use `silence` for first offenses when appropriate.

- **CRITICAL: Token lacks admin scopes — 403 on all admin endpoints.** If
  `/api/v1/accounts/verify_credentials` returns 200 (token valid) but
  `/api/v1/admin/reports` returns `403 {"error":"This action is outside the
  authorized scopes"}`, the token was created without admin OAuth scopes.
  The user being an Owner/Admin on the instance is NOT the same as the
  OAuth token having admin scopes.

  **Most common cause:** The Mastodon posting skill's `mastodon_reauthorize.py`
  script was used to fix a posting permission issue, and it overwrote the
  admin-scoped token with a `read write follow push` token. The posting
  and admin skills share the same `~/.hermes/secrets/mastodon_token` file.
  Always use the unified scope set when re-authorizing: `read write admin:read
  admin:write admin:read:reports admin:write:reports admin:read:accounts
  admin:write:accounts`.

  Fix: register a new OAuth app with the FULL scope set (admin + read/write)
  and re-authorize. Do NOT use `mastodon_reauthorize.py` to fix admin 403s —
  it registers with posting-only scopes and will make the problem worse.

  1. Register a new app with ALL scopes:
     ```bash
     curl -sS -X POST "https://dmv.community/api/v1/apps" \
       -F "client_name=Hermes Agent Admin" \
       -F "redirect_uris=urn:ietf:wg:oauth:2.0:oob" \
       -F "scopes=read write admin:read admin:write admin:read:reports admin:write:reports admin:read:accounts admin:write:accounts" \
       -F "website=https://hermes-agent.nousresearch.com"
     ```
     Note the `client_id` and `client_secret` from the response.

  2. Have the user visit this URL in a browser to authorize:
     ```
     https://dmv.community/oauth/authorize?client_id=CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=read+write+admin:read+admin:write+admin:read:reports+admin:write:reports+admin:read:accounts+admin:write:accounts&response_type=code
     ```

  3. Exchange the authorization code for a token — **save directly to file, not
     via curl stdout, to avoid Hermes output masking**:
     ```bash
     curl -sS -X POST "https://dmv.community/oauth/token" \
       -F "client_id=CLIENT_ID" \
       -F "client_secret=CLIENT_SECRET" \
       -F "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
       -F "grant_type=authorization_code" \
       -F "code=CODE_FROM_USER" \
       -F "scope=read write admin:read admin:write admin:read:reports admin:write:reports admin:read:accounts admin:write:accounts" \
       > /tmp/mastodon_token.json
     python3 -c "
     import json, os
     data = json.load(open('/tmp/mastodon_token.json'))
     os.rename(os.path.expanduser('~/.hermes/secrets/mastodon_token'),
               os.path.expanduser('~/.hermes/secrets/mastodon_token.bak'))
     with open(os.path.expanduser('~/.hermes/secrets/mastodon_token'), 'w') as f:
         f.write(data['access_token'])
     print('Token saved.')
     "
     ```

  4. Verify both admin AND posting access:
     ```bash
     # Admin scope check
     curl -sS "https://dmv.community/api/v1/admin/reports?limit=1" \
       -H "Authorization: Bearer $(cat ~/.hermes/secrets/mastodon_token)"
     ```
     A 200 with a JSON array means the token has admin scopes.
     ```bash
     # Posting scope check
     python3 ~/.hermes/skills/social-media/mastodon/scripts/mastodon_post.py --dry-run --status "test"
     ```
     A character count (not 403) means `write:statuses` is present.

  NOTE: OAuth authorization codes are ONE-TIME USE. If the token exchange
  fails, the code is consumed and you need a new one from the user. Always
  pipe the exchange response to a file and parse the token from there —
  Hermes output masking will truncate or redact token values in tool output.
- **Remote accounts.** You can only `suspend`/`silence` local accounts. For remote accounts, the action federates the moderation decision but the remote instance controls the actual account.
- **Always resolve reports after acting.** Unresolved reports pile up and make it hard to track what's been handled.
- **Don't suspend the admin.** Set your account ID via `MASTODON_ADMIN_ID` env var. Never moderate this account.
