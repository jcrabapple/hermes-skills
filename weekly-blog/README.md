# Weekly Blog Automation

Automated research-to-blog pipeline for [Hermes Agent](https://hermes-agent.nousresearch.com). Picks a random topic, runs deep research, saves to Obsidian, writes a blog post, humanizes it, generates a header image, and publishes via SSH/rsync.

## Features

- **Fully automated**: runs on a cron schedule with no user prompting
- **Research-backed**: uses deep-research skill for multi-source investigation
- **Obsidian integration**: saves research reports to your vault
- **Anti-AI writing**: mandatory humanizer pass strips AI patterns from posts
- **Header images**: generates relevant images via FAL/image gen
- **Topic dedup**: cross-references live blog feed to prevent repeats
- **Self-healing**: pipeline continues even if individual steps fail
- **Configurable**: works with prose.sh, personal servers, or any SSH host

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com) installed and running
- A blog host that accepts SSH/rsync (e.g. [prose.sh](https://prose.sh), a personal VPS)
- Obsidian vault (optional — for saving research reports)
- `rsync` installed locally

## Quick Start

### 1. Set up a blog host

**prose.sh** (free, zero-config):
```bash
# Sign up at https://prose.sh — your username becomes your blog URL
# Test it:
echo "# Hello World" | ssh prose.sh
# Visit: https://yourusername.prose.sh/hello-world
```

**Personal server** (any SSH-accessible host):
```bash
# Ensure rsync works
rsync -vr test.md user@yourserver:/var/www/blog/
```

### 2. Install the skill

```bash
git clone https://github.com/jcrabapple/hermes-skills.git /tmp/hermes-skills
cp -r /tmp/hermes-skills/weekly-blog ~/.hermes/skills/automation/weekly-blog
rm -rf /tmp/hermes-skills
```

### 3. Configure

```bash
cd ~/.hermes/skills/automation/weekly-blog
cp config.example.yaml config.yaml
```

Edit `config.yaml`:
```yaml
blog_name: "My Blog"
blog_url: "https://yourusername.prose.sh"
blog_ssh_target: "prose.sh:/"
obsidian_vault_path: "~/Documents/Obsidian Vault"
schedule: "0 10 * * 1,3,5"  # MWF at 10am
```

### 4. Create a topic pool

```bash
cat > ~/.hermes/skills/automation/weekly-blog/topic_pool.txt << 'EOF'
How CRISPR gene editing is being used beyond agriculture
The engineering challenge of building a fusion reactor
How noise-canceling headphones actually work
The science behind solid-state batteries
How satellite internet actually works
The biology of telomere extension and aging research
EOF
```

Add as many topics as you want — one per line. The agent picks randomly and removes them after publishing.

### 5. Set up the cron job

From within Hermes:

> "Load the weekly-blog skill and set up a cron job to run the automated blog pipeline on MWF at 10am."

Or manually:
```bash
hermes cron add --name "weekly-blog" \
  --schedule "0 10 * * 1,3,5" \
  --skills weekly-blog deep-research humanizer \
  --prompt "Load the weekly-blog skill. Read config.yaml. Run the full pipeline: pick a topic, deep research, save to Obsidian, write blog post, humanize, generate header image, publish via rsync, verify it's live, update state files."
```

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│ Topic Pool  │────▶│ Deep Research│────▶│   Obsidian   │
│ (random pick)│     │ (multi-source)│     │ (save report)│
└─────────────┘     └──────────────┘     └──────────────┘
                                                │
┌─────────────┐     ┌──────────────┐     ┌──────▼───────┐
│   Verify    │◀────│   Publish    │◀────│  Blog Post   │
│  (curl check)│     │ (rsync/SSH)  │     │ (humanized)  │
└─────────────┘     └──────────────┘     └──────────────┘
```

## State Files

The pipeline maintains several files in the skill directory:

| File | Purpose |
|------|---------|
| `topic_pool.txt` | Curated topic list (one per line) |
| `recent_topics.txt` | Last 50 posts: `Title \| slug \| date` |
| `published_slugs.txt` | All known blog slugs (synced from RSS) |
| `last_post_title.txt` | Most recent post title + URL |

## Blog Post Format

Posts follow this structure (compatible with most static blog platforms):

```markdown
# Engaging Title Here

*May 12, 2026 · Tags: science, technology, research*

One compelling sentence about why this matters.

---

## First Section

Content with 3-4 sentences and a key detail.

---

## Second Section

More content.

---

## Why This Matters

1-2 paragraph conclusion.
```

**Rules:**
- `# Title` as first line (becomes the page title)
- Italic date/tag line after
- `---` between sections
- No YAML frontmatter (rendered as raw text on many platforms)
- Plain English, no em-dashes

## Pitfalls

See the full SKILL.md for the complete pitfalls section. Key ones:

- **Never use generic slugs** — the filename becomes the URL
- **Always deduplicate topics** against the live blog feed, not just local files
- **Pipeline continues even if steps fail** — a published imperfect post beats a silent failure
- **Verify every post is live** with curl — don't trust "ok" status alone
- **Use `write_file` not `echo >>`** for state files (security scans block terminal writes in cron)

## Customization

### Publishing to a different platform

The pipeline uses rsync over SSH. Any host that supports this works:

```yaml
# prose.sh
blog_ssh_target: "prose.sh:/"

# Personal server
blog_ssh_target: "user@server:/var/www/blog/"

# GitHub Pages (via gh-pages branch)
# You'd need to modify the publish step to git push instead of rsync
```

### Adjusting post frequency

Change the cron schedule in config.yaml:

```yaml
# Weekly (Mondays)
schedule: "0 10 * * 1"

# Twice weekly (Tue/Fri)
schedule: "0 10 * * 2,5"

# Daily
schedule: "0 10 * * *"
```

### Adding topics automatically

Pull trending topics from any source and append to `topic_pool.txt`. Example with Monid:

```bash
~/.local/bin/monid trending --limit 10 --topic technology >> topic_pool.txt
```

## License

MIT

## Using with Hermes Agent

```bash
# Install
git clone https://github.com/jcrabapple/hermes-skills.git /tmp/hermes-skills
cp -r /tmp/hermes-skills/weekly-blog ~/.hermes/skills/automation/weekly-blog
rm -rf /tmp/hermes-skills

# Configure
cp ~/.hermes/skills/automation/weekly-blog/config.example.yaml \
   ~/.hermes/skills/automation/weekly-blog/config.yaml
# Edit config.yaml with your blog details
```

Once installed, Hermes loads the skill when blogging is mentioned. Example prompts:

> "Load the weekly-blog skill and publish today's post."
> "Add 'the future of quantum computing' to my blog topic pool."
> "What topics have been published recently?"
