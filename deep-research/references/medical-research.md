# Medical Research: Source Hierarchy & Query Patterns

When researching medical/health topics, prioritize sources in this order of authority:

> **Companion skill for patient-facing medical questions:** For symptom triage,
> condition summaries written for patients, and doctor-visit preparation, load
> the `health-research` skill instead of (or in addition to) this one. This
> reference covers the *academic literature* side (PubMed, Cochrane, StatPearls);
> `health-research` covers the *patient-facing* side (MedlinePlus, Mayo Clinic,
> NHS.uk), the safety contract (red flag screening, no diagnosis), and
> structured doctor-visit prep. Use both together for thorough coverage.

## Source Hierarchy

| Tier | Source Type | Examples |
|------|-------------|----------|
| **1** | Peer-reviewed clinical summaries | StatPearls (NCBI/NIH), BMJ Best Practice, UpToDate, Merck Manual Professional |
| **2** | Systematic reviews & meta-analyses | Cochrane Library, PubMed systematic reviews, JBI |
| **3** | Narrative reviews in indexed journals | PMC/PubMed, specialty journals (J Oral Pathol Med, Oral Surg Oral Med Oral Pathol) |
| **4** | Clinical practice guidelines | Specialty society guidelines (ADA, AAOP, EADV) |
| **5** | Primary RCTs | Individual randomized controlled trials |
| **6** | Case series / case reports | Use for rare conditions only |
| **7** | Encyclopedia / reference works | Wikipedia (good for history, nomenclature, overviews — verify claims against Tier 1–2) |

## Query Strategy for Medical Topics

### Phase 1: Landscape
```
"<condition> etiology pathogenesis review"
"<condition> clinical practice guidelines"
"<condition> epidemiology prevalence"
```

### Phase 2: Cause-Specific Dimensions
```
"<condition> <specific factor> association"      # e.g., "recurrent aphthous stomatitis vitamin B12 deficiency"
"<condition> <gene> polymorphism"                 # Genetic links
"<condition> cytokine <name>"                     # Immunological mechanisms
"<condition> microbiome"                          # Microbial factors
```

### Phase 3: Treatment
```
"<condition> treatment systematic review"
"<condition> <therapy> randomized controlled trial"
"<condition> Cochrane review"                     # Best evidence synthesis
"<condition> laser therapy meta-analysis"         # Non-pharmacological
```

### Phase 4: Differential Diagnosis
```
"<condition> differential diagnosis"
"<condition> vs <related condition>"
"<condition> associated systemic disease"
```

### Phase 5: Historical Context
```
"<condition> history first described"
"<condition> historical perspective"
```
Search for the original Greek/Latin etymology — Hippocratic references are common for conditions named in antiquity.

## Key Databases
- **PubMed / NCBI** — primary biomedical literature (use PMC for open-access full text)
- **Cochrane Library** — highest-quality systematic reviews
- **BMJ Best Practice** — concise clinical decision support
- **Merck Manual / MSD Manual** — practitioner-oriented summaries

## Patient-Facing Source Patterns (when the audience is the user, not a paper)

When the goal is to *inform the user* rather than produce a clinical paper, also
query these authoritative patient-education sources. The `health-research`
skill is built around this Tier 1–5 patient-facing hierarchy — see its
`references/sources.md` for full patterns. Quick starters:

```
"<condition>" site:medlineplus.gov         # NIH consumer health, ad-free, evidence-based
"<condition>" site:mayoclinic.org          # Comprehensive patient summaries
"<condition>" site:nhs.uk/conditions       # UK NHS, conservative + evidence-based
"<condition>" site:cdc.gov                 # US public health focus
"<condition>" site:merckmanuals.com/home   # Comprehensive consumer reference
```

## Pitfalls
- Avoid relying on single case reports for treatment efficacy
- Distinguish between "association" (correlative) and "causation" (proven) in etiological claims
- Note when systematic reviews find "insufficient evidence" — this is a real finding, not a gap to fill with speculation
- Cochrane reviews that find no conclusive evidence are valuable — cite them honestly rather than cherry-picking positive single trials
- Check whether the user wants clinical practice guidance or pure research — these have different source requirements
- For symptom triage, red flag screening, or doctor-visit prep, load the `health-research` skill — this reference is for literature research, not patient-facing decision support
- Do not use these academic sources to advise a user on their symptoms. No amount of PubMed reading replaces an in-person clinical evaluation.
