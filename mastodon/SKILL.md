---
name: mastodon
description: >-
  Post to Mastodon via the dmv.community API. Supports text statuses, media
  attachments, polls, content warnings, scheduled posts, visibility control,
  and thread creation. Use when the user asks to post/toot to Mastodon.
tags:
  - mastodon
  - social-media
  - posting
triggers:
  - post to mastodon
  - toot
  - mastodon post
  - share on mastodon
---

# Mastodon Skill

Post statuses, media, and threads to the user's Mastodon instance at **dmv.community**.

## Configuration

| Key | Value |
|-----|-------|
| Instance | `dmv.community` |
| API base | `https://dmv.community/api/v1/` |
| Token file | `~/.hermes/secrets/mastodon_token` |
| Account | `@your-handle@your.instance` |
| Max characters | **1989** |
| Max media attachments | 4 |
| Image size limit | 16 MB |
| Video size limit | ~99 MB |
| Supported media | image/jpeg, image/png, image/gif, image/webp, image/avif, video/mp4, video/webm, audio/mp3, audio/ogg, audio/wav, audio/flac, audio/aac |
| Polls | max 4 options, 50 chars each, 5min-30day expiry |
| Default visibility | `public` (account default) |
| Default language | `en` |
| URL reserved chars | 23 per URL |
| OAuth app | `Mastodon Web` (posts appear as "via Mastodon Web") — reauthorize via `scripts/mastodon_reauthorize.py` |
| User-Agent | Chrome 138 on Linux (spoofed in `mastodon_post.py` to avoid API-rate-limit discrimination) |

## Authentication

The bearer token is stored at `~/.hermes/secrets/mastodon_token`. Read it at runtime:

```bash
TOKEN=$(cat ~/.hermes/secrets/mastodon_token)
```

All API calls use:
```
Authorization: Bearer $TOKEN
```

## Core Operations

### Post a Status

```bash
curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=Your post text here" \
  -F "visibility=public"
```

**Parameters (all via -F form fields):**

| Field | Required | Description |
|-------|----------|-------------|
| `status` | Yes* | Text content (*required unless `media_ids` or `poll` is set) |
| `visibility` | No | `public`, `unlisted`, `private`, `direct` (default: account setting = `public`) |
| `sensitive` | No | `true`/`false` — mark as sensitive content |
| `spoiler_text` | No | Content warning text (shows as CW header) |
| `language` | No | ISO 639-1 code, e.g. `en` (default: account setting) |
| `media_ids[]` | No | Media attachment IDs (from upload step, max 4) |
| `in_reply_to_id` | No | Status ID to reply to (for threads) |
| `poll[options][]` | No | Poll choices (max 4, 50 chars each) |
| `poll[expires_in] | No | Poll duration in seconds (300 min, 2629746 max) |
| `poll[multiple]` | No | `true` for multiple-choice poll |
| `scheduled_at` | No | ISO 8601 datetime (min 5min future) — schedules the post |
| `quote_id` | No | Status ID to quote (quote post support) |

### Upload Media

```bash
curl -sS -X POST "https://dmv.community/api/v1/media" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/image.png" \
  -F "description=Alt text for accessibility"
```

Returns JSON with `"id"` — use that in `media_ids[]` when posting.

For images, always include `description` (alt text) when known.

### Post with Media (two-step)

```bash
# 1. Upload
MEDIA_ID=$(curl -sS -X POST "https://dmv.community/api/v1/media" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/image.png" \
  -F "description=Alt text" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Post with media
curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=Check out this image!" \
  -F "media_ids[]=$MEDIA_ID"
```

### Create a Thread

Post the first status, capture its `id` from the JSON response, then post each subsequent status with `in_reply_to_id` set to the previous status's `id`.

```bash
# First post
STATUS1=$(curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=Thread part 1/3")
ID1=$(echo "$STATUS1" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Reply (part 2)
STATUS2=$(curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=Thread part 2/3" \
  -F "in_reply_to_id=$ID1")
ID2=$(echo "$STATUS2" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# ... and so on
```

### Post a Poll

```bash
curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=What's the best?" \
  -F "poll[options][]=Option A" \
  -F "poll[options][]=Option B" \
  -F "poll[options][]=Option C" \
  -F "poll[expires_in]=86400" \
  -F "poll[multiple]=false"
```

### Schedule a Post

```bash
curl -sS -X POST "https://dmv.community/api/v1/statuses" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=This is a scheduled post" \
  -F "scheduled_at=2026-06-24T09:00:00.000Z"
```

Must be at least 5 minutes in the future. Use UTC ISO 8601 format.

### Edit a Status

Mastodon supports editing existing posts via PUT (not POST). Same params as
creating, but overwrites the status content.

```bash
curl -sS -X PUT "https://dmv.community/api/v1/statuses/$STATUS_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=Edited text here"
```

Returns the updated status JSON with the same `id` and `url`.

**Use Python, not inline curl, for multiline edits.** Same shell-escaping
issue as posting — use the helper script or a small Python script with
`requests.put()` for anything beyond a single line. Example:

```python
import requests
TOKEN = open(os.path.expanduser("~/.hermes/secrets/mastodon_token")).read().strip()
resp = requests.put(
    f"https://dmv.community/api/v1/statuses/{STATUS_ID}",
    headers={"Authorization": f"Bearer {TOKEN}"},
    data={"status": new_text},
)
# 200 = success, response has id+url
```

Always check character count with URL normalization before editing,
same as for new posts (max 1989).

### Delete a Status

```bash
curl -sS -X DELETE "https://dmv.community/api/v1/statuses/$STATUS_ID" \
  -H "Authorization: Bearer $TOKEN"
```

### Fetch Post Context (Replies / Thread)

To see replies to a post (its ancestors and descendants in the conversation
thread), use the context endpoint:

```bash
curl -sS "https://dmv.community/api/v1/statuses/$STATUS_ID/context" \
  -H "Authorization: Bearer $TOKEN"
```

Returns JSON with `ancestors` (posts above in the thread) and `descendants`
(replies below). Each entry is a full status object with `content` (HTML),
`account`, `url`, etc. Pipe through Python to strip HTML tags for
readable output.

This is the right way to check replies — it returns the full conversation
tree in one call without pagination. Note: replies from remote instances
may take time to federate.

### Get User's Own Recent Posts

```bash
curl -sS "https://dmv.community/api/v1/accounts/verify_credentials" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])"

# Then fetch statuses
curl -sS "https://dmv.community/api/v1/accounts/$ACCOUNT_ID/statuses?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## Workflow Patterns

### Standard Post

1. Confirm the post text with the user (unless they've already given exact text)
2. Check character count: `echo -n "$TEXT" | wc -m` — must be ≤ 1989
3. If text contains URLs, account for 23 chars reserved per URL
4. Post and capture the response JSON
5. Extract the post URL from the response: `"url"` field
6. Confirm to user with the live URL

### Post with Image

1. Confirm image path exists
2. Upload media with alt text → capture `media_id`
3. Post status with `media_ids[]`
4. Confirm with live URL

### Thread

1. Split content into chunks ≤ 1989 chars (account for URL overhead)
2. Post first status, capture ID
3. Post each subsequent status with `in_reply_to_id`
4. Confirm with URL of first post

### Research → Informational Post

For "research X and post about it on Mastodon" tasks (a recurring pattern):

1. **Batch parallel web_search calls** (3 queries from different angles) to gather facts, statistics, and source URLs
2. **Draft the post** following Formatting Rules: emoji hook first line, plain text, one source URL per major claim, 2-3 hashtags at the end. Keep under 1989 normalized chars (URLs = 23 chars each).
3. **Dry-run with the helper script**: `python3 scripts/mastodon_post.py --status "..." --dry-run`. This prints the normalized char count, so **no separate Python char-counting script is needed** before this step.
4. **Post** (same command without `--dry-run`) and capture the URL from the response.
5. **Return a summary** to the user with source links for verification (tables work well on Telegram).

## Formatting Rules (User Preferences)

- **No emdash characters (—).** Use regular dashes (-), commas, colons, or parentheses instead. This is a hard rule for all Mastodon posts.
- **No emdash characters (—).** Use regular dashes (-), commas, colons, or parentheses instead. This is a hard rule for all Mastodon posts.
- **Capitalize the first letter of every sentence.** Even casual/voice-matched posts should have proper sentence capitalization. The user's casual tone doesn't mean lowercase.
- **Write in the user's voice.** Casual, direct, no corporate speak. Match the register of the conversation without over-formalizing.
- **Don't mention features the user won't use.** Before listing capabilities (Spotify Connect, AirPlay, etc.), confirm the user actually wants those. If they've stated preferences (e.g. Bluetooth/wired headphones only), omit irrelevant features from the post. Ask if unsure.
- **No markdown formatting.** Mastodon doesn't render **bold** or *italic*. Use plain text only. Line breaks for readability.
- **Informational explainer, NOT adversarial fact-check.** Do not frame posts around "what's misleading," "what people get wrong," or "viral claims." Do verification during research, but deliver as a clean informational post. State nuanced details as interesting facts in the normal flow, not as "misconceptions" to debunk.
- Start with a relevant emoji
- Write a punchy hook as the first line (no bold — just make the text itself compelling)
- Include 2-3 relevant hashtags at the end (e.g., #science #nature #history)
- When sharing a blog post link: post a 1-2 sentence headline + the link only. Do NOT post a condensed version of the blog post content alongside the link.
- When posting factual content (interesting facts, research findings, trivia), include at least one source URL for verification. URLs count as 23 chars each toward the 1989 limit — account for this when counting.
- Keep posts shorter and punchier than the same content for Telegram

## Character Counting

Mastodon counts characters as Unicode code points. URLs are counted as 23 chars each regardless of actual length.

```python
import re
text = "Your post text with a link https://example.com"
# Replace URLs with 23-char placeholder for counting
normalized = re.sub(r'https?://\S+', 'x' * 23, text)
count = len(normalized)
```

## Instance Rules (dmv.community)

Be aware of these when posting on behalf of the user:
1. Sexually explicit or violent media must be marked sensitive
2. No racism, sexism, homophobia, transphobia, xenophobia, or casteism
3. No incitement of violence
4. No harassment or doxxing
5. No content illegal in the US
6. No intentional misinformation
7. No spam or advertising
8. Don't sell AI-generated art or pass it off as your own creation
9. No AI-generated music

## Helper Script

A reusable Python helper is available at `scripts/mastodon_post.py`. It handles:
- Single posts and threads
- Media uploads with alt text
- Content warnings
- Visibility control
- Polls
- Character counting with URL normalization
- Dry-run mode to preview before posting

Usage:
```bash
python3 scripts/mastodon_post.py --status "Hello world!"
python3 scripts/mastodon_post.py --status "With image" --media /path/to/image.png --alt "Description"
python3 scripts/mastodon_post.py --thread --status "Part 1" --status "Part 2"
python3 scripts/mastodon_post.py --status "Poll text" --poll "A" "B" "C" --poll-expires 86400
python3 scripts/mastodon_post.py --status "Test" --dry-run  # preview without posting
python3 scripts/mastodon_post.py --status "CW post" --cw "Content warning text"
python3 scripts/mastodon_post.py --status "Unlisted" --visibility unlisted
```

## Integrating Mastodon into Cron Jobs

When adding Mastodon posting to an existing cron job (e.g., daily digest, interesting fact):

1. Add the `mastodon` skill to the job's `skills` list
2. Ensure `terminal` toolset is enabled (needed to run the helper script)
3. In the prompt, add Mastodon posting as a step BEFORE the final delivery
4. Key rules to embed in the cron prompt:
   - No emdashes in Mastodon posts
   - No markdown formatting (plain text only)
   - Max 1989 chars with URL-aware counting
   - Include relevant hashtags
   - If the Mastodon post fails, the job should NOT fail entirely — note the failure and continue with the original delivery
5. Include the Mastodon post URL in the original delivery (e.g., Telegram message) as confirmation

### Dual-Delivery Pattern

For jobs that deliver to Telegram/Discord AND Mastodon:
- Compose the Mastodon version separately (shorter, punchier, no markdown, no emdashes)
- Post to Mastodon first, capture the URL
- Include the Mastodon URL in the Telegram/Discord delivery as "Also posted to Mastodon: URL"
- If Mastodon fails, still deliver to the original channel with a note about the failure

## Cron Jobs Using This Skill

- **Daily Interesting Fact** (`4567647fd0b1`): Posts a Mastodon version of the daily fact alongside the Telegram delivery. The cron prompt includes Mastodon formatting rules (no emdashes, no markdown, plain text, hashtags). The pre-run script (`daily_fact_fusion.py`) asks Fusion to include a Sources section with at least one URL. Both the Telegram and Mastodon outputs include at least one source link for verification.

When updating this job's prompt, always include the formatting rules section — cron jobs run without conversation context, so the rules must be self-contained in the prompt. When changing output requirements (e.g. adding source links), update BOTH the pre-run script's query AND the cron prompt — the script determines what Fusion returns, the prompt determines what the agent includes in the formatted output.

## Client Identity ("via" label)

The "via X" label on posts comes from the **OAuth application name** — not the User-Agent header. Setting a browser User-Agent alone won't change it.

The `mastodon_post.py` script sends a Chrome-on-Linux User-Agent for good practice, but to change the displayed client name, the OAuth token must be issued by an app registered with the desired name.

### Re-registering as "Mastodon Web"

Use `scripts/mastodon_reauthorize.py` to register a new OAuth app named "Mastodon Web" and swap the token:

```bash
# Step 1: register app and get auth URL
python3 scripts/mastodon_reauthorize.py

# Step 2: user opens the printed URL in browser, authorizes, gets a code
# Step 3: exchange code for token
python3 scripts/mastodon_reauthorize.py --code YOUR_CODE
```

This replaces `~/.hermes/secrets/mastodon_token` with a token from the "Mastodon Web" app — future posts will show "via Mastodon Web" instead of "via Hermes Agent". The old token is lost; the old app registration is backed up with a `.json.old` suffix.

## Pitfalls

- **No emdashes.** The user explicitly prohibits emdash (—) characters in Mastodon posts. Use regular dashes, commas, or colons. This is a hard rule, not a suggestion.
- **No markdown.** Don't use `**bold**`, `*italic*`, or `# headers` in Mastodon posts. They render as literal characters, not formatting.
- **Always verify the post succeeded.** Check the response JSON for an `id` and `url` field. If the response contains an `error` key, the post failed.
- **Character counting with URLs.** A long URL only counts as 23 chars. Don't reject a post as too long just because a URL is long — normalize first.
- **Media upload is a separate step.** You must upload media first, get the `id`, then reference it in the status post. You cannot embed media in a single call.
- **`media_ids[]` uses array notation.** In curl, use `-F "media_ids[]=$ID1" -F "media_ids[]=$ID2"` for multiple attachments. Each one is a separate `-F` flag.
- **Scheduled posts don't appear immediately.** If `scheduled_at` is set, the response contains `scheduled_at` instead of `url`. The post won't appear in the timeline until the scheduled time.
- **Rate limits.** The API allows 300 posts per 30 minutes. For bulk posting, space requests out.
- **Visibility can't be changed after posting.** Choose the right visibility upfront.
- **Instance rules prohibit AI music and selling AI art.** Don't post AI-generated music content.
- **OAuth endpoints are at the root path.** `/oauth/authorize` and `/oauth/token` live at `https://dmv.community/oauth/…`, NOT under `/api/v1/`. The `/api/v1/` prefix is only for the REST API (statuses, media, accounts, etc.).
- **Authorization codes are single-use.** If token exchange succeeds but verification fails, you cannot retry with the same code — you need a fresh authorization. Always save the token before verifying, or handle failures without losing it.
- **"via" label is OAuth app name, not User-Agent.** Changing the User-Agent header does not affect what client Mastodon displays on posts. To change the label, re-register the OAuth app with the desired `client_name` and swap the token.
- **Shell escaping kills multiline posts.** Raw `curl` in terminal breaks badly when the post contains multiline text, emoji, smart quotes, or special characters. `$()` command substitution, nested quotes, and newlines in `-F` arguments cause syntax errors. **For any post that isn't a simple single-line string, use the helper script** (`scripts/mastodon_post.py --status "..."`) or write a small Python script to `/tmp/mastodon_post.py` and run it. Never try to craft a complex multiline curl command inline — it will waste multiple turns on escaping failures.
- **Editing posts uses PUT, not POST.** `PUT /api/v1/statuses/{id}` with a `status` field. Same shell-escaping caveats apply to edits as to new posts — use Python `requests.put()` for anything multiline.
- **Fetching replies uses the context endpoint.** `GET /api/v1/statuses/{id}/context` returns `ancestors` and `descendants` arrays in one call. Don't try to scrape the HTML page or paginate notifications.
- **CRITICAL: Re-authorizing for posting breaks admin scripts.** The `mastodon_post.py`, `mastodon-admin`, and all admin cron jobs (signup monitor, report monitor, welcome bot) share the same token file at `~/.hermes/secrets/mastodon_token`. If you re-authorize with only `read write follow push` scopes (as `mastodon_reauthorize.py` does by default), the admin cron jobs immediately fail with 403. The token MUST have all scopes: `read write admin:read admin:write admin:read:reports admin:write:reports admin:read:accounts admin:write:accounts`. When re-authorizing, always use the full scope set. See `references/unified-token-setup.md` for the manual procedure.
