---
name: weekly-blog
description: >-
  Automated research blogging pipeline. Picks a random topic, runs deep
  research, saves to Obsidian, converts to a blog post, humanizes it,
  generates a header image, and publishes via SSH/rsync. Configurable
  for any blog platform that supports rsync or SSH upload.
tags: [blogging, automation, research, cron, obsidian, prose-sh]
triggers:
  - weekly blog automation
  - auto blog post
  - scheduled research blog
  - publish blog
related_skills:
  - deep-research
  - slop-cleaner
  - humanizer
---

# Weekly Blog Automation

Automated research-to-blog pipeline. Runs on a configurable schedule (default: 3x/week). No user prompting required.

## Configuration

Copy `config.example.yaml` to `config.yaml` and customize:

```bash
cp config.example.yaml config.yaml
```

The config defines:
- **Blog platform**: SSH/rsync target (prose.sh, your own server, etc.)
- **Blog URL**: your public blog URL
- **Publishing identity**: SSH username for your blog host
- **Obsidian vault**: path to your vault
- **Topic pool**: file path for your topic list
- **Schedule**: cron expression

## Pipeline Overview

```
topic pool → pick random (no repeats) → deep research →
save to Obsidian Research →
convert to blog post → humanizer pass (strip AI-isms) →
generate header image → rsync to blog host →
verify post is live → update state files
```

Every step MUST execute, even if prior steps are degraded. A published imperfect post beats a silently failed pipeline.

## Pipeline Steps

### 1. Pick a Topic

Topics are stored in `topic_pool.txt` — one topic per line. The pool is maintained by the agent.

**Deduplication is critical.** Before picking:
1. Fetch the live blog RSS/main page to get all published slugs
2. Cross-reference the candidate topic against existing slugs and titles
3. If any match, pick a new topic

### 2. Deep Research

Use the `deep-research` skill:

```
Deep research on: [topic]

Produce a comprehensive research report covering:
- Background and current state
- Key players, technologies, or developments
- Challenges and controversies
- Future implications
- Sources

Format output as a markdown research brief suitable for archiving in Obsidian.
```

If web sources are blocked (Cloudflare, rate limits), proceed with the model's existing knowledge. Never abort because research was limited.

### 3. Save to Obsidian

Use `write_file` (not terminal `cat >` or `echo >>` which get blocked in cron sessions):

```python
from hermes_tools import write_file
from datetime import date
import re

vault = os.environ.get("OBSIDIAN_VAULT_PATH", os.path.expanduser("~/Documents/Obsidian Vault"))
slug = re.sub(r'[^a-z0-9-]', '', re.sub(r'-+', '-', post_title.lower().replace(" ", "-")))[:60]
filename = f"{vault}/Research/{date.today().isoformat()}-{slug}.md"
write_file(filename, f"# {post_title}\n\n{research_content}")
```

### 4. Write Blog Post

Condense the research into a readable blog post:

```markdown
# [Engaging Title]

*DATE · Tags: tag1, tag2, tag3*

[Hook paragraph — one compelling sentence about why this matters]

---

## Section 1 (3-4 sentences + key detail)

[Content]

---

## Section 2

[Content]

---

## Why This Matters

[1-2 paragraph conclusion]
```

**Formatting rules:**
- Level-1 heading (`# Title`) as first line
- Italic date/tag line directly after
- `---` section dividers between major sections
- No YAML frontmatter (many platforms render it as raw text)
- Plain markdown only
- Write in English
- Avoid em-dashes — use commas or periods instead

### 5. Humanizer Pass (Required)

Load the `humanizer` skill and apply its anti-AI checklist:
- Remove AI vocabulary (crucial, delve, pivotal, tapestry, vibrant, landscape)
- Remove significance inflation ("testament", "pivotal moment", "evolving landscape")
- Remove promotional language ("groundbreaking", "nestled", "stunning")
- Remove superficial -ing endings ("highlighting", "underscoring", "showcasing")
- Remove rule-of-three patterns and synonym cycling
- Remove signposting ("let's dive in", "here's what you need to know")
- Add personality: opinions, varied rhythm, acknowledge complexity

After the pass, ask yourself: "What makes this obviously AI?" Fix remaining tells.

### 6. Generate Header Image

Use `image_generate` with a descriptive prompt and `aspect_ratio="landscape"`. Download locally:

```bash
curl -sL -o "/tmp/${TOPIC_SLUG}-header.jpg" "$IMAGE_URL"
```

If image generation fails (rate limited, blocked): skip it. A post with no image is better than a stalled pipeline.

### 7. Publish

**CRITICAL:** Never use a generic filename. Derive the slug from the post title.

```bash
# Derive slug
TOPIC_SLUG=$(echo "$POST_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | tr -s '-' | sed 's/^-//' | sed 's/-$//' | cut -c1-60)

# Copy to local file with correct name
cp "$BLOG_POST_FILE" "/tmp/${TOPIC_SLUG}.md"

# Upload post + image
rsync -vr --no-compress --force \
  "/tmp/${TOPIC_SLUG}.md" \
  "/tmp/${TOPIC_SLUG}-header.jpg" \
  "${BLOG_SSH_TARGET}:/"

# Verify it's live
sleep 2 && curl -sf "${BLOG_URL}/${TOPIC_SLUG}" > /dev/null && echo "Live: ${BLOG_URL}/${TOPIC_SLUG}"
```

**If header image doesn't exist:** only rsync the `.md` file.

### 8. Update State Files

| File | Purpose |
|------|---------|
| `topic_pool.txt` | curated list of blog topics, one per line |
| `recent_topics.txt` | last 50 posted topics (title, slug, date) for dedup |
| `published_slugs.txt` | all known slugs (synced from blog each run) |
| `last_post_title.txt` | title and URL of most recent post |

Use `write_file` via `execute_code` — terminal `echo >>` gets blocked by security scans in cron sessions.

## Pitfalls

- **Never use generic slugs.** The filename becomes the URL. Always derive from the title.
- **prose.sh doesn't support rsync compression.** Use `--no-compress`. The `-avz` flag fails silently.
- **prose.sh SSH creates, never deletes.** `ssh prose.sh rm file.md` creates a post called "rm file.md". To delete, use SFTP.
- **Duplicate topic detection is critical.** Always fetch the live blog feed before picking a topic. Don't rely solely on local tracking files.
- **Topic pool is a hint, not source of truth.** A topic may have been posted under a different title. Cross-reference against live slugs.
- **Model stalls mid-pipeline.** The model declares intent but never follows through with tool calls. The prompt must explicitly instruct the model to USE tools, not describe what it will do.
- **False OK status.** The cron system marks a job "ok" if the LLM returns without error, even if no actual work was done. Always verify the post is live.
- **Blocked web sources ≠ abort.** If web_search fails, write from the model's knowledge. Never skip publish steps.
- **Image gen failure ≠ abort.** Skip the image, publish without it.
- **Slug derivation trailing hyphen.** Add `sed 's/-$//'` to strip trailing hyphens from titles ending with special characters.

## Pipeline Length Mitigation

The research + blog pipeline is long. Models frequently stall after research. Options:

1. **Prompt tightening:** Every token in the cron prompt is a token the model can't use for output.
2. **Two-job split:** Job 1 (research → save to Obsidian, deliver: local). Job 2 (read research → write → publish, runs 15 min later, deliver: origin).
3. **Reduce scope:** 2-3 web searches max, extract 2 key sources, write ~500 words. A published short post beats a stalled long one.

## Manual Recovery When Pipeline Stalls

1. Find the session file: `ls -lt ~/.hermes/sessions/session_cron_* | head -1`
2. Check what was completed by reading the last few messages
3. If research exists in Obsidian: read it, write the blog post, publish, verify
4. If no research exists: pick a topic, do research, continue pipeline

## Environment

Requires:
- `OBSIDIAN_VAULT_PATH` env var (or defaults to `~/Documents/Obsidian Vault`)
- `deep-research` skill
- `humanizer` skill
- rsync access to your blog host (prose.sh, personal server, etc.)
- `NANOGPT_API_KEY` or other image gen backend (for header images)
