# ASR Number Mangling — Observed Examples

TikTok's ASR routinely collapses large numbers, especially when speech is rapid or clipped. Below are confirmed cases from research sessions.

## Antikythera Mechanism (May 2026)

| Video claim (what creator said) | ASR transcript output | Error type |
|---|---|---|
| "nothing comparable for 1,400 years" | "14 years" | Dropped the trailing "00" / collapsed "fourteen hundred" to "fourteen" |

**Context:** Creator @bynasiraziz (nasir), 1m7s video. The transcript output read "14 years" — a clearly nonsensical claim for a 2,000-year-old artifact. The correct figure is 1,400 years, aligning with the gap between ~100 BC and 14th-century medieval astronomical clocks.

**Signal pattern:** When a number claim in the ASR transcript is obviously wrong at the *scale* the video is operating at (centuries vs decades, millions vs thousands), trust the context over the transcript. The ASR clipped the speech rhythm — "fourteen hundred" compressed into "fourteen."

## How to Detect

1. Read the transcript number aloud — does it make sense given the video's subject scale?
2. Cross-reference the canonical VTT content (not just the `--show-transcript` summary) for the raw text
3. Check if the claim would be **more plausible** with a trailing zero appended (14→140, 15→1500, 100→1000)
4. For large round numbers, ASR nearly always drops the magnitude suffix before it drops the leading digits

## Reporting to the user

When you detect an ASR number mangling, say it directly:

> "The transcript reads '14 years' but the creator almost certainly said '1,400 years.' This is a common ASR artifact where speech-to-text collapses large round numbers."

## ASR Proper Name Mangling — Observed Examples

### Pornainen → "Portland" (June 2026)

| Video claim (what creator said) | ASR transcript output | Error type |
|---|---|---|
| "providing heat to the citizens in Pornainen" | "providing heat to the Citizens in Portland" | Phonetically similar place name substitution |

**Context:** Creator @interestingengineering, 2m41s video about Finland's Polar Night Energy sand battery. The Finnish town name "Pornainen" was transcribed as "Portland" — a completely different city in a different country. The ASR guessed a familiar English place name that sounds vaguely similar to the unfamiliar Finnish one.

**Signal pattern:** ASR replaces unfamiliar or foreign place names with phonetically similar familiar ones. "Pornainen" doesn't appear in English-language training data as frequently as "Portland," so the ASR defaults to the more common name. This is even more dangerous than number mangling because the replacement name is real and plausible in context ("a town called Portland" sounds fine until you realize the video is about Finland).

**Also in the same video:**

| Video claim | ASR transcript output | Error type |
|---|---|---|
| "crushed soapstone" | "crust soapstone" | Consonant cluster simplification ("crushed" → "crust") |
| "2,000 tons of crushed soapstone" | "2,000 tons of crust soapstone" | Same consonant cluster mangling |

**Context:** Both "crushed" → "crust" and "Pornainen" → "Portland" appeared in the same video. The proper name mangling is the more dangerous error because a reader might not realize "Portland" is wrong without checking the primary source.

### How to detect proper name mangling

1. When a transcript contains a place name that seems geographically inconsistent with the video's topic (e.g., "Portland" in a video about Finland), flag it immediately
2. Cross-reference with the video's caption, hashtags, or other metadata — the caption said "Pornainen" while the ASR said "Portland"
3. Foreign place names are especially vulnerable — ASR defaults to phonetically similar English names
4. Less common proper nouns (company names, product names, non-English names) are frequently replaced with more common English words that sound similar
