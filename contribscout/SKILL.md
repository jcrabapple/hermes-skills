---
name: contribscout
description: "Use when looking for open-source contribution opportunities, finding repos where you can create visible value, or running a weekly contribution scan. Discovers, enriches, and analyzes GitHub repos for contribution fit."
version: 1.0.0
author: Jason Crabtree
license: MIT
metadata:
  hermes:
    tags: [github, open-source, contributions, discovery, career, agent-tooling]
    related_skills: [gh-cli, github-workflow, repo-discovery, github-trending]
---

# ContribScout

Find open-source repos where a thoughtful contributor can create visible value *before* obvious paths get crowded. Unlike "find good first issues" tools, ContribScout evaluates the full opportunity surface — freshness, documentation gaps, issue quality, saturation risk, and your specific skills — then uses LLM reasoning to identify the single best target and a concrete first step.

## How It Works

Three phases, each building on the last:

1. **Discovery** (`scripts/discover.sh`) — Searches GitHub via `gh` API for recently created, actively maintained repos with low star counts. Sorts by stars ascending (low stars = high opportunity for visibility).

2. **Enrichment** (`scripts/enrich.py`) — For each candidate repo, fetches README content, open issues with contribution labels (good first issue, help wanted), CONTRIBUTING.md presence, recent PR activity, contributor count, and commit velocity.

3. **Analysis** (LLM, inline) — You read the enriched data and reason about fit, saturation, and specific opportunity. This is the part that can't be hardcoded — it requires reading actual repo content and matching it against the user's skills and goals.

## When to Use

- User asks "where should I contribute to open source?"
- User wants to build visibility in a specific domain (AI tooling, API infrastructure, developer tools)
- User wants a weekly contribution opportunity scan
- User is evaluating whether a specific repo is worth contributing to
- User wants to track repos over time for the right moment to contribute

**Don't use for:** Finding bugs to fix (use `gh search issues` directly), monitoring your own repos (use standard GitHub tooling), or finding paid open-source work.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- `jq` installed
- Python 3.11+

## Phase 1: Discovery

```bash
bash scripts/discover.sh --max-results 15 --max-stars 1000
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max-results N` | 30 | Max repos to return |
| `--languages lang1,lang2` | TypeScript,Python | Languages to search |
| `--keywords kw1,kw2` | mcp server,agent sdk,developer tools,... | Search keywords (comma-separated) |
| `--max-stars N` | 1000 | Filter out repos above this star count |
| `--min-stars N` | 0 | Filter out repos below this star count |
| `--created-days N` | 120 | Repo must be created within N days |
| `--pushed-days N` | 30 | Repo must have been pushed within N days |

### Customizing for User's Domain

For AI/API infrastructure focus:
```bash
bash scripts/discover.sh --keywords "api gateway,llm inference,api sdk,model serving,developer platform" --languages "TypeScript,Python,Go"
```

For broader open-source contribution:
```bash
bash scripts/discover.sh --keywords "open source,community,documentation,beginner friendly,help wanted" --max-stars 500
```

## Phase 2: Enrichment

```bash
bash scripts/discover.sh --max-results 10 | python3 scripts/enrich.py --max-repos 10
```

The enrichment script fetches (in parallel, 4 workers):
- README content (first 3000 chars) and quality assessment
- Open issues with "good first issue" and "help wanted" labels
- CONTRIBUTING.md presence
- Recent PRs (merge rate — saturation signal)
- Contributor count
- Recent commit activity (last 10 commits)

### Enrichment Output Fields

| Field | What it tells you |
|------|-------------------|
| `readmeContent` | First 3000 chars of README — read this to understand the project |
| `readmeQuality` | missing/thin/basic/strong — thin README = docs contribution opportunity |
| `hasContributing` | Whether CONTRIBUTING.md exists — absent = opportunity to create one |
| `goodFirstIssues` | Issues labeled "good first issue" — direct contribution entry points |
| `helpWantedIssues` | Issues labeled "help wanted" — maintainer is asking for help |
| `recentPrs` | PR activity — high merge rate = responsive maintainers, high open count = backlog |
| `contributorCount` | Fewer contributors = your work is more visible |
| `saturationLevel` | low/medium/high/unknown — low = best opportunity |
| `contributionSignalCount` | 0-5 — how many contribution paths exist |

## Phase 3: Analysis (LLM)

After running discovery + enrichment, you have enriched JSON data. **This is where you add value that no script can.** Read the data and produce a structured analysis.

### Analysis Framework

For each promising repo (top 3-5 by signal count), assess:

**1. Fit Assessment**
- Does the repo's domain match the user's skills? (TypeScript, Python, API infrastructure, AI tooling, support engineering)
- Is the tech stack something the user can be productive in quickly?
- Is the problem space interesting enough to sustain motivation?

**2. Opportunity Identification**
- Read `readmeContent` — what does the project do? What's missing from the docs?
- Read `goodFirstIssues` and `helpWantedIssues` — are there specific issues the user could tackle?
- If no labeled issues: are there open issues that match the user's skills?
- If no CONTRIBUTING.md: could the user create one as a first contribution?
- If `readmeQuality` is "thin" or "missing": documentation improvement is an entry point.

**3. Saturation Judgment**
- `contributorCount` < 5 and `stars` < 50: very low saturation, high visibility
- `contributorCount` 5-20 and `stars` 50-500: moderate saturation, still good visibility
- `contributorCount` > 20 or `stars` > 500: higher saturation, harder to stand out
- Recent PR merge rate: if PRs sit for weeks, contributions won't be noticed

**4. First Concrete Step**
Name the *specific* action to take first:
- "Comment on issue #X saying you'd like to work on it"
- "Read the README, then open an issue suggesting a CONTRIBUTING.md"
- "Fork the repo, fix the typo in src/utils.ts line 42, submit a PR"
- "Join their Discord/Discussions and ask where help is needed"
Not: "look at the good first issues." Be specific.

### Report Format

Deliver the analysis as a markdown report:

```markdown
# ContribScout Weekly Report — {date}

## Top Opportunity: {repo-name}

**What it is:** {1-2 sentence project description from README}

**Why it fits:** {skill match, domain relevance, tech stack alignment}

**Saturation:** {level} — {contributorCount} contributors, {stars} stars

**Specific opportunity:** {issue # or docs gap or feature you could add}

**First step:** {concrete action}

**Confidence:** {high/medium/low} — {why}

---

## Also Worth Looking At

### {repo-name 2}
{shorter analysis, 2-3 sentences}

### {repo-name 3}
{shorter analysis, 2-3 sentences}

---

## Watchlist Updates

{Repos from previous runs that changed — new issues, increased activity, etc.}

## Skipped
{Repos that were considered but rejected, with one-line reason}
```

### Watchlist Management

Maintain a watchlist at `data/watchlist.json`:

```json
{
  "repos": [
    {
      "fullName": "owner/repo",
      "addedDate": "2026-06-23",
      "lastChecked": "2026-06-23",
      "starsAtAddition": 0,
      "reason": "MCP server with thin docs, 2 open issues"
    }
  ]
}
```

On each run:
1. Load the watchlist
2. Check watched repos for changes (new issues, new stars, new PRs)
3. Alert on: new good-first-issue labels, stale issues (good time to grab), saturation increase
4. Add new interesting repos to the watchlist
5. Remove repos that have become too saturated or inactive

## Full Pipeline (One-Shot)

```bash
# Discover, enrich, and save results for analysis
bash scripts/discover.sh --max-results 15 | python3 scripts/enrich.py --max-repos 10 > /tmp/contribscout-results.json

# Then the LLM reads /tmp/contribscout-results.json and produces the analysis
```

## Cron Job Setup

For a weekly scan delivered to Discord:

```bash
# Schedule: every Monday at 9 AM ET
hermes cron add \
  --name "ContribScout Weekly" \
  --schedule "0 9 * * 1" \
  --prompt "Run the ContribScout skill. Execute: bash scripts/discover.sh --max-results 15 | python3 scripts/enrich.py --max-repos 10. Then read the results and produce the weekly analysis report. Load the watchlist from data/watchlist.json and check watched repos for changes. Deliver the report to Discord." \
  --skills contribscout \
  --toolsets terminal,file \
  --deliver discord
```

## Customizing Search Domains

Edit the default keywords in `scripts/discover.sh` or pass `--keywords`:

| Domain | Keywords |
|--------|----------|
| AI/Agent tooling | mcp server,agent sdk,llm tooling,ai agent,model serving |
| API infrastructure | api gateway,api sdk,developer platform,web framework |
| Developer tools | cli tool,developer tools,workflow automation,ci cd |
| DevRel/Docs | documentation,examples,tutorial,onboarding,quickstart |
| Security | security audit,vulnerability,dependency,compliance |

## Common Pitfalls

1. **GitHub API rate limits.** The enrichment script makes ~6 API calls per repo. With 10 repos that's 60 calls. If you hit rate limits, reduce `--max-repos` or add delays. The `gh` CLI handles auth automatically.

2. **0-star repos may be abandoned.** Always check `pushedAt` and `recentCommitCount`. A repo with 0 stars but 10 recent commits is active. A repo with 0 stars and no commits in 60 days is dead.

3. **"Good first issue" labels are often stale.** Read the issue content — was it opened 6 months ago and commented on last week, or opened 2 days ago? Recency matters.

4. **Low star count ≠ high opportunity.** A repo with 0 stars, 0 issues, 0 forks, and 1 contributor is probably someone's personal project. Look for repos with *some* activity but low saturation — forks, issues, and recent commits indicate the project is alive and accepting contributions.

5. **README quality is a double signal.** A "thin" README means the project is hard to get into, but it also means a docs contribution would be valuable. Flag both.

6. **The enrichment script times out on large batches.** Default timeout is 120s for 10 repos. For larger batches, increase `--timeout` or reduce `--max-repos`.

## Verification Checklist

- [ ] `gh auth status` shows authenticated
- [ ] `jq --version` is available
- [ ] `python3 --version` is 3.11+
- [ ] `bash scripts/discover.sh --max-results 3` returns JSON with repos
- [ ] `bash scripts/discover.sh --max-results 3 | python3 scripts/enrich.py --max-repos 3` returns enriched JSON
- [ ] Enriched JSON contains `readmeContent`, `contributorCount`, `contributionSignalCount`
- [ ] `data/watchlist.json` exists (create empty if not: `{"repos": []}`)
