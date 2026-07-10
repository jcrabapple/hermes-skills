# Tier 2 Integrations — last30days & deep-research

## Implementation Complete ✅

Both `last30days` and `deep-research` skills now have automatic wiki ingestion
via the `wiki-ingestion` infrastructure.

---

## What Was Built

### 1. Extended `wiki-ingestion/scripts/ingest.py`

**New sources added:**
- `--source last30days` — Ingest last30days saved reports
- `--source deep-research` — Ingest deep-research reports with type-aware page creation

**New functions:**
- `ingest_last30days_report(filepath, wiki_path)` — Parses last30days markdown output, extracts topic, creates `query/` page
- `ingest_deep_research(topic, research_content, wiki_path, query_type)` — Creates `concept/` or `comparison/` page based on query type

**Improved entity extraction:**
- Expanded stopword list (150+ terms) to filter out section headers, common verbs, generic nouns
- Heading fragment detection (rejects "Current State\n\nCurrent" type fragments)
- Better concept detection (excludes section header patterns)

**Clean output:** Human messages → stderr, JSON result → stdout

### 2. Wrapper Scripts

#### `last30days/scripts/with_wiki_ingestion.py`

Full wrapper that:
- Accepts topic + flags (same as last30days.py)
- Runs last30days research
- Saves output to `~/Documents/Last30Days/{slug}.md`
- Automatically calls wiki ingestion
- Prints summary + JSON result

**Usage:**
```bash
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "solid-state batteries" --days 30
```

#### `deep-research/scripts/with_wiki_ingestion.py`

Wrapper that:
- Accepts existing research file via `--input-file`
- Determines page type (concept vs comparison)
- Calls wiki ingestion with appropriate metadata
- Outputs research to stdout for agent consumption

**Usage:**
```bash
python3 ~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py \
  --input-file /path/to/research.md --type concept
```

---

## Test Results

### last30days Integration

Test with `kdenlive-video-editing-tips-raw.md` (95KB):
- 111 entities detected, 15 auto-created
- Query page: `query/kdenlive-video-editing-tips.md`
- Index updated, log entry created

### deep-research Integration

Test with solid-state batteries sample (2,200 words):
- 55 entities detected, 15 auto-created (QuantumScape, Toyota, Solid Power, etc.)
- Concept page: `concept/solid-state-batteries.md`
- Index updated, log entry created

---

## Files Created/Modified

**Created:**
- `~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py`
- `~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py`
- Updated `wiki-ingestion/SKILL.md` and `INTEGRATIONS.md`

**Modified:**
- `~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py` — +200 lines

---

## How to Use

### last30days
```bash
python3 ~/.hermes/skills/last30days/scripts/with_wiki_ingestion.py "topic"
```

### deep-research
```bash
python3 ~/.hermes/skills/research/deep-research/scripts/with_wiki_ingestion.py \
  --input-file research.md --type concept
```

---

## Next Steps

Tier 3 (final):
1. topic-monitor — Add post-processing to digest.py
2. arxiv — Build arxiv-ingest wrapper

After that, **all research skills feed the wiki automatically**.
