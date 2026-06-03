# here.now

Publish files and folders to the web instantly. Static hosting for HTML sites, images, PDFs, and any file type. Outputs a live, shareable URL at `{slug}.here.now`.

## What it does

- **Single file → rich auto-viewer** (image, PDF, video, audio)
- **Folder with `index.html` → static site**
- **Folder without `index.html` → directory listing with image gallery**
- **Anonymous mode (24h expiry)** or **authenticated (permanent)**
- **Incremental updates** with SHA-256 file hashing
- **Custom domains**, handles (`yourname.here.now`), and payment gating built in

## Quick start

```bash
# Anonymous — site lives 24h, you can claim it after
./scripts/publish.sh ./my-site.html

# Authenticated — permanent site
echo "your-api-key" > ~/.herenow/credentials
./scripts/publish.sh ./my-site/

# Update an existing site
./scripts/publish.sh ./my-site/ --slug bright-canvas-a7k2
```

The script handles the three-step publish flow (create → upload → finalize) and saves state to `.herenow/state.json` for follow-up updates.

## Setup

### Required tools

- `curl`, `file`, `jq` — the script needs all three (no Python, no Node)
- `jq` is the only one that's sometimes missing; the skill ships a bundled copy at `bin/jq` for environments where `jq` isn't installed

### Getting an API key (optional, for permanent sites)

1. The script can run the entire sign-up flow without leaving the agent:
   ```bash
   curl -sS https://here.now/api/auth/agent/request-code \
     -H "content-type: application/json" \
     -d '{"email": "you@example.com"}'
   ```
2. The user pastes the code from their inbox
3. Verify the code, receive the API key, save it to `~/.herenow/credentials`

Or sign up at [here.now](https://here.now) and copy the key from the dashboard.

## Install

```bash
# Recommended — official installer (keeps the skill updated):
npx skills add heredotnow/skill --skill here-now -g

# Or pin to a specific version by copying from this repo:
git clone https://github.com/jcrabapple/hermes-skills.git
cp -r hermes-skills/here-now ~/.hermes/skills/
```

## Limits

|                | Anonymous          | Authenticated                |
| -------------- | ------------------ | ---------------------------- |
| Max file size  | 250 MB             | 5 GB                         |
| Expiry         | 24 hours           | Permanent (or custom TTL)    |
| Rate limit     | 5 / hour / IP      | 60 / hour free, 200 / hour hobby |

Anonymous sites can be **claimed** (transferred to an authenticated account) within 24 hours. The claim URL is returned only once — save it immediately.

## Beyond the publish script

The script covers create / update / claim. For the full API surface (delete, password protection, payment gating, custom domains, handles, links, metadata patching, listing), see [references/REFERENCE.md](./references/REFERENCE.md).

## Common use cases

- Share a single HTML report with someone via a one-line URL
- Publish a generated dashboard that auto-updates on a cron
- Quick file hosting for screenshots, PDFs, videos
- Throwaway sites for demos, prototypes, landing pages
- Payment-gated content (stablecoin via Tempo network)
- Password-protected private sharing

## See also

- [here.now docs](https://here.now/docs) — full API reference
- [pico-sh](../pico-sh/) — alternative SSH-based static hosting
