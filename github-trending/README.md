# GitHub Trending Weekly Report

Weekly digest of the top 10 trending GitHub repositories, ranked by stars gained in the past 7 days. Designed to run as a cron job and email a clean report.

## What it does

1. Loads `https://github.com/trending?since=weekly` in a headless browser
2. Extracts repo data via `browser_vision` (the page is JS-rendered and too large for `browser_snapshot`)
3. Filters out non-English repos, ranks by weekly stars, takes the top 10
4. Emails a formatted report

## Why browser_vision and not web_extract?

- `web_extract` returns a one-paragraph LLM summary, not structured data
- `browser_snapshot(full=true)` truncates because the page renders 25+ repos (~8000+ chars)
- `browser_vision` reads the visual layout and returns clean structured data in one call

This is one of the few skills where vision is genuinely the right tool.

## Setup

Requires:
- A browser tool with vision support (Browserbase or similar)
- An email delivery method — himalaya, AgentMail, mutt, or any SMTP CLI

No API keys required — the GitHub trending page is public.

## Install

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/github-trending ~/.hermes/skills/research/
```

## Usage

Triggers on: "trending github repos", "github weekly report", "trending repositories".

Recommended cron schedule: Monday morning. GitHub's weekly window resets Sunday night US time, so Monday captures a complete week.

```python
cronjob(action="create", schedule="0 9 * * 1",
        prompt="Run the github-trending skill and email the top 10 report.")
```

## Output example

```
🔥 Top 10 Trending GitHub Repositories This Week (May 12–18, 2026)

1. openai/whisper-cpp          ⭐ +4,231 (total 38,402)  C++
   CPU-optimized Whisper inference — no Python, no PyTorch.

2. tanstack/router             ⭐ +2,108 (total 11,840)  TypeScript
   Modern type-safe router for React. ...
```

## Pitfalls

See [SKILL.md](./SKILL.md) for the full list. Key ones:
- First vision call can return a blank screenshot if the page hasn't finished loading — re-navigate and retry
- Always close the browser after extraction to free the Browserbase session
- Filter out Chinese-only repos (the trending page surfaces many)
