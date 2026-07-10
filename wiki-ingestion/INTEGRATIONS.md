# Wiki-Ingestion Integrations

## Overview

The `wiki-ingestion` skill connects research outputs to the llm-wiki knowledge base,
turning isolated research files into compounding knowledge.

## Active Integrations (Implemented)

### 1. answer-engine → wiki (✅ LIVE)

**Trigger:** Every time answer-engine saves research to `~/Documents/Obsidian Vault/Research/`

**What happens:**
- The research file is automatically ingested into the wiki
- A `query/` page is created with the full research content
- Up to 15 entities (people, tools, companies, models) are auto-detected
- New entity pages are created for previously unknown entities
- Existing entity pages are updated with a reference to the new query
- `index.md` is updated to list the new query page
- `log.md` is appended with the ingestion action

**Code path:**
`answer-engine/scripts/save_to_obsidian.py` → calls `wiki-ingestion/scripts/ingest.py`

**Example:**
```
Research file: Research/FTL Travel - Research Note.md
↓
Query page: query/faster-than-light-travel-theoretical-possibilities-and-modern-research.md
↓
Entity pages: alcubierre.md, alcubierre-warp-drive.md, applied-physics-lab.md, ... (15 created)
↓
Index: Queries section now lists "Faster-Than-Light Travel..."
```

### 2. weekly-blog → wiki (🟡 RUNNER CREATED, NOT YET AUTOMATED)

**Status:** Runner script exists at `automation/weekly-blog/run.py`

**What happens (when integrated):**
- Deep research is conducted on the weekly topic
- Full research is saved directly to wiki as a `concept/` page (bypassing Research/)
- Blog post is condensed from the concept page
- Blog post published to prose.sh
- The concept page remains as the permanent knowledge base entry

**To activate:** Update the weekly-blog cron job to call `run.py` instead of the old pipeline.

## Pending Integrations (Design Complete)

### 3. topic-monitor → wiki

**What:** Important findings from topic monitoring get logged in the wiki

**Design:**
- High-priority alerts create `query/` pages with timestamped titles
- Entity pages (companies, products) get timeline updates
- Creates historical record of developments

**Implementation:** Add post-processing to `topic-monitor/scripts/digest.py`

### 4. last30days → wiki

**What:** Notable social sentiment patterns become query pages

**Design:**
- When last30days research shows strong cross-platform signals, save as `query/`
- Include Reddit/X/YouTube/HN citations in the page content
- Link to relevant entities (tools, companies, people mentioned)

**Implementation:** Add `--save-to-wiki` flag to last30days script

### 5. deep-research → wiki

**What:** Comprehensive deep-dive reports become `comparison/` or `concept/` pages

**Design:**
- Comparison queries → `comparisons/` page
- Concept/exploration queries → `concepts/` page
- Auto-detection based on query type and output structure

**Implementation:** Wrap deep-research skill with wiki-ingestion

### 6. arxiv → wiki

**What:** Academic papers become entity pages with citation networks

**Design:**
- Paper metadata → `entities/` page (type: paper)
- Authors → `entities/` pages (type: person)
- Organizations (affiliations) → `entities/` pages (type: org)
- Techniques/models mentioned → `concepts/` pages
- Cross-link: paper page links to all author/org/concept pages

**Implementation:** Build arxiv-ingest wrapper around arxiv skill

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Research Skills                          │
│  (answer-engine, weekly-blog, topic-monitor, last30days)   │
└───────────────┬─────────────────────────────┬───────────────┘
                │ produce                    │ produce
                ▼                            ▼
    ┌────────────────────┐      ┌──────────────────────┐
    │  Markdown Output    │      │  Console/JSON Output │
    │  (Research/*.md)    │      │  (findings/, etc.)   │
    └──────────┬─────────┘      └──────────┬───────────┘
               │                            │
               │ call                        │ call
               ▼                            ▼
    ┌─────────────────────────────────────────────────────┐
    │         wiki-ingestion/scripts/ingest.py            │
    │  • Extracts entities & concepts                     │
    │  • Creates/updates wiki pages                       │
    │  • Updates index.md and log.md                      │
    └───────────────┬─────────────────────┬───────────────┘
                    │                     │
                    ▼                     ▼
         ┌─────────────────┐   ┌────────────────────┐
         │  query/ pages   │   │  entity/ pages     │
         │  concept/ pages │   │  concept/ pages    │
         │  comparison/    │   │  (auto-created)    │
         └─────────────────┘   └────────────────────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │  llm-wiki (compounding) │
                    └─────────────────────┘
```

## Configuration

The wiki path is read from `skills.config.wiki.path` in `~/.hermes/config.yaml`,
or defaults to `~/wiki`. All integrations respect this setting.

## Quality Controls

- **Threshold filtering:** Only entities mentioned in 2+ sources OR central to one source get pages
- **Tag taxonomy:** All tags must exist in `SCHEMA.md`; new tags added to taxonomy first
- **Cross-reference minimum:** Every new page links to at least 2 existing pages
- **Index completeness:** Every page added to `index.md`
- **Logging:** Every ingestion logged to `log.md` with details
- **Orphan detection:** Run `llm-wiki` lint to find isolated pages

## Monitoring

Check ingestion health:
```bash
# Recent activity
tail -20 ~/wiki/log.md

# Orphan pages (pages with no inbound links)
# Run the lint function from llm-wiki skill
```

## Future Enhancements

1. **Semantic deduplication:** Detect when a new finding is already covered
2. **Contradiction detection:** Flag conflicting claims across sources
3. **Auto-tag suggestion:** Recommend tags based on content similarity
4. **Batch ingestion mode:** Process multiple files efficiently
5. **Confidence scoring:** Rate auto-created entity pages by extraction confidence

## Related Skills

- `llm-wiki` — the destination knowledge base
- `answer-engine` — first integration (now live)
- `deep-research` — next integration candidate
- `weekly-blog` — runner created, needs cron update


## Active Integrations (Detailed)

### last30days → wiki

**Status:** ✅ LIVE — Wrapper script created

**Wrapper:** `~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py`

**How it works:**
1. User runs: `python3 with_wiki_ingestion.py "topic" --days 30`
2. Script executes `last30days.py` with the topic
3. Output saved to `~/Documents/Last30Days/{slug}.md`
4. Ingest script automatically called with `--source last30days --file {saved-file}`
5. Wiki creates `query/` page with full research + entity cross-links

**Usage:**
```bash
# Standard research (30 day lookback)
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "solid-state batteries"

# Custom date range
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "kdenlive tips" --days 7

# Skip wiki ingestion (just research)
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "topic" --no-wiki

# Specify output directory
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "topic" --save-dir ~/custom/path
```

**Output format:** last30days produces rich multi-source reports (Reddit, X, YouTube, HN, Polymarket, Web). The entire report is saved as a `query/` page. Entities (tools, companies, people, platforms) are auto-detected and cross-linked.

**Example:**
```
Input:  "kdenlive video editing tips"
↓
last30days runs (YouTube, Reddit, Web searches)
↓
Saved: ~/Documents/Last30Days/kdenlive-video-editing-tips.md (95KB)
↓
Wiki: query/kdenlive-video-editing-tips.md created
↓
Entities: 111 detected, 15 auto-created (Add, Animation, Bird, Breeze, ...)
↓
Index: Queries section updated
```

**Note:** last30days requires API keys for full data (X, Reddit, TikTok). Without keys it falls back to YouTube + Web, which still produces valuable research.

---

### deep-research → wiki

**Status:** ✅ LIVE — Wrapper script created

**Wrapper:** `~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py`

**How it works:**
1. User provides either a topic (for auto-research) or an existing research file
2. If topic provided, script delegates to deep-research skill (via `delegate_task`)
3. Research output captured and saved to temp file
4. Ingest script called with `--source deep-research --topic "X" --content {file}`
5. Wiki creates `concept/` or `comparison/` page based on query type

**Page type determination:**
- `--type comparison` or topic contains " vs " / " versus " → `comparison/` page
- `--type concept` or `--type general` → `concept/` page
- `--type news` → `query/` page

**Usage:**
```bash
# Ingest existing research file as concept
python3 ~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py \
  --input-file /path/to/research.md --type concept

# Ingest as comparison
python3 ~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py \
  --input-file /path/to/comparison.md --type comparison

# (Future) Auto-research + ingest — requires integration with delegate_task
# This would be the typical agent usage:
#   delegate_task(goal="Deep research on X", skills=["deep-research", "wiki-ingestion"])
```

**Output format:** deep-research produces comprehensive 4-phase reports with:
- Executive Summary
- Background & Current State
- Key Players / Technologies / Developments
- Challenges & Controversies
- Future Implications
- References

The full report becomes a permanent `concept/` or `comparison/` page in the wiki.

**Example:**
```
Input:  Solid-state batteries research (2000+ words, 10+ sources)
↓
Deep research methodology applied (broad → deep → diversity → synthesis)
↓
Wiki: concept/solid-state-batteries.md created
↓
Entities: QuantumScape, Toyota, Solid Power, Samsung SDI, Volkswagen, BMW, Ford
↓
Cross-links: Concept page links to all entity pages; entities link back
```

---

## Integration Pattern Reference

### For Skill Authors

To add wiki ingestion to any research skill:

```python
import subprocess
import os

def your_research_function(topic, ...):
    # 1. Conduct research (your existing logic)
    research_content = "..."
    research_file = "/tmp/research.md"
    
    with open(research_file, 'w') as f:
        f.write(research_content)
    
    # 2. Save to your skill's output location (if needed)
    # ... your existing save logic ...
    
    # 3. Ingest into wiki
    ingest_script = os.path.expanduser(
        "~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py"
    )
    subprocess.run([
        "python3", ingest_script,
        "--source", "your-skill-name",  # must match one of the choices
        "--file", research_file,
        "--wiki-path", os.path.expanduser("~/wiki")  # optional
    ], check=False, timeout=30)
    
    return research_content
```

**Supported `--source` values:**
- `answer-engine` — Research markdown files
- `weekly-blog` — Research drafts (topic + content)
- `last30days` — Last30Days saved reports
- `deep-research` — Deep research reports (topic + content)

**To add a new source:**
1. Add the source name to the `choices` list in `ingest.py` argparse
2. Add an `elif args.source == 'your-source':` branch in `main()`
3. Implement `ingest_your_source()` function following the existing pattern
4. Update this documentation

---

## Entity Extraction Strategy

The ingestion uses pattern-based extraction (no ML dependencies):

**Proper noun detection:**
- Regex: `[A-Z][a-z]+( [A-Z][a-z]+)*` — capitalized word sequences
- Filtered against 150+ stopwords (common words, verbs, section headers, units)
- Additional heuristics: rejects single-word common nouns, heading fragments

**Concept detection:**
- Extracted from H2/H3 headings (multi-word only)
- Filtered to exclude section header patterns ("Background & Current State" → rejected)
- Keeps substantive topic headings ("QuantumScape's Manufacturing Challenges" → kept)

**Wikilink harvesting:**
- Existing `[[wikilinks]]` in source content are added as entities
- This captures intentional entity mentions

**Thresholds:**
- Process top 15 entities per file (by order of appearance)
- Auto-create entity page if not found
- Update existing entity if found
- Minimum 2 outbound cross-links enforced on new pages

---

## Quality Verification

After running an integration, verify:

```bash
# 1. Check query/concept page created
ls ~/wiki/query/ | grep -i "topic-name"
ls ~/wiki/concept/ | grep -i "topic-name"

# 2. Check entity pages
ls ~/wiki/entities/ | grep -i "entity-name"

# 3. Verify index updated
grep -A2 "## Queries" ~/wiki/index.md
grep -A2 "## Concepts" ~/wiki/index.md

# 4. Check log entry
tail -5 ~/wiki/log.md

# 5. View cross-links (from entity page)
grep "\[\[" ~/wiki/entities/quantumscape.md
```

**Expected result:**
- Query/concept page exists with full content
- 10-15 entity pages created/updated
- Index lists the new page under appropriate section
- Log has entry with timestamp and details
- Entity pages contain `[[backlink]]` to the query/concept

---

## Troubleshooting

### "No such file or directory: ingest.py"

The wrapper script can't find the ingestion script. Ensure the path is correct:
```bash
ls ~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py
```

If missing, the wiki-ingestion skill wasn't installed correctly.

### "Wiki not found at ~/wiki"

The wiki hasn't been initialized. Create it:
```bash
hermes wiki init  # or manually create ~/wiki with SCHEMA.md, index.md, log.md
```

### Entities are garbage (common words, section headers)

The stopword list needs expansion. Add problematic terms to the `stopwords` set in `ingest.py`'s `extract_entities_simple()` function.

### Index not updating

Check that `index.md` follows the expected format:
```markdown
## Entities
- [[Entity Name]] — Description

## Concepts
- [[Concept Name]] — Description
```

The parser expects `## SectionName` headers and `- [[Link]] — Description` entries.

### Ingestion is slow

Entity extraction is O(n) in content length. For very large files (>100KB), consider:
- Increasing the entity limit (currently 15)
- Using spaCy for faster NER (optional enhancement)

---

## Future Enhancements

1. **Semantic deduplication** — Detect when new research is already covered by existing wiki pages
2. **Contradiction flagging** — Note when new claims conflict with established content
3. **Auto-tag suggestion** — Recommend tags based on content similarity to existing pages
4. **Confidence scoring** — Rate auto-created entities by extraction quality
5. **Batch ingestion** — Process multiple files efficiently (already supported via `--date` for answer-engine)
6. **spaCy integration** — Optional NER for better entity detection (requires `en_core_web_sm`)
7. **Wikilink suggestion** — Propose links to related existing pages during creation

---

## Summary Table

| Integration | Status | Wrapper | Page Type | Auto-entities |
|-------------|--------|---------|-----------|---------------|
| answer-engine | ✅ LIVE | Built-in | `query/` | Yes (15) |
| weekly-blog | ✅ RUNNER | `run.py` | `concept/` | Yes (15) |
| last30days | ✅ LIVE | `with_wiki_ingestion.py` | `query/` | Yes (15) |
| deep-research | ✅ LIVE | `with_wiki_ingestion.py` | `concept/` or `comparison/` | Yes (15) |
| topic-monitor | ⏳ Pending | TBD | `query/` | TBD |
| arxiv | ⏳ Pending | TBD | `entity/` (paper) + author/concept pages | TBD |

**All Tier 1 & 2 integrations are now complete.** Only topic-monitor and arxiv remain (Tier 3).
