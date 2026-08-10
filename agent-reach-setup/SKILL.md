---
name: agent-reach-setup
description: Scrape Instagram, LinkedIn, Reddit, YouTube via Agent Reach.
version: 1.0.0
---

# Agent Reach Setup

Agent Reach (Panniantong/Agent-Reach, v1.5.0) is installed via pipx as a free, open-source social media scraping layer for AI agents. It replaces several NanoGPT PAYG tools.

## Installation

```bash
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
```

**Critical for Fedora/Aurora:** `/home` is a symlink to `/var/home`. Always prefix commands with `HOME=/var/home/jason`:

```bash
HOME=/var/home/jason agent-reach <command>
```

## Currently Active Channels

| Channel | Backend | Status |
|---------|---------|--------|
| Instagram | OpenCLI (Chrome session) | ✅ Live |
| Reddit | OpenCLI (Chrome session) | ✅ Live |
| Facebook | OpenCLI (Chrome session) | ✅ Profiles work; search needs FB login |
| LinkedIn | mcp-server-linkedin (MCP) | ✅ Live, systemd service |
| YouTube | yt-dlp | ✅ Live |
| Web | Jina Reader | ✅ Live |
| Web Search | Exa via mcporter | ✅ Live |
| RSS | feedparser | ✅ Live |
| GitHub | gh CLI | ✅ Live |
| B站 | Search API | ✅ Live |
| V2EX | Public API | ✅ Live |
| Twitter/X | ❌ No account | twitter-cli installed but unusable |

## LinkedIn MCP Server

Installed via pipx: `mcp-server-linkedin` v4.21.0

**Critical:** Hermes sets `PYTHONPATH` to the gateway venv (Python 3.11), which breaks the pipx-installed mcp-server-linkedin (Python 3.14). Always unset:

```bash
PYTHONPATH= mcp-server-linkedin <args>
```

Runs as a systemd user service:
- Unit: `~/.config/systemd/user/linkedin-mcp.service`
- Port: 8001
- Profile: `~/.linkedin-mcp/profile/`
- Registered with mcporter: `linkedin http://localhost:8001/mcp`

### Available MCP tools (19)
`get_person_profile`, `search_people`, `get_company_profile`, `search_companies`, `get_company_employees`, `get_company_posts`, `search_jobs`, `get_job_details`, `get_saved_jobs`, `get_feed`, `search_posts`, `get_inbox`, `get_conversation`, `search_conversations`, `send_message`, `connect_with_person`, `get_sidebar_profiles`, `get_my_profile`, `close_session`

### Usage
```bash
HOME=/var/home/jason mcporter call linkedin.search_companies keywords="openai"
HOME=/var/home/jason mcporter call linkedin.get_person_profile linkedin_username="username"
HOME=/var/home/jason mcporter call linkedin.search_jobs keywords="software engineer" location="Remote"
```

## OpenCLI (Instagram, Reddit, Facebook)

OpenCLI v1.8.6 runs as a daemon on port 19825. Requires the Chrome extension from:
https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk

### Usage
```bash
HOME=/var/home/jason opencli instagram user nasa -f yaml
HOME=/var/home/jason opencli reddit search "query" -f yaml
HOME=/var/home/jason opencli facebook profile zuck -f yaml
```

## last30days Integration

Three bridge modules wire Agent Reach into the last30days research engine
as preferred (free) backends:

- `scripts/lib/reddit_agentreach.py` — replaces $0.11/search NanoGPT Reddit bridge
- `scripts/lib/instagram_agentreach.py` — adds keyword search (NanoGPT is profile-only)
- `scripts/lib/linkedin_agentreach.py` — new source type for professional context

Dispatch order (first available wins):
Reddit: Agent Reach → NanoGPT → public API
Instagram: Agent Reach → NanoGPT → ScrapeCreators
LinkedIn: Agent Reach only

All wired via `pipeline.available_sources()`, `reddit_public.search_reddit_public()`,
and `instagram.search_and_enrich()`.

| Platform | NanoGPT Cost | Agent Reach Cost |
|----------|-------------|-----------------|
| Instagram | ~$0.00 PAYG | Free |
| Reddit | ~$0.11 (broken tool) | Free (works) |
| YouTube | $0.01/video | Free |
| Web Search | $0.006/search | Free (Exa) |
| LinkedIn | Not available | Free |

NanoGPT still owns: TikTok, Google Maps, embeddings, reranking, image gen/edit, TTS/STT, translation.

## Pitfalls

- **HOME symlink:** Always `HOME=/var/home/jason` on Aurora
- **PYTHONPATH pollution:** Always `PYTHONPATH=` for mcp-server-linkedin
- **Doctor doesn't probe live:** `agent-reach doctor` shows `warn` for OpenCLI channels even when they work. Test with actual commands.
- **Facebook search:** Returns `[]` unless logged into facebook.com in Chrome
- **Twitter:** Useless without an X.com account for cookie export
- **mcp-server-linkedin login:** Opens Wayland-native Chromium cua-driver can't capture. Log in manually.
