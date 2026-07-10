---
name: fastmail-imap-newsletter-digest
description: >-
  Read emails from Fastmail via IMAP and process them (e.g., newsletter
  digest). Handles HTML→text extraction for newsletters where plain text
  fallbacks are useless. Summarization via self-contained Python script
  calling Qwen 3.5 (NanoGPT) and delivery via AgentMail.
version: 2.0.0
tags: [fastmail, imap, email, newsletters, digest, cron, nanogpt]
---

# Fastmail IMAP Newsletter Digest

Connect to Fastmail via IMAP to fetch and process emails, with a focus on newsletter summarization pipelines. The canonical implementation uses a self-contained Python script at `~/.hermes/scripts/newsletter_digest.py` that handles fetch → summarize → email in one process.

## Prerequisites

- Fastmail account with an **App Password** (Settings → Privacy & Security → Integrations → App Passwords)
- Environment variables: `FASTMAIL_EMAIL` and `FASTMAIL_APP_PASSWORD`
- NanoGPT API key: `OPENAI_API_KEY` or `NANOGPT_API_KEY` in `~/.hermes/.env`
- AgentMail API key: `AGENTMAIL_API_KEY` in `~/.hermes/.env`
- Python stdlib (imaplib, urllib, ssl, json) — no pip packages needed except `agentmail`

## Fastmail IMAP Connection

- **Server:** `imap.fastmail.com`
- **Port:** `993` (SSL)
- **Folder separator:** `/`
- **Labels** appear as folders, e.g., `+Newsletter`, `+Github`, `+Important`

## Critical Pitfall: Newsletter Plain Text Is Usually Useless

Most newsletter providers (Morning Brew, Tech Brew, etc.) send HTML-only emails. The `text/plain` part is often just:

> "Oops! Looks like your email provider is scrambling the email :( Click here to read it online"

**Always prefer HTML→text extraction** for newsletters. The HTML body contains the actual content. The canonical script (`newsletter_digest.py`) includes a robust `HTMLTextExtractor` class for this.

## Architecture (Current)

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│ Fastmail    │IMAP │ newsletter_  │HTTP  │ NanoGPT      │     │ AgentMail →      │
│ +Newsletter ├────►│ digest.py    ├─────►│ (Qwen 3.5)   │     │ Fastmail INBOX   │
│ (last 24h)  │     │              │      │ summarize    │     │                  │
└─────────────┘     │ fetch→summ→  │      └──────┬───────┘     └──────────────────┘
                    │ send email   │              │ JSON response
                    └──────┬───────┘              │
                           │                      │
                           ▼                      ▼
                      AgentMail API         HTML digest output
                      (herman-the-         wrapped in email
                       hermes-agent@
                       agentmail.to)
```

The script is fully self-contained. The cron job just runs the script and reports the result.

## The Self-Contained Script Pattern

The newsletter digest uses a **self-contained Python script** rather than an LLM-driven pipeline. This is the right pattern when:

- The LLM summarization and email sending can happen in one stateless API call
- You want to avoid double-execution (script + agent both running the same logic)
- Reliability matters more than agentic flexibility

### Script Structure

The script at `~/.hermes/scripts/newsletter_digest.py`:

1. **Fetch** — IMAP connect to Fastmail `+Newsletter` folder, search `SINCE` yesterday
2. **Extract** — HTML→text extraction with truncation at 2000 chars per newsletter
3. **Summarize** — Call NanoGPT OpenAI-compatible API with Qwen 3.5 (`qwen/qwen3.5-397b-a17b-thinking`)
4. **Send** — Deliver via AgentMail SDK (`your-agent@agentmail.to` → `your-email@example.com`)

### Critical: Always Build the Newsletter Text Before the Prompt

**Pitfall:** When constructing the summarization request, build the newsletter text (sender+subject+body for each email) FIRST and embed it in the prompt template string. Python f-strings can't reference variables that are defined inside the same f-string — so the newsletter text must be assembled as a separate string variable before being interpolated into the prompt. The canonical script does this correctly:

```python
nl_text = f"...{len(newsletters)} newsletters..."
for nl in newsletters:
    nl_text += f"--- Newsletter {i} ---\nFrom: {nl['from']}\n..."

prompt = f"""Summarize these...\n{nl_text}"""
```

This avoids `NameError: name 'nl_text' is not defined` at runtime.

## Cron Job: Newsletter Digest (Job 38029db0181a)

Runs daily at **4pm ET**. Schedule: `0 16 * * *`

### Configuration

```
job_id:   38029db0181a
script:   (none — self-contained script in prompt)
model:    qwen/qwen3.5-397b-a17b-thinking (from cron's default model set)
provider: NanoGPT
deliver:  local
enabled_toolsets: ["terminal"]
```

### Prompt

The cron prompt instructs the agent to:
1. Run `python3 ~/.hermes/scripts/newsletter_digest.py`
2. If output is `NO_NEWSLETTERS` → respond `[SILENT]`
3. If output contains `ERROR` → report the error
4. Otherwise → show a brief summary of what was covered

### The `deliver: local` Limitation

Because `deliver: local`, any output (including error reports) stays on the server in `~/.hermes/cron/output/38029db0181a/`. The user does NOT receive the error notification. To see whether the job actually ran:

```
ls -lt ~/.hermes/cron/output/38029db0181a/ | head -5
cat ~/.hermes/cron/output/38029db0181a/<latest>.md
```

**Trade-off:** This is acceptable because the script sends email directly via AgentMail, so successful runs deliver to the user's inbox. But failed runs (e.g., API 503) are invisible — you need to proactively check the output dir. Options to address this:
- Switch `deliver` to `telegram` so errors reach the user
- Have the script itself notify on failure (e.g., send a fallback message)
- Add a monitoring cron job that checks the output dir for recent error patterns

## NanoGPT API Integration

### Endpoint

```
POST https://nano-gpt.com/api/v1/chat/completions
Authorization: Bearer <OPENAI_API_KEY>
Content-Type: application/json
```

### Model

```
qwen/qwen3.5-397b-a17b-thinking
```

### Retry Logic

The script implements up to **5 retries** with exponential backoff:

| Attempt | Wait time | Cumulative |
|---------|-----------|------------|
| 0       | 10s       | 10s        |
| 1       | 20s       | 30s        |
| 2       | 40s       | 70s        |
| 3       | 60s       | 130s       |
| 4       | 60s       | 190s (~3min) |

Retryable codes: 429, 500, 502, 503. Network errors (URLError) also retry. All other HTTP errors report immediately.

This is sufficient to survive most transient API outages (including the Gemini 503 that lasted ~2.5 minutes in the May 7 incident that prompted the switch to NanoGPT).

### API Key Resolution Order

1. `OPENAI_API_KEY` from `~/.hermes/.env`
2. `NANOGPT_API_KEY` from `~/.hermes/.env`
3. If neither found → return `ERROR` (no fallback to config.yaml, unlike the old Gemini workflow)

`OPENAI_BASE_URL` is read from `~/.hermes/.env` if set, otherwise defaults to `https://nano-gpt.com/api/v1`.

## Digest Email Format

The email is sent as multipart (text + HTML) via AgentMail. The HTML body uses:

- **Structure:** Date header → Quick Overview → Top 3-5 stories (styled cards with blue left border) → Everything Else (bullets) → Newsletters Covered
- **Styling:** inline CSS, system fonts, max-width 700px, responsive
- **Plain text fallback:** stripped HTML with html entity unescaping

The Qwen 3.5 model generates the HTML content directly as part of its response. The script wraps it in a minimal email shell.

## Folder Name Quoting Trap

When accessing Fastmail folders with spaces in the name via IMAP, you MUST quote the folder name with literal double quotes inside the Python string:

```python
# WRONG — fails with "BAD Invalid modifier list in Examine"
m.select('Hermes Agent')

# RIGHT
m.select('"Hermes Agent"')
```

This applies to any folder with spaces or special characters.

## HTML→Text Extraction Pattern

[Existing pattern from v1.0.0 — the HTMLTextExtractor class is unchanged]

## IMAP Search Syntax

[Existing reference — unchanged]

## Session Learnings

### May 7, 2026 — Model Switch from Gemini to NanoGPT

**Problem:** The newsletter digest script used Gemini Flash Lite via `https://generativelanguage.googleapis.com/v1beta/openai` with the `GEMINI_API_KEY`. The Gemini API returned HTTP 503 Service Unavailable at 4pm ET and the script's retry logic (3 attempts, max 30s) couldn't outlast the outage. The failure was invisible because `deliver: local` swallowed the error report.

**Fix:**
1. Switched to NanoGPT (OpenAI-compatible) endpoint with model `qwen/qwen3.5-397b-a17b-thinking`
2. API key: `OPENAI_API_KEY` or `NANOGPT_API_KEY` from `.env`
3. Extended retry to 5 attempts with exponential backoff up to 60s (~3 minute total window)
4. Also retries on 429, 500, 502, and network errors (not just 503)

**Verification:** The new model produces comparable or better digest summaries with a richer formatting style.

### Key Pitfalls

1. **Gemini flash-latest can't use tools** — must call APIs directly from script (now moot; we use NanoGPT which also doesn't require tools for this)
2. **Pre-run script + agent prompt both running the script = double execution** — never set both `script` field and a prompt that runs the same script
3. **HTML extraction is critical** — many newsletters have useless plain-text fallbacks
4. **API outages are silent** — with `deliver: local`, an API 503 means the user never knows the job failed
5. **Check cron output dir** for verification: `cat ~/.hermes/cron/output/38029db0181a/<latest>.md`
4. **Model choice drift** — if you update the script to use a different model provider, also update this skill's "Specific Cron Job" section
5. **`OPENAI_BASE_URL=` empty string in `.env`** — If `.env` has `OPENAI_BASE_URL=` with no value (empty string), the script reads that empty string instead of falling back to `https://nano-gpt.com/api/v1`. This causes `ValueError: unknown url type: '/chat/completions'` because the URL becomes just the path with no host. Python's `dict.get('KEY', default)` returns the empty string if the key exists — it does NOT use the default.

   **Fix (script-level, preferred):** Use the `or` operator instead of relying on `dict.get()` default:
   ```python
   # BEFORE (broken — empty string defeats the default)
   base_url = env.get('OPENAI_BASE_URL', 'https://nano-gpt.com/api/v1')

   # AFTER (robust — empty string is falsy, falls through to default)
   base_url = env.get('OPENAI_BASE_URL', '') or 'https://nano-gpt.com/api/v1'
   ```
   This pattern is safer because it doesn't depend on `.env` hygiene. Apply to any `env.get(KEY, default)` call where the default must never be empty.

   **Fix (env-level, also valid):** Remove the line entirely from `.env`, or set explicitly: `OPENAI_BASE_URL=https://nano-gpt.com/api/v1`.

   **Diagnosis:** `grep OPENAI_BASE_URL ~/.hermes/.env` — if the value is empty after the `=`, that's the bug.
6. **Timeout on large newsletter batches** — 11+ newsletters can exceed a 60-second timeout because Qwen 3.5 thinking model processes each one. The script itself handles this fine (no timeout built in), but if running manually for testing, use `timeout 180` to give it enough runway.
7. **Folder name quoting** — folders with spaces need IMAP syntax `m.select('"Folder Name"')`
8. **Always check AgentMail outbox** to confirm email actually left the sender: `python3 ~/.hermes/skills/agentmail/agentmail/scripts/agentmail_helper.py list-messages herman-the-hermes-agent@agentmail.to`
9. **Don't assume the user deleted emails** — if they say they didn't get today's digest but 15 digests are in Trash, they likely delete them after reading. Check the cron output dir first, then the AgentMail outbox, then Fastmail folders.
10. **Newsletter body text built BEFORE the f-string** — construct the concatenated text as a separate variable, then interpolate it into the prompt template. Python f-strings are evaluated at definition time and can't reference variables defined inside them.
