# LinkedIn Job Extraction Fallback Chain

LinkedIn blocks all direct extraction (web_extract, Firecrawl, nanogpt_web_extract with stealth). The browser also fails in headless environments (Chrome not available). Use this fallback chain instead.

## Step 1: Search for the Job on Mirror/Aggregator Sites

Search the job title + company + LinkedIn job ID on web_search. Reliable mirrors that carry full JDs:

| Site | How to Find | Reliability |
|------|-------------|-------------|
| **jobright.ai** | Search `"company" "job title" site:jobright.ai` — structured breakdown with responsibilities, qualifications, salary, company info | High — best structured data |
| **indeed.com** | Search `"job title" "company" site:indeed.com` — may show salary range in snippet | Medium — sometimes abbreviated |
| **lensa.com** | Search `"job title" site:lensa.com` — mirrors full JDs with salary estimates | Medium |
| **jobilize.com** | Search `"job title" "company" site:jobilize.com` — may redirect to similar roles | Low — often expired |

## Step 2: Extract from the Best Source

Once you find a mirror URL, use `web_extract` (not stealth mode — these sites are cooperative). The jobright.ai page is the gold standard: it includes responsibilities, required/preferred qualifications, salary range, benefits, and company context.

## Step 3: Validate the Extracted JD

Always confirm:
- **Job title** matches the LinkedIn listing
- **Company** matches (some mirrors attribute to parent company vs. subsidiary)
- **Salary range** is present (most mirrors include it)
- **Responsibilities and qualifications** are complete (not truncated)

## Step 4: Cross-Reference if Needed

If the first mirror is incomplete, search for the job on 2-3 mirrors and merge the data. The Indeed snippet often provides salary when jobright.ai doesn't, and vice versa.

## Example: Priority/Rollfi Team Lead TCSE (2026-05)

- LinkedIn URL: `https://www.linkedin.com/jobs/view/team-lead-technical-customer-support-engineer-at-priority-4413564111/`
- `web_extract` → blocked
- `nanogpt_web_extract` (stealth) → blocked
- `web_search "Priority" "team lead technical customer support engineer" job description` → found jobright.ai and jobilize mirrors
- `web_extract` on jobright.ai URL → full structured JD with responsibilities, qualifications, salary ($92K–$121K), benefits, company info
- Verified: title, company (Rollfi/Priority Technology Holdings), and all requirements matched

## Key Search Query Pattern

```
"[company name]" "[job title keywords]" job description requirements responsibilities
```

Or search by the LinkedIn job ID number:
```
"[company]" "[job title]" "[linkedin job ID]"
```
