---
name: product-feature-availability
description: >-
  Investigate whether a documented product feature is actually available for a
  specific user context (region, account type, plan tier, platform). Triggered
  when the user says things like: "can't find this feature", "docs say it
  exists but", "is this actually available", "when will this be available",
  "feature missing", "not showing up".
category: research
---

# Product Feature Availability Investigation

## When to Use

The user suspects a discrepancy between what the product's docs/marketing promise and what's actually in their app/account. This skill helps resolve that by cross-referencing multiple sources systematically.

## Workflow

### Step 1: Extract Official Documentation

- `web_extract` the official help center / support article the user referenced (if any).
- Note exactly what the docs claim: prerequisites, steps, supported regions, account types, dependencies.
- Save direct quotes — do not paraphrase.

### Step 2: Search for User Reports

Search Reddit / forums / social media for:
- `[Product] [Feature] [Region] not available`
- `[Product] [Feature] missing`
- `[Product] [Feature] not showing`
- Include `Reddit` in searches for candid user experiences.

If a support rep or official account has responded, capture the exact wording.

### Step 3: Cross-Check Dependencies

Features often rely on other features. Verify whether those upstream features are actually available in the user's context:
- E.g. Income Sorter depends on Pockets *and* Savings Accounts — if Savings Accounts aren't available in the user's region, Income Sorter is effectively broken even if the UI exists.
- Check product comparison / pricing pages for region-specific availability.

### Step 4: Check Marketing Materials

- Search for region-specific marketing pages.
- Note if the feature name changes (e.g. "Income Sorter" → "Salary Sorter" in UK, generic "Pockets" in US).
- Check if the marketing page auto-redirects or geoblocks — that itself is a signal.
- Watch for vague language like "available in select markets" or "rolling out" without specifics.

### Step 5: Look for Rollout / Roadmap Info

- Search for announcements: earnings calls, press releases, blog posts.
- Look for quotes about: "UK and EEA first", "US expansion", "coming soon".
- Note if the company has committed to a timeline or is silent.

### Step 6: Synthesize

Structure the answer:
1. **Bottom line**: Is the feature actually available for the user's context? Yes / No / Partially.
2. **Evidence from docs**: What the help center says (with link).
3. **Evidence from reality**: What users + support reps + marketing actually show.
4. **Likely root cause**: Dependency missing? Phased rollout? Regional regulatory issue? Templated docs that don't reflect actual availability?
5. **Verification steps**: Give the user 2-3 concrete app paths to check for themselves.
6. **Timeline**: Any official info on when (or if) it'll be available.
7. **Workarounds**: Manual steps or alternative products if the feature is a hard requirement.

## Reference Files

- `references/us-banking-api-landscape.md` — Compiled research on US banking API capabilities for personal accounts (Plaid read-only limitations, Revolut API status, Mercury Personal as the only US neobank with a personal API, Dwolla me-to-me, B2B-only banks). Useful when the user asks about banking APIs, budget apps, programmable money movement, or comparing neobanks.

## Pitfalls

- Docs are often templated across regions; US help centers may describe UK-only features.
- Single Reddit comments can be wrong; look for patterns across multiple reports.
- Features can be removed after being available; check timestamps.
- Don't trust marketing pages if they redirect to a different region's version.
- When a feature depends on another feature, always verify the dependency's availability first.
- US banking APIs for personal accounts are extremely rare. No regulatory mandate (unlike EU PSD2) means banks have no incentive to offer them. Don't assume a US bank has a consumer-facing API just because it has a developer portal — most are B2B/commercial only.
