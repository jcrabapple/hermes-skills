---
name: repo-discovery
version: 1.0.0
description: Automated GitHub repository discovery and monitoring - scraping, scoring, and integration patterns
summary: Build and operate repo discovery pipelines (GitRadar, etc.) with proper metadata enrichment, scoring, and feedback loops
triggers:
  - github scraping
  - repo discovery
  - trending repos
  - gitradar
  - monitor github
  - find repositories
layer: session
requires:
  binaries:
    - python3
---

# Repo Discovery Automation

Automated GitHub repository discovery involves scraping trending/search results, enriching metadata, scoring relevance, and optionally learning from user feedback. Common tools: GitRadar, custom scripts, GitHub API integration.

## Core Patterns

### 1. Metadata Enrichment (Critical)

**Problem**: Scraping GitHub Trending or similar pages typically yields only repository names (e.g., `owner/repo`), not full metadata (stars, description, topics, license).

**Consequence**: Repos with 0 stars/metadata fail quality filters (e.g., `dead_repo` filter requiring min 10 stars), causing all trending repos to be filtered out.

**Solution**: Two-phase collection with API enrichment:

```python
def enrich_trending_repos(trending_repos):
    """Fetch metadata from GitHub API for scraped repos (otherwise they have 0 stars/metadata)."""
    enriched = []
    failed = 0
    for repo_info in trending_repos:
        full_name = repo_info["full_name"]
        url = f"https://api.github.com/repos/{full_name}"
        
        try:
            wait_for_rate_limit()  # Respect 60 req/hr unauthenticated, 5000 authenticated
            req = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github+json"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                enriched_repo = extract_repo_metadata(data)
                enriched_repo["source"] = repo_info.get("source", "trending")
                enriched.append(enriched_repo)
        except Exception as e:
            failed += 1
    
    if failed > 0:
        print(f"WARN: Failed to enrich {failed}/{len(trending_repos)} repos")
    return enriched
```

**Key points**:
- Use `GET /repos/{owner}/{repo}` endpoint for individual repo metadata
- Respect rate limits (60/hr unauthenticated, 5000/hr with token)
- Handle failures gracefully — partial enrichment is acceptable
- Set `Accept: application/vnd.github+json` header for v3 API

### 2. Rate Limiting

**Unauthenticated**: 60 requests/hour (harsh penalty for exceeding)
**Authenticated**: 5000 requests/hour (set `GITHUB_TOKEN` or `GH_TOKEN` env var)
**Search API**: 30 requests/minute (stricter limit)

```python
def wait_for_rate_limit():
    """Throttle to avoid hitting GitHub rate limits."""
    # Track timestamps of recent calls
    # Sleep if limit would be exceeded
    pass
```

**Authentication fallback**: Don't crash if `gh` CLI isn't installed — handle `FileNotFoundError` gracefully and continue unauthenticated.

### 3. Query Templates (Search API)

Structure queries as templates with `{stars}` placeholder:

```python
QUERY_TEMPLATES = [
    {"q": "topic:llm stars:>{stars}", "sort": "stars", "order": "desc", "star_base": 5},
    {"q": "topic:ai-agents stars:>{stars}", "sort": "stars", "order": "desc", "star_base": 5},
    # ...
]
```

**Dynamic threshold application**:
- Topic-specific queries: use `star_base` directly (allow low thresholds like 5)
- General queries: enforce global `star_threshold` as minimum floor

### 4. Scoring and Classification

**Scoring components** (typical weights):
- Stars (log-scaled): 40%
- Keyword relevance: 30%
- Freshness (pushed_at): 20%
- Activity (created_at): 10%

**Classification labels** (adjust thresholds to taste):
- ADOPT (80+): High-quality, integrate immediately
- EXTRACT (60-79): Useful patterns/components
- FORK/PRODUCT (50-59): Potential fork target
- PLUGIN/SKILL (40-49): Integration candidate
- INSPIRATION (20-39): Ideas for future work
- NOISE (<20): Skip

### 5. User Feedback Loop

Store user ratings (useful/noise/duplicate) and apply to scoring:

```json
{
  "ratings": {
    "owner/repo": {
      "rating": "useful",
      "timestamp": "2026-06-23T01:30:00Z"
    }
  }
}
```

Apply feedback bonuses:
- `useful`: +15 points
- `noise`: -20 points
- `duplicate`: -10 points

**Learning opportunity**: Track which topics/languages correlate with high ratings for semantic similarity boosting (advanced).

### 6. LLM Enrichment (Optional)

For top-scored repos, fetch README and generate one-line summary via LLM:

```python
def generate_summary(description, readme_excerpt):
    prompt = f"""Write ONE clear sentence summarizing what this tool does.
    
Repository Description: {description}
README Excerpt: {readme_excerpt[:3000]}

One-sentence summary:"""
    # Call LLM API
    pass
```

**NanoGPT enrichment** (if `NANOGPT_API_KEY` set):
- Endpoint: `https://nano-gpt.com/api/v1/chat/completions` (NOT `api.nanogpt.co` — that domain has TLS issues)
- Model: `gpt-4o-mini` works; Qwen models are not supported on the `/v1/chat/completions` endpoint (returns 400)
- README fetch: use GitHub API `Accept: application/vnd.github.v3.raw` to get raw text
- Truncate README to 3000 chars to stay within token limits

**Use cases**:
- Daily digest for Discord/Slack
- Obsidian note generation
- Blog post automation

## Common Pitfalls

1. **Trending scraping without enrichment**: All repos filtered as "dead" due to 0 stars
2. **Hard-crashing on missing `gh` CLI**: Use try/except around subprocess.run
3. **Counting enriched repos as "new"**: Track which repos were actually *added* (not in cache), not just enriched
4. **Sequential API calls**: Use asyncio + aiohttp for 5-10x speedup on large scans
5. **No deduplication**: Trending + search can return same repos — dedupe by `full_name`
6. **Wrong function name in `collect_weekly()`**: The weekly collection function calls `scrape_trending()` with no args, but the actual function signature is `scrape_trending(url, label)`. This crashes with `TypeError: missing 2 required positional arguments`. The correct call is `scrape_all_trending()` which iterates all trending pages internally. Fix applied 2026-07-06 in `~/workspace/gitradar-hermes/scripts/gitradar-discover.py` line 851.
7. **403 on one query aborts entire run**: GitHub's search API has both a primary limit (30 req/min) and a secondary "computed" rate limit that can return 403 even when the 30/min counter is fine. The original code bails out of the entire query loop on any 403, abandoning all remaining queries. Fix: wait 30s and continue to the next query instead of breaking. Also check the `Retry-After` header for GitHub's secondary rate limit and retry once after waiting.

8. **Daily mode pagination blowup — subprocess timeout**: Daily mode was using `MAX_PAGES=10` per query across 19 query templates. With the 30 req/min search API throttle, that's ~190 potential API calls at 2s each = 6+ minutes, exceeding the 300s subprocess timeout in the cron wrapper (`gitradar_daily.py`). The run gets killed before scoring even starts. Fix has three layers:
   - **Reduce daily pages**: `DAILY_PAGES = 2` (daily only needs new finds, not exhaustive scan). Weekly keeps `WEEKLY_PAGES = 5`.
   - **Time budget**: `DAILY_TIME_BUDGET = 180` (3 min soft limit inside `collect_daily()`). If elapsed time exceeds budget, bail out of the API loop gracefully and proceed to scoring with whatever was collected. Don't hard-abort — partial results are still useful.
   - **Outer timeout**: Bump `gitradar_daily.py` subprocess `timeout=600` as a safety net (was 300).
   Result: runtime dropped from 5m9s to ~2m10s, same top repos discovered.

## Architecture Patterns

### Dual-Mode Pipeline

**Daily mode**: Lightweight new-find scan
- Dedupe against 14-day cache
- Only report repos not seen before

**Weekly mode**: Full re-evaluation
- Re-score all cached repos
- Compare `pushed_at` timestamps to detect new activity
- Refresh metadata

### Output Structure

```json
{
  "collected_at": "2026-06-23T01:30:00Z",
  "mode": "daily",
  "stats": {
    "total_collected": 31,
    "after_filter": 30,
    "noise": 1
  },
  "repos": [
    {
      "full_name": "owner/repo",
      "description": "...",
      "stars": 73281,
      "score": 95.0,
      "label": "ADOPT",
      "llm_summary": "Provides..."
    }
  ]
}
```

## Integration Examples

### Hermes Cron Job

```bash
# Daily scan at 8am, post to Discord
0 8 * * * cd ~/workspace/gitradar-hermes && ./run.sh daily
```

### Feedback CLI

```bash
python3 scripts/gitradar-feedback.py rate owner/repo useful
python3 scripts/gitradar-feedback.py list
python3 scripts/gitradar-feedback.py stats
```

### LLM Enrichment

```bash
export NANOGPT_API_KEY="your...en"
python3 scripts/gitradar-enrich.py --top 20
```

## Reference Files

- `references/enrichment-code.md` — Full enrichment pattern with error handling
- `references/gitradar-fork-structure.md` — Hermes-specific GitRadar fork details
