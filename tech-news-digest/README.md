# Tech News Digest

Twice-weekly tech news digest covering the last 48-72 hours across five categories, delivered via [AgentMail](https://agentmail.to/).

## What it does

Pulls recent stories from five categories, ranks by impact/recency/credibility, and emails a clean HTML+text digest.

| Category | Example topics |
|----------|----------------|
| General Tech | Product launches, industry moves |
| AI / LLM / ML | Model releases, research, vendor news |
| Developer Tools & Platforms | GitHub, cloud providers, frameworks |
| Cybersecurity | Breaches, vulnerabilities, patches |
| Hardware | Chips, GPUs, consumer electronics |

The skill runs **three rounds of web searches** to build coverage:
1. Broad category sweeps
2. Targeted recent stories with specific names/dates
3. Gap-fill queries for thin categories

## Setup

Requires:
- A `web_search` tool (any of Kagi, NanoGPT, Brave, etc.)
- AgentMail API key — `AGENTMAIL_API_KEY` in `~/.hermes/.env` or your shell
- The companion `agentmail` skill loaded for sending patterns

## Install

```bash
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/tech-news-digest ~/.hermes/skills/research/
```

## Usage

Triggers on: "tech news digest", "weekly tech briefing", "tech newsletter", "what's happening in tech this week".

Designed for a twice-weekly cron job (e.g., Tue + Fri morning). For one-off use, just ask the agent to run it.

## Output

- **Subject:** `Tech News Digest — <Month> <Day>, <Year>`
- **Format:** HTML with inline styling (no external CSS) + plaintext fallback
- **Sections:** Top 3 This Week → 5 category sections → footer
- **Email labels:** `["digest", "newsletter"]`

## Pitfalls

See the full list in [SKILL.md](./SKILL.md), but the top three:
- Do NOT use browser tools — `web_search` is faster and cheaper
- Do NOT send multiple emails in a single run
- Do NOT skip categories when searches come up thin — run targeted gap-fill queries

## See also

- [agentmail](../agentmail/) — required for email delivery
- [weekly-blog](../weekly-blog/) — similar automation pattern, blog output instead of email
