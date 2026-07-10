---
name: llm-performance-benchmark
description: >
  Find LLM tokens-per-second (TPS), latency, and throughput metrics.
  If direct API benchmarking is impossible, pivot to published third-party
  benchmarks and provide a manual fallback script.
trigger: >
  User asks for model speed, TPS, tokens per second, throughput, latency,
  or performance benchmark of a specific LLM.
---

# LLM Performance Benchmark

## 1. Attempt Live Benchmark (if possible)
- If an API key is available and unmasked, run a timed generation (e.g., 400–500 tokens) and compute TPS = completion_tokens / elapsed_time.
- **Pitfall**: Config files may redact keys. Do not spend more than 2–3 attempts trying to extract a masked key.

## 2. Pivot to Published Benchmarks
If direct measurement is impossible, immediately search for third-party benchmark data.

### Trusted Aggregators (search these first)
| Site | What it tracks | URL pattern |
|---|---|---|
| **Artificial Analysis** | Provider-level TPS, TTFT, price | `artificialanalysis.ai/models/<model>/providers` |
| **DeepInfra Blog** | Provider shootouts (Groq, Fireworks, etc.) | `deepinfra.com/blog/<model>-api-benchmarks` |
| **LLM-Stats** | Leaderboard rankings, quality scores | `llm-stats.com/models/<model>` |

### Search Queries to Use
```
"<model-name>" tokens per second benchmark throughput
"<model-name>" API provider benchmark artificialanalysis
```

## 3. Watch for Model Name Confusion
- Moonshot models: `kimi-k2.6` is the current flagship; `kimi-k2-0905` / `kimi-k2-0711` are earlier K2 series variants. Do not conflate them.
- Always verify the exact model string in the provider's official model list.

## 4. Summarize Results
Present:
- **Output speed range** (median t/s per provider)
- **TTFT** (time to first token) — especially important for reasoning models
- **Provider spread** (same model can be 3× faster on Groq vs Fireworks vs official API)
- **Caveats** (reasoning tokens, context-length effects, 72-hour median vs burst speed)

## 5. Provide a Manual Fallback Script
Always give the user a copy-paste script they can run with their own key.

## Pitfalls
- **Do not report self-published marketing numbers as gospel** — cross-check with Artificial Analysis or DeepInfra.
- **Reasoning models inflate TTFT** because thinking tokens stream before the answer. Clarify whether the cited TTFT includes reasoning time.
- **Provider != Model**: A model can be 200 t/s on Groq and 27 t/s on Novita. Always name the provider.
- **Masked keys**: If an API key is redacted in config, move on to web research immediately.
