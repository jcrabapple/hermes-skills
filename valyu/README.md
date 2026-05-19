# Valyu Search & Research

Direct integration with [Valyu API](https://docs.valyu.ai/) — unified access to web search plus 36+ proprietary data sources through a single REST API.

## What it does

| Command | Description |
|---------|-------------|
| `search` | Semantic search across web, arXiv, PubMed, SEC filings, clinical trials, patents, news |
| `extract` | Clean markdown extraction from URLs (up to 50, Chrome rendering for JS-heavy pages) |
| `answer` | AI-synthesized answers with citations |
| `research` | Deep multi-step research reports (async) |

## Setup

1. Get an API key from [platform.valyu.ai](https://platform.valyu.ai/) ($10 free credits)
2. Add `VALYU_API_KEY=your-key-here` to `~/.hermes/.env` or export it in your shell

## Install

```bash
# Clone into your Hermes skills directory
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/valyu ~/.hermes/skills/research/valyu
```

Or copy the skill directory into any location Hermes scans for skills.

## Usage

```bash
# Web search
python3 scripts/valyu.py search "latest developments in quantum computing"

# Proprietary sources only (arXiv, PubMed, SEC, etc.)
python3 scripts/valyu.py search "CRISPR gene therapy" --type proprietary

# Filter by source preset
python3 scripts/valyu.py search "NVDA earnings report" --sources finance
python3 scripts/valyu.py search "clinical trial results" --sources medical

# Extract clean content from URLs
python3 scripts/valyu.py extract "https://arxiv.org/abs/2409.09057"

# AI-synthesized answer with citations
python3 scripts/valyu.py answer "What are the latest advances in mRNA vaccines?"

# Deep research report (async, polls until complete)
python3 scripts/valyu.py research "Comprehensive analysis of solid-state battery technology"
```

## Source Presets

| Preset | Sources |
|--------|---------|
| `medical` | PubMed, clinical trials, FDA |
| `finance` | SEC filings, earnings, stock data |
| `academic` | arXiv, PubMed, bioRxiv, journals |
| `legal` | Patents, court filings |

Or pass specific dataset IDs (`valyu/valyu-arxiv`) or domains (`arxiv.org`).

## Data Sources (36+)

| Category | Sources |
|----------|---------|
| Academic | arXiv, PubMed, bioRxiv, medRxiv, scholarly journals |
| Financial | SEC filings (10-K, 10-Q, 8-K, 13F), earnings transcripts, stock data |
| Healthcare | ClinicalTrials.gov, FDA drug labels, ChEMBL |
| Economic | FRED, BLS, World Bank |
| News | Real-time news with date/country filtering |
| Prediction | Polymarket, Kalshi |
| Legal | 8M+ US patents |

## Requirements

- Python 3.8+ (no external dependencies — uses stdlib only)
- Valyu API key

## License

MIT
