---
name: tech-news-digest
description: Generate a twice-weekly tech news digest covering the last 48-72 hours across five categories, then email it via AgentMail. Uses multi-round web_search strategy and formatted HTML/text email output.
trigger: User asks for a tech news digest, newsletter, or briefing covering recent stories.
---

# Tech News Digest Skill

Generate and deliver a curated tech news digest via email.

## Constraints
- **Use `web_search` ONLY.** Do NOT use `browser_navigate` or browser tools.
- Send exactly ONE email via AgentMail. No test/verification emails.
- Target stories from the **last 48-72 hours**.
- Load the `agentmail` skill for AgentMail sending patterns and API setup.

## Categories to Cover
1. General Tech (product launches, major updates, industry moves)
2. AI / LLM / ML (model releases, research, OpenAI, Anthropic, Google DeepMind, open-source)
3. Developer Tools & Platforms (GitHub, cloud providers, frameworks)
4. Cybersecurity (breaches, vulnerabilities, patches)
5. Hardware (chips, GPUs, consumer electronics)

## Search Strategy (Multi-Round)

### Round 1 — Broad Category Sweeps
Run 5 broad searches, one per category, using current month/year and general keywords:
- `tech news product launches major updates industry moves <Month> <Year>`
- `AI LLM ML model releases research breakthroughs OpenAI Anthropic Google DeepMind <Month> <Year>`
- `developer tools GitHub cloud providers frameworks updates <Month> <Year>`
- `cybersecurity breaches vulnerabilities patches <Month> <Year>`
- `hardware chips GPUs consumer electronics news <Month> <Year>`

### Round 2 — Targeted Recent Stories
Pick 2-3 promising threads per category from Round 1. Run focused searches with specific names, dates, and outlets. Also search exact dates (`<Month> <Day> <Year>`) to catch weekend/holiday stories.

### Round 3 — Gap Fill
Identify which categories are thin. Run additional searches to reach 3-4 solid stories per category. Good gap-fill queries:
- `<Company> <product> <Month> <Year>`
- `Patch Tuesday <Month> <Year>`
- `<Company> breach hack <recent date>`
- `MWC CES <Year> announcements`

### Search Tips
- **Date-bounded queries work best** for 48-72h windows: `<topic> April 19 2026`.
- Social media sources (Instagram, Reddit) sometimes break stories before traditional outlets.
- Search specific CVE IDs once a vulnerability thread is identified.
- If a major event is upcoming (e.g., Google I/O, NVIDIA GTC), search for teasers/pre-announcements.

## Story Selection Criteria
Pick the top 3-4 most significant stories per category based on:
- Impact (affects many users, major platforms, or critical infrastructure)
- Recency (published within last 48-72 hours)
- Credibility (major outlet, official company blog, or verified source)
- Diversity (avoid covering the same company 3 times in one category)

## Writing Summaries
- 2-3 sentences per story.
- Lead with the "what" and "why it matters."
- Include a source link.
- Bold key product names / numbers for scannability.

## Email Format

### Subject
`Tech News Digest — <Month> <Day>, <Year>`

### Body Structure
1. **Top 3 This Week** — Biggest stories overall (cross-category). Write 2-3 sentences each with source.
2. **General Tech** — 3-4 stories
3. **AI / LLM / ML** — 3-4 stories
4. **Developer Tools & Platforms** — 3 stories
5. **Cybersecurity** — 3 stories
6. **Hardware** — 3 stories
7. **Footer** — "Compiled by Hermes Agent · <agentmail-address>"

Provide both `text` and `html` versions to AgentMail `messages.send()` for best deliverability.

## Sending the Digest
Use the `agentmail` skill for the full AgentMail SDK reference, API key loading, and sending examples. The digest should be sent exactly once with `labels=["digest", "newsletter"]`.

## Pitfalls
- Do NOT rely on a single round of searches. The first round rarely yields enough recent, specific stories.
- Do NOT send multiple emails. Compose everything, then send once.
- Do NOT skip categories if they seem slow—run targeted gap-fill searches instead.
- Weekend/holiday news often drops on Friday or Monday; search exact dates to catch it.
