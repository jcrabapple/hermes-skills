---
name: tiktok-research
description: "When the user shares a TikTok URL, load this skill FIRST — before any tool calls. End-to-end workflow: scrape the URL, extract transcript, research claims, save to Obsidian, blog, and share to Mastodon. CRITICAL: Do NOT attempt nanogpt_tiktok_scraper, web_extract, or browser tools first — they all fail on TikTok URLs. The skill's CLI path is the only reliable scraper."
---

# TikTok Research Workflow

When the user shares a TikTok URL, follow this workflow to scrape, transcribe, research, and optionally save/blog the results.

## Overview

1. **Scrape & Transcribe** — Use `nanogpt-tiktok` skill to get video metadata and full ASR transcript
2. **Understand** — Read the transcript + video description to identify core topics and claims
3. **Deep Research** — Fact-check claims via parallel subagents or `web_search`; verify sources, note caveats
4. **Save to Obsidian** (ask first) — Comprehensive research note with full transcript, source links, creator profile
5. **Blog** (ask first) — Engaging summary post on prose.sh with the full transcript embedded
6. **Share to Mastodon** (ask first) — Punchy summary post with blog link, following Mastodon formatting rules
7. **Ingest into LLM Wiki** (if exists) — Entity/concept pages with cross-links and raw source archival

## Useful References

- `references/tiktoklink-vtt-discovery.md` — Technical details on how `subtitleLinks[].tiktokLink` serves WebVTT content from TikTok's CDN
- `references/misattribution-patterns.md` — Common viral science misattributions with real source numbers and the pattern to watch for. Includes ten patterns: institution misattribution, cross-contamination, benchmark inflation, ASR number mangling, research program conflation, metric confusion (AUC ≠ accuracy), pretraining-vs-labeled-data conflation, company-claimed performance numbers + thermal-vs-electrical energy conflation, organization mischaracterization (agency vs company), and sea ice vs land ice conflation.

## Prerequisites

- `nanogpt-tiktok` skill (social-media) — scraping + transcript via `tiktokLink`
- `obsidian` skill (note-taking) — saving research
- `pico-sh` skill (home-lab) — blog posting
- `mastodon` skill (social-media) — sharing to dmv.community
- `llm-wiki` skill (research) — wiki ingestion (optional)
- `web_search` tool — fallback research / fact-checking
- `~/.hermes/scripts/fusion_query.py` — OpenRouter Fusion research (primary research method)
- `~/.hermes/secrets/openrouter_api_key` — API key for Fusion
- NanoGPT API key in `~/.config/nanogpt/.env`

## Workflow Steps

### 0. Ask what the user wants first

Before proceeding past the scrape, clarify scope: "Want me to go deep on this? I can research it, save to Obsidian, and blog about it."

### 1. Scrape & Transcribe

**Preferred path — use the CLI:**
```bash
export $(grep NANOGPT_API_KEY ~/.config/nanogpt/.env | xargs)
cd ~/.hermes/skills/social-media/nanogpt-tiktok

# Full scrape + transcript (do NOT use --raw if using --show-transcript)
python3 scripts/scrape_tiktok.py --urls "<TIKTOK_URL>" --show-transcript \
  --output /tmp/tiktok_${TOPIC_SLUG}.json
```

**Fallback path (manual VTT fetch) — only when the saved JSON's transcript is genuinely empty/missing or you suspect the API returned a stale version:**

```bash
export $(grep NANOGPT_API_KEY ~/.config/nanogpt/.env | xargs)
cd ~/.hermes/skills/social-media/nanogpt-tiktok

# Scrape with raw JSON output
python3 scripts/scrape_tiktok.py --urls "<TIKTOK_URL>" --raw \
  --output /tmp/tiktok_${TOPIC_SLUG}.json

# Then manually fetch the VTT from tiktokLink
curl -s "$(python3 -c "import json; d=json.load(open('/tmp/tiktok_${TOPIC_SLUG}.json')); print(d['items'][0]['videoMeta']['subtitleLinks'][0]['tiktokLink'])")" \
  > /tmp/tiktok_${TOPIC_SLUG}.vtt
# Extract clean text
python3 -c "
import sys, re
lines = [l.strip() for l in open('/tmp/tiktok_${TOPIC_SLUG}.vtt').read().split('\n')
         if l.strip() and not l.startswith('WEBVTT') and '-->' not in l
         and not re.match(r'^\d{2}:\d{2}', l)]
print(' '.join(lines))
" > /tmp/tiktok_${TOPIC_SLUG}_transcript.txt
```

**Note on flags:** `--raw` and `--show-transcript` are mutually exclusive at the CLI, but you rarely need both. The `--show-transcript` call **saves the full raw JSON response to the output file** — display text, caption, metadata, and `subtitleLinks[].tiktokLink` are all in `/tmp/tiktok_${TOPIC_SLUG}.json`. Re-run with `--raw` only if the first call failed or returned no data. The manual VTT fetch (below) is for recovering transcripts the API response truncated, NOT for getting the raw JSON.

**Extract from response:**
- `items[0].text` — caption
- `items[0].webVideoUrl` — canonical URL
- `items[0].videoMeta.subtitleLinks[0].tiktokLink` — fetch immediately for VTT
- `items[0].authorMeta.name` — username (e.g. `astro_alexandra`)
- `items[0].authorMeta.nickName` — display name (e.g. `ASTRO ALEXANDRA 🪐`)
- `items[0].authorMeta.fans` — follower count (**not** `followers`)
- `items[0].authorMeta.following` — following count
- `items[0].authorMeta.verified` — verification status
- `items[0].diggCount, playCount, commentCount, shareCount, collectCount` — engagement
- `items[0].hashtags` — tags (list of `{name, ...}` dicts)
- `items[0].musicMeta` — soundtrack
- `items[0].videoMeta.duration` — duration in seconds

**Get the transcript:**
```python
import urllib.request, re, json
vtt_url = data["items"][0]["videoMeta"]["subtitleLinks"][0]["tiktokLink"]
vtt = urllib.request.urlopen(vtt_url).read().decode("utf-8")
lines = [l.strip() for l in vtt.split("\n") if l.strip() and
         not l.startswith("WEBVTT") and "-->" not in l
         and not re.match(r"^\d{2}:\d{2}", l)]
transcript = " ".join(lines)
```

### 2. Understand & Identify Claims

Read the full transcript + caption. Extract:
- **Core subject** — what is this actually about?
- **Specific claims** — factual assertions that can be verified
  - **⚠️ Flag obviously-wrong numbers immediately** — if a transcript claim seems nonsensical ("nothing comparable for 14 years" about a 2,000-year-old artifact), it's almost certainly an ASR number-mangling artifact. Tell the user "the transcript reads X but the creator likely said Y" rather than assuming the creator is wrong. This applies especially to round numbers, centuries, dates, and large counts.
  - **⚠️ Flag performance percentages in medical/AI claims** — "93% accuracy" is often AUC or sensitivity mislabeled as accuracy. Note this as a research question: "is this number actually accuracy, or is it AUC/sensitivity?" This is the most common metric confusion in health-tech TikToks.
  - **⚠️ Flag "trained on N images" claims** — N may be unlabeled pretraining data, not disease-specific training data. Note as a research question: "were these labeled or unlabeled images?"
- **Relative time references** — "next year," "last month," "just announced," "recently" — these must be anchored to the video's `createTime` before fact-checking
- **Named entities** — people, organizations, studies referenced
  - **⚠️ Flag organization mischaracterization** — a creator may call a government agency a "company," a university research lab a "startup," or a publicly funded program a "private venture." This is not ASR error — the creator said it — but it misrepresents the nature of the work. When a transcript names an organization, verify whether it's a government agency, public body, private company, university, or nonprofit. See `references/misattribution-patterns.md` for the "organization mischaracterization" pattern.
  - **⚠️ Flag sea ice vs land ice conflation in climate claims** — "melting polar ice caps raise sea levels" is a common misconception. Arctic sea ice is already floating in the ocean, so it contributes only ~2.6% additional volume when melted (NSIDC). The real drivers of sea level rise are land ice (Greenland, Antarctic ice sheets, glaciers) and thermal expansion. When a climate TikTok says ice melt → sea level rise, check whether they're talking about sea ice or land ice. See `references/misattribution-patterns.md` for the "sea ice vs land ice conflation" pattern.
- **The creator's angle** — their perspective/argument/narrative

### 3. Deep Research (Fusion-First Fact-Checking)

**Preferred: OpenRouter Fusion** — Use the Fusion API for multi-model deliberated research. Fusion runs a panel of models in parallel with web search, then a judge synthesizes consensus, contradictions, unique insights, and blind spots into one comprehensive answer. This is significantly better than sequential web_search calls for complex or multi-faceted claims.

Run Fusion via the helper script:

```bash
python3 ~/.hermes/scripts/fusion_query.py "Research and fact-check the following claims from a video transcript. For each claim, provide: verification status (verified/directionally correct/misleading/wrong), the real facts with sources, and any important caveats.

Claims to verify:
1. [Claim 1 from transcript]
2. [Claim 2 from transcript]
3. [Claim 3 from transcript]

Context: The video is about [topic]. The creator's angle is [perspective].

For each claim, identify the primary source and note if the numbers are accurate or if they may have been mangled by speech-to-text (common with large numbers, centuries, and round figures)."
```

Fusion output goes to stdout. Parse it for claim verifications and sources.

**For 3+ independent claims that span very different domains**, you can run multiple Fusion queries in parallel via `delegate_task`, one per claim domain:

```python
delegate_task(tasks=[
  {"goal": "Run this Fusion query via terminal: python3 ~/.hermes/scripts/fusion_query.py 'Research claim: [specific question]'. Return the full output.", "toolsets": ["terminal"]},
  {"goal": "Run this Fusion query via terminal: python3 ~/.hermes/scripts/fusion_query.py 'Research claim: [different question]'. Return the full output.", "toolsets": ["terminal"]},
])
```

**When Fusion fails (empty output, timeout, or JSON parse error)** — Three known failure modes:

1. **Empty output:** `fusion_query.py` succeeds (exits 0, charges money) but returns only the cost line with no actual research content. The panel deliberated but produced nothing useful.
2. **Timeout:** `fusion_query.py` runs past the foreground terminal timeout (default 180s) and gets killed. **Prevention:** always set `timeout=600` on the terminal call. The script now defaults to 900s HTTP timeout internally.
3. **JSON parse error:** `fusion_query.py` exits non-zero with a Python JSON decode error (e.g., `Expecting value: line 177 column 1 (char 968)`). This happens when the API response is truncated or malformed — the script's JSON parser chokes before it can extract the research content. The Fusion panel may have produced useful work, but the script can't parse the response.

In any of these cases, don't retry Fusion — immediately fall back to `delegate_task` with parallel web-search subagents (one per claim domain). The subagent path is slower (~5 minutes) but reliable. For the sand battery video (June 2026), the JSON parse error occurred and the 3-subagent fallback produced excellent results covering specs, performance claims, and technology context — better-structured than a single Fusion query would have been, because each subagent focused on one domain.

**Direct parallel web_search (fastest path for straightforward claims)** — When the claims are simple enough that you can verify each with 1-2 web searches, skip Fusion and subagents entirely. Fire 3-5 `web_search` calls in parallel (one per claim or claim cluster), then follow up with `web_extract` on the most promising URLs. This approach completed in under 2 minutes for the Arctic sea ice thickening video (July 2026), which had 5 claims across climate science, government policy, and field experiment results. The approach works best when:
- Claims are independently verifiable via well-indexed sources (government websites, press releases, peer-reviewed papers)
- No claim requires deep multi-step reasoning to verify
- You can quickly identify the primary source for each claim from search results

This is faster than Fusion (which takes 2-5 minutes) and much faster than subagents (5+ minutes). Use it as the default when claims don't span deeply interconnected domains requiring synthesis.

**Fallback: delegate to subagents with web_search** — When Fusion is unavailable, returns empty, or the claims are simple enough not to need multi-model deliberation:

```python
delegate_task(tasks=[
  {"goal": "Research claim 1: [specific factual question]. Provide details and sources.", "toolsets": ["web"]},
  {"goal": "Research claim 2: [specific factual question]. Provide details and sources.", "toolsets": ["web"]},
])
```

**Group related claims into themed buckets** — When a video makes 5-8+ claims, group them by domain into 2-3 research queries. This keeps each query focused on one knowledge domain while covering all claims efficiently.

**For each claim, classify as:**
- ✅ **Verified** — backed by real sources
- ⚠️ **Directionally correct** — numbers are real but framing needs caveats
- ❌ **Misleading or wrong**

**Store results in a structured dict** for the Obsidian note:
```python
research = {
  "claim_name": {
    "source": "Dr. Roger Clark / study name",
    "verdict": "directionally correct",
    "caveat": "...",
    "links": ["url1", "url2"]
  }
}
```

### 4. Save to Obsidian (ask first)

Ask: "Want me to save this research to Obsidian?"

Structure:
```
Path: Research/YYYY-MM-DD-<topic-slug>.md
Frontmatter: tags, source, author, date
Sections:
  - Full Transcript
  - Video Metadata (table)
  - Key Claims & Verifications (one per claim with source, verdict, caveat)
  - Creator Profile
  - Overall Verdict
  - Related Notes [[wikilinks]]
```

**Example filename format:** `2026-05-06-human-eye-camera-specs-tiktok-research.md`

### 5. Blog (ask first)

Ask: "Want me to turn this into a blog post?"

If yes, write an engaging summary post for prose.sh:
- **Title:** A hook that captures the video's premise
- **Structure:**
  - Opening — the hook and why it's interesting
  - One section per major claim with the caveat explained plainly
  - End with a Sources section listing references (studies, reports, articles)
  - The post must stand entirely on its own — no mention of the originating social media platform, creator, or ASR issues
  - No meta-disclaimers about tooling (no "this was researched using X" or "this post was generated by Y")
  - Do NOT embed the full transcript — it reveals the video source and bloats the post
- **Format:** No YAML frontmatter. Start with `# Title`, then `*Date · Tags: ...*`
- **Publish:** Save to `~/blog/<slug>.md`, then `rsync -vr --force --no-compress ~/blog/<slug>.md prose.sh:/<slug>.md`
- **Verify:** `curl -sf https://hermez.prose.sh/<slug>` returns HTTP 200

### 6. Share to Mastodon (ask first)

Ask: "Want me to share this to Mastodon?"

If yes, write a punchy summary post for Mastodon (@your-handle@your.instance):

- **Load the `mastodon` skill first** — it has the helper script (`scripts/mastodon_post.py`), formatting rules, and the token at `~/.hermes/secrets/mastodon_token`
- **Formatting rules (hard requirements):**
  - No emdash characters. Use regular dashes (-), commas, colons, or parentheses
  - No markdown formatting (no `**bold**`, `*italic*`, `# headers`). Plain text only
  - Start with a relevant emoji
  - Write a punchy hook as the first line
  - Include 2-3 relevant hashtags at the end
  - No source URLs in the post body (the blog link is the only URL)
  - Max 1989 chars with URL-aware counting (URLs count as 23 chars each)
- **Content structure (blog-sharing variant):**
  - Hook (1-2 lines) — the most interesting claim or counterintuitive finding
  - Key findings (3-5 lines) — what the research actually found, in plain language
  - Important caveat (1-2 lines) — what the viral version got wrong or oversimplified
  - Blog link: `https://hermez.prose.sh/<slug>`
  - Hashtags (e.g., #science #nature #corvids)
- **Standalone TIL-style variant (no blog):** When the user asks for a direct Mastodon post without a blog ("make a brief informational post", "TIL-style", "post about it"), use this variant instead:
  - Source URLs go directly in the post body — do NOT strip them. The blog-sharing rule "no source URLs in the post body" applies ONLY when linking to a blog post.
  - Content structure: hook (1-2 lines) → key findings (4-6 lines, in plain language) → any caveat (1-2 lines) → "Read more:" followed by 2-3 source URLs → hashtags
  - Include 2-3 primary source links (Honda heritage page, IEEE, Wikipedia, etc.) — these are the payoff for the reader, not filler
  - Still follows all other formatting rules (no emdashes, no markdown, emoji start, plain text, max 1989 chars with URL-aware counting)
  - No mention of TikTok — the post stands on its own as an interesting fact
- **TIL-style post example structure:**
  ```
  [emoji] TIL: [hook sentence]

  [2-3 sentences of context and how it worked]

  [1-2 sentences on what's notable or the catch]

  Read more:
  [source URL 1]
  [source URL 2]
  [source URL 3]

  #TIL #[topic] #history
  ```
- **Always dry-run first** — use `python3 scripts/mastodon_post.py --dry-run --status "..."` to check character count and formatting before posting
- **No mention of TikTok** — same rule as blog posts. The Mastodon post should stand on its own as an interesting science fact-check. Do not reference the originating platform, creator, or ASR issues
- **Post and confirm** — capture the post URL from the response and include it in the final summary to the user

## Example Output Structure (Obsidian)

```markdown
---
tags: [tiktok, research, vision, biology, photography]
source: https://www.tiktok.com/@user/video/123
author: "@creator"
date: YYYY-MM-DD
---

# Topic — TikTok Research

## Full Transcript

[cleaned VTT text]

## Video Metadata

| Field | Value |
|-------|-------|
| Creator | @name — X followers |
| Caption | "..." |
| Hashtags | #tag1 #tag2 |
| Likes | X |
| Views | X |

## Key Claims & Verifications

### 1. Claim Name
**Source:** Original researcher/study
**Verdict:** ✅ / ⚠️ / ❌
**Caveat:** What the viewer should know
**Links:** [source](url)

## Creator Profile

## Overall Verdict
```

### 7. Ingest into LLM Wiki (if wiki exists)

If the user has a wiki at `~/wiki` (or `$WIKI_PATH`), ingest the research:
1. Save raw source to `raw/articles/<creator>-<topic-slug>.md` with frontmatter (`source_url`, `ingested`, `sha256`)
2. Create/update entity pages for the creator and any major subjects
3. Create a concept page if the video covers a broader theme (e.g., "Disney's dark source material")
4. Update `index.md` and `log.md`
5. Use `[[wikilinks]]` to cross-reference all new pages

### 8. Ask about scope

After scraping and reading the transcript, ask: "Want me to go deep on this? I can research it, save to Obsidian, blog about it, and share to Mastodon." Let the user choose: research only, +Obsidian, +blog, +Mastodon, +wiki, or all of the above.

When the user requests the full pipeline (research + Obsidian + blog + Mastodon), execute all steps in sequence without re-asking at each stage. The initial request to "do everything" or "research, fact check, enrich, save to Obsidian, write a blog post, and share to Mastodon" is explicit consent for all steps.

## Trigger

**ALWAYS load this skill immediately when the user shares a TikTok URL.** Load the skill BEFORE trying any other tool — do not first experiment with `web_extract`, `browser_navigate`, `browser_console`, `browser_vision`, etc. Those tools cannot extract spoken audio content from TikTok videos, and each failed attempt wastes a round-trip. The skill's CLI path is the only reliable way to get the ASR transcript.

Do NOT use the `nanogpt_tiktok_scraper` Hermes tool directly. It is **structurally incapable** of scraping a specific video by URL — its schema has no `post_urls` parameter, only `hashtags`, `profiles`, and `search_queries`. Passing `post_urls`, `queries`, or any URL parameter produces `TypeError: unexpected keyword argument` before the API is even called. Use the `scripts/scrape_tiktok.py` CLI path described in Step 1 — this is the ONLY working path for URL-based scraping.

### Simple link shares ("What is this?")

When the user just wants to know what a video is (no research request), stop after Steps 1–2 (scrape + understand). Present the video's topic, creator, key points, and engagement stats. Do NOT launch into the full research/save/blog pipeline unless the user asks for it. The workflow above describes the full treatment — apply only what the user's request warrants.

## Pitfalls

- **`nanogpt_tiktok_scraper` Hermes tool ≠ the skill's CLI script.** The built-in `nanogpt_tiktok_scraper` Hermes tool is **structurally incapable** of scraping a specific video by URL. Its schema has no `post_urls` parameter — only `hashtags`, `profiles`, and `search_queries`. Passing `post_urls`, `queries`, or any URL-shaped argument produces `TypeError: unexpected keyword argument` immediately, before the API is even called. Even `profiles` + `videos_per_source` can fail with 400 errors on certain URL formats. The skill's CLI path (`scripts/scrape_tiktok.py`) handles URL canonicalization, retries, and has been battle-tested. Always use the CLI, never the Hermes tool.
- **ASR transcripts frequently mangle numbers** — This is the #1 source of error. Speech-to-text routinely collapses large numbers: "1400" becomes "14," "1500" becomes "15," "1000" becomes "100" or "10," "1,400,000" becomes "14,000," etc. Round numbers, centuries, and large counts are the most vulnerable. When the transcript contains a numeric claim that seems obviously wrong, illogical, or nonsensically small in context (e.g., "nothing comparable for 14 years" about a 2,000-year-old artifact), the creator almost certainly said the correct large number — flag the ASR error to the user rather than assuming the creator misspoke.
- **Cross-reference ASR number claims against context** — A claim that makes no sense at the scale of the video's subject (14 years vs 1,400 years for "lost technology") should trigger an explicit check: does the raw VTT or a manual re-listen confirm the number? When in doubt, give the creator the benefit of the doubt and let the user know what the ASR likely mangled.
- **Fetch the VTT immediately** — `tiktokLink` CDN URLs may expire after some time
- **The `tiktokLink` returns VTT text even though Content-Type says `video/mp4`** — trust the content, not the header
- **Never mention TikTok in blog posts** — the TikTok is just the topic seed. The post must stand entirely on its own with zero reference to the originating social media source, creator, or ASR issues. The reader should not know how the topic was discovered.
**Always ask before Obsidian/blog** — don't assume they want the full treatment
- **Cost is $0.0012–$0.0048 per scrape** — cheap enough to run as a first step without asking
- **`--show-transcript` printed preview is often truncated, but the saved JSON usually has the full transcript** — the display may end mid-word ("test how tough it ac" with a `... (1664 chars total)` footnote) while the JSON file the script saved contains the complete text. **Read the saved JSON first** before assuming the transcript is incomplete. However, `subtitleLinks[0].transcript` is sometimes an empty string (length 0) even when the display preview showed transcript text — the API embeds the transcript in CLI output but the parsed JSON field may be empty. When this happens, the VTT fetch via `tiktokLink` is required, not optional. The manual VTT fetch is a recovery step, not a magic fix — in many cases the VTT yields the same character count as the API response because they share the same source. Signs of *true* truncation (vs display-only or missing-JSON-field): `subtitleLinks[0].tiktokLink` is missing entirely, the JSON's transcript field is empty AND no VTT is available, the displayed text ends mid-sentence with no terminal period AND the char count is suspiciously low for the video length (e.g., <30 chars/second of video), or you suspect the API returned a stale transcript and the live VTT has a newer version.
- **Some videos lack ASR subtitles** — fall back to the `text` field for the caption
- **Claims from TikTok are often directionally correct but framed for virality** — note caveats but don't dismiss the core insight
- **Viral numbers attributed to institutions are frequently wrong** — when a transcript says "according to [University], the number is X," always check the primary source. Content creators often swap, round, or invent specific numbers while citing real institutions for credibility. The underlying scientific point may be valid even when the specific number is mangled (see `references/misattribution-patterns.md` for documented examples)
- **Viral headline cross-contamination (distinct from institution misattribution)** — sometimes a real number from one unrelated story gets grafted onto a completely different story. The ASR is correct, the named brand is real, but the *claim being attributed* never existed. The bridge is usually a shared noun (e.g., "Nvidia DGX Spark saves $22k in cloud costs" → "Nvidia pays you $22k/yr"). When a "$X" headline is too round or too good, search `[Brand] + claim keywords` AND trace the number to its real source — if official company materials (press releases, white papers) don't contain it, the claim is contaminated. See `references/misattribution-patterns.md` for the June 2026 "$22,000/yr from Nvidia" case study and detection method.
- **Viral benchmark inflation (distinct from ASR number mangling)** — a real benchmark result exists, but the numbers grow with each social media retelling until they're unrecognizable. The ASR transcript is **correct** — the creator actually said the inflated number; they heard it and repeated it in good faith. The error is in the information ecosystem, not the transcription. Example (June 2026): "quantum computer solved in 2 hours what would take 3.2 million years classically" — the real result was Google's 2019 Sycamore experiment (200 seconds vs ~10,000 years, itself disputed by IBM). Detection: search for the claim keywords + "benchmark"/"Nature"/"paper", find the closest real published result, compare numbers. If the real result has smaller but still impressive numbers, it's inflation. See `references/misattribution-patterns.md` for the full case study and detection method.
- **Research program conflation (distinct from benchmark inflation)** — two separate experiments from the same lab, studying related but distinct questions, get blended into one seamless "super-experiment" narrative with composite timelines that don't exist in any single paper. Unlike benchmark inflation (where one study's numbers grow), conflation stitches together **all-real numbers from different experiments** as if one study produced them. Example (June 2026): a video about crow funerals blended Swift's dead-crow experiments (6-week memory) with Marzluff's trapping/mask experiments (2.7-year individual memory, 5-year population spread) into a composite "weeks, months, a year, two years, five years" timeline. The tell-tale sign is a composite timeline that no single paper contains. Detection: search for the topic + named institution/researcher, find ALL relevant papers (not just one), and assign each claim to its correct source. Watch for different lead authors within the same lab (a grad student's thesis is often a distinct experiment from the PI's long-running project). See `references/misattribution-patterns.md` for the full case study and detection method.
- **Metric confusion — AUC ≠ accuracy ≠ sensitivity (distinct from number mangling)** — a viral health/medical claim cites a performance percentage that is real but **mislabeled**. The number 93 appears in the paper, but as **AUC** (discrimination across thresholds) or **sensitivity** (true positive rate), not as **accuracy** (overall correctness). Example (June 2026): "93% accuracy detecting Alzheimer's from an eye scan" — the 0.9355 was AUC in one study (actual accuracy: 89% internal, 82% external), and 93.2% was sensitivity in a different study (actual accuracy: 83.6%). The creator merged both into "93% accuracy." Detection: when a medical/AI claim cites a performance percentage, search for the original paper and check the exact metric. "AUC of 0.XX" or "AUROC" is not accuracy. This pattern often co-occurs with study conflation — different metrics from different papers merged into one headline number. See `references/misattribution-patterns.md` for the full case study.
- **Pretraining vs. labeled data conflation** — when a claim says "trained on N images," the N may be **unlabeled pretraining data** used to teach the AI what the input looks like, not disease-specific labeled training data. The actual labeled dataset is usually much smaller (hundreds vs. hundreds of thousands). Example (June 2026): "trained on 178,000 retinal photographs" — 178K were unlabeled UK Biobank images for self-supervised pretraining; the actual Alzheimer's-labeled training set was ~360 images. This inflates apparent training scale by 100-1000x. Detection: search for "pretrained" / "self-supervised" / "unlabeled" in the paper vs. "labeled" / "annotated" / "fine-tuned."
- **Thermal vs. electrical energy conflation** — when a technology video says "stores energy" or "battery," check whether the stored energy is electrical (electricity in, electricity out) or thermal (electricity in, heat out). "Store electricity in sand" sounds like grid-scale electrical storage, but the Polar Night Energy sand battery stores **heat** for district heating, not electricity. The "100 MWh" figure is thermal energy. The 80-90% round-trip efficiency is electricity-to-heat-to-heat, not electricity-to-electricity — comparing it to lithium-ion (85-95% electricity-to-electricity) is apples-to-oranges. Detection: when a "battery" stores heat, clarify the energy form early in the research output and avoid implying it competes with electrical storage technologies.
- **Company-claimed performance numbers vs. independently verified** — when a technology video reports efficiency, emissions reductions, or cost savings, check whether the numbers come from the company's own press releases vs. independent third-party audits. Tech media often repeats company press releases verbatim. The customer and investor are not independent parties — they have financial interest. Awards (TIME Best Inventions, industry awards) validate market interest but are NOT performance audits. Example (June 2026): all Polar Night Energy performance figures (100% oil reduction, 70% CO2 cut, 80-90% efficiency) are company-claimed, corroborated by customer/investor, but no independent audit exists. Don't dismiss the numbers — flag the source for the user.
- **Organization mischaracterization** — creators often call government agencies "companies" or university labs "startups." When a transcript names an organization behind a project, verify what type it is: government agency, university, private company, or nonprofit. Government agencies are created by legislation, funded by taxpayers, and have transparency requirements companies don't. Example (July 2026): ARIA (Advanced Research and Invention Agency) was called a "UK company" but is a government R&D agency established by Act of Parliament. ARIA also doesn't directly conduct the experiments — it funds grants to Real Ice and Arctic Reflections, with the RASI project led by University of Cambridge. See `references/misattribution-patterns.md` for the full case study.
- **Sea ice vs land ice conflation in climate claims** — "melting polar ice caps raise sea levels" is a common misconception. Arctic sea ice is already floating and contributes only ~2.6% additional volume when melted (NSIDC). The real drivers of sea level rise are land ice (Greenland, Antarctica, glaciers) and thermal expansion. When a climate video links ice melt to sea level rise, check whether they mean sea ice or land ice. The ice thickening project (RASI) targets sea ice — its climate value is through the albedo effect, not preventing sea level rise. See `references/misattribution-patterns.md` for the full case study.
- **ASR frequently mangles scientific names.** Similar-sounding taxonomic names get swapped. In one case, "Pterocetus diamantinae" (a newly described extinct beaked whale from the Pliocene) was transcribed as "Protocetidae" (a completely different family of Eocene whales that went extinct 37+ million years earlier). Both are real cetacean taxa, but from vastly different time periods. When a transcript names an obscure scientific taxon, cross-reference it against the primary source — if the named species/taxon doesn't match the time period or context of the discovery, the ASR likely swapped it for a similar-sounding name.
- **ASR mangles proper names and brand names.** Well-known surnames and company names get approximated phonetically: "Mike Fincke" → "Mike Fink," "SpaceX" → "Space X." When a transcript contains a person's name or a brand that looks slightly off, check the primary source before quoting it as written. The person/brand is almost certainly the canonical spelling — the ASR just guessed wrong phonetically.
- **ASR drops "hundred" from large numbers.** "1,200 kilometers" was transcribed as "12 kilometers" — the ASR collapsed "twelve hundred" to "twelve." Watch for internally inconsistent numbers: if a transcript says "12 km, or 750 miles" the two units don't match (12 km = 7.5 miles), which reveals the ASR error. Always cross-check unit conversions in the transcript against each other and against the primary source.
- **Written caption can contradict the spoken transcript.** The caption (`items[0].text`) is manually written by the creator; the transcript (VTT from `subtitleLinks`) is ASR of what they actually said. They can disagree. Example (July 2026): a Honda Electro Gyrocator video's caption said the navigation system "use satellites" while the spoken transcript correctly said "without satellites." When they conflict, the spoken transcript is the source of truth for claims — that's what the creator actually said on camera. The caption may be hastily edited or copy-pasted from notes. Always read both and flag any disagreement in your analysis.
- **Relative time references must be anchored to the video's post date.** When a creator says "next year," "last month," "just announced," "recently," etc., the actual calendar date depends on when the video was posted. Always verify `items[0].createTime` and cross-reference relative claims against current dates when fact-checking. A "next year" claim in an April 2026 video means 2027, which may differ from the project's currently stated timeline.
- **The Obsidian vault path** varies — check `OBSIDIAN_VAULT_PATH` env var, fallback to `~/Documents/Obsidian Vault`
- **Browser automation won't get the transcript** — `web_extract`, `browser_navigate`/`click`/`snapshot`, and `browser_console` cannot extract the spoken audio from TikTok videos. The video loads from a blob URL with no text tracks exposed to the DOM. The ONLY reliable path is nanogpt-tiktok's ASR transcript via `subtitleLinks[].tiktokLink`.
- **Short URLs (`tiktok.com/t/...`) redirect to the canonical video page** — the skill's scraping works on both, but always canonicalize to the full `/@user/video/...` URL before logging/saving.
- **Scrape script can take 60-120 seconds** — the NanoGPT TikTok API is not instant. The default terminal timeout of 60s will kill the scrape prematurely. Always set `timeout=180` (or higher) on the terminal call running `scrape_tiktok.py`. The script itself polls the API and waits for results internally.
- **Max 3 concurrent subagents:** `delegate_task` has a default `max_concurrent_children` of 3. If you have 4+ research tasks, split into multiple `delegate_task` calls or merge related claims into fewer subagents. The error looks like: `Too many tasks: N provided, but max_concurrent_children is 3`.

**Partial subagent failures are fine:** When delegating research to parallel subagents (one per claim via `delegate_task`), some may time out (600s default). If at least one subagent returns with comprehensive findings, proceed. Two out of three research reports is plenty to write a strong blog post and Obsidian note. Don't let one failed thread block the pipeline. Note the gap in the output (e.g., "Claim X: research subagent timed out, unverified") and continue.
