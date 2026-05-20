---
name: resume-workflow-orchestrator
description: Orchestrates the complete resume and job application workflow using specialized resume skills. Routes to the right skill based on user intent and chains multiple skills together for comprehensive career support.
---

# Resume Workflow Orchestrator

## Overview

This meta-skill orchestrates the complete resume and job application workflow by routing to specialized skills and chaining them together. It provides a unified interface for all resume-related tasks while leveraging the deep expertise of individual skills.

## Available Skills in Ecosystem

### Core Workflow Skills
- **job-description-analyzer** - Analyze job postings, calculate match scores, identify gaps
- **tailored-resume-generator** - Generate tailored resumes (enhanced with bullet writing, quantification, career change translation)
- **cover-letter-generator** - Create personalized cover letters
- **resume-ats-optimizer** - Optimize for ATS compatibility and keyword matching

### Enhancement Skills
- **resume-bullet-writer** - Transform weak bullets into achievement-focused statements
- **resume-quantifier** - Add metrics and numbers to vague achievements
- **resume-formatter** - Ensure ATS-friendly formatting and clean layouts
- **tech-resume-optimizer** - Specialized optimization for technical roles
- **career-changer-translator** - Translate skills across industries
- **executive-resume-writer** - C-suite and VP-level resumes
- **academic-cv-builder** - Academic CVs with publications and grants

### Supporting Skills
- **salary-negotiation-prep** - Research market rates and build negotiation strategy
- **interview-prep-generator** - Generate STAR stories and talking points
- **offer-comparison-analyzer** - Compare multiple job offers
- **resume-version-manager** - Track and organize resume versions
- **portfolio-case-study-writer** - Transform bullets into portfolio case studies
- **reference-list-builder** - Format professional references
- **linkedin-profile-optimizer** - Sync resume with LinkedIn
- **creative-portfolio-resume** - Balance design with ATS compatibility
- **resume-section-builder** - Create targeted sections for different experience levels

## Routing Logic

### Intent Detection

**Job Analysis & Fit Assessment:**
- "Should I apply to this job?" → job-description-analyzer
- "Analyze this job description" → job-description-analyzer
- "What's my match score?" → job-description-analyzer
- "Am I qualified for this role?" → job-description-analyzer

**Resume Creation & Tailoring:**
- "Tailor my resume for..." → tailored-resume-generator
- "Create a resume for..." → tailored-resume-generator
- "Optimize my resume for ATS" → resume-ats-optimizer
- "Improve my resume bullets" → resume-bullet-writer
- "Add metrics to my resume" → resume-quantifier
- "Format my resume" → resume-formatter
- "Tech resume for software engineer" → tech-resume-optimizer
- "Executive resume for VP role" → executive-resume-writer
- "Academic CV for faculty position" → academic-cv-builder
- "Career change from X to Y" → career-changer-translator

**Application Materials:**
- "Write a cover letter" → cover-letter-generator
- "Prepare for interview" → interview-prep-generator
- "Negotiate salary" → salary-negotiation-prep
- "Compare job offers" → offer-comparison-analyzer

**Portfolio & Supporting:**
- "Create case study from my project" → portfolio-case-study-writer
- "Format my references" → reference-list-builder
- "Optimize my LinkedIn" → linkedin-profile-optimizer
- "Track my resume versions" → resume-version-manager

## Orchestrated Workflows

### Complete Job Application Workflow

When user provides a job URL or description and wants to apply:

**Step 1: Analyze Job Fit**
```
Use: job-description-analyzer
Input: Job description/URL
Output: Match score, gap analysis, application strategy
```

**Step 2: Generate Tailored Resume**
```
Use: tailored-resume-generator (with enhancements from resume-bullet-writer, resume-quantifier, career-changer-translator as needed)
Input: Job analysis + candidate background + existing resume
Output: Tailored resume in markdown + DOCX
```

**Step 3: Create Cover Letter**
```
Use: cover-letter-generator
Input: Tailored resume + job description
Output: Personalized cover letter
```

**Step 4: ATS Optimization Check**
```
Use: resume-ats-optimizer
Input: Tailored resume + job description
Output: ATS compatibility report + keyword match score
```

**Step 5: Interview Preparation**
```
Use: interview-prep-generator
Input: Tailored resume + job description + salary data
Output: STAR stories, talking points, salary anchor
```

### Resume Enhancement Workflow

When user wants to improve an existing resume:

**Step 1: Assess Current State**
```
Use: resume-formatter (format check) + resume-ats-optimizer (ATS check)
Input: Current resume
Output: Formatting issues, ATS compatibility issues
```

**Step 2: Enhance Bullets**
```
Use: resume-bullet-writer + resume-quantifier
Input: Weak bullets + candidate context
Output: Achievement-focused, quantified bullets
```

**Step 3: Optimize for Target Role**
```
Use: tailored-resume-generator (lightweight, just reordering/emphasizing)
Input: Enhanced resume + target job description
Output: Role-optimized resume
```

### Career Change Workflow

When user is switching industries/roles:

**Step 1: Translate Experience**
```
Use: career-changer-translator
Input: Current experience + target industry/role
Output: Translated skills, reframed achievements, industry terminology mapping
```

**Step 2: Identify Transferable Skills**
```
Use: job-description-analyzer (on target role) + career-changer-translator
Input: Target job description + current background
Output: Gap analysis, transferable skills mapping, bridge strategy
```

**Step 3: Create Transition Resume**
```
Use: tailored-resume-generator (with career-changer-translator context)
Input: Translated experience + target job description
Output: Resume emphasizing transferable skills and relevant projects
```

### Executive/C-Suite Workflow

For senior leadership positions:

**Step 1: Executive Branding**
```
Use: executive-resume-writer
Input: Leadership experience + achievements + board experience
Output: Executive profile, leadership competencies, career highlights
```

**Step 2: Strategic Tailoring**
```
Use: tailored-resume-generator (executive mode)
Input: Executive resume + target C-suite role
Output: C-suite tailored resume emphasizing P&L, transformation, strategic impact
```

### Academic Career Workflow

For faculty/research positions:

**Step 1: Build Academic CV**
```
Use: academic-cv-builder
Input: Publications, grants, teaching, research experience
Output: Academic CV with proper formatting for target institution
```

**Step 2: Tailor for Specific Position**
```
Use: tailored-resume-generator (academic mode)
Input: Academic CV + job description (tenure-track, postdoc, etc.)
Output: Targeted academic CV emphasizing relevant research/teaching
```

## Skill Chaining Patterns

### Sequential Chain (Linear)
```
job-description-analyzer → tailored-resume-generator → cover-letter-generator → interview-prep-generator
```

### Parallel Chain (Concurrent)
```
resume-formatter + resume-ats-optimizer + resume-bullet-writer (all run on same resume)
```

### Conditional Chain (Branching)
```
job-description-analyzer → [if tech role: tech-resume-optimizer] → [if career change: career-changer-translator] → tailored-resume-generator
```

### Iterative Chain (Loop)
```
tailored-resume-generator → resume-ats-optimizer → [if score < 80%: back to tailoring] → finalize
```

## Integration with Existing Hermes Skills

### With hiring-manager-prep
- Use interview-prep-generator for talking points
- Use hiring-manager-prep for specific interviewer research
- Chain: interview-prep-generator → hiring-manager-prep

### With document-conversion
- Use document-conversion for final format conversions (PDF, DOCX)
- Chain: tailored-resume-generator → document-conversion

### With notion/obsidian
- Save application materials to Notion/Obsidian
- Use resume-version-manager to track versions in these tools

## Usage Examples

### Example 1: Full Application Package
```
User: "I want to apply for this Senior Product Manager role at Stripe [URL]"

Orchestrator:
1. Runs job-description-analyzer on the URL
2. Presents match score and recommendation
3. Asks for candidate background/resume
4. Runs tailored-resume-generator with job analysis
5. Runs cover-letter-generator
6. Runs resume-ats-optimizer for final check
7. Runs interview-prep-generator with salary data
8. Delivers complete application package
```

### Example 2: Resume Enhancement
```
User: "My resume bullets are weak, help me improve them"

Orchestrator:
1. Asks for current resume
2. Runs resume-bullet-writer on each bullet
3. Runs resume-quantifier to add missing metrics
4. Runs resume-formatter for layout improvements
5. Presents enhanced resume
```

### Example 3: Career Change
```
User: "I'm a teacher wanting to move into corporate training"

Orchestrator:
1. Runs career-changer-translator to map teaching → corporate training
2. Identifies transferable skills and reframes experience
3. Runs job-description-analyzer on sample training roles
4. Runs tailored-resume-generator with translation context
5. Suggests portfolio projects to bridge gaps
```

## Best Practices

1. **Always start with job analysis** before tailoring - don't waste effort on poor-fit roles
2. **Use specialized skills for specific needs** - don't force generic tailoring when executive/academic/tech optimizations exist
3. **Chain skills intelligently** - run ATS check after tailoring, not before
4. **Preserve user's voice** - enhancement skills should improve, not rewrite, the user's experience
5. **Validate before delivering** - always run ATS check and format verification on final output
6. **Track versions** - use resume-version-manager to avoid confusion when applying to multiple roles

## Skill Selection Decision Tree

```
Is user applying to a specific job?
├─ YES → job-description-analyzer first
│   └─ Match score > 60%? → Continue with tailored-resume-generator
│       └─ Specialized role?
│           ├─ Tech/SWE/PM/Data → tech-resume-optimizer
│           ├─ C-suite/VP/Director → executive-resume-writer
│           ├─ Academic/Faculty → academic-cv-builder
│           ├─ Creative/Design → creative-portfolio-resume
│           └─ General → tailored-resume-generator
│       └─ Career changer? → career-changer-translator first
│   └─ Match score < 60% → Advise against applying (unless dream job)
└─ NO → What does user need?
    ├─ Improve bullets → resume-bullet-writer
    ├─ Add metrics → resume-quantifier
    ├─ Fix formatting → resume-formatter
    ├─ ATS check → resume-ats-optimizer
    ├─ Career change → career-changer-translator
    ├─ Interview prep → interview-prep-generator
    └─ Salary negotiation → salary-negotiation-prep
```

## Notes

- This orchestrator skill should be loaded first for any resume-related task
- It routes to specialized skills but doesn't replace them - each skill has deep expertise
- The orchestrator maintains context across the workflow, so user doesn't have to repeat information
- Always verify skill availability before routing (some skills may not be installed)