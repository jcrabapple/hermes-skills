# ContribScout

Find open-source repos where a thoughtful contributor can create visible value *before* obvious paths get crowded.

## What It Does

ContribScout discovers, enriches, and analyzes GitHub repos for contribution fit. Unlike "find good first issues" tools, it evaluates the full opportunity surface — freshness, documentation gaps, issue quality, saturation risk, and your specific skills — then uses LLM reasoning to identify the best target and a concrete first step.

**Three phases:**

1. **Discovery** — Searches GitHub via `gh` API for recently created, actively maintained repos with low star counts. Sorts by stars ascending (low stars = high opportunity for visibility).

2. **Enrichment** — For each candidate repo, fetches README content, open issues with contribution labels, CONTRIBUTING.md presence, recent PR activity, contributor count, and commit velocity.

3. **Analysis** — The LLM reads the enriched data and reasons about fit, saturation, and specific opportunity. This is the part that can't be hardcoded — it requires reading actual repo content and matching it against the user's skills and goals.

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com/) installed
- `gh` CLI authenticated (`gh auth login`)
- `jq` installed
- Python 3.11+

## Install

Copy the `contribscout/` directory into your Hermes skills folder:

```bash
cp -r contribscout ~/.hermes/skills/contribscout
```

## Usage

### One-shot scan

```bash
cd ~/.hermes/skills/contribscout
bash scripts/discover.sh --max-results 15 | python3 scripts/enrich.py --max-repos 10 > /tmp/results.json
```

Then ask Hermes to analyze the results:

> "Load the contribscout skill. Read /tmp/results.json and produce the weekly contribution analysis report."

### Customizing searches

```bash
# Focus on AI/agent tooling
bash scripts/discover.sh --keywords "mcp server,agent sdk,llm tooling" --languages "TypeScript,Python"

# Broader search, higher star ceiling
bash scripts/discover.sh --max-stars 2000 --min-stars 10 --keywords "api gateway,developer tools,workflow automation"

# Add Go to the mix
bash scripts/discover.sh --languages "TypeScript,Python,Go" --keywords "cli tool,infrastructure,devops"
```

### Scheduled weekly scan (cron)

```bash
hermes cron add \
  --name "ContribScout Weekly" \
  --schedule "0 9 * * 1" \
  --prompt "Run the ContribScout skill. Execute: bash scripts/discover.sh --max-results 15 | python3 scripts/enrich.py --max-repos 10. Then read the results and produce the weekly analysis report. Load the watchlist from data/watchlist.json and check watched repos for changes. Deliver the report to Discord." \
  --skills contribscout \
  --toolsets terminal,file \
  --deliver discord
```

## Options

### discover.sh

| Flag | Default | Description |
|------|---------|-------------|
| `--max-results N` | 30 | Max repos to return |
| `--languages lang1,lang2` | TypeScript,Python | Languages to search |
| `--keywords kw1,kw2` | mcp server,agent sdk,... | Search keywords |
| `--max-stars N` | 1000 | Upper star count filter |
| `--min-stars N` | 0 | Lower star count filter |
| `--created-days N` | 120 | Repo age in days |
| `--pushed-days N` | 30 | Recent push window in days |

### enrich.py

| Flag | Default | Description |
|------|---------|-------------|
| `--max-repos N` | 10 | Max repos to enrich |
| `--timeout SECS` | 120 | Overall timeout |

## How It Works

The key insight: a small fresh project with weak docs and active issues can be a *better* contribution target than a huge saturated repo. ContribScout surfaces those opportunities.

**Discovery** uses the GitHub Search API with `sort=stars&order=asc` to find the lowest-starred repos matching your keywords and language. This is deliberately different from tools that surface popular repos.

**Enrichment** fetches data that scoring heuristics can't capture: actual README content (so the LLM can understand what the project does), specific issue titles (so the LLM can identify what to work on), and commit messages (so the LLM can judge project velocity).

**Analysis** is where Hermes adds the real value. Instead of arbitrary scoring weights, the LLM reads the enriched data and produces a structured assessment: does this repo match your skills? Is there a specific issue you could tackle? What's the first concrete step?

## Output

The LLM produces a markdown report with:

- **Top Opportunity** — the single best target, with fit assessment, saturation analysis, specific opportunity, and first concrete step
- **Also Worth Looking At** — 2-3 runners-up with shorter analysis
- **Watchlist Updates** — repos from previous runs that changed
- **Skipped** — repos that were considered but rejected, with reasons

## License

MIT
