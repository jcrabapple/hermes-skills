# Research → Obsidian → Blog Pipeline

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

Read 1-2 recent posts to match the user's established voice. Then write the post using your blog platform's conventions.

### Blog Post Conventions (generic)

- H1 title (punchy, specific, becomes page title)
- Italic date/tag line: `*Month DD, YYYY · Tags: tag1, tag2, tag3*`
- Conversational-but-substantive tone — real data, specific numbers, named sources
- Each section starts with something concrete (fact, data point, scene)
- Sections build a narrative or argument, each adding something new
- Real-citation Sources block at the end with numbered list and URLs

### Slug Style

Hyphenated descriptive phrase. Examples:
- `finland-sand-battery-survived-winter`
- `crow-funerals-are-not-what-you-think`

### Publish

Use your blog platform's publish method (rsync to a blog host, CLI tool, API, etc.). Verify publication by fetching the live URL and checking for expected content.

### Verification

**Primary**: Fetch the live page URL and check for expected content (title, headings). Do not rely on file stat commands — verify the rendered page is actually live.

## Step 4: Share to Social Media

Compose a short, punchy social media post:
- Start with relevant emoji
- Punchy hook first line
- Key finding or dramatic fact in 2-3 lines
- Blog post link
- 2-3 relevant hashtags
- No emdashes, no markdown, no source URLs in body
- Respect character limits for the target platform

Always dry-run social media posts before publishing for real. Use a helper script if available, or the platform's API directly.

## Pipeline Summary

1. Research (4-phase, batched parallel searches, `web_extract` for summaries)
2. Save to Obsidian (`$VAULT/Research/YYYY-MM-DD-slug.md`)
3. Read 1-2 recent blog posts for voice → write blog → publish → verify
4. Compose social media post → dry-run → post → capture URL

## Pitfalls

- **Don't skip reading existing blog posts for voice.** Match the user's established style: concrete opening hook, sections with real data, Sources block.
- **Don't use `nanogpt_web_extract` for Wikipedia.** It returns 100KB+ of raw wikitext. Use `web_extract` which returns a clean ~5000-char structured summary.
- **Always dry-run social media posts first.** Check character count and formatting before posting for real.
