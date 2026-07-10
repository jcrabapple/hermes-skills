---
name: tailored-resume-generator
description: Analyzes job descriptions and generates tailored resumes that highlight relevant experience, skills, and achievements to maximize interview chances
---

# Tailored Resume Generator

## Role Reframing & Application Questions

> See [references/role-reframing.md](references/role-reframing.md) for reusable
> reframing patterns (Support → SE, Support → CS/TAM, Support → Infrastructure/Cloud,
> Support → Technical Writer, Support → CX Leadership) and application question
> drafting strategies.
>
> See [references/application-answer-template.md](references/application-answer-template.md)
> for the "Why this company + fit" answer template and tone guidance.

## DOCX Conversion

> Use the reusable build script: [scripts/md_to_docx.py](scripts/md_to_docx.py)
> Handles all standard resume markdown → formatted DOCX. No need to rewrite
> the conversion each time. See the script header for prerequisites.

## When to Use This Skill

- Applying for a specific job position
- Customizing your resume for different industries or roles
- Highlighting relevant experience for career transitions
- Optimizing your resume for ATS (Applicant Tracking Systems)
- Creating multiple resume versions for different job applications
- Emphasizing specific skills mentioned in job postings

## What This Skill Does

1. **Analyzes Job Descriptions**: Extracts key requirements, skills, qualifications, and keywords from job postings
2. **Identifies Priorities**: Determines what employers value most based on the job description language and structure
3. **Tailors Content**: Reorganizes and emphasizes relevant experience, skills, and achievements
4. **Optimizes Keywords**: Incorporates ATS-friendly keywords naturally throughout the resume
5. **Formats Professionally**: Creates clean, professional resume layouts suitable for various formats
6. **Provides Recommendations**: Suggests improvements and highlights gaps to address

## How to Use

### Basic Usage
Provide a job description and your background information:

```
I'm applying for this job:

[paste job description]

Here's my background:
- 5 years as software engineer at TechCorp
- Led team of 3 developers on mobile app project
- Expert in Python, JavaScript, React
- Computer Science degree from State University
```

### With Existing Resume
Upload or paste your current resume along with the job description:

```
Please tailor my resume for this position:

Job Description:
[paste job description]

My Current Resume:
[paste resume content]
```

### Career Transition
When changing industries or roles:

```
I'm transitioning from marketing to product management.
Here's the job I'm applying for:

[paste job description]

My transferable experience:
- 7 years in digital marketing
- Led cross-functional teams
- Managed product launches
- Data analysis and A/B testing
```

## Example

**User Request:**
```
I need a tailored resume for this job:

Senior Data Analyst Position

Requirements:
- 5+ years experience in data analysis
- Expert in SQL, Python, and data visualization tools
- Experience with A/B testing and statistical analysis
- Strong communication skills to present findings
- Healthcare industry experience preferred

My background:
- Data Analyst at RetailCo (2019-2024)
- Created dashboards using Tableau and Power BI
- Built Python scripts for data automation
- Worked with marketing team on campaign analysis
- Business Analytics degree
- Also did 1 year internship at HealthPlus clinic
```

**Generated Output:**

```markdown
# JOHN DOE
Email: john.doe@email.com | Phone: (555) 123-4567 | Location: City, State

## PROFESSIONAL SUMMARY
Results-driven Data Analyst with 5+ years of experience leveraging SQL, Python, and advanced
visualization tools to deliver actionable insights. Proven track record in statistical analysis,
A/B testing, and cross-functional collaboration. Healthcare industry experience with strong
ability to communicate complex data findings to stakeholders.

## TECHNICAL SKILLS
- **Data Analysis & Programming**: SQL, Python, Statistical Analysis, A/B Testing
- **Visualization Tools**: Tableau, Power BI, Advanced Dashboard Development
- **Data Management**: Data Automation, ETL Processes, Database Optimization
- **Business Intelligence**: Campaign Analytics, Performance Metrics, KPI Tracking

## PROFESSIONAL EXPERIENCE

**Data Analyst** | RetailCo | 2019 - 2024
- Designed and implemented 50+ SQL queries and Python automation scripts, reducing manual
  data processing time by 60%
- Conducted rigorous A/B testing and statistical analysis for marketing campaigns,
  improving campaign ROI by 35%
- Built interactive Tableau and Power BI dashboards for executive team, enabling
  data-driven decision making
- Presented analytical findings to cross-functional stakeholders including marketing,
  operations, and executive leadership
- Collaborated with marketing team to analyze customer behavior patterns and optimize
  targeting strategies

**Data Analysis Intern** | HealthPlus Clinic | 2018 - 2019
- Supported healthcare analytics initiatives by analyzing patient data and operational metrics
- Gained exposure to healthcare industry data management and HIPAA compliance requirements
- Assisted in creating reports for clinical staff to improve patient care workflows

## EDUCATION

**Bachelor of Science in Business Analytics**
State University | Graduated 2018

## KEY ACHIEVEMENTS
- Reduced data processing time by 60% through Python automation
- Improved marketing campaign ROI by 35% through A/B testing and optimization
- Created data visualization system now used across entire organization
```

**Additional Recommendations:**
- Consider adding any specific healthcare projects or certifications
- Quantify more achievements with metrics when possible
- If you have experience with R or advanced statistical methods, add them
- Consider mentioning any familiarity with healthcare regulations (HIPAA, etc.)

---

## Instructions

When a user requests resume tailoring:

### 0. Verify the Job URL Matches Intent (Critical)

When the user provides a URL, **always extract and check the actual job title before proceeding.** Users often paste a URL from a prior conversation or search session — the job at that link may differ from what they discussed. If the extracted title doesn't match the role context, flag it immediately and confirm before tailoring.

Example: User says "tailor my resume for this Technical Support Manager job" but the URL points to a Solutions Engineer listing. Tailoring for the wrong role wastes a full cycle.

### 1. Gather Information

**Job Description Analysis**:
- Request the full job description if not provided
- Ask for the company name and job title

**Candidate Background**:
- **Proactively search for existing resume files** (common locations: ~/Documents, ~/Desktop, ~/Downloads) — ask the user to confirm if found. When multiple resumes exist, see [references/base-resume-selection.md](references/base-resume-selection.md) for selection strategy (leadership framing > technical overlap for leadership roles).
- If user provides existing resume (inline or file), use it as the foundation
- If no resume found, request:
  - Work history (job titles, companies, dates, responsibilities)
  - Education background
  - Key skills and technical proficiencies
  - Notable achievements and metrics
  - Certifications or awards
  - Any other relevant information

### 2. Analyze Job Requirements

Extract and prioritize:
- **Must-have qualifications**: Years of experience, required skills, education
- **Key skills**: Technical tools, methodologies, competencies
- **Soft skills**: Communication, leadership, teamwork
- **Industry knowledge**: Domain-specific experience
- **Keywords**: Repeated terms, phrases, and buzzwords for ATS optimization
- **Company values**: Cultural fit indicators from job description

Create a mental map of:
- Priority 1: Critical requirements (deal-breakers)
- Priority 2: Important qualifications (strongly desired)
- Priority 3: Nice-to-have skills (bonus points)

### 3. Map Candidate Experience to Requirements

For each job requirement:
- Identify matching experience from candidate's background
- Find transferable skills if no direct match
- Note gaps that need to be addressed or de-emphasized
- Identify unique strengths to highlight

### 4. Structure the Tailored Resume

**Professional Summary** (3-4 lines):
- Lead with years of experience in the target role/field
- Include top 3-4 required skills from job description
- Mention industry experience if relevant
- Highlight unique value proposition

**Technical/Core Skills Section**:
- Group skills by category matching job requirements
- List required tools and technologies first
- Use exact terminology from job description
- Only include skills you can substantiate with experience

**Professional Experience**:
- For each role, emphasize responsibilities and achievements aligned with job requirements
- Use action verbs: Led, Developed, Implemented, Optimized, Managed, Created, Analyzed
- **Quantify achievements**: Include numbers, percentages, timeframes, scale
- Reorder bullet points to prioritize most relevant experience
- Use keywords naturally from job description
- Format: **[Action Verb] + [What] + [How/Why] + [Result/Impact]**

### Bullet Writing Frameworks (from Resume Bullet Writer)

Apply these frameworks to transform weak bullets into achievement-focused statements:

**X-Y-Z Formula (Google Method):**
> "Accomplished [X] as measured by [Y] by doing [Z]"

- **X** = What you achieved
- **Y** = How you measured it  
- **Z** = What actions you took

Example:
```
❌ BEFORE: "Managed social media accounts"
✅ AFTER: "Grew Instagram following by 250% (5K to 17.5K) by implementing daily content calendar and influencer partnerships"
```

**STAR Method (condensed for bullets):**
> [Situation] + [Task] + [Action] + [Result]

Example:
```
"Inherited underperforming sales team (S) with 65% quota attainment. Tasked with improving performance within Q1 (T). Implemented new training program and revised commission structure (A). Achieved 92% quota attainment by Q2, generating $1.8M additional revenue (R)."
```

**Power Verbs by Category:**
- Leadership: Led, Directed, Managed, Spearheaded, Orchestrated
- Achievement: Achieved, Delivered, Exceeded, Surpassed, Attained
- Growth: Grew, Increased, Boosted, Expanded, Scaled
- Creation: Created, Developed, Designed, Built, Launched
- Optimization: Streamlined, Optimized, Enhanced, Improved, Automated
- Analysis: Analyzed, Assessed, Evaluated, Identified, Diagnosed
- Collaboration: Collaborated, Partnered, Facilitated, Coordinated
- Problem-Solving: Resolved, Solved, Troubleshot, Eliminated, Reduced

### Quantification Strategies (from Resume Quantifier)

**Rule:** Every bullet should have at least ONE number.

**Metric Categories:**
1. **Money**: Revenue generated, costs saved, budget managed, deal sizes
2. **Percentages**: Growth rates, improvement percentages, efficiency gains
3. **Time**: Hours saved, cycle time reduced, project duration, response times
4. **Volume/Scale**: People managed, projects delivered, customers served, users impacted
5. **Quality**: Satisfaction scores, error rates, accuracy rates, compliance rates
6. **Frequency**: Per day/week/month, annual totals, meeting cadences

**When exact numbers aren't available:**
- Use conservative estimates: "~40%" or "75+ hours"
- Use ranges: "Managed team of 8-12" or "$100K-$150K in revenue"
- Use minimum bounds: "Served 100+ customers daily"
- Calculate from known totals: "Company had 1000 customers → managed 200 accounts (20%)"

**Quantification Templates:**
```
Before/After: "Improved [X] from [before] to [after], resulting in [Y]% improvement"
Scale: "[Verb] [number] [things], resulting in [impact]"
Volume+Impact: "Processed [number] [items] per [time], achieving [quality metric]"
```

### Career Change Translation (from Career Changer Translator)

When user is changing careers/industries, use these translation patterns:

**Universal Transferable Skills:**
- Leadership → Team leadership, project management, strategic planning
- Communication → Presentation skills, stakeholder management, cross-functional collaboration
- Analytical → Data analysis, problem-solving, process improvement, decision-making
- Technical → Process design, systems implementation, quality assurance, vendor management

**Industry Translation Examples:**
- Teacher → Corporate Trainer: "Taught 25 students" → "Designed curriculum for 25 learners, achieving 95% proficiency"
- Military → Corporate: "Commanded platoon of 30" → "Led cross-functional team of 30 through high-stakes operations"
- Retail → Sales: "Sold products to customers" → "Consistently exceeded sales targets by 125%, generating $500K annual revenue"
- Hospitality → Customer Success: "Managed front desk" → "Served as primary contact for 100+ daily guests, resolving escalated issues with 95% satisfaction"

**Key Principle:** Translate experience into the target industry's language while maintaining truthfulness.

### Technical Resume Optimization (from Tech Resume Optimizer)

For technical roles (SWE, PM, Data, DevOps):

**Technical Bullet Formula:**
> [Action Verb] + [Technical What] + [Scale/Impact] + [Technology Used]

Example:
```
✅ "Architected microservices migration from monolith, reducing deployment time from 2 hours to 15 minutes and enabling independent team deployments"
✅ "Optimized PostgreSQL queries and implemented Redis caching, reducing API latency by 60% (from 500ms to 200ms) for 100K daily active users"
```

**Technical Metrics to Include:**
- Scale: "serving 500K DAU", "handling 10K requests/second", "processing 50TB daily"
- Performance: "reduced from Xms to Yms", "improved by X%", "decreased by X seconds"
- Efficiency: "reduced AWS costs by 40%", "cut deployment time from X to Y"
- Business: "features drove $XM revenue", "improved conversion by X%"

**Technical Skills Section Organization:**
- **By Category**: Languages, Frameworks, Databases, Cloud/Infrastructure, Tools
- **By Proficiency**: Expert, Proficient, Familiar (use carefully)
- **Flat List**: Simple comma-separated list (most ATS-friendly)

**What to Include for Tech Roles:**
- GitHub URL (required for SWE)
- Portfolio/personal website
- LinkedIn
- Tech blog (if applicable)

**Education**:
- List degrees, certifications relevant to position
- Include relevant coursework if early career
- Add certifications that match job requirements

**Optional Sections** (if applicable):
- Certifications & Licenses
- Publications or Speaking Engagements
- Awards & Recognition
- Volunteer Work (if relevant to role)
- Projects (especially for technical roles)

### 5. Optimize for ATS (Applicant Tracking Systems)

**ATS Compatibility Checklist (from Resume ATS Optimizer):**

**File Format:**
- ✅ Use .docx or .pdf (not .pages, .odt)
- ✅ PDF must be text-based, not scanned image
- ✅ File name: "FirstName_LastName_Resume.pdf"

**Font & Formatting:**
- ✅ Standard fonts: Arial, Calibri, Georgia, Times New Roman
- ✅ Font size: 10-12pt for body, 14-16pt for headers
- ✅ No text boxes, tables, or columns
- ✅ No headers/footers (put contact info in body)
- ✅ No images, graphics, or charts
- ✅ Consistent date formats (MM/YYYY)
- ✅ Standard bullet points (•, -, *)

**Section Headers (use standard, recognizable headers):**
- ✅ "Professional Experience" or "Work Experience"
- ✅ "Education"
- ✅ "Skills" or "Technical Skills"
- ✅ "Summary" or "Professional Summary"

**Contact Information (NOT in header/footer):**
```
John Smith
email@example.com | (555) 123-4567 | LinkedIn: linkedin.com/in/johnsmith
San Francisco, CA
```

**Keyword Optimization:**
- Incorporate exact keywords from job description naturally
- Include both acronyms and full terms (e.g., "SQL (Structured Query Language)")
- Match job title terminology where truthful
- Critical keywords: Appear 2-4 times throughout resume
- Important keywords: Appear 1-2 times
- Don't keyword stuff - keep it natural

**Match Score Calculation:**
```
Match Score = (Keywords Matched / Total Required Keywords) × 100
Target: 80%+ for strong match
```

**ATS Red Flags to Avoid:**
- ❌ Tables for contact info
- ❌ Special characters in email
- ❌ Multiple phone numbers
- ❌ Full mailing address (city/state is enough)
- ❌ Non-standard fonts
- ❌ Skill bars or progress indicators
- ❌ Emojis or color for essential information

### 6. Format and Present

**Format Options**:
- **Markdown**: Clean, readable, easy to copy
- **Plain Text**: ATS-optimized, safe for all systems
- **Tips for Word/PDF**: Provide formatting guidance

**Resume Structure Guidelines**:
- Keep to 1 page for <10 years experience, 2 pages for 10+ years
- Use consistent formatting and spacing
- Ensure contact information is prominent
- Use reverse chronological order (most recent first)
- Maintain clean, scannable layout with white space

### 7. Provide Strategic Recommendations

After presenting the tailored resume, offer:

**Strengths Analysis**:
- What makes this candidate competitive
- Unique qualifications to emphasize in cover letter or interview

**Gap Analysis**:
- Requirements not fully met
- Suggestions for addressing gaps (courses, projects, reframing experience)

**Interview Preparation Tips**:
- Key talking points aligned with resume
- Stories to prepare based on job requirements
- Questions to ask that demonstrate fit

**Cover Letter Hooks**:
- Suggest 2-3 opening lines for cover letter
- Key achievements to expand upon

---

## Interview Talking Points Mapping (Resume-to-JD Analysis)

This is a distinct workflow from resume generation. Use it when the user has an upcoming interview and wants to map their existing experience to the job description requirement-by-requirement, with scripted talking points and gap mitigation.

### When to Use
- User says "I have an interview" or "help me prepare for an interview"
- User asks to map their resume to a specific JD
- User wants talking points, not a rewritten resume
- User needs salary data to anchor their negotiation

### Workflow

#### Step 1: Gather Intelligence
1. **Find salary/compensation data**: Search web for the specific company + role. Check Glassdoor, Levels.fyi, company careers page, and the job posting itself. Note the posted range and market benchmarks.
2. **Retrieve the user's resume**: Proactively look in `~/Documents/Resumes/`, `~/Desktop/`, or `~/Downloads/` for `.docx`, `.pdf`, or `.md` files. Ask the user to confirm if found.
3. **Retrieve the full JD**: If the user only pasted a snippet, search for the complete posting or extract it from the URL.

#### Step 2: Read Resume Files (Troubleshooting)
- **DOCX**: Try `pandoc` first. If unavailable, use `python-docx` via terminal (not `execute_code`, due to venv import path issues). Read all paragraphs.
- **PDF**: Use `pdftotext` or PyPDF2 in terminal.
- **Markdown/txt**: Read directly with `read_file`.

#### Step 3: Map Requirements to Resume Bullets
For **each distinct requirement or responsibility** in the JD:
1. **Quote the JD requirement** verbatim or paraphrase closely.
2. **Draft a talking point**: A 1-2 sentence narrative the candidate can say in the interview. Use first-person ("I have...", "In my current role I...").
3. **Cite evidence from the resume**: Quote the exact resume bullet(s) that support this. Be specific — don't generalize.
4. **Flag gaps honestly**: If no direct match exists, provide **bridging language** — e.g., "I haven't used Datadog specifically, but I'm proficient in Grafana and Mode, so I'm confident I can get up to speed fast."

**Output format for each mapping:**
```
**[Number]. "[JD requirement text]"**

Your talking point:
"[1-2 sentence interview-ready narrative]"

Evidence from your resume:
- "[exact resume bullet]"
- "[exact resume bullet]"

Gaps to address:
[bridging language or none]
```

#### Step 4: Salary Anchoring
- Compare the user's years of experience to the JD's stated requirement (e.g., JD asks for 3–5 years, user has 10+).
- Reference the Glassdoor/market range found in Step 1.
- Recommend a specific anchor range (e.g., "With 10+ years, target $160K–$170K base").
- Remind them to ask about equity if it's a startup.
- Provide a floor: "Anything below $X for this role with your experience is underpaying."

#### Step 5: Summarize Gaps & Strengths
- **Top 3 strengths**: The areas where the user's profile most clearly exceeds the JD.
- **Gaps to prepare for**: Requirements with weak or no direct match, plus the exact bridging language to use.
- **Behavioral stories to prep**: Suggest 2-3 STAR-format stories based on the mapped evidence.

### Example Output Structure
```
**Salary context**: Glassdoor estimates $105K–$170K. OpenRouter advertises "top-of-market" packages.

**Your anchor**: $160K–$170K base (you exceed the 3–5 year requirement significantly).

---

**1. "Own the technical resolution... first line of defense for code-level debugging"**

Your talking point:
"I've spent the last four years as the primary escalation resource between Support and Engineering. I reproduce, isolate, and either resolve or hand off fully scoped bugs to Engineering with root cause identified."

Evidence from your resume:
- "Act as primary escalation resource for complex customer-reported issues, coordinating resolution between Support and Engineering"
- "Write and troubleshoot PowerShell and Bash scripts for endpoint management automation, directly impacting product debugging and issue reproduction"

Gaps to address:
None — this is a core strength.

---

**2. "Experience with Datadog, Cloudflare logs, or GCP Cloud Logging"**

Your talking point:
"I haven't used Datadog specifically, but I live in Grafana and Mode daily for observability. I'm confident I can transfer those skills quickly."

Evidence from your resume:
- "Leverage Mode and Grafana for data analysis and visualization to quantify issue scope, track trends, and inform cross-functional decisions"

Gaps to address:
No direct Datadog/Cloudflare experience. Frame as adjacent-tool proficiency + fast learner.
```

### Best Practices for This Workflow
- **Never fabricate evidence**: Only cite bullets that actually exist in the resume.
- **Be honest about gaps**: Interviewers detect BS instantly. Bridging language is more credible than pretending.
- **Use exact quotes**: Paraphrasing weakens the mapping. Quote resume bullets verbatim when possible.
- **Prioritize by JD emphasis**: If the JD repeats a requirement or puts it in the first 3 bullets, map it first.
- **Offer behavioral mock-ups**: After the mapping, ask if the user wants 2-3 mock behavioral answers (e.g., "Tell me about a time you debugged a complex API issue under pressure").

### 8. Iterate and Refine

Ask if user wants to:
- Adjust emphasis or tone
- Add or remove sections
- Generate alternative versions for different roles
- Create format variations (traditional vs. modern)
- Develop role-specific versions (if applying to multiple similar positions)

### 9. Application Question Drafting

When a job application includes custom questions (common on Greenhouse, Lever, Ashby), draft answers alongside the resume. This is a natural extension of the tailoring work — you already have the JD analysis and the candidate's background mapped. See [references/application-answer-template.md](references/application-answer-template.md) for the "Why this company + fit" template.

**Workflow:**
1. Extract application questions from the JD page (look for free-text questions at the bottom of Greenhouse/Lever listings)
2. For each question, draft a response that:
   - Uses a specific story from the candidate's experience (STAR-lite format: situation → action → result)
   - Maps directly to the JD's top priorities
   - Includes a "TODO" marker for details only the candidate can fill in (specific customer names, deal sizes, internal metrics)
   - Stays under 250 words per answer (recruiters skim)
3. Save answers alongside the resume (Obsidian note or markdown file)

**Common question types and strategies:**
- "Most difficult client/customer win" → Pick the most complex technical escalation that had a business outcome (renewal, expansion, churn prevention). Frame as: technical depth + cross-functional collaboration + customer trust rebuilt.
- "Re-invent something at your job" → Pick a process improvement you championed or wished you'd pushed harder. Tie it to the target company's domain. Shows high agency + strategic thinking.
- "Why this company?" → Reference specific customers, product capabilities, or recent funding. Never generic.
- "How would you approach building [X] from scratch?" → Three-phase answer: Audit current state → Establish foundations (processes, tooling, standards) → Ship first high-impact deliverable. Reference a specific past example of building something from zero.
- "Describe a time you [achieved] something that impacted [adoption/revenue]" → Problem (quantified) → Action (concrete deliverable) → Result (measured outcome) → Lesson (strategic insight). Be specific — "wrote an API integration guide" not "improved documentation."
- "Add up to three bullets showing exceptional ability" → Resume-level impact statements, 1-2 sentences each. Lead with outcome/scale, include metric, demonstrate differentiating skill. See `references/application-answer-template.md` for templates.
- **Writing portfolio requests** (common on Ashby for technical writer roles) → Create 2-3 targeted samples (getting-started guide, API reference) using a fictional product in the target company's domain. Save to `~/Documents/Resumes/portfolio/`. Host on GitHub repo to simultaneously demonstrate Docs-as-Code skills. See `references/application-answer-template.md` for full strategy.

### 10. URL Validation

> **LinkedIn extraction fails 100% of the time** — web_extract, Firecrawl, and stealth mode all return empty. See [references/linkedin-extraction-fallback.md](references/linkedin-extraction-fallback.md) for the proven fallback chain (search jobright.ai, Indeed, Lensa mirrors). Jobright.ai is the gold standard: structured data with responsibilities, qualifications, salary, and company context.

**Always extract and verify the JD before tailoring.** Job postings get filled, redirected, or replaced. When the user provides a URL:
1. Extract the page content
2. Confirm the job title and company match what the user described
3. If there's a mismatch (different role, or "this position has been filled"), flag it immediately before doing any work

#### Paywalled Job Boards — Extracting the Company Name

Some aggregator sites (Virtual Vocations, Lensa, etc.) hide the company name and full JD behind a subscription. Don't give up — the data is often in the page source as JSON-LD structured data:

1. **Open the browser** and navigate to the page
2. **Run in browser console:** `document.querySelector('script[type="application/ld+json"]')?.textContent`
3. **Look for the `hiringOrganization` object** in the JSON — specifically `hiringOrganization.name`. This field is required by schema.org/JobPosting and is rarely stripped even when the visual UI is gated.
4. Example output: `"hiringOrganization": {"@type": "Organization", "name": "Acme Corp."}`

If the page uses Next.js, check `document.querySelector('script#__NEXT_DATA__')?.textContent` for the same data in a different format.

**Fallback**: Search for the job URL's unique ID or text snippet on other job boards (ZipRecruiter, Indeed, LinkedIn) — aggregators often mirror listings that are more fully visible elsewhere.

Common mismatches:
- Greenhouse URLs can redirect to a different role at the same company
- Listings on aggregator sites (RemoteOK, BuiltIn) may be stale — the original posting may be gone
- Some URLs serve a generic "apply" page, not the actual JD — try to find the source listing

### 11. Best Practices to Follow

**Do**:
- Be truthful and accurate - never fabricate experience
- Use industry-standard terminology
- Quantify achievements with specific metrics
- Tailor each resume to specific job
- Proofread for grammar and consistency
- Keep language concise and impactful

**Don't**:
- Include personal information (age, marital status, photo unless requested)
- Use first-person pronouns (I, me, my)
- Include references ("available upon request" is outdated)
- List every job if career is 20+ years (focus on relevant, recent experience)
- Use generic templates without customization
- Exceed 2 pages unless very senior role
- **Add LinkedIn links unless user explicitly requests them**

### Pitfalls

- **ALWAYS use the canonical script `scripts/md_to_docx.py` — do NOT write a custom build script.** The inline sample script below is incomplete and has known bugs. The canonical script handles all edge cases correctly. Copy it to `/tmp/md_to_docx.py` and run it: `source /tmp/.venv/bin/activate && python3 /tmp/md_to_docx.py input.md output.docx`. Only write a custom script if the canonical one fails for a specific reason.
- **Markdown `#`/`##` header prefixes**: The canonical script now strips `#` prefixes automatically, but the SAFEST approach is to write section headers as plain ALL CAPS text without any `#` prefix (e.g., `PROFESSIONAL SUMMARY` not `## PROFESSIONAL SUMMARY`). The `isupper()` detection fails on lines starting with `# ` because the `#` and space aren't uppercase. If you must use `#` headers, verify the script version includes the stripping logic.
- **4-part job title lines lose the date**: Job entries like `**Title** | Company | Location | Date` have 4 pipe-separated parts. The canonical script renders all parts on one line with `_add_rich()` per part. If writing a custom script, do NOT assume exactly 3 parts — join `parts[2:]` back together for the subtitle line, or the date gets silently dropped.
- **Skill lines vs. bullets**: Skill category lines (`- **Category:** items`) should render as plain paragraphs with a bold category name, NOT as List Bullet items. The script detects these by leading `- ` + `**` + `:` within first 60 chars. If your markdown uses a different format (e.g., `**Category:** items` without the leading dash), they'll fall through to a different handler.
- **Job lines with separate location/date lines**: The markdown source may have the date/location as separate lines after the pipe-formatted title line. The script now skips trailing non-bullet text lines after a `|` line. If you're writing a custom script, handle this by consuming consecutive text lines after a pipe-delimited entry.

### DOCX Generation Workflow (Hermes Sandbox)

The Hermes sandbox terminal uses a venv that lacks `pip` and `python-docx`. Use this two-stage workflow:

#### Stage 1: Write the tailored resume as markdown
```python
# Use write_file to save as .md first — this lets you iterate and review
content = """
NAME | Contact | Location
# (full resume content)
"""
write_file(path="~/Documents/Resumes/tailored_company.md", content=content)
```

#### Stage 2: Convert markdown to formatted DOCX

**Preferred: Use the canonical script.** Copy it to a temp location and run:
```bash
cd /tmp && uv venv .venv && source .venv/bin/activate && uv pip install python-docx lxml
cp ~/.hermes/skills/tailored-resume-generator/scripts/md_to_docx.py /tmp/
python3 /tmp/md_to_docx.py input.md ~/Documents/Resumes/tailored_company.docx
```

**Only if the canonical script fails:** Create a temp venv and write a custom conversion script. The Hermes system Python is managed by `uv` and rejects `pip install --system`.

```python
# ⚠️ LEGACY INLINE SAMPLE — use scripts/md_to_docx.py instead (see Stage 2 above)
# This sample is illustrative only and has known bugs with 4-part job lines and ** markers.
# save as build_resume.py, then (with /tmp/.venv activated): python3 build_resume.py
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10.5)
style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

with open('tailored_company.md') as f:
    lines = f.readlines()

for line in lines:
    raw = line.strip()
    if not raw:
        continue
    
    # Name line
    if raw.isupper() and len(raw) < 50 and not ':' in raw:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(raw)
        r.bold = True
        r.font.size = Pt(16)
        continue
    
    # Contact line
    if '@' in raw or any(c.isdigit() for c in raw[:8]):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(raw)
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        continue
    
    # Section headers (all caps)
    if raw.isupper() and not raw.startswith('-') and '|' not in raw:
        p = doc.add_paragraph()
        p.space_before = Pt(6)
        r = p.add_run(raw)
        r.bold = True
        r.font.size = Pt(11)
        continue
    
    # Job lines with |
    if '|' in raw and not raw.startswith('-') and not raw.startswith('•'):
        parts = [x.strip() for x in raw.split('|')]
        p = doc.add_paragraph()
        p.space_before = Pt(4)
        p.space_after = Pt(0)
        r = p.add_run(parts[0])
        r.bold = True
        r.font.size = Pt(10.5)
        if len(parts) >= 2:
            r2 = p.add_run(' | ' + parts[1])
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        if len(parts) >= 3:
            p2 = doc.add_paragraph()
            p2.space_before = Pt(0)
            p2.space_after = Pt(1)
            r3 = p2.add_run(parts[2].strip())
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
            r3.italic = True
        continue
    
    # Bullets
    if raw.startswith('- ') or raw.startswith('• '):
        text = raw.lstrip('-• ').strip()
        p = doc.add_paragraph(text, style='List Bullet')
        p.space_before = Pt(0)
        p.space_after = Pt(1)
        for run in p.runs:
            run.font.size = Pt(10)
        continue
    
    # Tech skill lines with colon
    if ':' in raw and not raw.startswith('-'):
        parts = raw.split(':', 1)
        p = doc.add_paragraph()
        p.space_before = Pt(1)
        p.space_after = Pt(1)
        r = p.add_run(parts[0] + ':')
        r.bold = True
        r.font.size = Pt(10)
        if len(parts) > 1:
            r2 = p.add_run(parts[1])
            r2.font.size = Pt(10)
        continue
    
    # Regular text
    p = doc.add_paragraph(raw)
    for run in p.runs:
        run.font.size = Pt(10)

for section in doc.sections:
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

output_path = os.path.expanduser('~/Documents/Resumes/Jason_Crabtree_resume_Company_Role.docx')
doc.save(output_path)
print(f"Saved to {output_path}")
```

#### Stage 3: Verify DOCX has no markdown artifacts

After building the DOCX, **verify that no markdown syntax leaked into the output** before presenting it. The user will catch `**`, `*`, or `[text](url)` artifacts if they slip through.

Use the verification script from the skill:

```bash
source /tmp/.venv/bin/activate
python3 scripts/verify_docx.py ~/Documents/Resumes/tailored_company.docx
```

If artifacts are found, the script lists every paragraph containing them so you can debug the conversion. Common causes:
- The build script used `p.add_run(text)` instead of `_add_rich(p, text)` — `**bold**` markers pass through unprocessed
- A skill line (`- **Category:** items`) matched the generic bullet handler before the skill handler — reorder handlers so skill lines come first
- A job title with `**Title** | Company` was split on `|` but the `**` in the first part wasn't stripped

If using the skill's `scripts/md_to_docx.py` (the canonical converter), this should never happen. If it does, file a bug or patch the converter.

```python
# Quick inline check (no script needed):
source /tmp/.venv/bin/activate
python3 -c "
import docx
doc = docx.Document(os.path.expanduser('~/Documents/Resumes/tailored_company.docx'))
issues = [p.text for p in doc.paragraphs if '**' in p.text]
if issues:
    print(f'⚠️   Found {len(issues)} paragraphs with markdown artifacts:')
    for t in issues[:5]:
        print(f'     {t[:80]}')
else:
    print('✓  No markdown artifacts found')
"
```

#### Reading existing DOCX resumes in the sandbox
The Hermes system venv doesn't have python-docx. Use the same temp venv approach:
```bash
cd /tmp && uv venv .venv && source .venv/bin/activate && uv pip install python-docx
python3 -c "
import docx
doc = docx.Document(os.path.expanduser('~/Documents/Resumes/resume.docx'))
for p in doc.paragraphs:
    print(p.text)
"
```
If `/tmp/.venv` already exists from a prior Stage 2 run, skip the `uv venv` step — just activate and go.

### DOCX Formatting Rules (Critical)

When generating DOCX files, **never use markdown syntax**:

**❌ INCORRECT (markdown in DOCX):**
```
**Professional Summary**
*Manager, Technical Support Engineering*
[LinkedIn](https://linkedin.com/in/...)
| Category | Tools |
|----------|-------|
```

**✅ CORRECT (Word native formatting):**
- Use `run.bold = True` for bold text, not `**text**`
- Use `run.italic = True` for italic text, not `*text*`
- Use plain text lists or styled paragraphs, not markdown tables
- Never include LinkedIn links unless user specifically asks for them

**Key Principle:** DOCX files should contain only clean, formatted text with no markdown artifacts. The user may not use LinkedIn or want social media links on their resume.

### 10. Special Considerations

**Career Changers**:
- Use functional or hybrid resume format
- Emphasize transferable skills
- Create compelling narrative in summary
- Focus on relevant projects and coursework

**Recent Graduates**:
- Lead with education
- Include relevant coursework, projects, internships
- Emphasize leadership in student organizations
- Include GPA if 3.5+

**Senior Executives**:
- Lead with executive summary
- Focus on leadership and strategic impact
- Include board memberships, speaking engagements
- Emphasize revenue growth, team building, vision

**Technical Roles**:
- Include technical skills section prominently
- List programming languages, frameworks, tools
- Include GitHub, portfolio, or project links
- Mention methodologies (Agile, Scrum, etc.)

**Creative Roles**:
- Include link to portfolio
- Highlight creative achievements and campaigns
- Mention tools and software proficiencies
- Consider more creative formatting (while maintaining ATS compatibility)

---

## Tips for Best Results

- **Be specific**: Provide complete job descriptions and detailed background information
- **Share metrics**: Include numbers, percentages, and quantifiable achievements when describing your experience
- **Indicate format preference**: Let the skill know if you need ATS-optimized, creative, or traditional format
- **Mention constraints**: Share any specific requirements (page limits, sections to include/exclude)
- **Iterate**: Don't hesitate to ask for revisions or alternative approaches
- **Multiple applications**: Generate separate tailored versions for different roles

## Privacy Note

This skill processes your personal and professional information to generate tailored resumes. Always review the output before submitting to ensure accuracy and appropriateness. Remove or modify any information you prefer not to share with potential employers.
