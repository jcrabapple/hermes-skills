# TikTok → Research → Blog Pipeline

Full end-to-end workflow for fact-checking TikTok videos and publishing the results.

## Step 0: Get the Correct Video Content

**Always use the CLI scraper, NOT the browser.** TikTok pages mix the target video with recommended/fed content — the browser shows both and it's easy to grab the wrong description.

```bash
# Use the nanogpt-tiktok skill's CLI scraper if available
cd ~/.hermes/skills/social-media/nanogpt-tiktok/scripts
python3 scrape_tiktok.py --urls "https://www.tiktok.com/t/Zxxx/" --results 1
```

The scraper resolves short links (`/t/Zxxx/`) to canonical URLs and returns correct metadata: creator, description, hashtags, engagement metrics. The built-in `nanogpt_tiktok_scraper` tool throws 400s on short URLs — always use the CLI.

Extract from the response:
- Video description/caption (`text` field)
- Creator handle and display name
- Hashtags
- Engagement (likes, views, comments, shares)

## Step 1: Deep Research

Delegate to a subagent with the `deep-research` skill. Structure the research dimensions around **specific claims made in the video**, not just the general topic. Each claim should get a verdict.

Goal prompt template:
```
Deep research on [TOPIC], inspired by a TikTok video from @[CREATOR] that claims "[CLAIM]".

Explore these dimensions:
1. [Claim 1] — evidence for and against
2. [Claim 2] — evidence for and against
3. [How the technology actually works] — real science
4. [Performance/efficiency numbers] — real data
5. [Current state of development] — TRL, commercialization
6. [Criticisms and limitations] — expert perspectives
7. [Context] — where this fits in the broader landscape

Return a comprehensive research report with verdicts on each claim.
Print all findings to stdout. Do not save to files.
```

## Step 2: Save to Obsidian

Save the full research report (with all sources, data tables, and claim verdicts) to:
```
$VAULT/Research/YYYY-MM-DD-topic-slug.md
```

Use the Obsidian skill conventions. Include:
- Summary with overall verdict
- All dimensions with data
- TikTok claim analysis table (claim → verdict → explanation)
- Full sources list

## Step 3: Write Blog Post

Read 1-2 recent posts to match tone and structure. Then write the post using your blog platform's conventions.

**Blog post conventions (generic):**
- H1 title (becomes page title)
- Italic date/tag line: `*Month DD, YYYY · Tags: tag1, tag2, tag3*`
- Conversational but substantive tone
- Real citations with sources at the end (Sources block)
- For fact-checks: structure around specific claims with verdicts

**Publish:**
Use your blog platform's publish method (rsync to a blog host, CLI tool, API, etc.). Verify publication by fetching the live URL.

## Step 4: Share to Social Media

Compose a short, punchy social media post:
- Start with relevant emoji
- Punchy hook first line
- Key finding or verdict in 2-3 lines
- Blog post link
- 2-3 relevant hashtags
- No emdashes, no markdown, no source URLs in body
- Respect character limits for the target platform

Use a helper script or the platform's API for anything beyond a simple single-line post.

## Pitfalls

- **Never use browser_navigate for TikTok.** The page mixes target video with recommended content. Use the CLI scraper.
- **The `nanogpt_tiktok_scraper` built-in tool returns 400s on short URLs.** Always use `scripts/scrape_tiktok.py` CLI.
- **Fact-check structure matters.** Don't just research the topic — research the specific claims. The blog post should have clear verdicts.
- **Read existing blog posts first.** Match the established voice: italic date/tag line, conversational-but-substantive, real-citation Sources block at the end.
