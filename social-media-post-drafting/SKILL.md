---
name: social-media-post-drafting
description: Draft short-form social media posts (Mastodon, X, LinkedIn, Bluesky, Threads, etc.) for the user. Covers platform identification, char-limit verification, topic research, and character-count validation. Triggers on "write a post about X", "make a social post", "post about Y", "toot about W", "tweet about Z", "linkedin post about...".
---

# Drafting Social Media Posts

Use when the user asks for a short-form social media post — anything from a single toot/tweet to a longer Mastodon or LinkedIn-formatted post. **Not** for blog posts (use `article-writing` + `pico-sh`), cover letters (use `cover-letter-generator`), or other long-form content.

## Critical pitfalls

### 1. Don't default to a platform's "famous" char limit
Platforms are configurable. Guessing the default is the most common failure mode:
- **Mastodon** default is 500, but admins set `MAX_TOOT_CHARS` per instance. Jason's instance is 1989.
- **X/Twitter** default is 280 (free) or 4000 (Premium). Don't assume 280.
- **LinkedIn** posts: 3000 chars. Comments: 1250.
- **Bluesky**: 300. **Threads**: 500. **Facebook**: effectively no limit.

If the user says "my instance" or "my account," ask for the actual cap. See `references/char-limits.md` for the full table and verification commands.

### 2. Verify the char count programmatically
Don't eyeball. Use `execute_code` with `len(post)` and iterate. Eyeballing produced four over-shoot drafts in one session — `len()` would have caught each one in milliseconds. The pattern:

```python
post = """..."""
print(f"{len(post)} / {LIMIT}  (headroom: {LIMIT - len(post)})")
```

Iterate until the count is where you want it (at the cap, below the cap with headroom for tweaks, etc.).

### 3. Research before drafting
If the topic is a software release, version, company news, or anything fact-checkable, web-search the primary source (release notes, official blog, changelog). Read it — don't paraphrase from a single search snippet. Synthesized features harden into confident hallucination.

### 4. Don't add CTA / "Like and share" filler
Unless the platform's culture uses it (LinkedIn does, Mastodon generally doesn't). Platform-agnostic posts read better without it.

## Steps

1. **Identify the platform.** If not specified, ask one question (multiple-choice). Default to Mastodon if the topic is fediverse-related. If the user is on the fediverse and the topic is a fediverse release, Mastodon is the obvious target.
2. **Determine the char limit.** Known per-platform (see `references/char-limits.md`). If the user mentions "my instance" or "my X account," ask. For Mastodon, the compose box counter shows the live cap; for X, check the account tier.
3. **Research the topic.** Web-search the primary source. If the user supplied URLs or a topic they want summarized, read those.
4. **Draft within the limit.** Use the full length if the user explicitly asked for "longer" or "use the cap." Otherwise leave 10–20% headroom so they can tweak without a forced trim.
5. **Verify with `len()`.** Run `execute_code` to count. If over, trim a sentence from a less essential paragraph (e.g. admin/upgrade notes, accessibility, citation). If well under, expand with the next-highest-value point.
6. **Offer follow-up tweaks.** When posting without the exact platform target, state the assumption ("I optimized this for Mastodon") and offer to adapt length/format/tone for others.

## Output conventions
- Single post unless the user asks for a thread.
- Hashtags only at the end — functional on Mastodon (shows up in hashtag feeds), optional on X/LinkedIn, near-useless on Threads.
- No emoji unless the user uses them or the topic warrants it. Don't sprinkle them in to "add personality."
- When the post quotes real numbers, features, or specs, cite the source URL at the end (or in a "Learn more:" prefix line). The link doesn't have to be a full clickable anchor — a plain URL is fine.
- Match the user's existing voice. If they post casually, write casually. If they post formally, write formally. Default to warm-but-direct for Jason.

### Hard style rules (apply to ALL platforms, not just Mastodon)
- **No em dashes (—).** Use regular dashes (-), commas, colons, or parentheses. This is a hard rule for all social media drafts, not just Mastodon posts. Apply it during drafting, not just before posting.
- **Capitalize the first letter of every sentence.** Jason's casual tone means lowercase starts can slip in — don't let them. Even in a casual voice, sentence capitalization is required.

## Reference
- `references/char-limits.md` — per-platform limits table, how to verify a Mastodon instance's `MAX_TOOT_CHARS`, X tier detection.
