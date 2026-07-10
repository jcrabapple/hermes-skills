---
name: answer-engine
description: >
  Research-focused query handling with multi-source synthesis, citations,
  and Obsidian persistence. Like a self-hosted Perplexity/Vane but CLI-native.
  Best for quick-to-medium lookups using Kagi. Use when the user asks factual
  questions, needs citations, or wants a direct answer — not a full research
  report (use deep-research) or social sentiment (use last30days). Triggers on:
  research, look into, what's the latest on, compare, explain, investigate.
---

# Answer Engine Skill

## Purpose
Research-focused query handling with multi-source synthesis, citations, and Obsidian persistence. Like a self-hosted Perplexity/Vane, but CLI-native.

## Trigger

User asks questions requiring research, verification, or multi-source synthesis. Best for quick-to-medium lookups using Kagi as the search backend. For systematic 4-phase deep research reports, use `research/deep-research` instead. For social-signal / "what people are saying" research, use `last30days` instead.
See `research/deep-research/references/research-skill-routing.md` for the full routing table.

## Search Backend Stack
1. **Kagi tools plugin** — Use `kagi_search` (structured results), `kagi_quick` (factual answers with references), or `kagi_assistant` (open-ended research conversations). These are Hermes-native tools, no terminal required.
   - `kagi_search` — Best for finding sources with filters (region, time, lens)
   - `kagi_quick` — Best for single-answer factual queries with citations
   - `kagi_assistant` — Best for deep research with thread continuation
   - `kagi_ask_page` — Best for understanding a specific URL's content
   - Note: `kagi_fastgpt` is deprecated — use `kagi_quick` instead
2. **SearXNG** - Secondary, privacy-focused diversity (currently degraded — returns 0 results as of 2026-05; keep trying but don't rely on it)
   - Instance: https://searxng.snakepit.us
   - Query format: `https://searxng.snakepit.us/search?q={query}&format=json`
3. **web_search** - Not available in current toolset (stale reference, do not use)

## Workflow

### 1. Classify Query
Determine intent:
- **Factual**: Direct answer exists (e.g., "what is X")
- **Research**: Requires synthesis (e.g., "compare X vs Y", "best X for Y")
- **Technical**: Code, APIs, debugging
- **File-based**: References uploaded documents
- **Exploratory**: Open-ended, emerging topics (requires broader net)

### 2. Execute Searches (Parallel when possible)
**Minimum source targets:**
- Factual: 3-5 sources
- Research: 5-10 sources
- Exploratory: 8-15 sources

**Search stack (as of 2026-05):**
- Call `kagi_quick <query>` for quick factual answers with citations (replaces deprecated `kagi fastgpt`)
- Call `kagi_search <query>` for detailed search results with region/time/lens filters
- Query SearXNG JSON API for diverse/independent sources (currently degraded, 0 results as of 2026-05)
- For complex topics: `delegate_task` with batch mode (split into sub-questions)
- Note: `web_search` tool does NOT exist in current toolset — do not reference it

**Query expansion:** Generate 2-3 related search queries to capture adjacent angles:
- Example: "solid-state battery breakthroughs" → also search "quantum scape 2026", "toyota solid state battery timeline", "lithium metal anode challenges"

### 3. Track Sources with Quality Signals
For each source, record:
- Source URL
- Source title
- Publication type (academic, news, blog, forum, official docs)
- Date/timeliness
- Credibility indicators (peer-reviewed, primary source, expert author, etc.)
- Citation number [1], [2], etc.

### 4. Semantic File Search (if applicable)
If user references files or asks about prior research:
- Use NanoGPT API with `gemini-embedding-2-preview`
- Embed query, search Obsidian Research folder
- Include relevant excerpts as sources
- Note connections to prior research explicitly

### 5. Deep Synthesis (Multi-Pass)
**Pass 1 - Extraction:** Pull key facts, claims, data points from each source
**Pass 2 - Clustering:** Group related findings into thematic buckets
**Pass 3 - Tension Mapping:** Identify where sources agree, disagree, or fill gaps
**Pass 4 - Narrative:** Build coherent answer with logical flow

**Output structure for research-grade answers:**
- Executive Summary (2-4 sentences, high-level answer)
- Key Findings (bulleted, with citations)
- Detailed Analysis (paragraphs with synthesis, not just source regurgitation)
- Contradictions/Uncertainties (explicitly note disagreements or gaps)
- Methodology Notes (what was searched, limitations)

### 6. Format Output
```markdown
# {Query as Title}

## Executive Summary

{2-4 sentence high-level answer}

## Key Findings

- {Finding 1} [1][2]
- {Finding 2} [3]
- {Finding 3} [4][5]

## Detailed Analysis

{Multi-paragraph synthesis with inline citations}

## Contradictions & Uncertainties

{Note where sources disagree or information is incomplete}

## References

[1] Source Title - URL (publication type, date)
[2] Source Title - URL (publication type, date)

---
*Research saved to Obsidian: {filename}*
```

### 7. Save to Obsidian
- Path: `~/Documents/Obsidian Vault/Research/`
- Filename: `{YYYY-MM-DD}-{slugified-query}.md`
- Include full research + metadata (timestamp, sources, search terms, query expansions)
- Tag with relevant topics for future retrieval

**Note:** After saving, the research file is automatically ingested into the `llm-wiki`
knowledge base via the `wiki-ingestion` skill. This creates a `query/` page in the wiki,
auto-detects and creates entity pages for notable mentions, and updates the index.
See `research/wiki-ingestion/INTEGRATIONS.md` for details.

## Contact & Person Lookup

When the user needs to find someone's email, phone, or contact info at an organization (university, company, etc.), see [references/contact-lookup.md](references/contact-lookup.md) for the directory scraping technique, email naming convention inference, and fallback strategies.

## Search Mode
**Deep Research** (default):
- Factual queries: 5-8 sources minimum
- Research/synthesis queries: 8-15 sources minimum
- Exploratory queries: 10-20 sources minimum
- Kagi primary, SearXNG secondary when available (currently degraded)
- Deep synthesis with multi-pass analysis
- Target: 3-5 minutes for thorough coverage (quality over speed)
- Always include: executive summary, key findings, detailed analysis, uncertainties

**Quick Mode** (only when user explicitly asks for "quick" or "brief"):
- 3-5 sources
- Single-pass synthesis
- Target: <90 seconds

## Citation Rules
- Number sequentially [1], [2], [3]
- Each number = one URL
- Order by relevance, not discovery order
- Include in References section at end
- **Reference format**: `[N] Title - URL (publication type, date if available)`
- **Source type tags**: Use parentheticals like (academic), (news), (official docs), (blog), (forum), (primary source)
- **Multiple citations per claim**: When a claim is supported by multiple sources, cite all: "Solid-state batteries promise 2-3x energy density [1][3][7]"
- **Contradiction citations**: When sources disagree, cite each side: "Toyota targets 2027 launch [2], while QuantumScape claims 2025 [5]"

## File Embeddings
NanoGPT API config:
- Model: `gemini-embedding-2-preview`
- Use for: Semantic search over Research folder
- Embed new research files after saving
- **Fallback:** If API is unreachable, skill uses keyword-based `search_files` instead

## Tools Used
- `kagi_search` — Primary search (structured JSON results), available as a Hermes tool
- `kagi_quick` — Factual answers with references (replaces deprecated `kagi fastgpt`)
- `kagi_assistant` — Deep research conversations with thread continuation
- `kagi_ask_page` — Page-specific questions with citations
- `terminal` — SearXNG JSON queries (degraded), Obsidian operations
- `delegate_task` — Parallel research (complex queries) — also useful for browser-based search when JS rendering needed
- `execute_code` — Embedding API calls, text processing, citation tracking
- `write_file` — Obsidian output
- `search_files` — Keyword-based file search (fallback if embeddings unavailable)
- Note: `web_search` is NOT available — use `kagi_search` instead

## Wiki Integration

After research is saved to Obsidian, it is **automatically ingested** into the
`llm-wiki` knowledge base (see `research/wiki-ingestion` skill). This means:

- The research becomes a **permanent, cross-referenced wiki page** (not a disposable file)
- Entities (tools, people, companies, models) mentioned are auto-detected
- New entity pages are created for previously unknown entities
- Existing entity pages are updated with references to this research
- The wiki index and log are updated automatically

This creates a **compounding knowledge base** where each research session builds
on previous ones through cross-links, rather than accumulating isolated files.

## Pitfalls
- SearXNG may rate-limit — add 2s delay between queries
- NanoGPT API key in `~/.config/nanogpt/.env`
- Obsidian path has space — quote paths in shell commands
- Don't over-cite: 1 citation per distinct claim, not every sentence
- **Country/comparison statistics:** Comparison aggregator sites (versus.com, mylifeelsewhere.com, georank.org, countryeconomy.com) frequently have outdated, misread, or just wrong data. Examples: one claimed Cuba's obesity rate was 2.6% (actually 24.6% per CIA Factbook), another claimed US literacy was 86% (UNESCO has no recent US data; CIA Factbook says ~99%). Always verify against primary sources: CIA World Factbook, World Bank Open Data, WHO, UNESCO Institute for Statistics, NCES (for US education stats). If a comparison site's number seems surprising or dramatic, it's probably wrong — verify before including it.

## Usage Examples

See [references/examples.md](references/examples.md) for detailed walkthroughs of:
- Simple Factual Query
- Comparative Research (Deep Dive)
- Exploratory Research (Emerging Topic)
- File-Referenced Query

## Script Reference

### searxng_search.py
```bash
python scripts/searxng_search.py "search query"
# Returns: JSON array of {title, url, content, engine, score}
```

### citation_tracker.py
```bash
python scripts/citation_tracker.py add "Source Title" "https://url.com" "publication_type" "date"
python scripts/citation_tracker.py generate
python scripts/citation_tracker.py clear
python scripts/citation_tracker.py export  # Export as markdown references section
```

### save_to_obsidian.py
```bash
python scripts/save_to_obsidian.py "Query text" "Full markdown content" "tags"
# Returns: Full filepath where saved
```

### embedding_search.py
```bash
# Build index (run once, or when Research folder changes significantly)
python scripts/embedding_search.py rebuild

# Search for similar documents
python scripts/embedding_search.py search "your query"

# Embed a new file (auto-called after saving research)
python scripts/embedding_search.py embed "/path/to/file.md"
```

### query_expander.py
```bash
python scripts/query_expander.py "solid-state battery breakthroughs"
# Returns: JSON array of related queries:
# ["quantum scape 2026", "toyota solid state battery timeline", "lithium metal anode challenges"]
```

### source_evaluator.py
```bash
python scripts/source_evaluator.py "https://url.com"
# Returns: {publication_type, credibility_score, date, author_info, is_primary_source}
# Credibility signals: domain age, citation count, author credentials, peer-review status
```

## Credential Setup

```bash
# NanoGPT API key for embeddings (already configured)
# Located at: ~/.config/nanogpt/.env

# Kagi tools plugin is already installed and configured
# Available tools: kagi_search, kagi_quick, kagi_assistant, kagi_ask_page,
#                  kagi_translate, kagi_summarize, kagi_news, kagi_smallweb
# Session token is in env (KAGI_SESSION_TOKEN)
```

## Status

- ✅ Kagi tools plugin (`kagi_search`, `kagi_quick`, `kagi_assistant`, etc.): Working, primary search backend
- ⚠️ SearXNG: Connected but returning 0 results (snakepit.us, degraded since ~2026-05)
- ❌ `web_search`: Not available in current toolset
- ✅ Obsidian Research folder: Exists
- ✅ NanoGPT API key: Configured
- ✅ Embeddings: Working (text-embedding-3-small, 12 files indexed)
- ✅ Deep Research Mode: Active (default)
- ✅ Query Expansion: Available via query_expander.py
- ✅ Source Evaluation: Available via source_evaluator.py
