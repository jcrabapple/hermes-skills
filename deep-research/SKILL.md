---
name: deep-research
description: >-
  Systematic multi-source methodology for comprehensive reports and complex,
  multi-faceted investigations. Use when the user asks for a deep dive,
  comprehensive analysis, literature-style synthesis, or formal research
  report. Not for quick factual answers (use answer-engine), recent social
  sentiment (use last30days), proprietary academic/financial datasets (use
  valyu), or explicit multi-model deliberation (use openrouter-fusion-research).
origin: bytedance/deer-flow
---

# Deep Research Skill

For routing among the research ecosystem, load `references/research-skill-routing.md`.

## Core Principle

**Never generate content based solely on general knowledge.** A single search query is NEVER enough — conduct multi-angle research before producing output.

## Building the Research Prompt

Before starting Phase 1, craft a structured research prompt. This is critical when delegating to a subagent or using an external research tool — the prompt IS the only context the researcher gets.

### Rules for a Good Research Prompt

- **One paragraph.** No headers, no bullet list in the deliverable. Compress to one tight paragraph.
- **Prompt the job, not the topic.** Give search handles (timeframe, ranking, source type, decision logic) — not just a subject.
- **Assume zero prior knowledge.** Write for a researcher who has never heard of the project. Open by explaining what the project/product is, why it exists, and the current situation.
- **Lead with the goal + decision.** Right after the explainer, state the single question the research must answer and the decision/use it informs.
- **Embed all context.** Names, dates, product, prior known facts, constraints. The researcher must not need to ask anything or guess.
- **Number sub-questions inline** (1, 2, 3...) so coverage is explicit. Keep to 3-6. One mission per prompt — don't cram unrelated questions.
- **State constraints.** What to include, what to avoid (e.g. "only non-Chinese competitors", "no marketing fluff").
- **Source hierarchy.** Prefer primary sources (official docs, GitHub, papers, filings, changelogs); forums/X/Reddit are weak signal only, never factual proof.
- **Contradiction handling.** If sources conflict, separate confirmed facts / inference / unresolved uncertainty — don't force fake consensus. Flag low-confidence claims for verification.
- **Completion bar.** Don't stop at the first plausible answer. Corroborate each key claim with multiple independent primary sources where they exist; where sources are scarce, say so explicitly instead of padding.
- **Gap round.** Require a final self-critique pass: list gaps, contradictions, and single-source claims, then run another round of searches to close them — repeat until clean.
- **Demand a fixed output per finding:** source link + specific claim + one-line "why it matters".
- Verifiable, citable facts only. No opinions.
- **Last sentence:** instruct the researcher to output everything into a single detailed markdown file.

### Template

> [For a reader with zero prior knowledge: in 1-2 plain-English sentences, what the project/product is, why it exists, and the current situation.] Research [TOPIC + key identifying facts] to answer one question: [THE QUESTION] — for [DECISION / END USE]. Find: (1) ...; (2) ...; (3) ...; (4) .... [Constraints: include X, avoid Y.] Prefer primary sources; treat forums/social as weak signal only; if sources conflict, separate fact from inference and flag what needs verification. Don't stop at the first plausible answer: corroborate each key claim with multiple independent primary sources where they exist (and say so explicitly where they don't), continuing until every numbered question is covered to that bar. Before finishing, do a self-critique pass — list gaps, contradictions, and any single-source claims, then run another round of searches to close them, repeating until clean. For each point, give the source link, the specific claim, and a one-line "why it matters". No marketing fluff — verifiable, citable facts only. Output everything into a single detailed markdown file.

### When to Use This Prompt

- **Delegating research via `delegate_task`:** The prompt goes in the `goal` field
- **Using an external research tool (DeepAPI, Kagi Assistant, etc.):** The prompt is the query
- **Handing off to a human researcher:** The prompt is the brief
- **Structuring your own Phase 1:** Write the prompt first to clarify scope and dimensions, then execute the searches yourself

### Pre-Flight Check

Before starting research, verify web tools are available. Silent tool registration failures are common — the `web` toolset can show "enabled" while `nanogpt_web_search` and `nanogpt_web_extract` are actually missing from the session.

```
# Quick check: if you have nanogpt_web_search in your tool list, you're fine.
# If not, don't waste time curling search engines — fix the root cause.
```

**If delegation fails (model_not_supported, rate limits, crashes):** Fall back to inline execution using the 4-phase methodology with `nanogpt_web_search` + `nanogpt_web_extract` tools directly. This is often faster and more reliable than delegation for 5–10 search tasks. If `nanogpt_web_search` is also missing, use terminal-based Kagi CLI as last resort.

**If `nanogpt_web_search` is missing:**
1. Tell the user: "Web search tools aren't loaded — likely an auth or API key issue."
2. Diagnose: `hermes doctor 2>&1 | grep -i "web\\|nous\\|tool"` (see hermes-agent skill for full diagnosis)
3. If you can't fix it inline, fall back to `delegate_task` with `toolsets=["terminal", "file", "browser"]` — the subagent gets its own tool discovery and may have working browser tools even if the parent session doesn't.
4. Last resort: use browser tools directly (`browser_navigate` → Google/Bing → `browser_console` to extract text). This is ugly but works.

**Never silently fall back to `curl` scraping search engines.** Google/DuckDuckGo/Bing return garbage HTML that's hard to parse. If you're reduced to terminal-only, at least use `~/.local/bin/kagi search` if available.

## Research Methodology

### Phase 1: Broad Exploration

Start with broad searches to understand the landscape:

1. **Initial Survey**: Search for the main topic to understand the overall context
2. **Identify Dimensions**: From initial results, identify key subtopics, themes, angles, or aspects that need deeper exploration
3. **Map the Territory**: Note different perspectives, stakeholders, or viewpoints that exist

Example:
```
Topic: "AI in healthcare"
Initial searches:
  - "AI healthcare applications 2026"
  - "artificial intelligence medical diagnosis"
  - "healthcare AI market trends"
Identified dimensions:
  - Diagnostic AI (radiology, pathology)
  - Treatment recommendation systems
  - Administrative automation
  - Patient monitoring
  - Regulatory landscape
  - Ethical considerations
```

### Phase 2: Deep Dive

For each important dimension identified, conduct targeted research:

1. **Specific Queries**: Search with precise keywords for each subtopic
2. **Multiple Phrasings**: Try different keyword combinations and phrasings
3. **Fetch Full Content**: Use nanogpt_web_extract to read important sources in full, not just snippets
4. **Follow References**: When sources mention other important resources, search for those too

Example:
```
Dimension: "Diagnostic AI in radiology"
Targeted searches:
  - "AI radiology FDA approved systems"
  - "chest X-ray AI detection accuracy"
  - "radiology AI clinical trials results"
Then fetch and read:
  - Key research papers or summaries
  - Industry reports
  - Real-world case studies
```

### Phase 3: Diversity & Validation

Ensure comprehensive coverage by seeking diverse information types:

| Information Type | Purpose | Example Searches |
|-----------------|---------|------------------|
| **Facts & Data** | Concrete evidence | "statistics", "data", "numbers", "market size" |
| **Examples & Cases** | Real-world applications | "case study", "example", "implementation" |
| **Expert Opinions** | Authority perspectives | "expert analysis", "interview", "commentary" |
| **Trends & Predictions** | Future direction | "trends 2026", "forecast", "future of" |
| **Comparisons** | Context and alternatives | "vs", "comparison", "alternatives" |
| **Challenges & Criticisms** | Balanced view | "challenges", "limitations", "criticism" |

### Phase 4: Synthesis Check

Before proceeding to content generation, verify:

- [ ] Have I searched from at least 3-5 different angles?
- [ ] Have I fetched and read the most important sources in full?
- [ ] Do I have concrete data, examples, and expert perspectives?
- [ ] Have I explored both positive aspects and challenges/limitations?
- [ ] Is my information current and from authoritative sources?

**If any answer is NO, continue researching before generating content.**

## Search Strategy

See [references/search-guide.md](references/search-guide.md) for query patterns, temporal precision rules, and diversity checklist.

### When to Use nanogpt_web_extract vs web_extract

**`web_extract`** (preferred for Wikipedia and large pages): Returns clean markdown summaries capped at ~5000 chars/page. Handles 5 URLs per call. Best for Wikipedia articles, news articles, and any source where a structured summary is sufficient. Does NOT return raw full content.

**`nanogpt_web_extract`** (for raw full content): Returns raw page content in markdown. When extracting 3+ URLs, output can exceed 100KB and gets persisted to `/tmp/hermes-results/` — use `read_file` with offset/limit to access. Best for non-Wikipedia sources needing complete text (opinion pieces, niche sites, data tables). Use sparingly to avoid context overflow.

### Iterative Refinement

Research is iterative. After initial searches:
1. Review what you've learned
2. Identify gaps in your understanding
3. Formulate new, more targeted queries
4. Repeat until you have comprehensive coverage

## Quality Bar

Your research is sufficient when you can confidently answer:

- What are the key facts and data points?
- What are 2-3 concrete real-world examples?
- What do experts say about this topic?
- What are the current trends and future directions?
- What are the challenges or limitations?
- What makes this topic relevant or important now?

## Failure Modes

| Situation | Action |
|-----------|--------|
| Search rate-limited | Wait 2s, retry with different query phrasing |
| nanogpt_web_search times out (read timeout=30) | Retry with `depth='standard'` instead of `depth='deep'`. Deep searches hit the 30s backend timeout frequently; standard depth returns results in 3-5s. Deep depth is rarely worth the timeout risk — prefer 2 standard searches with different phrasings over 1 deep search. |
| All top results paywalled | Search for summaries, preprints, or news coverage of the same findings |
| Sources conflict | Note disagreement explicitly, cite both sides, flag which has stronger evidence |
| Low-quality sources (forums, AI-generated) | Deprioritize, seek primary/authoritative sources, note quality in methodology |
| Search returns nothing relevant | Broaden query, try adjacent terms, check spelling, use different search backend |
| nanogpt_web_search tool missing from session | Don't curl search engines. Run `hermes doctor` to diagnose. Fall back to `delegate_task` with `toolsets=["terminal","file","browser"]`. See Pre-Flight Check above. |
| delegate_task fails (model_not_supported, rate limits, subagent crash) | Fall back to inline execution immediately. Use `~/.local/bin/kagi search` directly. See [references/delegation-failures.md](references/delegation-failures.md). |

## Output

After completing research, you should have:

1. A comprehensive understanding of the topic from multiple angles
2. Specific facts, data points, and statistics
3. Real-world examples and case studies
4. Expert perspectives and authoritative sources
5. Current trends and relevant context

## Delegation

For substantial research tasks, use `delegate_task` to run the full 4-phase loop in a subagent. This gives the subagent minimax-m2.7's 1M token context window, preventing compression from cutting accumulated search results.

**When to delegate:**
- The topic has 3+ dimensions requiring independent deep dives
- You expect 10+ nanogpt_web_search + nanogpt_web_extract calls across phases
- The research is part of an automated pipeline (weekly-blog, etc.)
- **AND** the user is NOT in an active conversation waiting for results

**When NOT to delegate:**
- Quick lookups (2-3 searches) — do it inline
- The user is in an active conversation and wants real-time progress updates
- You need to interactively adjust the research direction based on early findings
- Task is time-critical and delegation adds latency risk

**Exception — Parallel decomposition (Mixture of Agents):** When a task has 3+ independent dimensions and the user is actively waiting, dispatching multiple parallel `delegate_task` subagents IS suitable. Each agent works a different dimension independently, results stream back as async batches, and you synthesize them into one deliverable. The user sees visible progress (todo updates, per-agent status) and gets a richer result than sequential single-agent research. See [references/moa-parallel-decomposition.md](references/moa-parallel-decomposition.md) for the pattern and template prompts.

**How to delegate:**
```
delegate_task(
  goal="Deep research on: [topic]. Complete all 4 phases (broad exploration, deep dive, diversity validation, synthesis). Return a comprehensive research report with key facts, data points, real-world examples, expert perspectives, current trends, and challenges.",
  skills=["deep-research"],
  toolsets=["web", "terminal"]
)
```

**Handling delegation failures:**
Delegation can fail due to upstream API issues, rate limits, or subagent crashes. Always have a fallback:

1. Check if `delegate_task` returned an error or incomplete status
2. If failed, immediately switch to inline execution using the same 4-phase methodology
3. Inform the user: "Delegation failed, handling directly"
4. Replicate the research process with direct tool calls (nanogpt_web_search, nanogpt_web_extract)
5. Maintain output quality — don't cut corners in the fallback

**Example fallback pattern:**
```python
# Attempt delegation
result = delegate_task(goal=..., skills=["deep-research"], toolsets=["web"])

# Check for failure
if result.get('error') or result.get('status') != 'completed':
    # Fallback: conduct research inline
    # Phase 1: Broad exploration (3-5 searches)
    # Phase 2: Deep dive (targeted searches per dimension)
    # Phase 3: Diversity validation (facts, examples, expert views, trends, challenges)
    # Phase 4: Synthesis into comprehensive report
    pass
```

**Note:** The subagent runs the entire research loop independently. It cannot ask clarifying questions, so make the goal prompt specific about dimensions to explore and output format. **Always specify "Print all findings to stdout as your final response. Do not save to files"** in the goal — subagents that claim to save files may fail silently (see `references/delegation-failures.md`).

### Delegation Fallback: Inline Execution

Delegation can fail for ANY topic, not just complex historical ones. The subagent runs on `gemini-flash-lite-latest` which may be unsupported on the completions endpoint (`model_not_supported`), or may hit rate limits, timeouts, or crashes. When delegation fails:

1. **Immediate Fallback**: Switch to inline execution using the 4-phase methodology. Say "Delegation failed, handling directly."
2. **Search tool**: Use `~/.local/bin/kagi search "<query>" --format json` directly from terminal. Do NOT try `web_search` from execute_code — it's not available there.
3. **Extract tool**: Use `~/.local/bin/kagi summarize --url "<url>" --subscriber` for full content extraction. Always use `--subscriber` flag to avoid burning paid API credits.
4. **Query Strategy**: Use 5-6 broad initial searches, then 2-3 targeted deep dives per dimension. Space searches ~2s apart.
5. **Source Prioritization**: Wikipedia for overviews, academic journals for depth, news outlets for recent context. Extract 3-5 authoritative sources per dimension.
6. **Output Quality**: Maintain full report quality — don't cut corners in fallback mode.

See [references/delegation-failures.md](references/delegation-failures.md) for specific error patterns and resolutions.

### Mixture of Agents (MoA) Parallel Decomposition

For tasks with 3+ independent research dimensions (e.g. "analyze this project's codebase + bugs + upstream compatibility"), dispatch multiple `delegate_task` subagents in parallel — one per dimension — and synthesize their results. This is faster than sequential single-agent research and produces deeper coverage. Results stream back as async batches. See [references/moa-parallel-decomposition.md](references/moa-parallel-decomposition.md) for the full pattern, template prompts, and synthesis document structure.

## Routing Guide

When multiple research skills could match a user's request, see [references/research-skill-routing.md](references/research-skill-routing.md) for the disambiguation framework covering all 5 research modes (quick lookup, deep research, social-last-30-days, paper research, multi-model deliberation).

## Wiki Ingestion Step

If a Karpathy-style LLM wiki exists (at `~/wiki/` or `$WIKI_PATH`), ingest key findings after synthesis:

**Wiki path:** `~/wiki/` (always verify with `ls ~/wiki/SCHEMA.md` — don't assume). If missing, check `$WIKI_PATH` env var.

1. **Read SCHEMA.md** — understand domain, conventions, tag taxonomy. Add new tags to the taxonomy if needed (e.g., a research topic in a new domain requires new category tags).
2. **Read index.md** — check what already exists to avoid duplicates.
3. **Scan log.md** (last 20–30 entries) — understand recent activity.
4. **Create/update concept or entity pages** in the appropriate subdirectory (`concepts/`, `entities/`):
   - Follow schema conventions (YAML frontmatter, tags from taxonomy, `[[wikilinks]]`)
   - Minimum 2 outbound `[[wikilinks]]` per new page
   - Set appropriate `confidence:` level
5. **Save raw source material** to `raw/articles/<topic-date>.md` with frontmatter (source_url, ingested date, sha256)
6. **Update index.md** — add new pages to the correct section, bump revision count
7. **Update log.md** — append a log entry listing every file created or updated
8. **Report what was created/updated** to the user

If the wiki doesn't have a suitable tag category for the research domain, add it to SCHEMA.md first (as was done to add `health`, `medical`, `autoimmune` tags in this session's RAS research).

The `scripts/with_wiki_ingestion.py` script provides automated wrappers for this pipeline, but manual ingestion (as documented above) gives better control over cross-referencing and schema consistency.

## Pitfalls

- **web_extract may be blocked in cron sessions.** Cloudflare WAF, rate limits, or billing errors can block web extraction when running from cron. When this happens, proceed with the model's existing knowledge rather than aborting. A degraded research report is better than no output. The weekly-blog skill documents this pattern ("proceed with model knowledge") but any skill loading deep-research in cron should be aware.
- **Banking/financial API research**: When researching US banking APIs, always separate read access (transactions/balances via Plaid — widely available) from write access (money movement — almost never available for personal accounts). The US has no PSD2 equivalent. Plaid Transfer explicitly prohibits same-person transfers. Mercury Personal is the only US personal account with a full API including internal transfers. See [references/us-banking-apis.md](references/us-banking-apis.md).
- **hermes_tools is not available in cron Python sandbox.** `from hermes_tools import web_search` (or any hermes_tools import) will fail with `ModuleNotFoundError` in cron sessions. Use terminal `curl` commands or agent-level `web_search`/`nanogpt_web_search` tool calls instead of trying to import them in `execute_code`.
- **Wiki path:** The wiki lives at `~/wiki/` (not `/home/wiki/` or `$HOME/wiki/` without expanding). Always use the full absolute path with `~` or `$HOME` expanded. Write operations that use bare `/home/wiki/` will fail silently.
- **Entity + Concept pair:** When research covers both a specific organism/entity AND a broader technique or concept (e.g., colossal squid + eDNA), create BOTH an entity page and a concept page. Don't force everything into one page type.
- **TikTok → Research → Blog pipeline:** When fact-checking a TikTok video, structure the research around the specific claims made in the video. Each claim gets a verdict (true/mostly true/false/nuanced) with evidence. This makes the blog post and Obsidian note much more useful than a generic topic overview. See [references/tiktok-blog-pipeline.md](references/tiktok-blog-pipeline.md) for the full end-to-end workflow (scrape → research → Obsidian → blog → Mastodon).
- **TikTok/social media extraction via browser:** When `nanogpt_tiktok_scraper` or `video_analyze` fails on TikTok URLs (common — TikTok blocks direct video extraction), use `browser_navigate` to load the page, then `browser_snapshot` to extract the key metadata: creator handle, caption text, hashtags, engagement metrics (likes/comments/favorites/shares), and the music/sound name. This gives enough context to research the topic even when the video itself can't be downloaded. The alt text on the video thumbnail often contains the full caption — look for `img "..."` elements with descriptive text.

## Next Step: Content Generation

After research is complete, the output depends on what the user asked for:

- **Research report only** — load the **article-writing** skill for structured report/article output
- **Save to Obsidian** — save full research findings (with sources, data tables, timelines) to `$VAULT/Research/YYYY-MM-DD-slug.md` using the Obsidian skill conventions
- **Blog post** — write to `~/blog/slug.md` using the pico-sh blog post template (H1 title, italic date/tag line, conversational-but-substantive voice, Sources block at end), then rsync to prose.sh
- **Mastodon** — compose a short punchy post (no emdashes, no markdown, ≤1989 chars, relevant hashtags + blog link), use `mastodon_post.py` helper script

### Full Research → Obsidian → Blog → Mastodon Pipeline

When the user asks for the full pipeline ("research X, save to Obsidian, write a blog post, share to Mastodon"), follow the workflow documented in [references/research-blog-pipeline.md](references/research-blog-pipeline.md).

Key conventions:
- Save research to Obsidian **before** writing the blog (the research note is the detailed source; the blog is the readable distillation)
- Read 1-2 recent blog posts from `~/blog/` to match Jason's established voice before writing
- Batch independent searches in Phase 1 (3 queries in parallel) to speed up broad exploration
- Use `web_extract` for Wikipedia and large pages (returns ~5000-char structured summaries). Reserve `nanogpt_web_extract` for non-Wikipedia sources needing raw full content.
- Verify prose.sh publication with `curl -sf https://hermez.prose.sh/slug`, not `ssh prose.sh stat` (the latter fails on valid files)
- Always `--dry-run` Mastodon posts before publishing for real
