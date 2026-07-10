---
name: wiki-ingestion
description: Ingest research outputs from other skills into the llm-wiki knowledge base. Handles answer-engine files, deep research reports, weekly blog research, and topic-monitor findings. Automatically cross-references existing wiki pages and updates navigation.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: research
    tags: [wiki, ingestion, integration, automation]
    related_skills: [llm-wiki, answer-engine, deep-research, weekly-blog, topic-monitor]
---

# Wiki Ingestion

Automatically ingest research outputs from other skills into the llm-wiki knowledge base.

## Purpose

Bridge the gap between **ephemeral research outputs** (answer-engine files, weekly blog drafts, topic monitor findings) and the **compounding knowledge base** (llm-wiki). This skill:

- Reads research markdown files from various sources
- Extracts entities, concepts, and claims
- Creates/updates wiki pages with proper cross-references
- Updates index.md and log.md
- Maintains the wiki's integrity (frontmatter, tags, links)

## When to Use

This skill is typically called **by other skills**, not directly:

### Active Integrations (Live)

- **answer-engine** → after saving to Obsidian Research, automatically ingests to wiki
- **weekly-blog** → runner script (`automation/weekly-blog/run.py`) saves directly to wiki
- **last30days** → use wrapper `scripts/with_wiki_ingestion.py` to auto-ingest
- **deep-research** → use wrapper `scripts/with_wiki_ingestion.py` to auto-ingest

### Integration Pattern

Other skills integrate by calling:
```bash
python3 ~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py \
  --source <skill-name> \
  --file /path/to/research.md \
  --wiki-path ~/wiki  # optional
```

For deep-research and last30days, wrapper scripts are provided that handle
the research execution and automatic ingestion.

## Quick Start

### For Skill Developers

Call the ingestion script directly:

```bash
# Ingest a single research file
python3 ~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py \
  --source answer-engine \
  --file ~/Documents/Obsidian\ Vault/Research/2026-04-15-biochar.md

# Ingest all answer-engine files from today
python3 ~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py \
  --source answer-engine \
  --date today

# Ingest last30days output
python3 ~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py \
  --source last30days \
  --file ~/Documents/Last30Days/solid-state-batteries.md

# Ingest deep-research output
python3 ~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py \
  --source deep-research \
  --topic "solid-state batteries" \
  --content /tmp/research.md
```

### Using Wrapper Scripts

For last30days and deep-research, use the provided wrappers that handle
research execution and ingestion in one step:

```bash
# last30days with auto-ingestion
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "solid-state batteries" --days 30

# deep-research with auto-ingestion (requires input file)
python3 ~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py \
  --input-file /path/to/research.md --type concept
```

## Architecture

```
┌────────────────────┐
│  Source Research   │  answer-engine, weekly-blog, topic-monitor,
│   (Markdown)       │  last30days, deep-research outputs
└─────────┬──────────┘
          │ read
          ▼
┌────────────────────┐     ┌────────────────────┐
│   Extraction       │────▶│   Entity/Concept   │
│  (YAML frontmatter,│     │   Detection        │
│   headings,        │     │  (spaCy/pattern)   │
│   wikilinks)       │     └─────────┬──────────┘
└─────────┬──────────┘               │ check existing
          │                          ▼
          │                ┌────────────────────┐
          │                │   Wiki Update      │
          │                │  (create/update    │
          │                │   pages, links,    │
          │                │   frontmatter)     │
          │                └─────────┬──────────┘
          │                          │
          ▼                          ▼
┌────────────────────┐     ┌────────────────────┐
│  Content Mapping   │────▶│   Navigation       │
│  (source type →    │     │   (index.md,       │
│   wiki page type)  │     │    log.md)         │
└────────────────────┘     └────────────────────┘
```

## Source Types → Wiki Page Types

| Source Skill | Output Location | Wiki Page Type(s) | Notes |
|--------------|----------------|-------------------|-------|
| answer-engine | `Research/*.md` | `query/` | Full research + entity/concept links |
| weekly-blog | Research draft | `concept/` | Full research as permanent record |
| last30days | `~/Documents/Last30Days/*.md` | `query/` | Social sentiment + cross-platform signals |
| deep-research | In-memory or file | `concept/` or `comparison/` | Based on query type (general→concept, comparison→comparison) |
| topic-monitor | `.findings/*.json` | `query/` | Timestamped news items (pending) |

## Ingestion Rules

### 1. Answer-Engine Files → Queries + Entity Links

When ingesting `Research/YYYY-MM-DD-slug.md`:

1. **Create a query page** in `queries/`:
   - Title: The research question/topic
   - Content: Executive summary + key findings
   - Frontmatter: `type: query`, tags from source, sources list
   - Link to all mentioned entities/concepts via `[[wikilinks]]`

2. **Update existing entity pages** that appear in the research:
   - Add new information to `entities/` pages
   - Bump `updated` date
   - Add cross-reference to the new query page

3. **Create new entity pages** for notable mentions:
   - Threshold: mentioned in 2+ research files OR central to one file
   - Types: person, organization, tool, model, paper
   - Extract from: author names, tool names, company names, paper titles

4. **Update index.md** alphabetically under Queries section
5. **Append to log.md**: `## [DATE] ingest | answer-engine | Query Title`

### 2. Weekly Blog Research → Concepts

When weekly-blog runs:

1. **Create/update a concept page** in `concepts/`:
   - Title: Blog post title
   - Content: Full research (not the condensed blog version)
   - Frontmatter: `type: concept`, tags, sources
   - Cross-link to related entities

2. **No separate query page** — the concept page IS the permanent record
3. **Blog post** is a derivative view of the concept page (condensed)
4. **Update index.md** under Concepts
5. **Append to log.md**: `## [DATE] ingest | weekly-blog | Topic`

### 3. Topic Monitor Findings → Queries + Entity Updates

For each important finding:

1. **Create query page** if the finding is novel:
   - Title: Brief description of the development
   - Content: What happened, why it matters, sources
   - Frontmatter: `type: query`, `tags: [news, monitoring]`
   - Date in title: `2026-04-16 — Company X announces Y`

2. **Update relevant entity pages**:
   - Company X page: add announcement to timeline
   - Product Y page: new version/release note
   - Link both ways

3. **Log**: `## [DATE] ingest | topic-monitor | Finding summary`

## Content Extraction Strategy

### From answer-engine files:

```markdown
# Query Title

*Research Date: YYYY-MM-DD HH:MM:SS ET*

---

## Executive Summary
[2-4 sentence answer]

## Key Findings
- Finding 1 [1][2]
- Finding 2 [3]

## Detailed Analysis
[Full synthesis]

## References
[1] Source Title - URL (publication type, date)
[2] ...

---

## Metadata
- **Query**: original query text
- **Timestamp**: ISO timestamp
- **Sources**: N sources
```

**Extract:**
- Title = first heading (`# ...`)
- Summary = Executive Summary section content
- Entities = proper nouns in Key Findings + Detailed Analysis (tools, people, companies, models)
- Concepts = noun phrases from headings and key findings
- Sources = References section URLs

### From weekly-blog research:

The raw research file (before blog condensation) should be saved. If only the blog post exists:
- Use the blog post content as the concept page
- Add a note: "This is the published blog version; full research notes available at [link to raw]"

## Frontmatter Template

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from-taxonomy]
sources:
  - type: answer-engine | weekly-blog | topic-monitor | last30days | deep-research
    reference: "Query title or finding summary"
    date: YYYY-MM-DD
    file: path/to/source.md (optional)
---
```

## Cross-Reference Policy

- **Minimum 2 outbound wikilinks** per new page
- **Check for existing pages** before creating new ones
- **Update backlinks**: when page A mentions entity B, ensure B's page links to A
- **Orphan detection**: run lint after batch ingestion

## Script: `scripts/ingest.py`

Main ingestion entry point. Handles:
- Argument parsing (source type, file/date, wiki path)
- Source-specific extraction logic
- Entity detection (spaCy or pattern-based)
- Wiki page creation/update
- Navigation updates (index.md, log.md)
- Lint report

## Script: `scripts/extract_entities.py`

Standalone entity extraction:
```bash
python3 extract_entities.py --file research.md --format json
# Output: {"entities": [...], "concepts": [...], "title": "...", "summary": "..."}
```

Uses:
- spaCy (if available) for NER
- Regex patterns for common patterns (tool names, company names, arXiv IDs)
- Heading structure for concept extraction

## Integration Points

### With answer-engine:
Modify `scripts/save_to_obsidian.py`:
```python
# After saving to Research/
subprocess.run([
    "python3", 
    os.path.expanduser("~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py"),
    "--source", "answer-engine",
    "--file", filepath,
    "--wiki-path", wiki_path
])
```

### With weekly-blog:
Modify `automation/weekly-blog/SKILL.md` pipeline:
1. Deep research → save to wiki (via ingestion) instead of Research/
2. Extract condensed version → blog post
3. Publish blog post

### With topic-monitor:
Modify `scripts/digest.py` or add post-processing:
- For each high-priority finding, call ingestion
- Batch findings by topic for efficiency

## Configuration

No separate config — uses the wiki path from llm-wiki skill config:
- `skills.config.wiki.path` in `~/.hermes/config.yaml`
- Falls back to `~/wiki`

## Dependencies

- Python 3.8+
- `spaCy` with `en_core_web_sm` model (optional, for better NER)
- Or fall back to regex-based extraction

## Wiki Lint (Health Check)

Run a comprehensive programmatic audit of the llm-wiki. Use `execute_code` for these checks:

### 1. Broken Wikilinks

```python
import os, re
from collections import defaultdict

wiki = os.path.expanduser("~/wiki")
wiki_pages = []
for subdir in ['entities', 'concepts', 'comparisons', 'queries']:
    subdir_path = os.path.join(wiki, subdir)
    if os.path.exists(subdir_path):
        for f in os.listdir(subdir_path):
            if f.endswith('.md'):
                wiki_pages.append(os.path.join(subdir_path, f))

# Extract all wikilinks and find broken ones
target_to_file = {}
for subdir in ['entities', 'concepts', 'comparisons', 'queries']:
    subdir_path = os.path.join(wiki, subdir)
    if os.path.exists(subdir_path):
        for f in os.listdir(subdir_path):
            if f.endswith('.md'):
                target_to_file[f[:-3]] = os.path.join(subdir_path, f)

broken_links = []
for filepath in wiki_pages:
    with open(filepath, 'r') as f:
        content = f.read()
    for link in re.findall(r'\[\[(.*?)\]\]', content):
        target = link.split('|')[1] if '|' in link else link
        if target not in target_to_file:
            broken_links.append((os.path.basename(filepath), target))
```

### 2. Tag Validation

Check all tags on wiki pages exist in SCHEMA.md's tag taxonomy.

### 3. Index Completeness

Ensure every wiki page is listed in index.md.

### 4. Page Sizes

Flag pages over 200 lines as candidates for splitting.

### 5. Orphaned Pages

Query pages are intentionally orphaned (leaf nodes). Entity or concept pages with no inbound links warrant investigation.

### Output Format

Report grouped by severity: 🔴 CRITICAL (broken links) → 🟡 WARNING (invalid tags) → 🟢 INFO (large pages) → ✅ PASS.

## Pitfalls

- **Over-ingestion**: Don't create pages for passing mentions. Apply the 2+ source threshold.
- **Tag sprawl**: Only use tags from SCHEMA.md taxonomy. Add new tags to SCHEMA.md first.
- **Orphan pages**: Always ensure new pages link to existing content.
- **Index drift**: Every new page must be added to index.md.
- **Log rotation**: Check log.md size; rotate if >500 entries.

## Future Enhancements

- **Semantic deduplication**: Detect when a new finding is already covered
- **Contradiction detection**: Flag when new research conflicts with existing pages
- **Auto-tag suggestion**: Recommend tags based on content similarity
- **Link suggestion**: Propose wikilinks to related pages
- **Batch ingestion mode**: Process multiple files efficiently
