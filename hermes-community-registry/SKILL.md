---
name: hermes-community-registry
description: "Search, filter, evaluate, and install community Hermes Agent skills, plugins, tools, and agents from the babylondreams.de community registry. Use when a user asks what's available in the community, wants to discover skills by topic/type, or mentions the babylondreams registry."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [registry, community, discovery, skills, plugins, tools, babylondreams]
    related_skills: [hermes-optional-skills]
---

# Hermes Community Registry

## Overview

The babylondreams.de Hermes Community Registry is a curated directory of 490+ community-built Hermes Agent plugins, skills, tools, and agents. It is maintained by Alexander Kucera at https://babylondreams.de/hermes-registry/ and is synced from the Hermes Discord #community-projects and #plugins-skills-skins channels. The registry is a useful complement to the `hermes-optional-skills` skill — that skill targets the official `optional-skills/` directory in NousResearch/hermes-agent; this one targets the broader community ecosystem (which includes many Discord-only references and third-party repos not in the official tree).

**The registry is a discovery surface, not an installer.** Entries link to GitHub repos, Discord posts, PyPI packages, or install scripts, but the registry itself provides no install command. Once you find a candidate, you must fetch the upstream repo or url to find installation instructions.

## When to Use

- User asks "what Hermes skills exist for X" or "find a plugin that does Y"
- User shares a link to babylondreams.de/hermes-registry/
- User mentions a community skill by name and want to verify it is registered
- `hermes-optional-skills` returned nothing for the user's interest (this registry covers a much broader range)
- User wants to browse by category (memory, devops, observability, etc.)

**Don't use when:**
- The user already knows the GitHub URL of the skill — go directly to that repo and read its README.
- The skill is in the official `optional-skills/` tree (use `hermes-optional-skills`).

## Data Source

The registry is a static site: the HTML page queries `data.json` for all entries. Always fetch `data.json` directly — never drive the browser just to read listings.

```
https://babylondreams.de/hermes-registry/data.json
```

Schema:

| field | example |
|---|---|
| `id` | `532` (integer) |
| `name` | `"Agent Memory Skill"` |
| `slug` | `"agent-memory-skill"` (URL-safe) |
| `author` | displayed author (may be display name) |
| `description` | long-form description (sometimes includes GitHub repo path) |
| `url` | primary canonical link (may be GitHub repo, install script, or Discord message) |
| `repo_url` | GitHub repo URL when available, empty string otherwise |
| `docs_url` | documentation URL (typically empty in current snapshot) |
| `type` | one of: `skill`, `plugin`, `tool`, `agent`, `integration`, `skin`, `other` (see `data.json:type_order` for canonical order) |
| `category` | one of: `memory`, `productivity`, `ui`, `devops`, `observability`, `creative`, `security`, `research`, `orchestration`, `voice`, `finance`, `web`, `gaming`, `ml-inference`, `ml-training`, `smart-home` |
| `discord_url`, `discord_author`, `discord_channel`, `discord_date` | provenance — when/where the entry was synced from Discord |
| `stars` | GitHub stars (currently 0 for most entries — the upstream scraping layer is incomplete; do not use as a quality signal) |
| `first_seen` | when the entry joined the registry (UTC) |

The full list of `type` and `category` values can change at any time — read them from the data rather than hardcoding. The `type_order` array at the top of `data.json` lists the canonical display order for types and is the only authoritative source for which types exist.

## Discovering

### Use the bundled search script

The skill bundles `scripts/search_registry.py` — it fetches `data.json` once, then filters by keyword + type/category flags in a single pass. This is the right tool when the user described what they want in their own words (it does substring match across name + description + author; results are sorted by author + name).

```bash
# All skills related to memory
python3 scripts/search_registry.py --type skill --category memory --keyword sqlite

# All plugins by a specific author
python3 scripts/search_registry.py --author "Hypercubed"

# Plain keyword search across everything
python3 scripts/search_registry.py --keyword "code review"

# Same search, JSON output for piping into another script
python3 scripts/search_registry.py --keyword "code review" --json | python3 -m json.tool
```

Output fields per row: `name`, `type`, `category`, `author`, `url`, `repo_url`, `slug`, `description`. Use `--json` to get the full record including `id`, `discord_url`, `first_seen`.

The script returns exit code 0 with a "No results" line when the query matches nothing — this is intentional (an empty result is a valid answer, not an error).

### Inline curl pipeline

When you don't want to install the script (or want exact control over what to show), use a one-shot `curl | python3`. Templates:

**List all entries of a type or category:**
```bash
curl -fsSL https://babylondreams.de/hermes-registry/data.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for e in data['entries']:
    if e['type'] == 'skill' and e['category'] == 'memory':
        print(f\"- {e['name']} — {e.get('repo_url') or e['url']}\")
"
```

**Keyword search (substring across name + description + author):**
```bash
curl -fsSL https://babylondreams.de/hermes-registry/data.json | python3 -c "
import json, sys, re
q = re.compile(r'(?i)your keyword')
for e in json.load(sys.stdin)['entries']:
    if q.search(e['name'] + ' ' + e['description'] + ' ' + e['author']):
        print(f\"{e['type']:6} {e['category']:14} {e['name']}\")
\        print(f\"  → {e.get('repo_url') or e['url']}\")
"
```

**List birthdays of a category (when did notable entries land):**
```bash
curl -fsSL https://babylondreams.de/hermes-registry/data.json | python3 -c "
import json, sys
entries = [e for e in json.load(sys.stdin)['entries'] if e.get('category')=='security']
entries.sort(key=lambda e: e.get('discord_date','') or '', reverse=True)
for e in entries[:20]:
    print(f\"{e['discord_date'][:10]} {e['name']}\")"
```

### Browsing the web UI

Don't drive the browser just to read listings — fetch `data.json` directly. The web UI is useful for two reasons only:
- Verifying the registry is up-to-date (the homepage shows "synced Jul 06, 2026" date)
- Confirming a candidate entry is on the registry (helpful when the user shares an entry link)

If the user specifically asks to browse the UI, navigate to https://babylondreams.de/hermes-registry/ — it uses Fuse.js client-side search and has type/category filter chips.

### Listing all types / categories (for filtering)

```bash
curl -fsSL https://babylondreams.de/hermes-registry/data.json | python3 -c "
import json, sys
from collections import Counter
data = json.load(sys.stdin)
ents = data['entries']
print('Types:', dict(Counter(e['type'] for e in ents).most_common()))
print('Type order:', data['type_order'])
print('Categories:', dict(Counter(e['category'] for e in ents).most_common()))
"
```

Always re-fetch the counts live — the registry is synced regularly from Discord and the distribution shifts.

## Evaluating

When presenting results to the user, the registry metadata alone is rarely enough to make a decision. Apply this checklist:

1. **Resolve the actual source.** The `url` field can be:
   - A GitHub repo (326 of 496 entries) — the `repo_url` field will usually mirror it.
   - A raw `install.sh` script on raw.githubusercontent.com — never run these blindly; fetch and read them first.
   - A Discord message URL — means the entry has no public repo; the user must open Discord to see the actual code.
   - A third-party service URL (pypi.org, huggingface.co, apify.com, custom domains).
2. **Read the upstream README / repo description.** Use `web_extract` on the repo URL or `curl -fsSL https://api.github.com/repos/OWNER/REPO | python3 -m json.tool` to check description, stars, last update, license, open issues.
3. **Check the SKILL.md / plugin manifest.** For skills, fetch `SKILL.md` from the repo root (or `optional-skills/` subpath) and review description, prerequisites, and security considerations. For plugins, look for `plugin.yaml` or similar.
4. **Look at recent commits.** A repo untouched for months may be abandoned. Use `curl -fsSL https://api.github.com/repos/OWNER/REPO/commits | python3 -c "import json,sys; [print(c['commit']['committer']['date'], c['commit']['message'].split(chr(10))[0]) for c in json.load(sys.stdin)[:10]]"` to confirm recent activity.
5. **Assess install surface.** Does it need API keys? Database? Scheduled jobs? Network access to a third-party service? Capture these and surface them to the user as prerequisites.
6. **Security review.** For any entry whose install involves writing to `~/.hermes/`, running scripts, or requesting API credentials, read the skill's source before endorsing it. Several community entries are unvetted; treat as you would any third-party open-source code.

`stars` field caveat: the upstream scraping layer is currently incomplete (most entries show 0 stars). Do not use this field as a quality signal. Instead, retrieve live GitHub stars via the GitHub API when needed: `curl -fsSL 'https://api.github.com/repos/OWNER/REPO' | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"{d['stargazers_count']} stars, last push {d['pushed_at']}\")"`.

### Provenance as a signal

The two Discord channels that seed the registry have different norms:
- **community-projects** (292 entries) — general community project announcements. Quality varies widely.
- **plugins-skills-skins** (186 entries) — typically more polished, registered shareable work.

This is a weak signal but useful context. The registry entries expose `discord_channel` for exactly this reason.

## Installing

The registry does not provide install commands. Treat each result as a lead to the upstream source:

**For GitHub-backed skills:**
```bash
# Clone, inspect SKILL.md, then copy to the Hermes skills dir
git clone https://github.com/OWNER/REPO /tmp/registry-skill-inspect
cat /tmp/registry-skill-inspect/SKILL.md  # or REPO/skills/category/name/SKILL.md
cp -r /tmp/registry-skill-inspect/SKILL_DIR ~/.hermes/skills/<category>/<name>/
```

**For GitHub-backed skills that ship with an installer script:**
1. Fetch the install script URL (often a raw.githubusercontent.com URL).
2. Read the script before running it — never `curl | bash` without inspection.
3. Look for what it writes to (config files, ~/.hermes/, ~/.config/) and what env vars / API keys it expects.

**For plugins (which use Hermes plugin manifests):**
Refer to the Hermes plugin documentation and the `hermes-plugin-authoring` skill for plugin structure. Plugins typically install via `hermes plugins install <source>` or by copying to `~/.hermes/plugins/`.

**For install script entries (AgentWeb pattern):**
```bash
# 1. Fetch and review
curl -fsSL <install_sh_url>
# 2. Read what it modifies (files, env, PATH)
# 3. Only run after the user has seen what it does
```

**For Discord-only entries:**
The `url` is a Discord message URL. Open it in a browser with the user's Discord session, or use `nanogpt_reddit_scraper` if it's been cross-posted to Reddit. There is no programmatic Discord message fetch in the current Hermes toolset — these entries must be human-inspected.

Always verify after install via `skills_list` or `skill_view(name='...')`.

## Filtering by Use-Case

When the user says "I want X" and you cannot find a name match, pivot to a category filter:

| User asks about... | Likely category |
|---|---|
| Memory, persistence, recall, knowledge bases | `memory` / `observability` |
| Productivity, task management, calendaring | `productivity` |
| UI changes, themes, dashboard elements | `ui` |
| Deployments, infra, CI/CD, hosting | `devops` |
| Logging, metrics, tracing, QA | `observability` |
| Writing, design, art generation | `creative` |
| Auth, scanning, vulnerabilities | `security` |
| Papers, knowledge graphs, news digests | `research` |
| Multi-agent workflows, subagents | `orchestration` |
| TTS, STT, voice skills | `voice` |
| Money, budgets, market data | `finance` |

Mismatched categories can also succeed — a renamer tool might live under `productivity` rather than `ui`. Run a keyword search if a category filter fails. The bundled search script does both — try `--keyword X --category Y` first and fall back to just `--keyword X`.

## Updating the Registry Source

The registry is third-party and out of your control. If `data.json` 404s or the schema changes:

1. Try fetching `https://babylondreams.de/hermes-registry/` directly and look at the page source for any new data endpoint references.
2. Check the registry homepage for the "synced YYYY-MM-DD" stamp — if it's not recent, the maintainer may be on a break.
3. Contact: Alexander Kucera, a.kucera@babylondreams.de (Discord channel for the registry is linked on the homepage).
4. As a fallback, the Hermes Discord server's #community-projects and #plugins-skills-skins channels are the upstream source — but they are not pre-indexed, so this is a slow fallback.

## Common Pitfalls

1. **Driving the browser for discovery.** The browser path provides no API surface beyond what `data.json` already gives you. Use `curl + data.json` (or the bundled script) directly.

2. **Trusting `stars`.** The registry scraping layer reports `0` for almost every entry. This is not zero stars on GitHub — it's a missing field. Use the GitHub API to retrieve live stars.

3. **Running install scripts blind.** Some Discord-posted skills with raw.githubusercontent.com install URLs do whatever the author put on a side channel. Always fetch and read the installer before executing.

4. **Treating Discord-only entries as installable.** ~10% of entries (49 of 496) have a Discord message URL as their primary link. There is no public API to fetch Discord message bodies without credentials, so these effectively require the user to click through. Don't pretend otherwise.

5. **Confusing registry's author field with the GitHub owner.** The registry's `author` is a freeform display string copied from Discord; the actual GitHub repo owner is in `repo_url`. Use the repo URL to determine the canonical maintainer.

6. **Assuming one category per skill.** Some skills genuinely span categories. The registry picks one, so a search by category can miss adjacent entries. Run a keyword search to find strays.

7. **Caching `data.json`.** The registry is regularly resynced from Discord, and new entries land frequently. Always re-fetch for fresh results. The bundled script does not cache.

8. **Hardcoding types or categories.** The `type_order` field at the top of `data.json` is the only authoritative source. If a new type or category is added, code that branches on hard-coded strings will silently miss it. The bundled script reads `type_order` and `set(categories)` from the live data.

9. **Treating the registry as the source of truth.** The registry is a secondary index. The canonical source for any entry is its upstream repo or its Discord announcement. If a registry entry and the upstream repo disagree (e.g., description is stale), the upstream wins.

## Verification Checklist

- [ ] `data.json` fetched fresh (not from any local cache)
- [ ] Result counts cross-checked (could be empty due to query, not network failure)
- [ ] `type` and `category` values read from the data, not assumed from the cheat sheet
- [ ] Presented `name`, `author`, `type`, and a link (`repo_url` preferred, `url` fallback) per result
- [ ] When proposing install: upstream repo fetched and SKILL.md or README reviewed; prerequisites enumerated
- [ ] For Discord-only entries: explicitly told the user they need to open the Discord link
- [ ] After install: verified via `skills_list` / `skill_view` (current session can be cached — check in a fresh session if missing)
