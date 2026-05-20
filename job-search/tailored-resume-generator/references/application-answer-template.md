# Application Answer Templates

## "Why do you want to join [Company] specifically and what makes you a great fit?"

This is the most common free-text application question. Structure your answer in two parts:

### Part 1: Why this company (100-150 words)

Open with what genuinely excites you about the company — be specific. Reference:
- Their mission or product in concrete terms (not "I love your mission")
- A specific customer segment, use case, or recent milestone (funding round, user count, product launch)
- The stage/size if it matters to you (e.g., "Series B with 250 people means I can shape process, not just inherit it")

Then connect to the role: describe the *type of problem* you'd be solving and why that's what you love doing.

**Template:**
> What grabbed me is [specific thing about company/product]. I've spent [X years] doing [relevant work], and the idea of [specific aspect of role] is genuinely exciting to me. I want to be part of [concrete goal], not just sell it.
>
> The role itself is exactly where I thrive. [Describe the core work in their words]. At [Current Company] I did this daily: [one-line concrete example]. That [relationship-building / problem-solving / technical depth] under pressure is what I love, and [Company]'s description of [quote or paraphrase from JD] is the exact kind of problem I want to own.
>
> I also care about the stage. [Funding/valuation/team size context] means there's real traction but still room to shape how things work. I don't want to join a 5,000-person org and inherit a playbook — I want to help write it.

### Part 2: What makes you a great fit (100-150 words)

Pick 3 things from the JD that map most directly to your experience. For each:
1. Name the skill/requirement
2. Give a one-line concrete example from your resume
3. Quantify if possible

Close with an honest, brief note about any gap — frame it as "here's how I'd ramp" rather than apologizing.

**Template:**
> Three things map directly:
>
> 1. **[Skill/requirement from JD]:** [One-line example from your experience]. [Quantify if possible.]
>
> 2. **[Skill/requirement from JD]:** [One-line example].
>
> 3. **[Skill/requirement from JD]:** [One-line example].
>
> [Optional gap acknowledgment]: The one thing I'd flag: [honest gap]. But [bridging language — adjacent experience, fast learner, specific ramp plan].

### Tone notes
- Write in first person. Conversational but professional — like you're talking to a human, not writing an essay.
- 250-350 words total is the sweet spot. Recruiters skim.
- Never generic. If you could swap the company name out and it still works, it's too vague.
- Specificity > enthusiasm. "I helped an enterprise customer debug a SAML integration that was blocking 200 users" beats "I'm passionate about identity."

---

## Platform-Specific Patterns

### Greenhouse
- **Question location:** Free-text questions appear at the bottom of the job listing page, after the demographic survey. Extract them during JD analysis.
- **Word limit:** Greenhouse text fields typically accept ~250 words. Draft answers to fit — recruiters skim, and the field may silently truncate longer responses.
- **Common question types:**
  - "Why are you interested in [Company]?" — Use the template above.
  - "Will you now or in the future require sponsorship?" — Binary yes/no, not a writing opportunity.
  - Custom role-specific questions — Vary by company, but often ask about difficult wins, process improvements, or domain-specific experience.
- **No cover letter field by default:** Some Greenhouse listings include an optional cover letter upload, but many only have the free-text questions. Treat the questions as your cover letter — they're the only narrative space you get.

### Ashby
- **Question location:** Free-text questions appear on the application form, often after basic info fields.
- **Common patterns for technical writer roles:**
  - "Please submit multiple examples of your own writing" — See Writing Portfolio section below.
  - "Please add up to three bullets showing exceptional ability" — See Exceptional Ability Bullets section below.
- **Word limit:** Ashby fields are generally generous (~1000+ chars), but keep answers concise.

---

## Additional Application Question Templates

### "How would you approach building [X] from scratch?"
Structure: Audit → Foundation → First Win
- **Phase 1 (Audit):** Assess current state, map gaps, understand user needs
- **Phase 2 (Foundation):** Establish processes, tooling, standards (Docs-as-Code workflows, style guides, templates)
- **Phase 3 (First Win):** Ship high-impact content first (getting-started guide, onboarding tutorial, most-requested doc)

Template:
> I'd start with three things in the first 90 days:
>
> **1. Audit and restructure.** [Read every existing doc / map the user journey / identify gaps]. At [Company], I did this by [specific example].
>
> **2. Establish the foundation.** [Set up Git workflow, contribution guidelines, style guide, review process, templates for common doc types].
>
> **3. Ship the first high-impact content.** [The single most important doc for adoption — getting-started guide, onboarding tutorial, etc.]

### "Describe a time you [created/delivered/achieved] something that significantly impacted [adoption/revenue/customer success]"
Structure: Problem → Action → Measurable Result → Lesson
- **Problem:** What was broken or missing (with quantified impact — ticket volume, time wasted, churn risk)
- **Action:** What you specifically built/created (be concrete — "wrote an API integration guide" not "improved documentation")
- **Result:** Quantified outcome (ticket reduction, onboarding speed, adoption rate, self-service resolution)
- **Lesson:** One insight that shows strategic thinking

Template:
> At [Company], [specific problem with quantified impact].
>
> I [specific action — what you created, built, or authored]. [One sentence on the content/structure/approach].
>
> The result: [quantified outcome]. [Secondary positive effect].
>
> The key insight was [one sentence showing you understand why it worked — user perspective, content structure, delivery method].

### "Please add up to three bullets showing exceptional ability"
These are resume-level impact statements, not interview answers. Each bullet should:
1. Lead with the outcome or scale (not the activity)
2. Include a specific metric or scope indicator
3. Demonstrate a skill that distinguishes the candidate from peers

Format: 1-2 sentences each. Bold the first clause (the outcome), then explain.

Template bullets:
1. **[Built/founded/created] [something from zero] for a [X]-person organization.** [One sentence on what it became and why it matters].
2. **[Achieved/delivered] [specific measurable outcome] by [specific action].** [One sentence on the mechanism or approach].
3. **[Unique differentiator — domain expertise, user empathy, cross-functional bridge].** [One sentence explaining why this is rare or valuable].

---

## Writing Portfolio Samples for Technical Writer Applications

When applying for technical writer roles that request writing samples, create targeted portfolio pieces that demonstrate the exact skills the JD requires. Generic blog posts are weak — purpose-built docs are strong.

### Strategy
1. **Audit the JD for doc types mentioned:** API references, getting-started guides, tutorials, code samples, white papers, educational materials
2. **Create 2-3 samples** that cover the most-requested doc types
3. **Use a fictional but realistic product** in the target company's domain (e.g., for a secrets management company, create docs for a fictional secrets management API)
4. **Include code samples** in languages the JD mentions (Python, Node.js, Bash, etc.)
5. **Use Docs-as-Code formatting** — clean Markdown with proper headings, code blocks, tables, admonitions

### Recommended Portfolio Pieces

**Piece 1: Getting Started Guide** — Developer onboarding flow
- Introduction explaining why the technology matters
- Prerequisites section
- Step-by-step setup (install → configure → first use)
- Code samples in 2-3 languages
- Common pitfalls / troubleshooting
- This is the highest-impact doc type — every company needs it

**Piece 2: API Reference** — Full endpoint documentation
- Overview with authentication
- 3-5 endpoints with consistent structure: description, parameters (table), request example (curl + one language), response schema, error codes
- Rate limiting, pagination, error handling sections
- Use Stripe/Twilio as the quality benchmark

**Piece 3: Existing blog posts or articles** — Shows communication breadth
- Pick the most technical posts that demonstrate ability to explain complex topics clearly
- Link directly in the application form

### Where to Host
- **GitHub repo** (best — simultaneously shows Docs-as-Code skills)
- **Personal blog** (good if already established)
- **Paste into application text field** (fallback — works for Markdown-formatted content)

### Naming Convention
Save portfolio pieces to `~/Documents/Resumes/portfolio/` with descriptive names:
- `secrets-management-getting-started.md`
- `api-reference-secrets-management.md`
- These files are reusable across applications in the same domain
