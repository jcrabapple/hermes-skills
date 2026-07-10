# Common Misattribution Patterns in Viral Science Claims

When fact-checking TikTok science claims, watch for numbers that have been distorted through the social media telephone game. These are cases where a real source exists but the specific number got mangled in retelling.

## "10 million bananas for a lethal dose — McGill University"

- **What the video says:** "According to McGill University, you need to eat about 10 million bananas in a single sitting to receive a lethal dose"
- **What McGill actually published:** Dr. Joe Schwarcz (McGill OSS, March 2018) said **"a billion bananas"** — based on the linear no-threshold cancer risk model, not acute radiation poisoning
- **The real acute lethal figure:** ~35 million bananas (4-5 Sv LD50/30 at 0.1 μSv per banana)
- **Why it doesn't matter:** Potassium poisoning kills at ~26-42 bananas (oral lethal dose ~300 mEq / 11.7g K). The radiation number is irrelevant by 6 orders of magnitude
- **Source:** [McGill OSS — Is it true that bananas are radioactive?](https://www.mcgill.ca/oss/article/you-asked/it-true-banana-radioactive)

### Pattern to watch for
Media outlets and content creators frequently cite "McGill University" as a credibility anchor for numbers that McGill never published. When a viral claim attributes a specific number to a university or research institution, always check the primary source — the number may have been simplified, rounded, or replaced during retelling.

## General approach
1. When a transcript attributes a specific number to a named institution, treat it as a claim to verify, not a fact to repeat
2. Search for the institution + topic to find the original publication
3. Compare the actual number to the claimed number — viral science content often rounds aggressively or swaps order-of-magnitude figures (million ↔ billion)
4. If the number is wrong but the underlying point is correct, note both in the research output

## "$22,000 a year from Nvidia" — viral headline cross-contamination (June 2026)

This is a **third pattern** distinct from the two above: a real number from one unrelated story gets grafted onto a completely different story. The ASR transcript is correct, the named institution is real, but the *claim being attributed* never existed.

- **What the video says:** "Nvidia will pay $22,000 a year to put a mini AI data center in your backyard"
- **Where the $22,000 actually came from:** An X (Twitter) post titled *"HOW ONE $2,999 NVIDIA BOX MADE ME $22,000 IN A YEAR"* — about the **NVIDIA DGX Spark** desktop computer. The $22k was **cloud GPU costs avoided** by running inference locally ($1,900/mo × 12 ≈ $22,800), not a payment from anyone
- **The real program being discussed (Span XFRA, April 2026):** Homeowner economics are ~$150/month flat fee covering electricity + internet. **No payment to homeowner in any official Span or Nvidia material**
- **How the contamination happened:** Social media accounts copy-pasted the "$22,000" figure from the DGX Spark X post and appended it to the Span/Nvidia/Pulte story. Span's actual materials never claim $22k. The two stories share the word "Nvidia" — that's the only real connection
- **The correct response:** Debunk the $22k number by tracing it to its actual source, then explain what the real program actually offers. Don't just say "the number is wrong" — give the user the origin story so they understand the pattern
- **Sources:** [Chip & Script EP.069 YouTube debunk](https://www.youtube.com/watch?v=RAwEkD3az04), [DGX Spark X post](https://x.com/w1nklerr/status/2060057563991884060), [Span XFRA white paper](https://ap.span.io/XFRA_White_Paper.pdf)

### Pattern to watch for
When a viral claim is **too good, too round, or too specific** ("$22,000/year!", "10 million bananas!", "exactly 1,400 years!"), it almost always has a provenance worth tracing. Specifically watch for:
- **Two viral stories that share a brand or person** (e.g., "Nvidia DGX Spark saves cloud costs" → "Nvidia pays you $22k/yr"). The shared noun becomes the bridge
- **Round numbers with no primary source citation** — if the creator is reporting a headline they saw but can't link to a press release, the headline is probably wrong
- **Creator says "according to [Company] the number is X"** — but no press release, blog post, or SEC filing backs it. Treat the named institution as a credibility anchor, not a citation
- **"Tech X pays you to do Y"** is the most common vehicle for this — the structure almost always traces back to a different program

### Detection method
1. When a viral "$X" claim is reported, search `[Brand] + claim keywords` AND `[Brand] + "X" + [topic]` separately
2. The real source usually lives at one URL; the contaminated version lives at many
3. If the official company materials (press releases, white papers, blog posts) do not contain the number, the claim is cross-contaminated
4. Trace the contamination back to its origin to give the user the full story, not just the correction

## "2 hours vs 3.2 million years" — viral benchmark inflation (June 2026)

A **fourth pattern**: a real benchmark result exists, but the numbers get inflated through social media retelling until they bear no resemblance to the original. Unlike cross-contamination (where a number jumps stories), inflation keeps the same story but grows the numbers with each retelling.

- **What the video says:** "A quantum computer just solved something in two hours that would take a classical computer 3.2 million years"
- **The real benchmark:** Google's 2019 Sycamore quantum supremacy experiment — a 53-qubit processor completed a random circuit sampling task in **200 seconds**, with Google estimating a classical supercomputer would take **~10,000 years**
- **IBM's dispute of even that:** IBM argued the same task could be done classically in ~2.5 days with optimizations. By 2022, improved classical algorithms had narrowed the gap further
- **How the inflation happened:** The original "200 seconds vs 10,000 years" got progressively inflated through social media channels. "200 seconds" became "2 hours." "10,000 years" became "3.2 million years." Neither inflated figure appears in any published paper or official source
- **Key distinction from ASR mangling:** The ASR transcript is **correct** — the creator clearly says "3.2 million years" and "two hours." This is not a speech-to-text number collapse. The creator is repeating a number they heard elsewhere. The error is in the claim itself, not the transcription
- **The correct response:** Trace the claim back to the closest real benchmark (Google Sycamore 2019), state the actual numbers, and explain that even those were disputed. Don't just say "wrong" — give the user the real comparison so they understand what quantum computers have actually demonstrated

### Pattern to watch for
When a viral claim cites an extreme performance comparison ("X seconds vs Y million years"), check whether:
- **The numbers appear in any peer-reviewed publication or official press release** — if not, they're inflated
- **A real benchmark exists with smaller but still impressive numbers** — the inflation usually starts from a legitimate result
- **The inflated numbers are round or dramatic** — "3.2 million" has a false-precision quality (the ".2") that makes it sound measured, but it's no more real than "3 million"
- **Multiple sources repeat the same inflated numbers without citation** — viral inflation spreads through retelling, so you'll find many sources with the wrong number and zero with the right one

### Detection method
1. Search for the core claim keywords + "benchmark" or "study" or "Nature" or "paper"
2. Find the closest real published result and compare its numbers to the viral claim
3. If the real result exists but with smaller numbers, it's inflation — trace the inflation chain if possible
4. Note that the creator may be passing along the inflated number in good faith — they heard it, believed it, repeated it. The error is in the information ecosystem, not the creator's honesty

## "Crow funerals" — research program conflation (June 2026)

A **fifth pattern**: two separate experiments from the same lab, studying related but distinct questions, get blended into one seamless "super-experiment" narrative with composite timelines and protocols that don't exist in any single paper.

- **What the video says:** A researcher at the University of Washington conducted experiments where volunteers wore masks while handling dead crows. The crows remembered the masks for weeks, months, a year, two years, five years — alarm calling, dive bombing, and agitated circling. Crows not present during the original encounter also responded. Even crows born after the experiment mobbed the masks.
- **What actually happened — two separate studies:**
  - **Study A (Swift & Marzluff, 2015, *Animal Behaviour*):** The "crow funeral" / dead-crow experiments. Masked volunteers held taxidermied dead crows on territories for 30 minutes. Crows remembered the face associated with the dead crow for **up to 6 weeks**. They also showed location avoidance for up to 72 hours.
  - **Study B (Marzluff et al., 2010, *Animal Behaviour*; Cornell et al., 2012, *Proc. R. Soc. B*):** The "dangerous face" / trapping experiments. Crows were physically trapped and banded by a person wearing a "caveman" mask. Individual crows remembered this mask for **at least 2.7 years**. Over a **5-year period**, the scolding response spread through the population (doubling in frequency, spreading ~1.2 km) via **horizontal social learning** (to crows never trapped) and **vertical social learning** (to offspring born after trapping concluded).
- **How the conflation happened:** Both studies came from the same UW lab (Marzluff + his grad student Swift). Both used masks. Both involved crows learning about threats. The video creator (or their source) encountered both studies in popular-science coverage (TED talks, NPR interviews) where they're often discussed together as "the crow research," and merged them into a single experiment. The 6-week result, the 2.7-year individual memory, and the 5-year population spread became "weeks, months, a year, two years, five years" — a composite timeline.
- **Key distinction from benchmark inflation:** In benchmark inflation, one study's numbers grow. In research program conflation, the numbers are **all real** — they just come from **different experiments with different methodologies**. The error is stitching them together as if one study produced all of them.
- **The correct response:** Identify the individual studies, assign each claim/number to its correct source, and explain why the composite narrative is misleading even though every individual fact is true. Don't call it "wrong" — call it "conflated."

### Pattern to watch for
When a single narrative attributes overlapping findings to "researchers at [University]" or "a study from [Lab]," check whether the findings come from:
- **Multiple papers by the same group** — labs often publish several studies on related topics, and pop-science coverage discusses them as a unit
- **Different methodologies with different timelines** — a field study tracking memory over 6 weeks vs. a trapping study tracking memory over 5 years are not the same experiment
- **Different lead authors** — grad student's thesis project vs. PI's long-running field experiment may study different questions with different scopes

The tell-tale sign is a **composite timeline** ("weeks, months, a year, two years, five years") that no single paper contains. If you can't find one paper that covers the full claimed timeline, you're looking at conflation.

### Detection method
1. Search for the topic + the named institution/researcher to find all relevant papers (not just one)
2. For each claim, identify which paper it actually comes from — check methodology, sample, and timeline
3. If claims span multiple papers, note the conflation and assign each claim to its correct source
4. Pay attention to different lead authors within the same lab — a grad student's thesis is often a distinct experiment from the PI's long-running project
5. Popular-science coverage (TED, NPR, press releases) often discusses a lab's body of work as a unit, making conflation easy for downstream creators

## "93% accuracy from a photograph" — metric confusion + multi-study conflation (June 2026)

A **sixth pattern** that combines two distortions: (a) **metric confusion** — labeling AUC or sensitivity as "accuracy," and (b) an extension of research program conflation where the conflated studies use **different imaging technologies** that look equivalent to a layperson.

- **What the video says:** "An AI trained on 178,000 retinal photographs can detect early Alzheimer's with 93% accuracy, using a standard eye camera."
- **What actually happened — at least three separate studies:**
  - **Study A (ADRET, Dumitrascu et al., 2024, *Mayo Clinic Proceedings: Digital Health*):** 178,803 **unlabeled** UK Biobank fundus photos used for **self-supervised pretraining** only. The actual labeled Alzheimer's training set was ~360 images from ~230 patients. The 178K was not an Alzheimer's training set.
  - **Study B (Eye-AD, Hao et al., Oct 2024, *npj Digital Medicine*):** 5,751 **OCT angiography (OCTA)** images — not photographs — from 1,671 participants. Achieved **AUC of 0.9355** for early-onset AD. Actual **accuracy was ~88.9% internal, ~81.8% external**. The "93%" is the AUC rounded, not accuracy.
  - **Study C (Cheung et al., 2022, *Lancet Digital Health*):** ~13,000 fundus photographs (the actual "standard camera" study). Achieved **83.6% accuracy, 93.2% sensitivity, AUC 0.93**. The "93%" here is *sensitivity*, not accuracy.
- **How the metric confusion happened:** The creator (or their source) encountered both the Eye-AD AUC (0.9355) and the Cheung sensitivity (93.2%) in popular coverage, merged them into "93% accuracy." Both are real numbers — neither is "accuracy." AUC measures discrimination across all thresholds; sensitivity measures the true positive rate at a specific threshold. Neither tells you how often the model is right in practice.
- **The imaging technology conflation:** The video says "from a photograph" and "a standard camera, a flash of light, two seconds." But the 93% (AUC) study used **OCTA** — expensive, specialized equipment most optometry offices don't have. The study that actually used standard fundus photos (Cheung) achieved 83.6% accuracy. The "from a photograph" framing applied the Cheung methodology description to the Eye-AD results.
- **Pretraining-vs-labeled-data conflation:** The 178K images were **unlabeled** — the AI learned what retinas look like, not what Alzheimer's looks like. The actual Alzheimer's-specific training used ~360 labeled images. The video presents 178K as the Alzheimer's training set.
- **Additional source errors:** The cited "Graefe's Archive (May 2026)" is a **narrative review**, not original research. The cited "BrightFocus Foundation (Feb 2025)" article is actually dated **April 14, 2023** — the Feb 2025 date appears confused with an unrelated mouse study.

### Pattern to watch for — metric confusion
When a viral science/health claim cites a specific performance percentage ("93% accuracy!"), check whether the number is actually:
- **AUC (Area Under the ROC Curve)** — measures discrimination across thresholds, ranges 0-1, often reported as "0.93" or "93%." NOT accuracy. A model with AUC 0.93 might have 82% real-world accuracy.
- **Sensitivity (true positive rate)** — among actual cases, how many the model catches. NOT accuracy. A model with 93% sensitivity might have 83% overall accuracy if specificity (true negative rate) is lower.
- **Actual accuracy** — overall correct predictions / total predictions. This is what "accuracy" means to a layperson and what matters clinically.

The pattern: "93%" appears in multiple papers about the same topic — as AUC in one, as sensitivity in another — and gets merged into a single "93% accuracy" claim. Always check which metric the original paper reports, not what the popular coverage says.

### Pattern to watch for — pretraining vs. labeled training data
When a claim says "trained on N images," check whether those N images were:
- **Labeled training data** (images with known diagnoses used to teach the model the disease pattern)
- **Unlabeled pretraining data** (general images used to teach the model what the input looks like, before fine-tuning on labeled data)

Large pretraining datasets (100K+) are often presented as if they're the disease-specific training set. The actual labeled dataset is usually much smaller (hundreds to low thousands). This inflates apparent training scale by 100-1000x.

### Detection method
1. When a medical/AI claim cites a performance percentage, search for the original paper and check the **exact metric** (AUC, sensitivity, specificity, accuracy)
2. When a claim says "trained on N images," search for whether N refers to pretraining or fine-tuning — look for phrases like "self-supervised," "unsupervised," "pretrained on," vs. "labeled," "annotated," "fine-tuned on"
3. When a claim says "photographs" or "standard camera," check the paper's imaging modality — OCTA, MRI, CT are NOT photographs even though they produce images
4. When multiple sources are cited, verify each source's date and type (primary research vs. review vs. press release) independently for the Alzheimer's retinal AI pattern above — the "Graefe's Archive" was a review, not original research, and the "BrightFocus Foundation" date was wrong by two years.

## "Stored electricity in sand" — company-claimed numbers + thermal-vs-electrical conflation (June 2026)

A **seventh pattern**: a technology video reports company-claimed performance numbers as fact, and conflates thermal energy storage with electrical energy storage. Unlike academic research conflation (where multiple peer-reviewed studies get blended), this pattern involves a single company's press releases repeated by a media outlet without independent verification.

- **What the video says:** "An AI trained on 178,000 photographs... stores 100 MWh... 93% accuracy" — wait, wrong video. The sand battery video says: "Store electricity in sand... 100 MWh of thermal energy... 80-90% round-trip efficiency... 100% oil reduction, 70% emissions cut."
- **What actually happened:**
  - The 100 MWh is **thermal energy (heat)**, not electrical energy. The system converts electricity to heat, stores it, and returns it as heat for district heating. It cannot power lights, computers, or EVs. The framing "store electricity in sand" implies grid-scale electrical storage, which this isn't.
  - The "sand" is actually **crushed soapstone** — a byproduct from Finnish fireplace manufacturing. Soapstone was chosen for higher specific heat capacity and density. "Sand battery" is company branding, not the actual material.
  - The 80-90% round-trip efficiency is **electricity-to-heat-to-heat**, not electricity-to-electricity. Comparing it to lithium-ion batteries (85-95% electricity-to-electricity) is apples-to-oranges.
  - All performance numbers (100% oil reduction, 70% CO2 cut, 60% wood chip reduction, 80-90% efficiency) are **company-claimed**, corroborated by the customer (Loviisan Lämpö) and investor (CapMan Infra) — parties with financial interest. No independent third-party audit exists.
  - The underlying technology (packed-bed thermal storage) is decades old. What's new is the application, branding, and business model.

### Pattern to watch for — thermal vs. electrical energy
When a technology video says "stores energy" or "battery," check whether the stored energy is:
- **Electrical energy** (electricity in, electricity out — like lithium-ion, pumped hydro)
- **Thermal energy** (electricity in, heat out — like sand batteries, molten salt, refractory brick)

The "battery" branding is applied to both, but they solve different problems. Thermal storage addresses heating demand (~50% of global final energy), not grid electricity storage. A "100 MWh battery" that stores heat is not comparable to a "100 MWh battery" that stores electricity.

### Pattern to watch for — company-claimed performance vs. independently verified
When a technology video reports performance numbers (efficiency, emissions reductions, cost savings), check whether the numbers are:
- **Company-claimed** — from press releases, company blog, or CEO interviews
- **Corroborated by customer/investor** — meaningful but not independent (customer and investor have financial interest)
- **Independently verified** — by a third-party audit, academic study, or regulatory filing

Tech media often repeats company press releases verbatim without attribution. The numbers may be real but unverified. Awards and recognitions (TIME Best Inventions, industry awards) are NOT independent performance audits.

### Detection method
1. Search for the company name + performance claim keywords to find the original source
2. Check whether the numbers appear only in company press releases or also in independent coverage
3. Look for phrases like "company claims," "according to [CEO]," "expects to" vs. "has achieved"
4. Awards and recognitions validate market interest but not performance numbers — don't treat them as verification
5. When "battery" is used for a thermal storage system, clarify the energy form (heat vs. electricity) early in the research output

## "A UK company with the acronym of ARIA" — organization mischaracterization (July 2026)

A **ninth pattern**: a creator mischaracterizes what type of organization is behind a project, calling a government agency a "company," a university research lab a "startup," or a publicly funded program a "private venture." Unlike institution misattribution (where a fake number is attributed to a real institution), this pattern misrepresents the *nature* of the institution itself.

- **What the video says:** "This project is called re-thickening Arctic Sea Ice, and it's done by a UK company with the acronym of ARIA."
- **What ARIA actually is:** The Advanced Research and Invention Agency — a UK government R&D funding agency. It is an executive non-departmental public body sponsored by the Department for Science, Innovation and Technology (DSIT). It was established by the Advanced Research and Invention Agency Act 2022, launched in January 2023, with an initial allocation of approximately £800 million in taxpayer funding. It operates like a civilian DARPA. It is not a company.
- **Furthermore:** ARIA does not directly conduct the ice thickening experiments. It **funds** the research through grants. The actual field work is conducted by Real Ice (a UK company) and Arctic Reflections (another funded team), with the RASI project led by the University of Cambridge's Centre for Climate Repair.
- **Why it matters:** Calling a government agency a "company" implies private ventures are solving climate problems, when in reality this is publicly funded, transparent research with government oversight, community engagement requirements, and a statutory mandate to serve the public interest. The nature of the institution determines accountability, transparency, and governance — all critical context for the viewer.

### Pattern to watch for
When a transcript names an organization behind a project or claim, verify what *type* of organization it is:
- **Government agency** (funded by taxpayers, created by legislation, accountable to the public) — e.g., ARIA, DARPA, NASA, NIH, EPA
- **University research lab** (academic, peer-reviewed, often publicly funded) — e.g., Centre for Climate Repair at Cambridge
- **Private company** (profit-driven, accountable to shareholders) — e.g., Real Ice, Arctic Reflections
- **Nonprofit/NGO** (mission-driven, accountable to a board) — e.g., World Wildlife Fund

Creators often default to "company" because it's the simplest word. But government agencies have transparency requirements, statutory mandates, and public accountability that companies don't. University labs have peer review and academic freedom. These distinctions matter for how the viewer should evaluate the credibility and motivations of the work.

### Detection method
1. Search for the named organization + "about" or "what is" to find its official description
2. Check government websites (gov.uk, usa.gov) for agencies — they are listed as public bodies
3. Check legislation — government agencies are typically established by acts of parliament/congress
4. Look for the funding chain: who funds the project, who conducts the research, who reports to whom?

## "Polar ice caps melting raises sea levels" — sea ice vs land ice conflation (July 2026)

A **tenth pattern**: a climate claim conflates sea ice (floating in the ocean) with land ice (on Greenland, Antarctica, glaciers), attributing sea level rise to the wrong type of ice. This is one of the most common climate misconceptions in popular science content.

- **What the video says:** "The polar ice caps are melting, and it's not only raising the sea levels around the world..."
- **What actually happens:** Arctic sea ice is already floating in the ocean. By Archimedes' principle, it displaces its own weight in seawater. When it melts, the meltwater fills exactly the volume it was displacing, with only a ~2.6% additional volume from the density difference between fresh water and salt water (Noerdlinger and Brower, 2007). The NSIDC states: "Sea ice melt is not a significant contributor to sea level rise."
- **The real drivers of sea level rise are:**
  1. **Thermal expansion** — warming ocean water expands, accounting for roughly one-third of observed sea level rise
  2. **Land ice melt** — the Greenland ice sheet, Antarctic ice sheet, and mountain glaciers flowing into the ocean. Greenland alone accounts for about 46% of Arctic land ice contribution to sea level rise
  3. Together, thermal expansion and land ice melt account for the vast majority of sea level rise
- **The correlation trap:** Sea ice loss and sea level rise are correlated because the same warming temperatures cause both. But correlation is not causation — melting sea ice does not cause significant sea level rise. The NSIDC warns: "Prolonged sea ice loss indicates that sea level rise could worsen because the same warming pressures drive both sea ice melt and sea level rise."

### Pattern to watch for
When a climate video says "melting ice caps raise sea levels," check whether they're talking about:
- **Sea ice** (Arctic Ocean ice, Antarctic sea ice) — already floating, minimal sea level contribution (~2.6%)
- **Land ice** (Greenland ice sheet, Antarctic ice sheet, mountain glaciers) — the real driver of ice-caused sea level rise

The "polar ice caps" phrasing is ambiguous — it could refer to either. But when a video shows footage of the Arctic Ocean (sea ice) while talking about sea level rise, it's conflating the two. The ice thickening project (RASI) specifically targets sea ice, which means it would have negligible direct impact on sea level — its climate value is through the albedo effect (reflecting sunlight), not preventing sea level rise.

### Detection method
1. When a claim links "ice melt" to "sea level rise," identify the ice type: floating sea ice or land-based ice
2. Search NSIDC ("Does sea ice melt raise sea level?") for the authoritative answer
3. If the video shows Arctic Ocean footage while discussing sea level rise, flag the conflation
4. Note that the ~2.6% figure (Noerdlinger & Brower) is real but small — don't say sea ice has "zero" effect, say it's "not a significant contributor"
