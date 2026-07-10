# Working GitRadar Fork

**Location**: `~/workspace/gitradar-hermes`

A fully functional Hermes-specific fork of [Sahil-SS9/gitradar](https://github.com/Sahil-SS9/gitradar) with all features implemented and tested.

## Improvements Over Original

1. **Trending metadata enrichment** — Fetches full GitHub API metadata for scraped trending repos (original only gets names, causing all repos to fail "dead_repo" filter with 0 stars)

2. **User feedback loop** — Rate repos as useful/noise/duplicate, bonuses are applied to scores:
   - `useful`: +15 points
   - `noise`: -20 points  
   - `duplicate`: -10 points

3. **LLM-powered enrichment** — Top 20 repos get README-based one-line summaries via NanoGPT gpt-4o-mini

4. **Hermes-specific scoring** — Configured for Jason's interests:
   - AI/ML frameworks (PyTorch, HuggingFace, LangChain)
   - Agent tooling (MCP, agent-framework, autonomous-agents)
   - MLOps (vLLM, Ollama, fine-tuning, vector databases)
   - Hermes ecosystem (hermes-plugin, hermes-skill, hermes-theme)

5. **CLI wrapper** — `cli.py` provides unified interface:
   ```bash
   python3 cli.py scan daily
   python3 cli.py rate owner/repo useful
   python3 cli.py show top 20
   ```

## File Structure

```
gitradar-hermes/
├── scripts/
│   ├── gitradar-discover.py    # Main discovery pipeline (1122 lines)
│   ├── gitradar-score.py       # Scoring with feedback integration (341 lines)
│   ├── gitradar-enrich.py      # LLM README summarization (195 lines)
│   └── gitradar-feedback.py    # User feedback system (106 lines)
├── config/
│   ├── stack.json              # Hermes-specific interest weights
│   ├── thresholds-schema.json  # Threshold configuration schema
│   └── crontab.example         # Cron integration example
├── data/
│   ├── cache.json              # 14-day rolling cache
│   ├── thresholds.json         # Self-tuning thresholds
│   ├── metrics.json            # Historical metrics
│   ├── feedback.json           # User ratings
│   ├── discoveries.json        # Raw discoveries
│   └── enriched.json           # Enriched with LLM summaries
├── tests/
│   └── test_gitradar.py        # 148 lines of tests
├── run.sh                      # Bash orchestrator for full pipeline
└── cli.py                      # Unified CLI wrapper
```

## Usage

```bash
# Set up authentication
export GITHUB_TOKEN=*** auth token)

# Run full pipeline
./run.sh daily

# Or use CLI
python3 cli.py scan daily
python3 cli.py enrich 20
python3 cli.py list
python3 cli.py stats feedback
```

## Key Implementation Details

- **Dual-mode pipeline**: Daily (lightweight cache diff) vs Weekly (full re-scan with activity detection)
- **Self-tuning thresholds**: Star threshold adjusts based on signal/noise ratios (range 25-500)
- **Rate limiting**: Respects GitHub API limits (60/hr unauthenticated, 5000/hr authenticated, 30/min search)
- **19 query templates**: Covers AI/agents/MCP/MLOps/Hermes ecosystem
- **Pagination**: `DAILY_PAGES=2` (new finds only), `WEEKLY_PAGES=5` (broader scan), `MAX_PAGES=10` (cap)
- **Time budget**: `DAILY_TIME_BUDGET=180s` soft limit inside `collect_daily()` — bails API loop early and proceeds to scoring with partial results
- **Cache TTL**: 14-day rolling window to avoid stale data
- **Classification labels**: ADOPT (80+), EXTRACT (60-79), FORK/PRODUCT (50-59), PLUGIN/SKILL (40-49), INSPIRATION (20-39), NOISE (<20)

## Cron Wrapper

`~/.hermes/scripts/gitradar_daily.py` wraps the discover + score pipeline for the
cron job. Key config:
- Subprocess `timeout=600` (was 300, caused kill before scoring)
- Runs `gitradar-discover.py --mode daily` then `gitradar-score.py`
- Reads `data/recommendations.json` and outputs top 10 as JSON for the cron agent

## Performance History

| Date | Mode | Repos found | Runtime | Notes |
|------|------|-------------|---------|-------|
| 2026-06-23 | daily | 2633 | ~5min | Original MAX_PAGES=10, near timeout limit |
| 2026-07-08 | daily | 1287 | 5m9s | Timed out (300s subprocess limit) |
| 2026-07-08 | daily | 528 | 2m10s | After DAILY_PAGES=2 + time budget fix |