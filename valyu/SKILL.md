---
name: valyu
description: >
  Search web + 36+ proprietary data sources (arXiv, PubMed, SEC filings,
  clinical trials, patents, financial data, news) via Valyu API. Also
  provides URL content extraction, AI-synthesized answers with citations,
  and deep research reports. Use instead of web_search/web_extract when
  you need academic papers, financial filings, medical data, or higher-
  quality search results.
triggers:
  - "search for papers"
  - "academic search"
  - "search arxiv"
  - "search pubmed"
  - "SEC filings"
  - "financial data"
  - "clinical trials"
  - "deep research on"
  - "research report on"
  - "valyu search"
  - "patent search"
  - "search proprietary sources"
---

# Valyu Search & Research

Direct integration with [Valyu API](https://docs.valyu.ai/) — unified
access to web search plus 36+ proprietary data sources through a single
REST API.

## Setup

1. Get an API key from [platform.valyu.ai](https://platform.valyu.ai/) ($10 free credits)
2. Add to your environment: `export VALYU_API_KEY="your-key-here"`
3. Or add to `~/.hermes/.env`: `VALYU_API_KEY=your-key-here`

The helper script reads the key from the environment or `~/.hermes/.env` automatically.

## Quick Reference

Use the helper script at `scripts/valyu.py` (relative to this skill's directory):

```bash
SCRIPT="scripts/valyu.py"  # adjust to your install path

# Web search
python3 $SCRIPT search "query here"

# Proprietary sources only (arXiv, PubMed, SEC, etc.)
python3 $SCRIPT search "query" --type proprietary

# Search specific sources
python3 $SCRIPT search "CRISPR trials" --sources "medical"
python3 $SCRIPT search "NVDA earnings" --sources "finance"

# Extract content from URLs (up to 50)
python3 $SCRIPT extract "https://example.com" "https://example2.com"

# AI-synthesized answer with citations
python3 $SCRIPT answer "What are the latest CRISPR advances?"

# Deep research report (async, may take a few minutes)
python3 $SCRIPT research "Comprehensive analysis of quantum computing in 2026"
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/search` | POST | Semantic search across web + proprietary datasets |
| `/v1/contents` | POST | Extract clean markdown from URLs |
| `/v1/answer` | POST | AI-synthesized answers with citations |
| `/v1/deepresearch` | POST | Multi-step research reports (async) |

## Search Types

- `all` (default) — web + proprietary, LLM-selected
- `web` — web search only
- `proprietary` — academic, financial, premium sources only
- `news` — news articles only

## Source Presets

Use with `--sources` flag:

| Preset | Sources |
|--------|---------|
| `medical` | PubMed, clinical trials, FDA |
| `finance` | SEC filings, earnings, stock data |
| `academic` | arXiv, PubMed, bioRxiv, journals |
| `legal` | Patents, court filings |

Or pass specific dataset IDs: `valyu/valyu-arxiv`, `valyu/valyu-pubmed`, etc.
Or pass domains: `arxiv.org`, `sec.gov`, `nasa.gov`.

## Response Fields

Each search result contains:
- `title`, `url`, `content` — the essentials
- `source` — where it came from (web, arxiv, pubmed, etc.)
- `relevance_score` — 0.0 to 1.0
- `publication_date` — when available
- `price` — cost in dollars for this result

## Cost Awareness

- Search: charged per result based on source and content length
- Contents: charged per URL extracted
- Answer: charged per search + generation
- Research: charged per step in the research chain
- Always check `total_deduction_dollars` in responses

## Pitfalls

- **API key**: set `VALYU_API_KEY` in your environment or `~/.hermes/.env`.
  The helper script loads it automatically. If running from cron, ensure
  the env var is available.
- **Rate limits**: no documented rate limits, but be mindful of cost.
  Use `--max-results` to cap results on exploratory queries.
- **DeepResearch is async**: returns a task ID, not immediate results.
  The helper script polls automatically but it can take 2-5 minutes.
- **search_type vs sources**: `--type proprietary` restricts to non-web
  sources. `--sources` further narrows within a type. Don't confuse them.
- **Content extraction**: Valyu's extract is more reliable than
  `web_extract` for JS-heavy pages (supports Chrome rendering via
  `extract_effort=high`).

## When to Use Valyu vs Built-in Tools

| Need | Use |
|------|-----|
| Quick web lookup | `web_search` (faster, free) |
| URL content extraction | `web_extract` (free) or `valyu extract` (higher quality) |
| Academic papers | `valyu search --type proprietary --sources academic` |
| Financial filings | `valyu search --sources finance` |
| Medical/clinical data | `valyu search --sources medical` |
| High-quality research | `valyu answer` or `valyu research` |
| JS-heavy page extraction | `valyu extract` with effort=high |

## Helper Script

Full script at `scripts/valyu.py`. Pure Python 3, no external dependencies.
Reads `VALYU_API_KEY` from environment or `~/.hermes/.env`. Outputs JSON
to stdout for easy piping.
