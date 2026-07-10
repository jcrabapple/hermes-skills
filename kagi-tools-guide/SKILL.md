---
name: kagi-tools-guide
description: "Guide for using the kagi-tools Hermes plugin — which tool for what, auth requirements, fallback patterns, and known quirks."
version: 1.0
---

# Kagi Tools Guide

Guide for using the 14 tools provided by the `kagi-tools` Hermes plugin at `~/.hermes/plugins/kagi-tools/`.

## When to Use

- `kagi_search` is the **primary search tool** — use it instead of `web_search` when Kagi is the working backend. Supports region, time window, lens, verbatim, and order filters for narrowing results.
- `kagi_quick` for **single-answer factual queries** — returns a concise AI answer with cited references. Faster than `kagi_assistant` for "what is X" questions.
- `kagi_ask_page` to **ask a question about a specific URL** — gives you an AI summary of a page with citations. Use when you need to understand content on a single page without extracting it.
- `kagi_assistant` for **open-ended research conversations** — supports thread continuation (`thread_id`), model override, lens scoping, and web access toggles.
- `kagi_translate` to **translate text** — auto-detects source language, supports 100+ languages. Returns alternatives, word insights, and alignments.
- `kagi_summarize` to **summarize a URL or text** — defaults to subscriber mode (free with session token). Set `subscriber=false` with an engine (cecil/agnes/daphne/muriel) for paid API mode.
- `kagi_news` for **AI-curated news** — category slugs: world, usa, tech, science, business, etc. Use `kagi_news_categories` to list available categories first.
- `kagi_smallweb` for **indie blog posts** — independent personal blogs curated by Kagi.

**Deprecated tools** (v0 API endpoints, no Kagi v1 equivalent yet):
- `kagi_fastgpt`, `kagi_enrich_web`, `kagi_enrich_news` — return a clear error message. Use `kagi_search` or `kagi_quick` instead.

## Auth Model

| Auth | Tools | Status |
|------|-------|--------|
| None (public) | `kagi_news`, `kagi_news_categories`, `kagi_smallweb` | Always available |
| `KAGI_SESSION_TOKEN` (env) | `kagi_search`, `kagi_quick`, `kagi_ask_page`, `kagi_assistant`, `kagi_assistant_thread_list`, `kagi_assistant_thread_get`, `kagi_translate`, `kagi_summarize` | Set via env |
| `KAGI_API_TOKEN` (env) | `kagi_fastgpt`, `kagi_enrich_web`, `kagi_enrich_news` | Set, but endpoints are deprecated |

## Known Issues

- **kagi-cli v0.6.1 uses `Bot` auth header, not `Bearer`** — the Rust binary at `~/.local/bin/kagi` sends `Authorization: Bot <token>` on v0 API endpoints. Kagi's v1 API requires `Authorization: Bearer <token>`. The session-token path (cookie-based) still works, so `kagi_search` etc. function correctly.
- **FastGPT and Enrichment are deprecated** — the old `/api/v0/fastgpt` and `/api/v0/enrich/*` endpoints no longer accept new JWT-format API keys. Kagi's v1 API only offers `/search` and `/extract`.
- **kagi-cli auth check** — `kagi auth check` validates session token only. To test API token, use `kagi fastgpt "test"` (will fail with v0 deprecation).
- **Summarize subscriber mode** — always use `subscriber=true` (default) to use the free web summarizer. The paid API mode requires `KAGI_API_TOKEN` and a summarization engine.

## Fallback Patterns

When `kagi_search` returns no results:
1. Try `kagi_quick` for a synthesized answer from live results
2. Try `kagi_assistant` with `web_access=true` for a research conversation
3. Fall back to browser tools for direct page inspection

When a Kagi tool fails with auth errors:
- Session-token tools: verify `KAGI_SESSION_TOKEN` is set in env
- API-token tools: verify `KAGI_API_TOKEN` is set in `~/.hermes/.env`; test with direct curl: `curl -s https://kagi.com/api/v1/search -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"test","limit":1}'`
