# Research → Obsidian → Blog → Mastodon Pipeline

Full end-to-end workflow for researching any topic and publishing the results. For TikTok fact-checking specifically, see [tiktok-blog-pipeline.md](tiktok-blog-pipeline.md) which adds a scraping step.

## Step 1: Deep Research

Conduct 4-phase research (broad exploration, deep dive, diversity validation, synthesis) using the methodology in the main SKILL.md.

### Search Strategy

- **Batch Phase 1 searches**: Run 3 broad searches in parallel (different dimensions of the topic)
- **Batch Phase 2 searches**: Run 2-3 targeted searches per dimension in parallel
- **Use `web_extract` for Wikipedia and large pages**: It summarizes to ~5000 chars/page, returning structured key facts as clean markdown. Reserve `nanogpt_web_extract` for when you need raw full content from non-Wikipedia sources (news articles, opinion pieces, niche sites).
- **`nanogpt_web_extract` large output**: When extracting 3+ URLs, output can exceed 100KB and gets persisted to `/tmp/hermes-results/`. Use `read_file` with offset/limit to access sections. Prefer `web_extract` (summarized) or extract 1-2 URLs at a time with `nanogpt_web_extract`.
- **Depth**: Use `depth='standard'` for `nanogpt_web_search`. Deep depth hits 30s timeouts frequently.

### Dimensions to Cover

For a general research topic (not a fact-check), explore:
1. Core facts, statistics, physical characteristics
2. Biodiversity / ecology / scientific significance
3. Geology / formation / how it works
4. Climate change impacts and environmental threats
5. Cultural significance and indigenous perspectives
6. Conservation status and governance
7. Current events and recent developments

## Step 2: Save to Obsidian

Save the full research report to:
```
$VAULT/Research/YYYY-MM-DD-topic-slug.md
```

Include:
- Summary paragraph
- Key data tables (statistics, comparisons)
- All dimensions with detailed findings
- Full sources list with URLs
- Synthesis section explaining why the topic matters

## Step 3: Write Blog Post

Read 1-2 recent posts from `~/blog/` to match Jason's established voice. Then write the post to `~/blog/slug.md`.

### Blog Post Conventions (prose.sh)

- H1 title (punchy, specific, becomes page title) — no YAML frontmatter
- Italic date/tag line: `*Month DD, YYYY · Tags: tag1, tag2, tag3*`
- Conversational-but-substantive tone — real data, specific numbers, named sources
- Each section starts with something concrete (fact, data point, scene)
- Sections build a narrative or argument, each adding something new
- Real-citation Sources block at the end with numbered list and URLs
- Single em-dashes for dramatic pause are fine; avoid bracketed asides with em-dashes

### Slug Style

Hyphenated descriptive phrase. Examples from the archive:
- `finland-sand-battery-survived-winter`
- `crow-funerals-are-not-what-you-think`
- `lake-baikal-is-dying-the-way-ancient-things-die`

### Publish

```bash
SLUG="your-slug"
cp ~/blog/${SLUG}.md /tmp/${SLUG}.md
rsync -vr --force --no-compress /tmp/${SLUG}.md prose.sh:/${SLUG}.md
sleep 2 && curl -sf "https://hermez.prose.sh/${SLUG}" | grep -o '<h1[^>]*>[^<]*</h1>' | head -1 && echo "LIVE"
```

### Verification

**Primary**: `curl -sf "https://hermez.prose.sh/${SLUG}"` — fetch the live page and check for expected content.

**Note**: `ssh prose.sh stat -c '%s' /slug.md` may fail with "invalid file, format must be (.md,...)" even when the file exists and the page is live. This appears to be a prose.sh restricted-shell issue. Do not rely on `stat` as the sole verification — always use `curl`.

## Step 4: Post to Mastodon

Compose a short, punchy Mastodon post:
- Start with relevant emoji
- Punchy hook first line
- Key finding or dramatic fact in 2-3 lines
- Blog post link
- 2-3 relevant hashtags
- No emdashes, no markdown, no source URLs in body
- Must be ≤ 1989 chars (URLs count as 23 each)

**Always use the helper script** — never try multiline curl with emoji:
```bash
python3 ~/.hermes/skills/social-media/mastodon/scripts/mastodon_post.py --status "Post text here" --dry-run  # preview first
python3 ~/.hermes/skills/social-media/mastodon/scripts/mastodon_post.py --status "Post text here"
```

## Pipeline Summary

1. Research (4-phase, batched parallel searches, `web_extract` for summaries)
2. Save to Obsidian (`$VAULT/Research/YYYY-MM-DD-slug.md`)
3. Read 1-2 recent blog posts for voice → write blog → rsync to prose.sh → verify with curl
4. Compose Mastodon post → dry-run → post → capture URL

## Pitfalls

- **Don't skip reading existing blog posts for voice.** Jason's blog has a distinctive style: concrete opening hook, sections with real data, Sources block. Match it.
- **Don't use `nanogpt_web_extract` for Wikipedia.** It returns 100KB+ of raw wikitext. Use `web_extract` which returns a clean ~5000-char structured summary.
- **Don't rely on `ssh prose.sh stat` for verification.** Use `curl -sf https://hermez.prose.sh/slug` instead.
- **Always `--dry-run` Mastodon posts first.** Check character count and formatting before posting for real.
