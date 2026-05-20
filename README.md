# Hermes Skills 🧠⚡

**Reusable skills and tools for [Hermes Agent](https://hermes-agent.nousresearch.com) — your AI's procedural memory.**

Hermes Agent is an open-source AI assistant framework that can use tools, run code, and persist context across sessions. This repo is a collection of **skills**: packaged expertise that gives Hermes domain-specific capabilities on demand.

## What is a Skill?

A skill is a reusable knowledge module — the AI equivalent of a plugin. Each skill includes:

- **SKILL.md** — structured instructions with when-to-use/not-use guidance, exact commands, workflows, and common pitfalls
- **Scripts** — CLI tools or Python code the agent executes
- **References** — API docs, config templates, and supporting material

When you ask Hermes to do something, it scans its available skills and loads the relevant ones. A skilled agent doesn't just answer — it has a battle-tested playbook for that specific task.

## Skills in This Repo

### Resume & Career Development

| Skill | What it does |
|-------|-------------|
| [`resume-workflow-orchestrator`](resume-workflow-orchestrator/) | Meta-skill that routes to the right resume skill and chains workflows together |
| [`tailored-resume-generator`](tailored-resume-generator/) | Analyzes job descriptions and generates tailored resumes with DOCX conversion |
| [`job-description-analyzer`](job-description-analyzer/) | Analyze job postings, calculate match scores, identify gaps, create application strategy |
| [`cover-letter-generator`](cover-letter-generator/) | Create personalized, compelling cover letters from resume + job description |
| [`resume-ats-optimizer`](resume-ats-optimizer/) | Optimize resumes for Applicant Tracking Systems, check ATS compatibility, analyze keyword match |
| [`resume-bullet-writer`](resume-bullet-writer/) | Transform weak bullets into achievement-focused statements with metrics and impact |
| [`resume-quantifier`](resume-quantifier/) | Find opportunities to add metrics and estimate numbers when exact data unavailable |
| [`resume-formatter`](resume-formatter/) | Ensure ATS-friendly formatting and create clean, scannable layouts |
| [`tech-resume-optimizer`](tech-resume-optimizer/) | Optimize resumes for software engineering, PM, and technical roles |
| [`career-changer-translator`](career-changer-translator/) | Translate skills from one industry to another, identify transferable skills |
| [`executive-resume-writer`](executive-resume-writer/) | Create C-suite and VP level resumes emphasizing strategic leadership |
| [`academic-cv-builder`](academic-cv-builder/) | Format CVs for academic positions with publications, grants, teaching |
| [`creative-portfolio-resume`](creative-portfolio-resume/) | Balance visual design with ATS compatibility for creative roles |
| [`resume-section-builder`](resume-section-builder/) | Create targeted sections optimized for different experience levels and roles |

### Supporting Career Skills

| Skill | What it does |
|-------|-------------|
| [`salary-negotiation-prep`](salary-negotiation-prep/) | Research market rates, build negotiation strategy, create counter-offer scripts |
| [`interview-prep-generator`](interview-prep-generator/) | Generate STAR stories, practice questions, talking points from resume |
| [`offer-comparison-analyzer`](offer-comparison-analyzer/) | Compare multiple job offers side-by-side with total compensation analysis |
| [`resume-version-manager`](resume-version-manager/) | Track different resume versions, maintain master resume, manage tailored versions |
| [`portfolio-case-study-writer`](portfolio-case-study-writer/) | Transform resume bullets into detailed portfolio case studies |
| [`reference-list-builder`](reference-list-builder/) | Format professional references properly and prepare reference materials |
| [`linkedin-profile-optimizer`](linkedin-profile-optimizer/) | Sync resume with LinkedIn, optimize for searchability and engagement |

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

### Automation & Publishing

| Skill | What it does |
|-------|-------------|
| [`concert-monitor`](concert-monitor/) | Weekly concert digest for any metro area — configurable venues, multi-platform search, email/Telegram/Discord delivery |
| [`weekly-blog`](weekly-blog/) | Automated research-to-blog pipeline — deep research → Obsidian → humanized blog post → publish via SSH/rsync |

## Quick Start

```bash
# Clone the skills
git clone https://github.com/jcrabapple/hermes-skills.git ~/.hermes/skills/custom/

# Or install individual skills from within Hermes
# /skill add jcrabapple/hermes-skills/nanogpt-tiktok
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