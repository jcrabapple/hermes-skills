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
| [`nanogpt-tiktok`](nanogpt-tiktok/) | Scrape TikTok hashtags, profiles, keyword searches, and video URLs with ASR transcripts via NanoGPT API |
| [`nanogpt-instagram`](nanogpt-instagram/) | Scrape Instagram posts (captions, metrics, media, comments) via NanoGPT API |
| [`nanogpt-linkedin`](nanogpt-linkedin/) | Scrape LinkedIn profile data (name, title, company, email, education) via NanoGPT API |

### Research & Information

| Skill | What it does |
|-------|-------------|
| [`valyu`](valyu/) | Search web + 36+ proprietary data sources (arXiv, PubMed, SEC filings, clinical trials, patents, financial data) via Valyu API |
| [`github-trending`](github-trending/) | Weekly top 10 trending GitHub repos, ranked by stars gained — vision-based extraction, English-only filter, formatted email report |
| [`contribscout`](contribscout/) | Discover open-source contribution opportunities — GitHub search, enrichment, and LLM analysis to find repos where you can create visible value before they get crowded |

### Automation & Publishing

| Skill | What it does |
|-------|-------------|
| [`concert-monitor`](concert-monitor/) | Weekly concert digest for any metro area — configurable venues, multi-platform search, email/Telegram/Discord delivery |
| [`weekly-blog`](weekly-blog/) | Automated research-to-blog pipeline — deep research → Obsidian → humanized blog post → publish via SSH/rsync |
| [`tech-news-digest`](tech-news-digest/) | Twice-weekly tech news digest — 5 categories, 3-round web search, multi-source synthesis, HTML email via AgentMail |
| [`new-music-digest`](new-music-digest/) | Weekly new releases for your Last.fm top artists — MusicBrainz dates + Deezer cover art/genres, HTML email with inline covers |
| [`here-now`](here-now/) | Publish any file or folder to a live URL instantly. Static hosting, anonymous (24h) or authenticated (permanent), custom domains |

### Travel

| Skill | What it does |
|-------|-------------|
| [`flight-tracker`](flight-tracker/) | Real-time flight tracking via AviationStack — status, gates, delays, baggage. Auto-discovers flights from forwarded booking emails; cron monitoring on travel days |
| [`travelogue`](travelogue/) | Log trip experiences into a structured Obsidian journal — text and photos via Discord/Telegram, daily entries with emoji sections, end-of-trip recaps |

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