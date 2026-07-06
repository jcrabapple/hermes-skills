# Hermes Community Registry

Search, filter, evaluate, and install community Hermes Agent skills, plugins, tools, and agents from the [babylondreams.de community registry](https://babylondreams.de/hermes-registry/).

## What it does

The babylondreams.de registry is a curated directory of 490+ community-built Hermes Agent projects, synced from the Hermes Discord `#community-projects` and `#plugins-skills-skins` channels. This skill gives your Hermes Agent a structured way to search it.

The registry covers skills, plugins, tools, agents, integrations, and skins across categories like memory, productivity, devops, observability, security, research, and more. It's a broader index than the official `optional-skills/` directory in `NousResearch/hermes-agent`.

**The registry is a discovery surface, not an installer.** This skill helps you find and evaluate entries; installation always goes through the upstream source (GitHub repo, install script, etc.).

## Features

- **Bundled search script** (`scripts/search_registry.py`) — fetches the live `data.json` and filters by keyword, type, category, or author in a single pass
- **Evaluation checklist** — resolve the actual source, read upstream README, check recent commits, assess install surface, security review
- **Category cheat sheet** — map user intent ("I want memory/persistence") to registry categories
- **Provenance awareness** — entries from `community-projects` vs `plugins-skills-skins` have different quality norms

## Prerequisites

- Python 3.8+ (stdlib only — no pip installs needed)
- `curl` (for the inline pipeline alternative)
- Network access to `babylondreams.de`

No API keys required. The registry is a public static site.

## Install

```bash
# Clone the full skills repo
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/hermes-community-registry ~/.hermes/skills/

# Or just this skill
git clone https://github.com/jcrabapple/hermes-skills.git /tmp/hermes-skills
cp -r /tmp/hermes-skills/hermes-community-registry ~/.hermes/skills/
```

Verify installation in a new Hermes session:

```bash
hermes skills list | grep community-registry
```

## Usage

### Search by keyword

```bash
python3 scripts/search_registry.py --keyword sqlite
python3 scripts/search_registry.py --keyword "code review"
```

### Filter by type and category

```bash
python3 scripts/search_registry.py --type skill --category memory
python3 scripts/search_registry.py --type plugin --category devops --keyword grafana
```

### Search by author

```bash
python3 scripts/search_registry.py --author "Hypercubed"
```

### JSON output (for piping)

```bash
python3 scripts/search_registry.py --keyword "code review" --json | python3 -m json.tool
```

### List all types and categories

```bash
python3 scripts/search_registry.py --list-values
```

### Inline curl (no install needed)

```bash
curl -fsSL https://babylondreams.de/hermes-registry/data.json | python3 -c "
import json, sys
for e in json.load(sys.stdin)['entries']:
    if e['type'] == 'skill' and e['category'] == 'memory':
        print(f\"- {e['name']} — {e.get('repo_url') or e['url']}\")
"
```

## Output

Each result shows:

```
  Agent Memory Skill
    type=skill  category=memory  author=xPerryx
    desc: Local-first SQLite memory for Hermes with authority lanes, recall snippets, ...
    url : https://github.com/xMannixx/agent-memory-skill
```

With `--json`, full records including `id`, `discord_url`, `discord_date`, `first_seen`.

## How it works

1. The script fetches `https://babylondreams.de/hermes-registry/data.json` (the static data backing the registry's Fuse.js search UI)
2. Filters in-memory by the provided criteria (keyword is a case-insensitive substring match across name + description + author + category + slug)
3. Sorts by author + name and prints a table, or dumps JSON

The registry data is synced from Discord by the maintainer (Alexander Kucera). No caching is done — every run fetches fresh data.

## Pitfalls

- **Don't trust the `stars` field.** The upstream scraping layer reports 0 for almost every entry. Use the GitHub API for live star counts.
- **Don't run install scripts blind.** Some entries point to `raw.githubusercontent.com` install scripts. Always fetch and read them before executing.
- **~10% of entries are Discord-only.** Their `url` is a Discord message link with no public repo. These require manual inspection.
- **Re-fetch every time.** The registry is regularly resynced. Don't cache `data.json`.

## See also

- [babylondreams.de Hermes Community Registry](https://babylondreams.de/hermes-registry/)
- [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs)
- The `hermes-optional-skills` skill (covers the official `optional-skills/` tree in `NousResearch/hermes-agent`)

## License

MIT
