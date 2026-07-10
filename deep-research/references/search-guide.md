# Search Strategy Guide

Quick reference for effective query construction and temporal precision.

## nanogpt_web_search Depth Parameter

| `depth` | Speed | Reliability | When to use |
|----------|-------|-------------|-------------|
| `standard` | 3-5s | High — almost never times out | Default. Use for all searches. |
| `deep` | 10-30s | **Frequently times out** (read timeout=30s) | Avoid unless you specifically need deeper Linkup crawling. Prefer 2 standard searches with different phrasings. |

**If a `deep` search times out:** Retry the same query with `depth='standard'`. It will almost always succeed. Do not retry with `deep` — it will likely time out again.

## Effective Query Patterns

```
# Be specific with context
❌ "AI trends"
✅ "enterprise AI adoption trends 2026"

# Include authoritative source hints
"[topic] research paper"
"[topic] McKinsey report"
"[topic] industry analysis"

# Search for specific content types
"[topic] case study"
"[topic] statistics"
"[topic] expert interview"

# Use temporal qualifiers — always use the ACTUAL current year
"[topic] 2026"
"[topic] latest"
"[topic] recent developments"
```

## Temporal Awareness

Always check the current date before forming search queries. Match precision to intent:

| User intent | Temporal precision | Example query |
|---|---|---|
| "today / this morning / just released" | **Month + Day** | `"tech news February 28 2026"` |
| "this week" | **Week range** | `"technology releases week of Feb 24 2026"` |
| "recently / latest / new" | **Month** | `"AI breakthroughs February 2026"` |
| "this year / trends" | **Year** | `"software trends 2026"` |

**Rules:**
- When the user asks about "today" or "just released", use **month + day + year** to get same-day results
- Never drop to year-only when day-level precision is needed — `"tech news 2026"` will NOT surface today's news
- Try multiple phrasings: numeric (2026-02-28), written (February 28 2026), and relative (today, this week)

## Diversity Checklist

| Information Type | Purpose | Example Searches |
|-----------------|---------|------------------|
| **Facts & Data** | Concrete evidence | `"statistics"`, `"data"`, `"numbers"`, `"market size"` |
| **Examples & Cases** | Real-world applications | `"case study"`, `"example"`, `"implementation"` |
| **Expert Opinions** | Authority perspectives | `"expert analysis"`, `"interview"`, `"commentary"` |
| **Trends & Predictions** | Future direction | `"trends 2026"`, `"forecast"`, `"future of"` |
| **Comparisons** | Context and alternatives | `"vs"`, `"comparison"`, `"alternatives"` |
| **Challenges & Criticisms** | Balanced view | `"challenges"`, `"limitations"`, `"criticism"` |

## Parallel Search Strategy

Batch independent searches in a single assistant turn — the runtime executes them concurrently:

```python
# Phase 1: Broad exploration — batch 3 searches
nanogpt_web_search(query="topic overview")
nanogpt_web_search(query="topic alternatives theories")
nanogpt_web_search(query="topic latest evidence 2025")
```

If one search in a batch times out, the others still return results. Retry the failed query with `depth='standard'` in the next turn.

## Extraction Strategy

Use `nanogpt_web_extract` to read full source content when:
- A search result looks authoritative (NASA, Nature, Science, university press releases)
- You need detailed data, case studies, or expert quotes beyond the snippet
- The source is a Wikipedia article for comprehensive overviews

Batch 3-5 URL extractions per call (the tool accepts up to 5 URLs). Prioritize:
1. Wikipedia for overviews and context
2. Academic journals (Nature, Science, PNAS) for data and findings
3. University press releases for accessible summaries of recent research
4. Science news outlets (ScienceDaily, Phys.org) for recency
