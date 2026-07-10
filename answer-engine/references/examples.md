# Answer Engine — Usage Examples

## Simple Factual Query (Still Deep)

```
User: "What's the latest news on solid-state battery breakthroughs?"

1. kagi fastgpt "solid-state battery breakthroughs 2026"
2. kagi search "solid-state battery breakthroughs 2026"
3. python scripts/searxng_search.py "solid-state battery breakthrough"  # may return 0 results — degraded
5. Query expansion: also search "quantum scape 2026", "toyota solid state battery", "lithium metal anode"
6. Extract key claims, cluster by theme (energy density, timeline, challenges, companies)
7. Note contradictions (competing timeline claims)
8. Synthesize with executive summary + key findings + detailed analysis
9. Save to Obsidian with full metadata
```

## Comparative Research (Deep Dive)

```
User: "Compare Framework Laptop 16 vs Lenovo ThinkPad P14s for Linux development"

1. kagi search "Framework Laptop 16 Linux review"
2. kagi search "ThinkPad P14s Linux compatibility"
3. python scripts/searxng_search.py "Framework Laptop 16 Linux"  # may return 0 results
4. python scripts/searxng_search.py "ThinkPad P14s Linux"  # may return 0 results
6. Query expansion: "Framework 16 AMD Linux issues", "ThinkPad P14s Fedora", "Framework Linux driver support"
7. Extract: hardware compatibility, driver issues, community reports, official support status
8. Build comparison matrix (CPU/GPU, WiFi, suspend/resume, audio, trackpad, community support)
9. Note gaps (e.g., "no long-term reliability data yet for Framework 16")
10. Synthesize with pros/cons, recommendation by use case
11. Save to Obsidian
```

## Exploratory Research (Emerging Topic)

```
User: "What are the promising approaches to AI alignment in 2026?"

1. Break into sub-questions via delegate_task (batch mode):
   - "RLHF alternatives 2026"
   - "Constitutional AI developments"
   - "Interpretability research 2026"
   - "AI governance policy 2026"
2. kagi search each sub-question --num-results 10
3. web_search for broader coverage
4. SearXNG for independent sources (academic, blogs, forums)
5. Query expansion: "DPO vs PPO", "Anthropic alignment research", "OpenAI superrlhf"
6. Cluster findings: technical approaches, policy/governance, industry practices, academic research
7. Map disagreements (e.g., "interpretability-first vs RLHF-first camps")
8. Synthesize with landscape overview, key players, open questions
9. Save to Obsidian with topic tags for future retrieval
```

## File-Referenced Query

```
User: "Based on my previous research, what are the key trends in mead fermentation?"

1. python scripts/embedding_search.py search "mead fermentation trends"
2. Read top 5 matching files from Obsidian Research
3. Extract prior findings, note dates (identify outdated info)
4. web_search "mead fermentation techniques 2026"
5. kagi search "modern mead making methods" --num-results 10
6. Compare prior research with new findings (what's confirmed, what's updated)
7. Synthesize with explicit callouts: "Prior research confirmed [1][3]", "New finding: [5]"
8. Save updated synthesis to Obsidian, link to prior files
```
