---
name: llm-prompt-analysis
description: "Analyze external LLM system prompts — leaked, officially published, or competitor-released — to extract transferable patterns for improving your own persona/SOUL.md/skills. Triggers: user shares a leak link, new prompt leak surfaces, user asks 'what is [vendor] doing', 'analyze this prompt', 'compare system prompts', or a follow-up session wants to apply insights from a previous leak analysis."
version: 1.0.0
metadata:
  hermes:
    tags: [llm, prompt-engineering, research, persona, system-prompt, competitors]
---

# LLM Prompt Analysis

Methodology for reading another LLM's system prompt (or any large behavioral spec) and extracting the patterns worth stealing — without copying IP, copying vendor-specific product plumbing, or copying rules that are overblown for a one-user personal assistant.

## When to use

- User shares a link to a leaked LLM system prompt (Twitter, GitHub, news)
- A new system prompt is published officially (model card, system card, blog)
- User asks to compare prompts across vendors (Anthropic vs OpenAI vs Google vs xAI)
- User says "what is [vendor] doing differently" or "steal ideas from [vendor]"
- A follow-up session wants to revisit / apply a previous analysis

## Workflow

### 1. Get the source file

Most leaks land in Pliny the Prompter's `CL4R1T4S` GitHub repo (publicly available, organized by vendor). Use the **raw** URL, not the blob URL — the blob URL returns HTML, the raw URL returns the file:

```bash
curl -fsSL "https://raw.githubusercontent.com/elder-plinius/CL4R1T4S/main/{VENDOR}/{MODEL}.md" \
  -o /tmp/{vendor}-{model}.md && wc -l /tmp/{vendor}-{model}.md
```

For blog posts / official announcements, use `web_extract` first; for raw prompt files in a GitHub repo, `curl` is faster and survives JS-rendered pages.

For Twitter/X links, `web_extract` often fails — fall back to `curl` with a browser User-Agent and parse the `og:description` + embedded `note_tweet` JSON (Twitter embeds the full text in a `__TSR_router` JSON blob in the HTML).

### 2. Read in chunks

System prompts are typically 1,000–3,000 lines. Use `read_file` with `offset` and `limit=500` to read in 500-line chunks. First chunk reveals the structure; subsequent chunks fill in details. Don't `cat` the whole thing — you'll blow context.

```python
read_file(path, offset=1, limit=500)
read_file(path, offset=500, limit=500)
read_file(path, offset=1000, limit=500)
# ...repeat until EOF
```

### 3. Categorize each section

For every section in the prompt, classify into ONE of these buckets:

| Bucket | Examples | Action |
|---|---|---|
| **Persona / behavior** | Tone, refusal style, mistake handling, evenhandedness, formatting rules, anti-sycophancy, "acknowledge without collapsing" | **Evaluate for transfer** |
| **Search / web** | When to search, query length rules, citation format, harmful-content gates | Evaluate for transfer |
| **Product information** | Vendor's product line, model strings, feature lists, version numbers | Skip — vendor-specific |
| **Tool definitions** | JSON schemas for vendor tools (web_search, artifact create, etc.) | Skip — vendor-specific |
| **Copyright / safety rails** | Quotation limits, refusal conditions, harm categories, IP posture | Skip — vendor's legal stance |
| **MCP / app integration** | Third-party connector flow, app suggestion picker, opt-in gates | Skip — vendor's product surface |
| **Skills list** | Trigger phrases + paths for vendor's skill library | Skip — vendor's skill system |
| **Persistent state** | window.storage, memory systems, artifact persistence | Skip — vendor's product features |

### 4. For persona/behavior sections, score against your own system

For each persona/behavior section, ask:

1. **Already in SOUL.md?** If yes, confirm and move on — no double-loading.
2. **Overblown for a one-user personal assistant?** Most consumer-product safety rules (mental-health triage, eating-disorder handling, means restriction, suicide prevention rails) are for public products with millions of users. A personal assistant for one capable adult doesn't need them. Mark "skip — overblown."
3. **Genuinely transferable?** Mark high/medium value and adopt.

Common high-value patterns to look for:

- **Anti-sycophancy framing** — "acknowledge without collapsing into self-abasement," "maintain self-respect," "acknowledge what went wrong, stay on the problem"
- **Best-steelman rule** — "A request to defend X is a request for the best case its defenders would make, not for Claude's own view"
- **File-vs-inline decision rule** — explicit trigger list for when to create a file vs respond inline
- **Skill-loader mandate** — "Don't first decide whether the task needs a skill; the skills themselves define what they cover"
- **Tone / formatting constraints** — anti-bullet prose rules, max-one-question-per-response, "no thank you for reaching out"
- **Search-query brevity** — "1–6 words for best results"
- **Search-before-answering on contested state** — current holders, policies, recent deaths
- **Tool failure honesty** — "NEVER substitute fabricated output for missing results"
- **Evenhandedness on contested topics** — present opposing views, don't project personal opinion

### 5. Present a tiered recommendation

Format the response as three buckets with one-line reasoning each:

- **High value, low cost — would adopt** ← concrete suggestions
- **Medium value — would consider** ← with caveats
- **Not transferable** ← explicit list so the user doesn't wonder why you skipped it

End with: *"Want me to draft a patch for [specific skill/SOUL.md]?"* — don't auto-apply, let the user decide.

### 6. Don't reproduce the leaked prompt verbatim

Treat the leaked prompt as the vendor's IP. Summarize the structure, quote short fragments for illustration only, and don't paste sections wholesale into your context. Protects against: IP reproduction, context bloat, and the trap of using someone else's prompt as a template (it isn't — it's shaped by their product surface).

## Pitfalls

- **The prompt's *shape* reflects the vendor's product surface, not best practice.** Anthropic's ~1,500-line prompt is shaped by Claude.ai's UI, MCP integrations, and consumer safety rules. Most of it is product plumbing, not transferable prompt engineering. Don't measure your own prompt length against theirs.
- **Don't adopt consumer-product safety rails for a personal assistant.** The Fable 5 prompt has extensive mental-health triage, eating-disorder handling, and suicide prevention. For a public consumer product with millions of users, fine. For a one-user personal assistant, overkill. Filter ruthlessly.
- **Formatting rules are vendor-specific.** Fable 5's "Claude writes prose without bullets" rule fights how Discord chat actually scans. Bullets are fine in Discord. Don't copy formatting constraints wholesale — test them against your delivery medium.
- **Copyright hard limits are vendor legal posture.** The 15-word quote cap is Anthropic's IP-protection stance, not yours. Don't copy legal constraints you don't have.
- **Don't paste the leaked prompt into the user's context.** Summarize, don't reproduce. Otherwise you risk IP issues and bloat the conversation.
- **Twitter/X fetches often fail via web_extract.** Fall back to `curl` with a real browser User-Agent and parse the embedded `note_tweet` JSON from the page's `__TSR_router` block. The full text is there even when `web_extract` returns nothing.
- **GitHub blob URLs return HTML, not raw content.** Always use `raw.githubusercontent.com/...` for file fetches.
- **"Best-steelman" doesn't mean "no opinion."** Present the strongest case for the user's position, then the strongest case against, then let the user decide. Don't pretend to be neutral on settled facts.

## Verification

After patching SOUL.md or a skill with adopted patterns, re-test by sending a scenario where the new pattern should fire:

- Adopted **anti-sycophancy** → send a message where you're wrong; check the response acknowledges without groveling
- Adopted **best-steelman** → ask "defend [contested position]"; check it frames as the case others would make
- Adopted **file-vs-inline** → ask for a 200-word blog post; check it creates a file, not inline prose
- Adopted **search-query brevity** → ask a research question; check the first search query is ≤ 6 words

## Support files

- `references/prompt-sources.md` — canonical leak repos, Twitter accounts to watch, official model card URLs
