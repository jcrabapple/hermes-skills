---
name: github-trending
description: Fetch top trending GitHub repositories for the past week, format a ranked list, and deliver via email. Designed for weekly cron jobs.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [GitHub, Trending, Research, Cron, Email]
    triggers:
      - trending github repos
      - github weekly report
      - trending repositories
---

# GitHub Trending Weekly Report

Fetch the top trending GitHub repositories from the past week, filter for English-language, rank by weekly stars, and deliver via email.

## Steps

### 1. Fetch the trending page

Navigate to `https://github.com/trending?since=weekly` using the browser.

```python
browser_navigate(url="https://github.com/trending?since=weekly")
```

**Important:** The GitHub trending page is JavaScript-rendered. `web_extract` returns only a summary, not structured data. `browser_snapshot(full=true)` truncates on long pages (25+ repos). The reliable approach is `browser_vision`.

### 2. Extract repo data with vision

```python
browser_vision(question="List all trending repositories visible on this page. For each repo give: owner/repo name, description, total stars, language, and stars this week.")
```

This captures all repos visible in the viewport. If you need repos beyond the first screen, scroll down and call `browser_vision` again, or combine with `browser_snapshot` data from the first screenful.

**Why vision over snapshot:** The snapshot for this page is very large (~8000+ chars) and gets truncated. Vision processes the visual layout and returns structured data for all visible repos in one call. One vision call typically captures 15-20 repos.

### 3. Filter and rank

- Remove non-English repositories (e.g., repos with Chinese-only descriptions like `TradingAgents-CN`, or primarily Chinese repos like `MoneyPrinterTurbo` which has a bilingual but Chinese-primary description).
- Rank by **stars gained this week** (descending).
- Take the top 10.

### 4. Format the report

For each repo, include:
- **Rank and name** with link
- **Stars this week** and **total stars**
- **Programming language**
- **One-line description**

### 5. Send via email

Pick the email CLI that fits your stack. A himalaya example:

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: you@example.com
Subject: 🔥 Top 10 Trending GitHub Repositories This Week (date range)

[formatted report body]
EOF
```

Or send via AgentMail / any SMTP CLI. The skill is delivery-agnostic — pick the tool you already have configured.

## Pitfalls

- **Do not use `web_extract` alone** for the trending page — it returns an LLM-summarized paragraph, not structured repo data.
- **Do not rely on `browser_snapshot` for the full list** — the page is too large and gets truncated. Use `browser_vision` instead.
- **The first vision attempt may return a blank screenshot** if the page hasn't finished loading. If this happens, navigate again and retry the vision call immediately.
- **GitHub trending page structure is stable** — the article/heading/link pattern is consistent. The vision prompt should always work.
- **Close the browser** after extraction to free up the Browserbase session.
