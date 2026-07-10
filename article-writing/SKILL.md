---
name: article-writing
description: "Write articles, guides, blog posts, tutorials, newsletter issues, research reports, and deep research outputs in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph, deep research on a topic, or a research report — especially when voice consistency, structure, and credibility matter. Triggers on: 'write an article', 'research report', 'deep research', 'long-form', 'blog post', 'guide', 'newsletter', 'white paper', 'research paper'."
origin: ECC
---

# Article Writing

Write long-form content that sounds like an actual person with a point of view, not an LLM smoothing itself into paste.

## When to Activate

- drafting blog posts, essays, launch posts, guides, tutorials, or newsletter issues
- turning notes, transcripts, or research into polished articles
- matching an existing founder, operator, or brand voice from examples
- tightening structure, pacing, and evidence in already-written long-form copy

## Core Rules

1. Lead with the concrete thing: artifact, example, output, anecdote, number, screenshot, or code.
2. Explain after the example, not before.
3. Keep sentences tight unless the source voice is intentionally expansive.
4. Use proof instead of adjectives.
5. Never invent facts, credibility, or customer evidence.

## Voice Capture Workflow

If the user wants a specific voice, collect one or more of:

- published articles
- newsletters
- X posts or threads
- docs or memos
- launch notes
- a style guide

Then extract:

- sentence length and rhythm
- whether the writing is compressed, explanatory, sharp, or formal
- how parentheses are used
- how often the writer asks questions
- whether the writer uses fragments, lists, or hard pivots
- formatting habits such as headers, bullets, code blocks, pull quotes
- what the writer clearly avoids

If no voice references are given, default to a sharp operator voice: concrete, unsentimental, useful.

## Framing: Explainer, Not Fact-Check

Blog posts and social media posts should be **informational explainers**, not adversarial fact-check pieces.

- Do not structure posts around "what's wrong" or "what's misleading" about other coverage.
- Do not reference "viral claims," "what people get wrong," or similar adversarial framing.
- Do verification during research to ensure accuracy, but deliver the result as a clean explainer — the reader shouldn't see the verification process or be told what other people got wrong.
- If a detail is more nuanced than common understanding (e.g., "it stores heat, not electricity"), state it as an interesting fact in the normal flow of explaining what the thing does — not as a "misconception" or "myth" to debunk.
- If a term is technically broader than it seems (e.g., sand is a grain size classification, not a mineral identity), get the classification right. Don't say "it's not X, it's Y" when X is the broader category that includes Y. Instead: "it's X made specifically from Y, chosen for [reason]."

## Banned Patterns

Delete and rewrite any of these:

### Generic AI Transitions
- "In today's rapidly evolving landscape"
- "Furthermore", "Moreover", "Additionally" as sentence openers
- "It is important to note that"
- "It should be noted that"
- "It is worth noting that"
- "Here's the thing"
- "Let me be clear"
- "Moving forward"

### Corporate Jargon
- "leverage", "utilize", "facilitate", "implement", "demonstrate"
- "landscape" (as in "the competitive landscape")
- "deep dive", "circle back", "take a step back"
- "game-changer", "cutting-edge", "revolutionary"

### AI Vocabulary (overused by LLMs)
- "delve", "tapestry", "meticulous", "meticulously"
- "bolstered", "garner", "intricate", "intricacies"
- "testament", "showcase", "exemplifies"

### Collaborative / Polite Overdrive (AI-to-user artifacts)
- "I hope this helps"
- "Of course", "Certainly"
- "Feel free to", "Let me know if"
- "Would you like", "I'm happy to"

### Knowledge Cutoff Disclaimers
- "As of my knowledge cutoff"
- "Based on available information"
- "While specific details are limited"

### Promotional / Travel-Guide Language
- "boasts a", "renowned", "nestled in the heart of"
- "showcasing", "exemplifies", "diverse array"

### Vague Attributions
- "experts argue", "industry reports", "several sources"
- "observers have cited"

### Filler Phrases
- "at its core", "at the end of the day"
- "in a world where", "when it comes to"
- "the reality is"

### Other AI Habits
- "no fluff"
- "not X, just Y"
- "here's why this matters" as a standalone bridge
- fake vulnerability arcs
- a closing question added only to juice engagement
- forced lowercase
- corny parenthetical asides
- biography padding that does not move the argument
- em-dashes used to bracket asides — use commas instead

## Writing Process

1. Clarify the audience and purpose.
2. Build a hard outline with one job per section.
3. Start sections with proof, artifact, conflict, or example.
4. Expand only where the next sentence earns space.
5. Cut anything that sounds templated, overexplained, or self-congratulatory.

## Structure Guidance

### Technical Guides

- open with what the reader gets
- use code, commands, screenshots, or concrete output in major sections
- end with actionable takeaways, not a soft recap

### Essays / Opinion

- start with tension, contradiction, or a specific observation
- keep one argument thread per section
- make opinions answer to evidence

### Research Reports / Deep Research

- open with the key finding or thesis — not background preamble
- organize by evidence, not by source
- cite specific data points, studies, or primary sources inline
- distinguish established facts from analysis and speculation
- use tables, timelines, or comparison grids where they compress information better than prose
- close with implications or actionable conclusions, not a summary of what was already said
- every claim earns its place — cut filler that doesn't advance understanding

### Newsletters

- keep the first screen doing real work
- do not front-load diary filler
- use section labels only when they improve scanability

### Deep Research / Research Reports

- open with a concrete hook — the most surprising or consequential finding
- structure by argument or chronology, not by source
- cite sources inline (name, date, URL) — never drop bare claims
- synthesize across sources; don't just summarize them one after another
- include a "so what" section that answers why this research matters now
- end with forward-looking takeaways or open questions, not a generic summary
- use tables, timelines, or data comparisons where they compress information better than prose
- See [references/historical-research-formatting.md](references/historical-research-formatting.md) for historical civilization report templates

### Comparative Technology Surveys ("X and Others Like It")

When the user asks to research a specific technology "and others like it," "and similar approaches," or "compared to alternatives," the post is a comparative survey, not a single-subject explainer. This pattern requires both a research dimension change and a specific output structure.

**Research phase:** Deliberately include competitors, alternatives, and adjacent approaches as a named research dimension. Search for the category/field, not just the specific product. A technology that looks unique often has 3-5 peers using different organisms, materials, or active-vs-passive approaches. Find them.

**Structure:**
1. The primary technology in full detail (what it does, how it works, what it claims)
2. Current deployment status (pilot sites, installations, partnerships)
3. What independent science says about the core claims (lab studies, field studies, peer-reviewed evidence)
4. The broader landscape: 2-4 alternative/competing approaches, each with enough detail to compare
5. A comparison table compressing the parallel attributes (organism/type, energy output, maintenance, cost, maturity)
6. Honest unknowns: what claims are company-stated vs independently verified, durability gaps, real-world vs lab performance gaps, regulatory status, cost-at-scale questions
7. Why this matters: the cumulative-scale argument for the category, not just the one product

**The comparison table is mandatory for this post type.** Readers of survey posts want to compare options side by side. Columns should be the attributes that differentiate the approaches (technology type, key metric, maintenance level, cost, maturity/deployment status). Keep it scannable.

**The "honest unknowns" section is critical.** Emerging technologies often have company-stated claims that sound impressive but lack independent field validation. Name what is peer-reviewed vs company-stated. Distinguish lab results from real-world performance. Note what hasn't been tested across climate zones, time scales, or regulatory frameworks. This builds credibility without adversarial framing.

**Ground numbers in context.** A 41% PM2.5 reduction means nothing alone. Frame it: "measured in a controlled chamber with a linear barrier, not on a vertical wall." Give the reader the reference point and the limitation in the same sentence.

### Science & Technology Posts

Based on analysis of science journalism from SciTechDaily and ScienceAlert. These posts explain a discovery, technology, or scientific finding to a general audience. Key patterns:

**Lead with the discovery, not the institution.**
Open with what happened and why it matters. The university name, journal, and publication date come in a citation block or footer — not the first sentence. The reader cares about the finding, not who funded it.

**Use analogies anchored in everyday experience.**
Complex mechanisms get a concrete comparison before the technical explanation. Examples from the source articles:
- Volcano erupting like a shaken soda bottle (degassing magma = carbonated drink)
- UV upconversion efficiency of 1.9% framed as "may sound low, but it runs on natural sunlight alone"
- Frozen vegetables compared to fresh produce stored in a fridge for a week

The analogy goes first. The mechanism follows. Never the reverse.

**Let researchers speak in their own words.**
Pull quotes from the actual scientists — not paraphrased summaries of quotes. These carry authority and personality that paraphrasing kills. Attribution format: Quote. — Name, Role. Let the quote do work; don't precede it with a sentence that says the same thing the quote says.

**Use comparison tables to compress parallel information.**
When two or more things have comparable attributes, a table communicates faster than paragraph prose. The volcano article compared two eruptions across six dimensions; the food article presented concerns vs. recommendations. If the reader would want to compare things side by side, use a table.

**Ground numbers in human scale.**
A number like "1.9% efficiency" means nothing alone. Frame it: "about 2 UV photons for every 100 visible photons absorbed" or "most solid-state materials can't achieve this even at much higher light intensity." Give the reader a reference point — comparison to existing technology, everyday scale, or the previous state of the art.

**Structure: finding first, mechanism second, implications third.**
1. What was discovered / achieved (the headline finding)
2. How it works (the mechanism, with analogy)
3. Why it matters (applications, future work, what changes)
4. Who did it and where (citation details — institution, authors, journal, DOI)

This mirrors how the source articles flow: the discovery hooks you, the mechanism satisfies curiosity, the implications answer "so what," and the citation block provides credibility for readers who want to go deeper.

**Include the "so what" without overselling.**
Name concrete potential applications. Don't inflate them. The UV article lists "solar-driven photocatalysis, indoor air purification, low-intensity 3D printing, curing resins and dental fillings" — specific, bounded, not "this could change everything." If the researchers filed a patent, say so. If not, don't speculate about commercialization.

**Practical guidance articles: use what-to-watch-for tables.**
When the post has actionable advice (health, consumer, practical tips), present decision guidance as a table: concern on the left, recommendation on the right. Easier to scan and act on than paragraph-prose advice.

**Include a bottom line.**
End with a single-sentence takeaway that captures the core finding. Not a summary of everything said — the one thing the reader should remember.

## Post-Publication Corrections (Blog + Social)

When the user asks to review replies to a published post and verify corrections:

1. **Fetch replies** via the Mastodon context API (`GET /api/v1/statuses/{id}/context`), not by scraping the HTML page. See the `mastodon` skill for endpoint details.
2. **Identify factual corrections** — distinguish corrections (claim X is wrong) from questions, opinions, and tangents. Only verify corrections.
3. **Verify each correction independently** with web_search against authoritative sources. Don't apply a correction just because a commenter said it — confirm it.
4. **Apply verified corrections to the blog** using the patch tool (or write_file for larger rewrites).
5. **Apply verified corrections to the Mastodon post** using the Edit endpoint (`PUT /api/v1/statuses/{id}`). Use Python `requests.put()`, not inline curl, for multiline edits.
6. **Re-publish the blog** via rsync to prose.sh (`rsync -vr --no-compress --force file.md prose.sh:/`).
7. **Report to the user**: which corrections were verified and applied, which were rejected (and why), and which were questions/opinions (not corrections).

**Pitfall:** Don't rewrite the post framing during a corrections pass. If the original used "What's misleading:" adversarial framing, a corrections pass fixes specific factual errors — it doesn't restructure the article. Restructuring is a separate task that should be done deliberately, not opportunistically.

**Pitfall:** When a commenter corrects a technical definition (e.g., "sand is a grain size, not a composition"), check whether the correction is about the word's *definition* vs the blog's *claim*. A blog that says "it's not sand, it's soapstone" is making a composition claim that's technically wrong (soapstone of the right grain size IS sand geologically), even if the everyday-language distinction is useful. Fix the technical accuracy while preserving the useful distinction.

## Quality Gate

Before delivering:

- factual claims are backed by provided sources
- generic AI transitions are gone
- the voice matches the supplied examples
- every section adds something new
- formatting matches the intended medium
