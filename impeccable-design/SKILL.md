---
name: impeccable-design
description: >-
  Production-grade frontend design guidance for AI agents. Embeds deep
  typography, color, layout, motion, and UX-writing intelligence into web app
  building sessions. Adapted from Impeccable (pbakaus/impeccable) for Hermes
  Agent.
version: 1.0.0
author: Hermes Agent (adapted from Impeccable by Paul Bakaus)
license: Apache-2.0
metadata:
  hermes:
    tags: [design, frontend, ui, ux, web-dev, css, typography, color]
    related_skills: [design-md, popular-web-designs, claude-design]
    resources:
      homepage: https://impeccable.style/
      source: https://github.com/pbakaus/impeccable
---

# Impeccable Design (Hermes Edition)

A lightweight adaptation of the Impeccable design language for Hermes Agent.
Provides real design vocabulary and structured workflows for building
production-grade web interfaces, without eating your context window.

## When to Use This Skill

Load this skill when the task involves:
- Building or redesigning websites, landing pages, dashboards, product UI, app
  shells, components, forms, settings, onboarding, or empty states
- CSS, HTML, Tailwind, component libraries, or design tokens
- Design critique, polish, audit, or refinement of existing frontend code

**Not for:** Backend-only or non-UI tasks.

## Trigger Phrases

These map Impeccable's 23 commands to natural language for Hermes:

| Impeccable Command | Natural Language Trigger |
|---|---|
| `/impeccable teach` | "Set up design context for this project" / "Create PRODUCT.md and DESIGN.md" |
| `/impeccable shape` | "Plan the UX/UI before we build" / "Shape the design brief first" |
| `/impeccable craft` | "Design and build this in one flow" / "Shape then build" |
| `/impeccable critique` | "Critique this design" / "UX review of this page" |
| `/impeccable audit` | "Audit this UI" / "Accessibility and quality check" |
| `/impeccable polish` | "Polish this page" / "Final design pass" |
| `/impeccable bolder` | "Make this more impactful" / "Push the design bolder" |
| `/impeccable quieter` | "Tone this down" / "Less shouting, more subtlety" |
| `/impeccable distill` | "Strip this down to essentials" / "Simplify ruthlessly" |
| `/impeccable harden` | "Production-harden this UI" / "Handle edge cases and errors" |
| `/impeccable typeset` | "Fix the typography" / "Improve font hierarchy" |
| `/impeccable layout` | "Fix the layout and spacing" / "Improve visual rhythm" |
| `/impeccable colorize` | "Add strategic color" / "Better color usage" |
| `/impeccable animate` | "Add purposeful motion" / "Improve transitions" |
| `/impeccable delight` | "Add moments of joy" / "Make this memorable" |
| `/impeccable clarify` | "Improve the UX copy" / "Better button labels and errors" |
| `/impeccable adapt` | "Make this responsive" / "Adapt for mobile and desktop" |
| `/impeccable optimize` | "Optimize UI performance" / "Reduce bundle size, improve LCP" |
| `/impeccable document` | "Generate DESIGN.md" / "Document the design system" |
| `/impeccable extract` | "Extract reusable components" / "Pull tokens into design system" |
| `/impeccable overdrive` | "Go beyond conventional" / "Extraordinary effects" |
| `/impeccable live` | "Iterate visually in the browser" / "Live component tuning" |

## Setup: Design Context (Non-Negotiable)

**Before any design work or file edits, check for `PRODUCT.md` and `DESIGN.md`**
in the project root.

- `PRODUCT.md` = Strategy: who is this for, what is the brand voice, references
  and anti-references
- `DESIGN.md` = Visual system: colors, typography, components, spacing

**If missing:** Run the discovery interview below and write them. Every design
decision downstream depends on this context. Generic design produces generic
output.

### Discovery Interview (for PRODUCT.md)

1. **Register:** Brand surface (marketing, landing, portfolio — design IS the
   product) OR product surface (dashboard, tool, app — design SERVES the
   product)?
2. **Who is this for?** Be specific. "Solo founders evaluating a tool on their
   phone between meetings" not "users."
3. **Brand voice in three words.** Pick real words. "Warm and mechanical and
   opinionated" beats "modern and clean."
4. **Visual references?** Named brands/products, not adjectives.
   "Klim Type Foundry specimen pages," not "technical and clean."
5. **Anti-references?** Things to explicitly avoid resembling.

### DESIGN.md

If the project has existing tokens (CSS custom properties, Tailwind config,
themed CSS-in-JS), extract them. Otherwise run in seed mode with quick
questions about color strategy, type direction, and motion energy.

For the Google Stitch DESIGN.md spec format, load the `design-md` skill.

## Core Design Laws

Apply to every design task. Interpret creatively; vary across projects.

### Color
- **Use OKLCH.** Reduce chroma as lightness approaches 0 or 100.
- **Never use `#000` or `#fff`.** Tint every neutral toward the brand hue
  (chroma 0.005–0.01 is enough).
- **Pick a color strategy before picking colors:**
  1. **Restrained:** tinted neutrals + one accent ≤10%. *(Product default)*
  2. **Committed:** one saturated color carries 30–60% of surface. *(Brand
     default)*
  3. **Full palette:** 3–4 named roles, each deliberate. *(Campaigns, data
     viz)*
  4. **Drenched:** surface IS the color. *(Hero sections, campaigns)*
- Don't collapse every design to Restrained by reflex.

### Theme (Light vs. Dark)
Never default. Not dark "because tools look cool dark." Before choosing, write
**one sentence of physical scene**: who uses this, where, under what ambient
light, in what mood. Add detail until the answer is forced.

> Bad: "Observability dashboard"  
> Good: "SRE glancing at incident severity on a 27-inch monitor at 2am in a
> dim room"

### Typography
- Cap body line length at **65–75ch**.
- Hierarchy through **scale + weight contrast** (≥1.25 ratio between steps).
  Avoid flat scales.

### Layout
- **Vary spacing for rhythm.** Same padding everywhere is monotony.
- **Cards are the lazy answer.** Use only when truly the best affordance.
  Nested cards are always wrong.
- Don't wrap everything in a container. Most things don't need one.

### Motion
- **Don't animate CSS layout properties** (width, height, top, left).
- **Ease out** with exponential curves (`ease-out-quart`, `quint`, `expo`).
- No bounce, no elastic easing.

### Absolute Bans
Match-and-refuse. If you're about to write any of these, rewrite with
different structure:

- **Side-stripe borders:** `border-left` or `border-right` as the primary
  visual accent on cards/features/testimonials
- **Purple gradients:** especially as hero backgrounds
- **Bounce/elastic easing:** on UI transitions
- **Dark glows/box-shadow on dark backgrounds**
- **Italic serif display heroes:** unless the brand IS editorial/literary
- **Hero eyebrow chips:** tiny pill labels above headlines
- **Repeated tiny uppercase tracked kicker labels:** `text-xs uppercase
  tracking-widest` spam
- **Inter for everything:** intentional type pairing beats default
- **Gray text on colored backgrounds:** without sufficient contrast
- **Content flush to viewport edges:** without padding
- **Skipped heading levels:** h1 → h3
- **Small touch targets:** < 44×44 CSS px
- **Placeholder copy:** "Lorem ipsum" surviving to production

## Workflow by Task Type

### Building Something New
1. **Shape:** Run discovery if PRODUCT.md is missing. Write DESIGN.md brief.
2. **Build:** Produce working code with design intelligence applied.
3. **Polish:** Meticulous final pass — alignment, spacing, states, copy,
   transitions.

### Improving Something Existing
1. **Critique:** UX review — hierarchy, clarity, emotional resonance,
   persona fit.
2. **Audit:** Technical check — a11y, performance, responsive, anti-pattern
   detection.
3. **Fix:** Targeted fixes, not rewrites. Small diffs from "done" to "done
   well."

### Hardening for Production
- **Edge cases:** Empty states, loading states, error states, overflow,
   long content
- **i18n:** Text expansion, RTL, date/number formats
- **Accessibility:** Focus states, ARIA labels, color contrast, reduced motion
- **Performance:** LCP, CLS, bundle size, image optimization

## Anti-Pattern Detection

For deterministic anti-pattern scanning (no LLM needed), install the
Impeccable CLI:

```bash
npx -y impeccable detect src/                 # scan directory
npx -y impeccable detect index.html           # scan HTML file
npx -y impeccable detect --fast --json .      # regex-only, JSON output
```

This catches the 29 deterministic rules (AI slop tells + quality fundamentals)
independent of AI generation.

## Integration with Other Skills

- **`design-md`**: For formal DESIGN.md token specs, linting, and exporting
  to Tailwind/DTCG
- **`popular-web-designs`**: For 54 real design system references (Stripe,
  Linear, Vercel) as HTML/CSS
- **`claude-design`**: For throwaway prototypes and one-off HTML artifacts

## Pitfalls

- **Designing without context** is the #1 source of generic output. Always
  write or read PRODUCT.md first.
- **Don't trust AI color contrast** — use the CLI or a contrast checker.
- **Bans are match-and-refuse, not aesthetic dogma.** If a banned pattern is
  genuinely right for the project, justify it in the design rationale.
- **`/impeccable live`** (visual browser iteration) requires the full
  Impeccable toolchain including a dev server. It's not included in this
  lightweight skill; install the full CLI if you need live iteration.
