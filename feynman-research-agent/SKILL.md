---
name: feynman-research-agent
description: Install, configure, or explicitly operate the external Feynman research-agent CLI for paper reading, literature reviews, audits, replication, and experiments. Use only when the user names Feynman or asks to manage that tool; not for ordinary Hermes research.
category: research
triggers:
  - feynman

  - literature review
  - paper audit
---

# Feynman — Open Source AI Research Agent

**Website:** https://www.feynman.is/
**GitHub:** https://github.com/feynman

## Overview

Feynman is an open-source AI research agent that reads papers, searches the web, writes drafts, runs experiments, and cites every claim — all running locally. Built on Pi and alphaXiv.

When the user asks to install, set up, or use Feynman, follow the steps below.

## Installation

Two methods:

```bash
# Method 1: curl (bundled runtime, recommended)
curl -fsSL https://feynman.is/install | bash

# Method 2: npm (if you already manage Node locally)
npm install -g feynman

# Skills-only bundle also available on the site
```

## Usage

Ask a question or run a workflow. Every answer is cited.

```bash
feynman "what do we know about scaling laws"
# → Cited research brief from papers and web

feynman deepresearch "mechanistic interpretability"
# → Multi-agent deep dive with synthesis and verification

feynman lit "RLHF alternatives"
# → Literature review with consensus and open questions

feynman audit 2401.12345
# → Paper claims vs. what the code actually does

feynman replicate "chain-of-thought improves math"
# → Replication plan, compute target, experiment execution
```

## Workflows (slash commands / natural language)

| Workflow | Description |
|----------|-------------|
| `/deepresearch` | Multi-agent investigation across papers, web, and code |
| `/lit` | Literature review from primary sources with consensus mapping |
| `/review` | Simulated peer review with severity scores and a revision plan |
| `/audit` | Paper-to-code mismatch audit for reproducibility claims |
| `/replicate` | Replication plan and execution in a sandboxed Docker container |
| `/compare` | Side-by-side source comparison with agreement and conflict matrix |
| `/draft` | Polished paper-style draft with inline citations from findings |
| `/autoresearch` | Autonomous loop: hypothesize, experiment, measure, repeat |
| `/watch` | Recurring monitor for new papers, code, or product updates |

## Agents

Feynman assembles a team of specialized agents:

- **Researcher** — Hunts for evidence across papers, the web, repos, and docs
- **Reviewer** — Grades claims by severity, flags gaps, and suggests revisions
- **Writer** — Structures notes into briefs, drafts, and paper-style output
- **Verifier** — Checks every citation, verifies URLs, removes dead links

## Skills & Tools

| Tool | Description |
|------|-------------|
| Paper search | Search, Q&A, code reading, and annotations via alpha CLI |
| Web search | Searches via Gemini or Perplexity |
| Session search | Indexed recall across prior research sessions |
| Preview | Browser and PDF export of generated artifacts |

## Compute Options

- **Isolated local containers** — safe experiments on your machine
- **Serverless GPU** — burst training and inference when needed
- **Persistent GPU pods** — SSH access for long-running runs

## Notes

- All output stays source-grounded with inline citations
- Capabilities ship as Pi skills
- Feynman replaces/augments the need for running separate deep research tools
