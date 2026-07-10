# Cross-Ecosystem Skill Import: Open Design → Hermes Agent

Open Design (github.com/nexu-io/open-design) is an open-source Claude Design alternative that ships 90+ design skills (SKILL.md) and 100+ brand design systems (DESIGN.md). Its skills follow Claude Code's SKILL.md convention with optional `od:` frontmatter extensions. This reference covers how to adapt them for Hermes Agent.

## Quick Context

- **OD's architecture**: Browser → Local Daemon (Node 24, Express, SQLite) → Agent CLI via adapter layer. It delegates the agent loop to your local CLI agent (Claude Code, Codex, Hermes via ACP, etc.)
- **Hermes is already supported**: OD auto-detects Hermes CLI on PATH and uses it as a design engine via ACP. But that's unidirectional (OD talks to Hermes). This reference is about the reverse: bringing OD's capabilities into Hermes.
- **Skill count**: ~90 design skills in `skills/` + ~100 brand/aesthetic design systems in `design-systems/`
- **License**: Apache 2.0 — compatible with importing and adapting.

## SKILL.md Format Mapping

OD skills use two layers of frontmatter:

### Base (Claude Code convention, shared with Hermes)

```yaml
---
name: saas-landing
description: Hero / features / pricing / CTA layout for SaaS landing pages.
triggers:
  - "saas landing"
  - "landing page"
  - "startup page"
---
```

### OD Extensions (`od:` block)

```yaml
od:
  mode: prototype                    # one of: prototype | deck | template | design-system
  preview:
    type: html                       # html | jsx | pptx | markdown
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography]
  craft:
    requires: [typography, color, anti-ai-slop]
  inputs:
    - name: title
      type: string
      required: true
    - name: theme
      type: enum
      values: [editorial, minimal, brutalist]
      default: editorial
  outputs:
    primary: index.html
  capabilities_required:
    - surgical_edit
    - file_write
```

### Mapping to Hermes Format

| OD Field | Hermes Equivalent | Notes |
|---|---|---|
| `name` | `name` | Direct 1:1 — both lowercase hyphenated |
| `description` | `description` | Direct 1:1 |
| `triggers` | `metadata.hermes.tags` | Map to tags; triggers also inform `description` |
| `od.mode` | (no direct equivalent) | Used for routing logic in OD skills — can be noted in SKILL.md body as a context hint |
| `od.design_system` | (reference file) | Load `DESIGN.md` as a reference in the skill dir |
| `od.craft` | (quality gate) | Embed craft rules as verification checklist in SKILL.md body |
| `od.inputs` | `metadata.hermes.config` | Declare user-configurable params via config key pattern |
| `od.preview` | (not needed) | Hermes doesn't run a preview iframe; just note output format |
| `od.outputs` | (not needed) | Implicit from task description |

## Import Strategies (Three Tiers)

### Tier 1: Direct Skill Copy (fastest, ~90 skills)

1. Clone OD: `git clone https://github.com/nexu-io/open-design.git /tmp/open-design`
2. For each skill in `open-design/skills/<name>/SKILL.md`:
   - Copy the base frontmatter (name, description, triggers)
   - Add `metadata.hermes` block with tags and category
   - Append OD's body (workflow steps, principles)
   - Convert `od.inputs` to `metadata.hermes.config` blocks if interactive params
   - Place at `~/.hermes/skills/open-design/<name>/SKILL.md`
3. Copy relevant `design-systems/<brand>/DESIGN.md` into `~/.hermes/skills/open-design/<name>/references/`
4. Result: `/open-design saas-landing make a Stripe-style landing` style commands

### Tier 2: Hybrid (OD discovery via meta-skill)

Create one meta-skill `open-design` that:
1. Clones/pulls OD repo on first load
2. Scans `open-design/skills/` for available skills
3. Presents them as sub-commands
4. Resolves `DESIGN.md` from `design-systems/` based on user's brand request
5. Injects relevant craft rules as post-generation quality checks

### Tier 3: Full Protocol Bidirectional

- OD daemon runs as a Hermes-managed background service
- Hermes routes design requests to OD daemon's `/api/chat` endpoint
- OD's agent adapter for Hermes uses Hermes' full native tools (not ACP subset)

## Design Systems Library (~100+ brands)

Available under `open-design/design-systems/`. Each is a `DESIGN.md` following a 9-section schema. Notable brands:

- Product: Linear, Stripe, Vercel, Airbnb, Tesla, Notion, Apple, Cursor, Supabase, Figma
- Media: The Verge, Xiaohongshu
- Aesthetic: minimal, brutalist, cyberpunk, glassmorphism, vintage, neon
- Enterprise: Starbucks (37KB!), Vodafone, BMW, Binance

Each `DESIGN.md` contains: color palette (OKLch), typography stack, spacing scale, component tokens, brand voice, iconography, motion principles.

To use: copy to `~/.hermes/skills/open-design/<name>/references/<brand>/DESIGN.md` and reference it from the skill body.

## Craft Lint Rules (Quality Gates)

OD ships brand-agnostic craft rules under `craft/` directory:

| Rule | Severity | Check |
|---|---|---|
| `ai-default-indigo` | P0 | Blocks hardcoded indigo hexes (#6366f1, #4f46e5, #4338ca, #8b5cf6, #3730a3, #a855f7) |
| `all-caps-no-tracking` | P1 | Flags `text-transform: uppercase` without ≥0.06em letter-spacing |
| `typography` | P1 | Checks font scales, line heights, responsive type |
| `color` | P1 | Verifies all colors in output match the declared palette |
| `anti-ai-slop` | P2 | Detects generic AI design patterns (generic gradients, default shadows, stock icons) |
| `state-coverage` | P2 | Verifies hover/active/focus/disabled states for interactive elements |
| `animation-discipline` | P2 | Checks motion durations and easing curves |

Embed the relevant lint rules in your SKILL.md body under a `## Verification Checklist` section rather than running a separate lint pipeline (Hermes doesn't have a CSS linter natively).

## Key OD Skills by Category

| Scenario | Skills |
|---|---|
| Design | web-prototype, mobile-app, mobile-onboarding, wireframe-sketch |
| Marketing | saas-landing, blog-post, email-marketing, social-carousel, magazine-poster |
| Engineering | docs-page, dashboard, kanban-board, pm-spec |
| Sales | pricing-page, invoice |
| Personal | gamified-app, dating-web, digital-eguide |
| Deck | guizang-ppt, simple-deck, replit-deck, kami-deck, weekly-update, html-ppt-* |
| Media | hyperframes (HTML→MP4), sprite-animation, video-shortform, motion-frames |
| Critique | tweaks, critique (automated design review) |

## Pitfalls

1. **OD skills are large** — some are 20-27KB. Stay under Hermes' 100KB SKILL.md limit, but if importing many, consider whether you need all of them or just a curated subset.
2. **OD `od:` frontmatter is optional** — skills without it still work. Don't skip importing a skill just because it lacks OD extensions.
3. **The `triggers` field** is not standard Hermes frontmatter — map to `tags` and rephrase the `description` to be trigger-aware.
4. **Design system resolution is manual** — there's no automatic `DESIGN.md` loader in Hermes. You must either inline the relevant tokens or copy the file as a skill reference.
5. **OD's repo moves fast** — they have commits within hours. If you reference upstream, use a pinned commit or tag, not `main`.
6. **ACP vs native tools** — when OD spawns Hermes via ACP, Hermes only gets what ACP exposes. For richer design work, use Hermes' native tools instead (terminal, web_search, file_ops).
