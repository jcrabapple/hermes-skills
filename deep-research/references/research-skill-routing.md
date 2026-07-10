# Research Skill Routing

Use one canonical mode per task, then add specialist sources only when needed.

| User intent | Primary skill | Why |
|---|---|---|
| Direct factual answer, comparison, explanation, citations | `answer-engine` | Fast-to-medium cited synthesis |
| Comprehensive report, deep dive, multi-faceted investigation | `deep-research` | Systematic multi-phase methodology |
| What people are saying now, reactions, trends, recommendations | `last30days` | Last-30-day social and community signals |
| Explicit Fusion request or high-stakes independent-model critique | `openrouter-fusion-research` | Multi-model consensus and blind spots |
| Papers, PubMed, SEC, patents, trials, proprietary datasets | `valyu` | Specialist source access |
| Search arXiv by author/category/ID | `arxiv` | Focused paper discovery |
| Query market prices or order books | `polymarket` | Structured prediction-market data |
| Install or operate the external Feynman CLI | `feynman-research-agent` | Tool-specific operations only |
| Analyze a product feature's actual availability | `product-feature-availability` | Region/account/platform verification |
| Research a major purchase | `consumer-durables-research` or `cross-border-shopping` | Domain-specific decision methodology |

## Rules

1. Do not load Fusion, Valyu, and deep-research by default for the same task.
2. Start with `answer-engine` unless the requested deliverable clearly needs another mode.
3. `deep-research` controls methodology; Valyu/arXiv may supply specialist evidence inside it.
4. `last30days` measures current discourse, not factual truth. Verify factual claims separately.
5. External-tool skills such as Feynman and Parallel CLI trigger only when the user names the tool or explicitly requests its unique capability.
6. Writing, Obsidian persistence, wiki ingestion, and publishing are downstream stages, not competing research modes.
