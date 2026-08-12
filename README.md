# Hermes Skills 🧠⚡

**Reusable skills and tools for [Hermes Agent](https://hermes-agent.nousresearch.com/) — your AI's procedural memory.**

Hermes Agent is an open-source AI assistant framework that can use tools, run code, and persist context across sessions. This repo is a collection of **skills**: packaged expertise that gives Hermes domain-specific capabilities on demand.

## What is a Skill?

A skill is a reusable knowledge module — the AI equivalent of a plugin. Each skill includes:

- **SKILL.md** — structured instructions with when-to-use/not-use guidance, exact commands, workflows, and common pitfalls
- **Scripts** — CLI tools or Python code the agent executes
- **References** — API docs, config templates, and supporting material

When you ask Hermes to do something, it scans its available skills and loads the relevant ones. A skilled agent doesn't just answer — it has a battle-tested playbook for that specific task.

## Skills in This Repo

### Job Search & Career Development (21 skills)

All resume and career skills are organized under [`job-search/`](job-search/) for easy installation as a complete career toolkit.

| Skill | What it does |
|-------|-------------|
| [`job-search/resume-workflow-orchestrator`](job-search/resume-workflow-orchestrator/) | Meta-skill that routes to the right resume skill and chains workflows together |
| [`job-search/tailored-resume-generator`](job-search/tailored-resume-generator/) | Analyzes job descriptions and generates tailored resumes with DOCX conversion |
| [`job-search/job-description-analyzer`](job-search/job-description-analyzer/) | Analyze job postings, calculate match scores, identify gaps, create application strategy |
| [`job-search/cover-letter-generator`](job-search/cover-letter-generator/) | Create personalized, compelling cover letters from resume + job description |
| [`job-search/resume-ats-optimizer`](job-search/resume-ats-optimizer/) | Optimize resumes for Applicant Tracking Systems, check ATS compatibility, analyze keyword match |
| [`job-search/resume-bullet-writer`](job-search/resume-bullet-writer/) | Transform weak bullets into achievement-focused statements with metrics and impact |
| [`job-search/resume-quantifier`](job-search/resume-quantifier/) | Find opportunities to add metrics and estimate numbers when exact data unavailable |
| [`job-search/resume-formatter`](job-search/resume-formatter/) | Ensure ATS-friendly formatting and create clean, scannable layouts |
| [`job-search/tech-resume-optimizer`](job-search/tech-resume-optimizer/) | Optimize resumes for software engineering, PM, and technical roles |
| [`job-search/career-changer-translator`](job-search/career-changer-translator/) | Translate skills from one industry to another, identify transferable skills |
| [`job-search/executive-resume-writer`](job-search/executive-resume-writer/) | Create C-suite and VP level resumes emphasizing strategic leadership |
| [`job-search/academic-cv-builder`](job-search/academic-cv-builder/) | Format CVs for academic positions with publications, grants, teaching |
| [`job-search/creative-portfolio-resume`](job-search/creative-portfolio-resume/) | Balance visual design with ATS compatibility for creative roles |
| [`job-search/resume-section-builder`](job-search/resume-section-builder/) | Create targeted sections optimized for different experience levels and roles |
| [`job-search/salary-negotiation-prep`](job-search/salary-negotiation-prep/) | Research market rates, build negotiation strategy, create counter-offer scripts |
| [`job-search/interview-prep-generator`](job-search/interview-prep-generator/) | Generate STAR stories, practice questions, talking points from resume |
| [`job-search/offer-comparison-analyzer`](job-search/offer-comparison-analyzer/) | Compare multiple job offers side-by-side with total compensation analysis |
| [`job-search/resume-version-manager`](job-search/resume-version-manager/) | Track different resume versions, maintain master resume, manage tailored versions |
| [`job-search/portfolio-case-study-writer`](job-search/portfolio-case-study-writer/) | Transform resume bullets into detailed portfolio case studies |
| [`job-search/reference-list-builder`](job-search/reference-list-builder/) | Format professional references properly and prepare reference materials |
| [`job-search/linkedin-profile-optimizer`](job-search/linkedin-profile-optimizer/) | Sync resume with LinkedIn, optimize for searchability and engagement |

### Social Media & Content

| Skill | What it does |
|-------|-------------|
| [`mastodon`](mastodon/) | Post to Mastodon via API — text statuses, media attachments, polls, scheduled posts, visibility control, threads |
| [`mastodon-admin`](mastodon-admin/) | Administer a Mastodon instance — view/manage reports, suspend/silence accounts, resolve reports, welcome new users |
| [`social-media-post-drafting`](social-media-post-drafting/) | Draft short-form posts for Mastodon, X, LinkedIn, Bluesky, Threads — platform identification, char-limit verification, topic research |
| [`tiktok-research`](tiktok-research/) | Research TikTok content — scrape URLs, extract transcripts, analyze trends, draft Mastodon share posts from findings |
| [`nanogpt-tiktok`](nanogpt-tiktok/) | Scrape TikTok hashtags, profiles, keyword searches, and video URLs with ASR transcripts via NanoGPT API |
| [`nanogpt-instagram`](nanogpt-instagram/) | Scrape Instagram posts (captions, metrics, media, comments) via NanoGPT API |
| [`nanogpt-linkedin`](nanogpt-linkedin/) | Scrape LinkedIn profile data (name, title, company, email, education) via NanoGPT API |
| [`article-writing`](article-writing/) | Write articles, guides, blog posts, tutorials, newsletters, and research reports in a distinctive voice from supplied examples |
| [`hermes-tweet`](hermes-tweet/) | Use the native Hermes Tweet plugin for X/Twitter search, reads, monitors, follower exports, and approved X actions through Xquik |

### Research & Information

| Skill | What it does |
|-------|-------------|
| [`deep-research`](deep-research/) | Systematic multi-source methodology for comprehensive reports and complex, multi-faceted investigations |
| [`answer-engine`](answer-engine/) | Research-focused query handling with multi-source synthesis, citations, and Obsidian persistence — like a self-hosted Perplexity |
| [`hackernews-scraper`](hackernews-scraper/) | Scrape top Hacker News stories, filter by topic or keyword, return structured JSON with titles, URLs, scores, comment counts |
| [`stock-recommendations`](stock-recommendations/) | Weekly stock recommendation digest using mixed signals — technical, fundamental, and sentiment analysis |
| [`domain-intel`](domain-intel/) | Passive domain reconnaissance — subdomain discovery, SSL certs, WHOIS, DNS records, domain availability. No API keys needed |
| [`repo-discovery`](repo-discovery/) | Automated GitHub repository discovery and monitoring — scraping, scoring, and integration patterns |
| [`product-feature-availability`](product-feature-availability/) | Investigate whether a documented product feature is actually available for a specific user context (region, plan, platform) |
| [`consumer-durables-research`](consumer-durables-research/) | Systematic research for major purchases (appliances, HVAC, power tools) — reliability data, failure modes, head-to-head comparisons |
| [`cross-border-shopping`](cross-border-shopping/) | Research and evaluate gray-market / cross-border products — carrier compatibility, ROM verification, retailer vetting, pricing benchmarks |
| [`llm-performance-benchmark`](llm-performance-benchmark/) | Find LLM tokens-per-second, latency, and throughput metrics with fallback to published third-party benchmarks |
| [`llm-prompt-analysis`](llm-prompt-analysis/) | Analyze external LLM system prompts (leaked, published, or competitor-released) to extract transferable patterns |
| [`kagi-tools-guide`](kagi-tools-guide/) | Guide for using the kagi-tools Hermes plugin — which tool for what, auth requirements, fallback patterns, known quirks |
| [`feynman-research-agent`](feynman-research-agent/) | Install and operate the external Feynman CLI for paper reading, literature reviews, audits, and replication |
| [`ai-context-generation`](ai-context-generation/) | Generate compact AI-readable context maps from codebases for feeding to LLMs |
| [`wiki-ingestion`](wiki-ingestion/) | Ingest research outputs into an interlinked markdown knowledge base for LLM querying |
| [`parallel-cli`](parallel-cli/) | Agent-native web research using Parallel CLI — multi-page extraction, structured data, screenshots |
| [`valyu`](valyu/) | Search web + 36+ proprietary data sources (arXiv, PubMed, SEC filings, clinical trials, patents, financial data) via Valyu API |
| [`github-trending`](github-trending/) | Weekly top 10 trending GitHub repos, ranked by stars gained — vision-based extraction, English-only filter, formatted email report |
| [`contribscout`](contribscout/) | Discover open-source contribution opportunities — GitHub search, enrichment, and LLM analysis to find repos where you can create visible value before they get crowded |

### Automation & Publishing

| Skill | What it does |
|-------|-------------|
| [`weekly-blog`](weekly-blog/) | Automated research-to-blog pipeline — deep research → Obsidian → humanized blog post → publish via SSH/rsync |
| [`tech-news-digest`](tech-news-digest/) | Twice-weekly tech news digest — 5 categories, 3-round web search, multi-source synthesis, HTML email via AgentMail |
| [`fastmail-imap-newsletter-digest`](fastmail-imap-newsletter-digest/) | Read emails from Fastmail via IMAP, extract newsletter content, summarize via NanoGPT, deliver digest via AgentMail |
| [`concert-monitor`](concert-monitor/) | Weekly concert digest for any metro area — configurable venues, multi-platform search, email/Telegram/Discord delivery |
| [`new-music-digest`](new-music-digest/) | Weekly new releases for your Last.fm top artists — MusicBrainz dates + Deezer cover art/genres, HTML email with inline covers |
| [`deezer-playlist-creator`](deezer-playlist-creator/) | Create Deezer playlists from any query — similar artists, genre mixes, festival lineups. Three-tier pipeline: public API discovery → GQL search → playlist creation via ARL auth |
| [`here-now`](here-now/) | Publish any file or folder to a live URL instantly. Static hosting, anonymous (24h) or authenticated (permanent), custom domains |

### Learning & Education

| Skill | What it does |
|-------|-------------|
| [`teaching-workspace`](teaching-workspace/) | Stateful teaching system with a structured workspace — MISSION.md, lessons, reference docs, and learning records. Fluency vs storage strength, zone of proximal development, cross-session continuity |

### Travel

| Skill | What it does |
|-------|-------------|
| [`flight-tracker`](flight-tracker/) | Real-time flight tracking via AviationStack — status, gates, delays, baggage. Auto-discovers flights from forwarded booking emails; cron monitoring on travel days |
| [`travelogue`](travelogue/) | Log trip experiences into a structured Obsidian journal — text and photos via Discord/Telegram, daily entries with emoji sections, end-of-trip recaps |

### Software Development & Agent Workflows

| Skill | What it does |
|-------|-------------|
| [`session-handoff`](session-handoff/) | Compact a session into a structured handoff document for delegate_task subagents or cross-session continuity. State not instructions, capture the "why", reference don't duplicate |
| [`subagent-driven-development`](subagent-driven-development/) | Execute implementation plans via delegate_task subagents with 2-stage review (spec then quality). Includes the 5-part contract for autonomous loops with reward-hacking prohibition |
| [`hermes-agent-skill-authoring`](hermes-agent-skill-authoring/) | Author in-repo SKILL.md files — frontmatter validation, directory placement, design philosophy, anti-patterns, ship checklist, cross-ecosystem import, and pre-publish audit scripts |
| [`yolo-dev`](yolo-dev/) | Run AI coding agents on disposable repo clones. Clone → delegate → diff → review → apply. Optional container isolation (Podman/Docker). You're always the gatekeeper |

### Research

| Skill | What it does |
|-------|-------------|
| [`deep-research`](deep-research/) | Systematic 4-phase research methodology (broad exploration → deep dive → diversity validation → synthesis). Includes research-prompt construction, delegation patterns, MoA parallel decomposition, and wiki ingestion |

### Hermes Ecosystem

| Skill | What it does |
|-------|-------------|
| [`hermes-community-registry`](hermes-community-registry/) | Search, filter, evaluate, and install community skills/plugins/tools from the babylondreams.de registry — 490+ entries synced from Discord, bundled Python search script, evaluation checklist |

### Recommended External Skills

Skills not maintained here but worth installing alongside Hermes:

| Skill | What it does | Source |
|-------|-------------|--------|
| `last30days` | Multi-source "what are people saying about X" research across Reddit, X, YouTube, HN, TikTok, Polymarket, GitHub, and the web | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) |

## Quick Start

```bash
# Clone all skills
git clone https://github.com/jcrabapple/hermes-skills.git ~/.hermes/skills/custom/

# Or install just the job search toolkit
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/job-search ~/.hermes/skills/
```

Each skill's directory is self-contained with its own README and usage docs.

## How Skills Work in Hermes Agent

Hermes Agent discovers skills from `~/.hermes/skills/`. When an agent encounters a task matching a skill's domain, it loads the SKILL.md automatically — giving it expert-level instructions, code, and gotchas without manual prompting.

Skills are:

- **Reusable** — use the same skill across sessions and tasks
- **Composable** — load multiple skills for complex workflows
- **Versionable** — each skill is a directory tracked by git
- **Shareable** — drop a skill directory into any Hermes setup

## Contributing

PRs welcome! To add a skill:

1. Create a new directory with `SKILL.md` (see existing skills for format)
2. Include any scripts, templates, or references needed
3. Add an entry to this README
4. Submit a pull request

## License

MIT — use freely, share widely.
