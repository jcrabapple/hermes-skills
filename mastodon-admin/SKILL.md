---
name: mastodon-admin
description: >-
  Administer the dmv.community Mastodon instance: view and manage user reports,
  suspend/silence rule-breaking accounts, resolve reports, and escalate
  ambiguous cases to the instance owner. Use when checking or acting on
  Mastodon moderation reports.
tags:
  - mastodon
  - admin
  - moderation
  - reports
triggers:
  - mastodon admin
  - mastodon reports
  - mastodon moderation
  - check mastodon reports
  - mastodon suspend
---

# Mastodon Admin Skill

Moderate the **dmv.community** Mastodon instance via the admin API. The access
token at `~/.hermes/secrets/mastodon_token` requires admin-level OAuth scopes
(`admin:read:reports`, `admin:write:reports`, `admin:read:accounts`,
`admin:write:accounts`). If the token was created without these scopes, admin
endpoints return 403 — see **Pitfalls** for the regeneration procedure.

## Configuration

| Key | Value |
|-----|-------|
| Instance | `dmv.community` |
| API base | `https://dmv.community/api/v1/admin/` |
| Token file | `~/.hermes/secrets/mastodon_token` |
| Admin account | `@admin@your.instance` (ID: `your-account-id`) |
| Instance rules | 9 rules (see below) |

## Authentication

See `references/api-scopes-and-quirks.md` for the full token scope list, endpoint
compatibility matrix, and known API quirks (403 on already-approved accounts,
rate limiting, shell quoting, write_file mangling).

```bash
TOK="$(cat ~/.hermes/secrets/mastodon_token)"
```

All admin API calls use `Authorization: Bearer $TOK`.

**Shell quoting gotcha:** The `$(cat ...)` subshell expansion breaks when
nested inside python3 `-c` strings that also use double quotes. Always pipe
curl output to a temp file first, then parse with python3:

```bash
curl -sS "https://dmv.community/api/v1/admin/reports" \
  -H "Authorization: Bearer $TOK" > /tmp/reports.json
python3 -c "import json; data=json.load(open('/tmp/reports.json')); ..."
```

## Instance Rules

| ID | Rule |
|----|------|
| 1 | Sexually explicit or violent media must be marked as sensitive |
| 2 | No racism, sexism, homophobia, transphobia, xenophobia, or casteism |
| 3 | No incitement of violence or promotion of violent ideologies |
| 4 | No harassment, dogpiling or doxxing |
| 5 | No content illegal in the United States |
| 6 | Do not share intentionally false or misleading information |
| 7 | No spam or advertising |
| 8 | Do not sell AI-generated art or pass it off as your own creation |
| 9 | Do not post AI-generated music |

## API Endpoints

### List Reports

```bash
curl -sS "https://dmv.community/api/v1/admin/reports?resolved=false&limit=20" \
  -H "Authorization: Bearer $TOK" > /tmp/reports.json
```

**Query params:**
- `resolved` — `true`/`false` (filter by resolution status)
- `limit` — max 40 (default 20)
- `max_id` — pagination (older reports)
- `since_id` — pagination (newer reports)

**Report object structure:**
```json
{
  "id": "123",
  "action_taken": false,
  "action_taken_at": null,
  "category": "viilation" | "spam" | "other" | "legal",
  "comment": "Reporter's comment text",
  "forwarded": false,
  "created_at": "2026-01-01T00:00:00.000Z",
  "updated_at": "2026-01-01T00:00:00.000Z",
  "account": { "id": "...", "username": "...", "email": "...", "ip": "...", ... },
  "target_account": { "id": "...", "username": "...", "domain": "...", "account": {...}, ... },
  "assigned_account": { ... } | null,
  "action_taken_by_account": { ... } | null,
  "statuses": [ { "id": "...", "content": "...", "url": "...", ... } ],
  "rules": [ { "id": "1", "text": "..." } ]
}
```

Key fields:
- `account` — the reporter (who filed the report)
- `target_account` — the reported user (who was reported)
- `statuses` — array of reported statuses (posts)
- `rules` — which instance rules were cited
- `comment` — reporter's free-text explanation
- `category` — `violation`, `spam`, `other`, or `legal`

### Get Single Report

```bash
curl -sS "https://dmv.community/api/v1/admin/reports/$REPORT_ID" \
  -H "Authorization: Bearer $TOK"
```

### Assign Report to Self

```bash
curl -sS -X POST "https://dmv.community/api/v1/admin/reports/$REPORT_ID/assign_to_self" \
  -H "Authorization: Bearer $TOK"
```

### Unassign Report

```bash
curl -sS -X POST "https://dmv.community/api/v1/admin/reports/$REPORT_ID/unassign" \
  -H "Authorization: Bearer $TOK"
```

### Resolve Report

```bash
curl -sS -X POST "https://dmv.community/api/v1/admin/reports/$REPORT_ID/resolve" \
  -H "Authorization: Bearer $TOK"
```

### Reopen Report

```bash
curl -sS -X POST "https://dmv.community/api/v1/admin/reports/$REPORT_ID/reopen" \
  -H "Authorization: Bearer $TOK"
```

### Perform Account Action

This is the key endpoint for moderating users. Actions include warnings,
silencing, and suspension.

```bash
curl -sS -X POST "https://dmv.community/api/v1/admin/accounts/$ACCOUNT_ID/action" \
  -H "Authorization: Bearer $TOK" \
  -F "type=suspend" \
  -F "warning=0"
```

**Action types:**
| Type | Effect |
|------|--------|
| `silence` | User's posts are hidden from public timelines, only visible to followers |
| `suspend` | Account is permanently suspended (reversible within ~30 days via admin UI) |
| `disable` | Disable login (user can't sign in) |
| `none` | No action, just send a warning message (use with `warning=1`) |
| `sensitive` | Force all user's media as sensitive |

**Parameters:**
- `type` (required) — one of: `silence`, `suspend`, `disable`, `sensitive`, `none`
- `warning` — `0` (no warning email) or `1` (send warning email to user)
- `text` — optional warning message text (sent to user if `warning=1`)
- `report_id` — optional: link this action to a specific report ID
- `send_email_notification` — `true`/`false` (whether to email the user)

### Get Admin Account Info

```bash
curl -sS "https://dmv.community/api/v1/admin/accounts/$ACCOUNT_ID" \
  -H "Authorization: Bearer $TOK"
```

Returns detailed account info including `suspended`, `silenced`, `sensitized`,
`disabled`, `email`, `ip`, `role`, etc.

### List Admin Accounts

```bash
curl -sS "https://dmv.community/api/v1/admin/accounts?origin=local&limit=20" \
  -H "Authorization: Bearer $TOK"
```

**Filters:** `origin` (`local`/`remote`), `status` (`active`/`suspended`/`silenced`/`disabled`/`pending`)

## Moderation Decision Framework

When reviewing reports, classify each into one of these categories:

### Auto-Action (Clear Violations)

Act immediately without consulting Jason:

| Rule | Violation Examples | Action |
|------|-------------------|--------|
| 3 (violence) | Direct threats, inciting violence, promoting terrorism | `suspend` |
| 5 (illegal US) | CSAM, illegal weapons sales, drug trafficking | `suspend` |
| 2 (hate) | Slurs, targeted harassment based on protected characteristics | `silence` (first offense) or `suspend` (repeat/severe) |
| 4 (harassment/doxxing) | Posting someone's personal info, coordinated harassment | `silence` or `suspend` |
| 7 (spam) | Bot spam, commercial advertising, crypto scams | `suspend` |

**After acting:** Resolve the report with a comment documenting the action taken.

### Escalate to Jason (Ambiguous Cases)

Do NOT auto-act. Instead, send a notification to Jason with the report details.

| Scenario | Why Escalate |
|----------|-------------|
| Rule 1 (sensitive media) | Need to verify if media is actually explicit |
| Rule 6 (misinformation) | Hard to verify truthfulness automatically |
| Rule 8 (AI art) | Need judgment on whether art is being "sold" |
| Rule 9 (AI music) | Need judgment on whether music is AI-generated |
| Borderline hate speech | Context-dependent, may be political commentary |
| Reports with no rule cited | Need human judgment |
| Disputes between users | Both sides need review |
| Repeat reporter patterns | May be weaponizing reports |

**Escalation message format** (send to Jason via the cron job's delivery channel):

```
⚠️ MASTODON REPORT NEEDS REVIEW

Report ID: $ID
Category: $category
Reported user: @$target_acct
Reporter: @$reporter_acct
Rules cited: $rule_numbers
Comment: $comment

Reported status content:
$status_content

Link: https://dmv.community/admin/reports/$ID
```

### Dismiss (No Action Needed)

| Scenario | Action |
|----------|--------|
| Empty report with no comment and no statuses | Resolve with "No action needed - empty report" |
| Report is clearly a disagreement, not a violation | Resolve with "No violation - personal disagreement" |
| Reported content has been deleted by the user | Resolve with "Content removed by user" |

**Always resolve dismissed reports** with a comment explaining why.

## Helper Script

A Python monitoring script is available at `scripts/mastodon_reports.py`. It:

1. Fetches all unresolved reports
2. Classifies each report using the decision framework above
3. Auto-acts on clear violations (suspend/silence + resolve)
4. Outputs a JSON summary of actions taken and escalations needed
5. Returns exit code 0 always (never blocks the cron job)

Usage:
```bash
python3 ~/.hermes/skills/social-media/mastodon-admin/scripts/mastodon_reports.py
```

Output (JSON on stdout):
```json
{
  "timestamp": "2026-06-23T15:00:00Z",
  "total_reports": 3,
  "auto_actioned": 1,
  "escalated": 1,
  "dismissed": 1,
  "details": [
    {
      "report_id": "123",
      "action": "suspended",
      "target": "spam_bot@example.com",
      "reason": "Rule 7: spam"
    },
    {
      "report_id": "124",
      "action": "escalated",
      "target": "user@domain.com",
      "reason": "Ambiguous - AI art rule needs human review"
    }
  ]
}
```

## New User Welcome Bot

dmv.community has a welcome message stored in Jason's Obsidian vault at
`~/Documents/Obsidian Vault/General/DMV.Community welcome message.md`.

A monitoring script at `scripts/mastodon_welcome.py` sends this as a DM to
every newly approved local account from Jason's admin account.

### What It Does

1. Fetches all active local accounts from the admin API
2. **Skips accounts older than `MAX_ACCOUNT_AGE_DAYS` (7 days)** based on
   the `created_at` field — prevents belated welcomes to old accounts that
   predate the state file
3. Checks the state file at `~/.hermes/state/mastodon_welcomed.json` for
   accounts that have already been welcomed
4. Sends a personalized welcome DM (visibility=direct) to each new user,
   mentioning them so they get a notification
5. Records the account ID in the state file to prevent duplicate welcomes
6. Skips Jason's own admin account

### The Welcome Message

Sends as a direct message (DM) with `visibility=direct`. The message includes:
- Personal greeting with @username mention
- Links to the About page and wiki
- Link to Roma's Mastodon Starter Pack
- Recommendations to follow @FediFollows and @FediTips
- Note that it's automated from the instance admin

### State File

`~/.hermes/state/mastodon_welcomed.json` tracks which account IDs have been
welcomed. This survives across runs and prevents duplicate DMs.

### Running

```bash
python3 ~/.hermes/skills/social-media/mastodon-admin/scripts/mastodon_welcome.py
```

### DM API Details

DMs in Mastodon are just statuses with `visibility=direct`. To ensure the
recipient sees it in their notifications, mention them with `@username`:

```bash
curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer *** \
  -F "status=@newuser Welcome to DMV.Community! ..." \
  -F "visibility=direct"
```

**Pitfall:** DMs require the `write:statuses` scope (which the token has).
The recipient receives a notification because of the @mention, not because
of the direct visibility alone.

**Pitfall:** If a user hasn't confirmed their email or hasn't logged in yet,
the DM is still delivered to their inbox and will be visible when they first
log in.

## Signup Approval Assistant

dmv.community requires approval for new signups. The instance is restricted to
people in the **DMV area** (DC, Maryland, Virginia, and nearby regions).

A monitoring script at `scripts/mastodon_signups.py` handles this automatically:

### What It Does

1. Fetches all pending account registrations
2. Classifies each based on the invite request text:
   - **Approve**: Invite request mentions a DMV-area location (city, county, state, or "DMV")
   - **Reject**: Non-DMV location mentioned, disposable email domain, spam indicators, or empty request
   - **Escalate**: Has text but no DMV mention and no clear spam (borderline case)
3. Auto-acts on approve/reject, escalates the rest to Jason
4. Skips accounts that are already approved (403 from API = already done)

### DMV Area Matching

The script checks invite requests against:
- States: MD, VA, DC, WV, DE, PA
- 100+ DMV cities and counties (Baltimore, Arlington, Silver Spring, Winchester, etc.)
- General references: "DMV", "NOVA", "National Capital Region"
- Local universities: JHU, UMD, GMU, GW

**Secondary location signal: username pattern matching.** If the invite text doesn't mention a DMV location but the username clearly does (e.g. `vegan_baltimore`, `nova_writer`, `arlington_dev`), the signup is auto-approved. Conservative pattern list — only unambiguous city names like `baltimore`, `arlington`, `alexandria`, `reston`, `frederick`, etc. — to prevent spammer gaming. State abbreviations (`md`, `va`, `dc`) and common surnames (`fairfax`, `shaw`, `bowie`, `richmond`, `norfolk`, `vienna`) are intentionally excluded. Add new tokens to `DMV_USERNAME_PATTERNS` in BOTH copies of `mastodon_signups.py` when needed.

**Order of precedence in `classify_account()`:** invite-text non-DMV check fires before username approval, so a sign-up like `vegan_baltimore who lives in NYC` still gets rejected for the explicit non-DMV location. Disposable email, spam phrases, and empty invites also block username approval.

### Spam Detection

- Generic templated phrases ("looking to connect with others", "join a friendly community")
- Crypto/SEO/marketing keywords
- Disposable email domains — checked two ways:
  - Exact match against `SPAM_EMAIL_DOMAINS` set (tmail.lt, guerrillamail.com, free.nf, onionmail.org, 2mail.co, etc.)
  - Substring match against `SPAM_EMAIL_DOMAIN_SUBSTRINGS` list (spammail, tempmail, tmpmail, throwaway, disposable, fakeinbox, mailnesia, guerrilla, 10minutemail) — catches domain variants like `cc.spammail.free.nf`
  - When a new disposable domain slips through (user had to manually reject), add it to BOTH the `SPAM_EMAIL_DOMAINS` set in `mastodon_signups.py` AND check if a substring would catch variants. Update both script copies: `~/.hermes/scripts/mastodon_signups.py` and `~/.hermes/skills/social-media/mastodon-admin/scripts/mastodon_signups.py`
- Non-DMV locations — both international AND US:
  - International: UK, Germany, Brazil, Vietnam, Nigeria, Canada, etc.
  - US states/cities outside DMV: all 50 states with abbreviations, plus major cities (San Diego, New York, Chicago, Seattle, Miami, etc.)

### Running

```bash
python3 ~/.hermes/skills/social-media/mastodon-admin/scripts/mastodon_signups.py
```

Output is JSON on stdout. The cron job agent formats it for delivery.

### API Endpoints

```bash
# List pending accounts
curl -sS "https://dmv.community/api/v1/admin/accounts?status=pending&limit=40" \
  -H "Authorization: Bearer $TOK"

# Approve an account
curl -sS -X POST "https://dmv.community/api/v1/admin/accounts/$ACCOUNT_ID/approve" \
  -H "Authorization: Bearer $TOK"

# Reject an account
curl -sS -X POST "https://dmv.community/api/v1/admin/accounts/$ACCOUNT_ID/reject" \
  -H "Authorization: Bearer $TOK" \
  -F "comment=Spam - no DMV area mentioned"
```

**Pitfall:** The approve endpoint returns 403 "This action is not allowed" when
the account is already approved. This is NOT a permission error - treat 403 on
approve as "already done" (success).

**Pitfall:** Rate limiting. Space approve/reject calls 2+ seconds apart to avoid
cascading 403s. The script handles this automatically.


## Extended Reference

Load `references/extended-reference.md` when the task requires any of these advanced or less-common topics:

- Cron Jobs
- Pitfalls

Keep the common operational path in this file; use the reference for the detailed continuation.
