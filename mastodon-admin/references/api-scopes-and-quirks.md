# Mastodon Admin API — Token Scopes and Quirks

## Token Configuration

The token at `~/.hermes/secrets/mastodon_token` was created via a Mastodon
OAuth application on dmv.community.

**IMPORTANT:** The token's OAuth scopes are set at creation time and cannot be
upgraded. If admin endpoints return 403 with "outside the authorized scopes"
while verify_credentials returns 200, the token lacks admin scopes — see the
CRITICAL section below.

**Required scopes for admin operations:**
```
admin:read, admin:read:reports, admin:write:reports,
admin:read:accounts, admin:write:accounts
```

## What Works

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/admin/reports` | GET | ✅ 200 | List reports, supports `resolved`, `limit` |
| `/admin/reports/{id}` | GET | ✅ 200 | Single report details |
| `/admin/reports/{id}/assign_to_self` | POST | ✅ 200 | Assign report to admin account |
| `/admin/reports/{id}/resolve` | POST | ✅ 200 | Resolve a report |
| `/admin/reports/{id}/reopen` | POST | ✅ 200 | Reopen a resolved report |
| `/admin/accounts?action` | GET | ✅ 200 | List accounts, supports `status`, `origin`, `limit` |
| `/admin/accounts/{id}/action` | POST | ✅ 200 | Suspend/silence/disable/sensitive/none |
| `/admin/accounts/{id}/approve` | POST | ✅ 200 (or 403 if already approved) | Approve pending signup |
| `/admin/accounts/{id}/reject` | POST | ✅ 200 (or 403 if already rejected) | Reject pending signup |
| `/statuses` (POST, visibility=direct) | POST | ✅ 200 | Send DM (requires @mention for notification) |
| `/accounts/verify_credentials` | GET | ✅ 200 (needs `read` scope) | Verify token + get account ID. Requires the `read` OAuth scope — NOT included in admin-only tokens. |
| `/apps/verify_credentials` | GET | ✅ 200 | Verify app + list token scopes |
| `/api/v1/timelines/home` | GET | ✅ 200 (needs `read` scope) | Also requires `read` scope — good secondary verification |

## What Doesn't Work / Quirks

### CRITICAL: 403 on ALL admin endpoints = token lacks admin scopes

**Symptom:** `verify_credentials` returns 200 (valid token, correct user, Owner
role), but every `/api/v1/admin/*` endpoint returns:
```
{"error":"This action is outside the authorized scopes"}
```

**Root cause:** The OAuth token was created without admin scopes. The user being
Owner/Admin on the instance is NOT the same as the OAuth token having admin
scopes — Mastodon OAuth tokens have their own scope set at creation time.

**Diagnosis command:**
```bash
# This works — token is valid and authenticates as the Owner
curl -sS "https://dmv.community/api/v1/accounts/verify_credentials" \
  -H "Authorization: Bearer $(cat ~/.hermes/secrets/mastodon_token)" | jq '.role.name'
# → "Owner"

# This fails — token lacks admin scopes
curl -sS "https://dmv.community/api/v1/admin/reports?limit=1" \
  -H "Authorization: Bearer $(cat ~/.hermes/secrets/mastodon_token)"
# → {"error":"This action is outside the authorized scopes"}
```

**Fix — OAuth app registration + re-authorization (see SKILL.md pitfalls for full procedure):**

1. Register a new app with admin scopes via POST `/api/v1/apps`
2. User authorizes via browser at the `/oauth/authorize` URL
3. Exchange the returned code for a token via POST `/oauth/token`
4. Save to `~/.hermes/secrets/mastodon_token`

**Pitfall:** OAuth authorization codes are ONE-TIME USE. If the token exchange
fails or output gets truncated, you need a fresh code from the user.

### 403 "This action is not allowed" — Not Always an Error

The approve and reject endpoints return `403 {"error": "This action is not allowed"}`
when the account has already been approved/rejected. This is NOT a permission error.
The token has the correct scopes (`admin:write:accounts`). Treat 403 on these
endpoints as "already done" = success.

Detection: check the `approved` field on the account object before calling approve.
If `approved=True`, skip the API call entirely.

### Accounts with `approved=True` Still in `status=pending` Results

Mastodon 4.6 returns already-approved accounts in the `status=pending` list.
The `approved` field on the account object is the source of truth, not the
`status` query parameter.

### Rate Limiting on Bulk Operations

When calling approve/reject in a loop (e.g., processing 40 pending accounts):
- With 1-second delays: cascading 403 errors
- With 2-second delays: works reliably
- The API shares the standard 300 requests / 30 minutes limit

### Admin Account Lookup

The `/admin/accounts/{id}` endpoint returns 403 for some accounts (possibly
remote accounts that the instance doesn't fully control). Use the
`/admin/accounts?origin=local` filter for local account management.

### Shell Quoting

The `$(cat ~/.hermes/secrets/mastodon_token)` subshell expansion breaks when
nested inside `python3 -c "..."` strings that also use double quotes. Two
solutions:

1. **Pipe to temp file** (works for one-off curl commands):
   ```bash
   curl -sS "https://dmv.community/api/v1/admin/reports" \
     -H "Authorization: Bearer $(cat ~/.hermes/secrets/mastodon_token)" > /tmp/reports.json
   python3 -c "import json; data=json.load(open('/tmp/reports.json')); ..."
   ```

2. **Standalone Python script** (preferred for complex operations):
   ```python
   with open(os.path.expanduser("~/.hermes/secrets/mastodon_token")) as f:
       token = f.read().strip()
   ```

### write_file Tool Mangling

The `skill_manage(action='write_file')` tool sometimes truncates
`os.path.expanduser("~/.hermes/secrets/mastodon_token")` lines in Python scripts.
After writing a script, always verify it parses:
```bash
python3 -c "import ast; ast.parse(open('script.py').read()); print('OK')"
```
Fix any mangled lines with `patch` before relying on the script.

## Instance Details (dmv.community)

- **Mastodon version**: 4.6.0
- **Max characters**: 1989
- **Max media attachments**: 4
- **Image size limit**: 16 MB
- **Video size limit**: ~99 MB
- **Polls**: max 4 options, 50 chars each, 5min–30day expiry
- **Admin account ID**: Set via `MASTODON_ADMIN_ID` environment variable (your own account ID)
- **Approval required**: Yes
- **Registrations**: Open (with approval)