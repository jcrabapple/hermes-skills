# Unified Mastodon Token Setup

The mastodon (posting) and mastodon-admin (moderation) skills share
`~/.hermes/secrets/mastodon_token`. Both must work — a token with only
posting scopes breaks admin, and a token with only admin scopes can't
verify credentials or post.

## Required Scopes

```
read write admin:read admin:write admin:read:reports admin:write:reports admin:read:accounts admin:write:accounts
```

## Full Re-Authorization Procedure

### 1. Register OAuth App

```bash
curl -sS -X POST "https://dmv.community/api/v1/apps" \
  -F "client_name=Hermes Agent Admin" \
  -F "redirect_uris=urn:ietf:wg:oauth:2.0:oob" \
  -F "scopes=read write admin:read admin:write admin:read:reports admin:write:reports admin:read:accounts admin:write:accounts" \
  -F "website=https://hermes-agent.nousresearch.com"
```

Note `client_id` and `client_secret` from the response.

### 2. User Authorizes

Send the user this URL (substitute CLIENT_ID):

```
https://dmv.community/oauth/authorize?client_id=CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=read+write+admin:read+admin:write+admin:read:reports+admin:write:reports+admin:read:accounts+admin:write:accounts&response_type=code
```

### 3. Exchange Code for Token — pipe to file

**Never rely on Hermes tool output for the token value** — it will be masked.
Pipe the exchange response to a file and extract with Python:

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

### 4. Verify Both Sides

```bash
# Admin access
curl -sS "https://dmv.community/api/v1/admin/reports?limit=1" \
  -H "Authorization: Bearer *** ~/.hermes/secrets/mastodon_token)"

# Posting access
python3 ~/.hermes/skills/social-media/mastodon/scripts/mastodon_post.py --dry-run --status "test"
```

Admin check should return 200 with JSON array. Posting check should show a character count, not 403.

## Common Failure Mode

Running `mastodon_reauthorize.py` (from the mastodon posting skill) registers a new app with only `read write follow push` scopes and overwrites the token. This silently breaks all three admin cron jobs (signup monitor, report monitor, welcome bot) with HTTP 403. If admin jobs start failing after a token refresh, this is the cause.
