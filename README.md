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

| Skill | What it does |
|-------|-------------|
| [`nanogpt-tiktok`](nanogpt-tiktok/) | Scrape TikTok hashtags, profiles, keyword searches, and video URLs with ASR transcripts via NanoGPT API |
| [`nanogpt-instagram`](nanogpt-instagram/) | Scrape Instagram posts (captions, metrics, media, comments) via NanoGPT API |
| [`nanogpt-linkedin`](nanogpt-linkedin/) | Scrape LinkedIn profile data (name, title, company, email, education) via NanoGPT API |
| [`concert-monitor`](concert-monitor/) | Weekly concert digest for any metro area — configurable venues, multi-platform search, email/Telegram/Discord delivery |
| [`weekly-blog`](weekly-blog/) | Automated research-to-blog pipeline — deep research → Obsidian → humanized blog post → publish via SSH/rsync |

*More skills coming — PRs welcome.*

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

## License

MIT — use freely, share widely.
