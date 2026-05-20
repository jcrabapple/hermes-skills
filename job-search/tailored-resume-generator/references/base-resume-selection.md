# Base Resume Selection Strategy

When the candidate has multiple existing tailored resumes, picking the right foundation saves time and produces better output than rewriting from scratch.

## Selection Criteria (in priority order)

### 1. Role Dimension Match (highest priority)
Match the **primary dimension** of the target role to the base resume's framing.

| Target Role Dimension | Best Base | Why |
|---|---|---|
| Team Lead / Manager | Resume already framed for leadership (e.g., Tailscale Team Lead) | Summary, skills ordering, and bullets already emphasize coaching, mentoring, process-building |
| Senior IC / Deep Technical | Resume framed for infrastructure or domain depth (e.g., Mirantis K8s, Upbound CSE) | Summary and skills lead with technical stack, not leadership |
| Solutions Engineer / Pre-Sales | Resume framed for SE (e.g., Metronome SE) | Customer lifecycle framing, POC/consultative language |
| Technical Writer | Resume framed for content (e.g., Infisical TW, Postman TW) | Documentation ownership, content metrics, Docs-as-Code |
| Customer Success / TAM | Resume framed for CS (e.g., Buildkite CS Manager, Camunda CS Strategist) | Proactive engagement, retention, expansion framing |

**Key insight:** For leadership roles, leadership framing > technical overlap. A Team Lead resume that lacks K8s keywords is better than a K8s resume that lacks leadership framing — you can add technical keywords to the leadership-framed resume more easily than you can retrofit leadership narrative into a technical IC resume.

### 2. Recency and Quality
When two resumes match the same dimension, prefer:
- The most recently created/modified (likely the most refined)
- The one with the strongest metrics and quantified achievements
- The one closest to the target company's domain/industry

### 3. Keyword Overlap
After selecting by dimension, scan the target JD for technical keywords and note which are already present in the base vs. which need to be added. This informs the tailoring pass, not the base selection.

## Anti-Patterns

- **Don't pick based on company name similarity** (e.g., picking the "database company" resume for a database role if it was framed as a TW role)
- **Don't pick the "most technical" resume for leadership roles** — the reframing cost is higher than adding a few technical keywords
- **Don't start from scratch if a good base exists** — even a 60% match resume saves significant effort vs. writing from the default template

## Workflow

1. List all existing .md resumes in ~/Documents/Resumes/
2. Scan filenames for role-dimension signals (Team Lead, TSE, SE, TW, CS, Manager)
3. Read the top 2-3 candidates' summaries and skills sections
4. Select based on dimension match first, recency second
5. Proceed with tailoring — reorder skills, adjust summary, add/remove keywords, reframe bullets
