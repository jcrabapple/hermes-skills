---
name: hermes-agent-skill-authoring
description: "Author in-repo SKILL.md: frontmatter, validator, structure."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, authoring, hermes-agent, conventions, skill-md]
    related_skills: [writing-plans, requesting-code-review]
---

# Authoring Hermes-Agent Skills (in-repo)

## Overview

There are two places a SKILL.md can live:

1. **User-local:** `~/.hermes/skills/<maybe-category>/<name>/SKILL.md` — personal, not shared. Created via `skill_manage(action='create')`.
2. **In-repo (this skill is about this case):** `skills/<category>/<name>/SKILL.md` inside the hermes-agent repo — committed, shipped with the package. Use `write_file` + `git add`. `skill_manage(action='create')` does NOT target this tree.

## When to Use

- User asks you to add a skill "in this branch / repo / commit"
- You're committing a reusable workflow that should ship with hermes-agent
- You're editing an existing skill under `skills/` in the hermes-agent repo (use `patch` for small edits, `write_file` for rewrites; `skill_manage` still works for patch on in-repo skills, but not for `create`)

## Required Frontmatter

Source of truth: `tools/skill_manager_tool.py::_validate_frontmatter`. Hard requirements:

- Starts with `---` as the first bytes (no leading blank line).
- Closes with `\n---\n` before the body.
- Parses as a YAML mapping.
- `name` field present.
- `description` field present, ≤ **1024 chars** (`MAX_DESCRIPTION_LENGTH`).
- Non-empty body after the closing `---`.

Peer-matched shape used by every skill under `skills/software-development/`:

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)
description: Use when <trigger>. <one-line behavior>.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill, another-skill]
---
```

`version` / `author` / `license` / `metadata` are NOT enforced by the validator, but every peer has them — omit and your skill sticks out.

## Size Limits

- Description: ≤ 1024 chars (enforced).
- Full SKILL.md: ≤ 100,000 chars (enforced as `MAX_SKILL_CONTENT_CHARS`, ~36k tokens).
- Peer skills in `software-development/` sit at **8-14k chars**. Aim for that range. If you're pushing past 20k, split into `references/*.md` and reference them from SKILL.md.

## Peer-Matched Structure

Every in-repo skill follows roughly:

```
# <Title>

## Overview
One or two paragraphs: what and why.

## When to Use
- Bulleted triggers
- "Don't use for:" counter-triggers

## <Topic sections specific to the skill>
- Quick-reference tables are common
- Code blocks with exact commands
- Hermes-specific recipes (tests via scripts/run_tests.sh, ui-tui paths, etc.)

## Common Pitfalls
Numbered list of mistakes and their fixes.

## Verification Checklist
- [ ] Checkbox list of post-action verifications

## One-Shot Recipes (optional)
Named scenarios → concrete command sequences.
```

Not every section is mandatory, but `Overview` + `When to Use` + actionable body + pitfalls are the minimum for the skill to feel like a peer.

## Directory Placement

```
skills/<category>/<skill-name>/SKILL.md
```

Categories currently in repo (confirm with `ls skills/`): `autonomous-ai-agents`, `creative`, `data-science`, `devops`, `dogfood`, `email`, `gaming`, `github`, `leisure`, `mcp`, `media`, `mlops/*`, `note-taking`, `productivity`, `red-teaming`, `research`, `smart-home`, `social-media`, `software-development`.

Pick the closest existing category. Don't invent new top-level categories casually.

## Workflow

1. **Survey peers** in the target category:
   ```
   ls skills/<category>/
   ```
   Read 2-3 peer SKILL.md files to match tone and structure.
2. **Check validator constraints** in `tools/skill_manager_tool.py` if unsure.
3. **Draft** with `write_file` to `skills/<category>/<name>/SKILL.md`.
4. **Validate locally**:
   ```python
   import yaml, re, pathlib
   content = pathlib.Path("skills/<category>/<name>/SKILL.md").read_text()
   assert content.startswith("---")
   m = re.search(r'\n---\s*\n', content[3:])
   fm = yaml.safe_load(content[3:m.start()+3])
   assert "name" in fm and "description" in fm
   assert len(fm["description"]) <= 1024
   assert len(content) <= 100_000
   ```
5. **Git add + commit** on the active branch.
6. **Note:** the CURRENT session's skill loader is cached — `skill_view` / `skills_list` will not see the new skill until a new session. This is expected, not a bug.

## Cross-Referencing Other Skills

`metadata.hermes.related_skills` unions both trees (`skills/` in-repo and `~/.hermes/skills/`) at load time. You CAN reference a user-local skill from an in-repo skill, but it won't resolve for other users who clone the repo fresh. Prefer referencing only in-repo skills from in-repo skills. If a frequently-referenced skill lives only in `~/.hermes/skills/`, consider promoting it to the repo.

## Cross-Ecosystem Skill Import (External SKILL.md Format Mapping)

Hermes Agent is not the only agent with a skill system. Claude Code, Open Design (github.com/nexu-io/open-design), and several other agents use SKILL.md files with similar but distinct frontmatter conventions. When importing skills from another ecosystem, the reference at `references/cross-ecosystem-skill-import.md` documents the format mapping, especially for Open Design's 90+ design skills and 100+ brand design systems.

Key differences to handle during import:
- OD uses an `od:` frontmatter block with `mode`, `design_system`, `craft`, `inputs`, `outputs`, and `capabilities_required` fields — map these to Hermes' `metadata.hermes.*` equivalents where possible.
- OD's `triggers` field (YAML list) maps to `metadata.hermes.tags` or gets embedded in the `description`.
- OD's `design_system.requires` field indicates the skill needs a `DESIGN.md` brand reference — copy the relevant design system as a skill reference file.
- OD's `craft` rules (anti-AI-slop, color discipline, typography) should be embedded in the SKILL.md body as a verification checklist, not kept as a separate lint pipeline.

See `references/cross-ecosystem-skill-import.md` for full details, format tables, import strategies, and pitfall notes.

## Editing Existing In-Repo Skills

- **Small fix (typo, added pitfall, tightened trigger):** `skill_manage(action='patch', name=..., old_string=..., new_string=...)` works fine on in-repo skills.
- **Major rewrite:** `write_file` the whole SKILL.md. `skill_manage(action='edit')` also works but requires supplying the full new content.
- **Adding supporting files:** `write_file` to `skills/<category>/<name>/references/<file>.md`, `templates/<file>`, or `scripts/<file>`. `skill_manage(action='write_file')` also works and enforces the references/templates/scripts/assets subdir allowlist.
- **Always commit** the edit — in-repo skills are source, not runtime state.

## Publishing User-Local Skills to a Public Repo

When you have a personal skill in `~/.hermes/skills/` that's useful enough to share (e.g., to a public GitHub repo), generalize it first.

### Pre-Publish Authorship Check

**Before any generalization work, verify the skill is yours to share.** Skills installed from third-party sources (Claude Code marketplaces, MCP, `npx skills add <owner>/<repo>`, `pip install` of a skill-shaped package) often look local because they live in `~/.hermes/skills/`, but they have an upstream maintainer. Copying them into your own repo as if you wrote them is attribution laundering and confuses users who go to your account expecting the canonical source.

Run this check on the skill before touching it:

| Signal | Where to look | What it means |
|--------|---------------|---------------|
| `LICENSE` file with non-MIT copyright | `<skill>/LICENSE` | Upstream has its own terms. Don't redistribute without honoring them. |
| `author` / `homepage` / `repository` in frontmatter | top of `SKILL.md` | Names a different maintainer. |
| `git remote -v` pointing elsewhere | `cd <skill> && git remote -v` | Cloned from upstream. |
| Install hint like `npx skills add owner/repo` | `SKILL.md` body | The skill expects a specific installer. |
| Bundled vendor dir (e.g. `lib/vendor/`, `node_modules/`) | `<skill>/` | Likely vendored from a third party. |
| Size > ~50KB with a `pyproject.toml` / `package.json` | `<skill>/` | Probably a packaged plugin, not a hand-written skill. |

**If any of these fire, do not copy the code.** Instead:

- **Add a "Recommended External Skills" entry to the repo's root README** with a one-line description, the original maintainer name, the license, and a link to the upstream project. The original session that surfaced this pattern added `last30days` (Matt Van Horn, MIT) this way rather than duplicating 1.1MB of code. A worked example of the README row:
  ```
  | `last30days` | Multi-source "what are people saying about X" research across Reddit, X, YouTube, HN, TikTok, Polymarket, GitHub, and the web | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) |
  ```
  This is a deliberate alternative to "just fork it" — the upstream repo is the source of truth, the README is the pointer.
- **If you have local changes**, fork upstream and PR them back. Don't maintain a silent fork in your own repo.
- **If the license allows and you have meaningful local modifications**, a fork with the upstream LICENSE preserved and clear "forked from X" attribution is OK — but default to linking, not forking.

### Generalization Checklist

1. **Remove personal paths.** Replace hardcoded paths like `~/Documents/Obsidian Vault` or personal email addresses with configurable values.
2. **Add `config.example.yaml`.** A template with annotated comments showing every configurable value. Users copy to `config.yaml` and customize.
3. **Write a standalone README.md.** The SKILL.md is for the agent; the README is for humans browsing GitHub. Include: what it does, prerequisites, quick start, configuration, how it works, pitfalls, and a "Using with Hermes Agent" install section.
4. **Remove session-specific state.** Don't include `recent_topics.txt`, `last_run.log`, or other runtime files. The skill directory should be clean templates and code.
5. **Replace hardcoded credentials with `os.environ`.** See the SKILL.md double-leak pitfall below — this is the single most common leak.
6. **Genericize domain-specific prose.** Replace cron commands that reference your own CLI flags, dashboard layouts, or naming conventions with general patterns. ("Pre-run script does X" beats "Pre-run script calls `hermes skills list` and parses the table output.")
7. **Run the audit script before committing.** `bash scripts/audit-skill-for-publish.sh <skill-dir>` runs every leak check in one pass and exits non-zero on any hit. Treat any hit as a cleanup task before `git add`. The script covers everything the inline grep one-liners cover plus extra categories (real flight numbers, rental confirmation patterns, npx installer hints, LICENSE upstream check).
8. **Update the repo's root README.** Add a row to the skills table under the right category.

### Workflow

```bash
# 1. Clone the shared repo
cd /tmp && git clone https://github.com/OWNER/REPO.git

# 2. Copy the skill
cp -r ~/.hermes/skills/CATEGORY/SKILL-NAME /tmp/REPO/SKILL-NAME

# 3. Remove runtime state files
rm -f /tmp/REPO/SKILL-NAME/recent_topics.txt /tmp/REPO/SKILL-NAME/*.log

# 4. Create config.example.yaml (annotated template)
# 5. Write README.md (human-facing docs)
# 6. Update root README.md (add to skills table)
# 7. Commit and push
cd /tmp/REPO && git add -A && git commit -m "Add SKILL-NAME" && git push origin main

# 8. Clean up
rm -rf /tmp/REPO
```

### Pitfalls

- **The SKILL.md double-leak.** SKILL.md is loaded by the LLM as context every time the skill fires. A hardcoded API key in an illustrative code block gets read into the model's context (one leak) and then runs in the agent's environment (second leak). A real-world example: a `new-music-digest` SKILL.md had `LASTFM_KEY = "85109521..."` in Step 1 of a workflow block. Anyone running the skill in a fresh session would have the key sitting in their LLM context. Always extract credentials to `os.environ["..."]` and document the required env vars in the README.

- **Don't publish personal credentials or email addresses.** The config template should use placeholders like `your-email@example.com`. This is the most common leak in personal skills. Same goes for: AgentMail inbox IDs (e.g. `herman-the-hermes-agent@agentmail.to`), service-specific instance URLs (e.g. `annoying-petrel.pikapod.net`), User-Agent strings that include a real email, and the user's account username in service APIs.

- **Don't publish real names of family members or friends in worked examples.** Worked examples in SKILL.md and README.md are templates for downstream users — when the author uses the real names of people they know, those names get baked into the published skill. Audit *all* example text, not just code: trip-recap templates, "Places Visited" sections, default user-message examples, sample data tables. Replace with first-name-only placeholders or generic wording ("Travelers: TBD", "user@example.com").

- **Don't publish real trip-specific or transaction-specific data as the "example".** This includes real flight numbers (`UA1234`), hotel names, car rental confirmation numbers, real PNRs, real restaurant reservations, real bank transaction IDs, real street addresses. These look like illustrative placeholders to the author but are personal history. Either invent plausible-but-fake example data, or use generic placeholders like `<flight-number>` and `<confirmation-code>`.

- **Partial redaction is not redaction.** A phone number shown as `+140****8075` still leaks the area code (401) and last 4 digits — that's enough to identify a person, especially in a small sample (one user on a single platform). Credit-card `**** **** **** 1234`, SSN `***-**-1234`, and IP `192.168.1.***` have the same problem. Either fully mask (`+1-XXX-XXX-XXXX`, `XXXX-XXXX-XXXX-1234` is borderline), use a structural placeholder (`+1-REDACTED`, `<phone-number>`), or — best — move the value to an env var and never embed it in the file at all. The audit script now flags any `+1`-prefixed digit-or-asterisk pattern, including partial-redaction forms.

- **When you find one leak, sweep all local skills.** Leaks cluster — a user who hardcodes one API key has usually hardcoded others. After finding the first leak, run the audit script (see "Pre-publish automation" below) against every skill in `~/.hermes/skills/` that might ever be exported, not just the one you're publishing today. A pre-publish sweep of 6 local skills in one session turned up 2 separate hardcoded API keys (Last.fm, AviationStack) plus family-name data in a third skill's example template.

- **Don't publish runtime state.** Files like `recent_topics.txt` or `published_slugs.txt` are session-specific.

- **Don't redistribute third-party skills as your own work.** See the Pre-Publish Authorship Check above. If the skill has a LICENSE file, an `author:` frontmatter field, or a different `git remote`, link to it from your README — don't copy the code.

- **Don't ship a skill whose README has unedited env-var examples.** When you genericize placeholders like `you@example.com`, double-check the SKILL.md and any other docs got the same treatment. It's easy to update the README and forget the SKILL.md code blocks (or vice versa).

- **Keep the local skill and shared skill in sync.** After pushing, update your local copy with the generalized version so your own setup uses the same config pattern.

- **Git push may hang on HTTPS.** If the credential helper (e.g., `gh auth git-credential`) is unavailable, switch the remote to SSH: `git remote set-url origin git@github.com:OWNER/REPO.git`.

- **Push timeouts on the first attempt are common.** If `git push -u origin <branch>` times out, retry once — the objects often transferred successfully and the second attempt just finishes the negotiation.

### Verification Grep Patterns

Run these against the new skill directory **before** committing. Each line is a one-liner that should return zero hits for a clean export.

```bash
SKILL_DIR="path/to/<skill>"

# Personal email addresses
grep -rIn '@' "$SKILL_DIR" --include='*.md' --include='*.py' --include='*.sh' \
  | grep -E '[a-z0-9._-]+@[a-z0-9.-]+\.(com|us|to|net|org)' \
  | grep -vE '(@example\.com|@your-domain|@contact|@hermes|@your-email)' \
  || echo "✓ no personal emails"

# API key shapes (Last.fm, Stripe, OpenAI, Anthropic, etc.)
grep -rInE '(sk-[a-zA-Z0-9]{20,}|pk_[a-z]+_[a-zA-Z0-9]+|[a-f0-9]{32})' "$SKILL_DIR" \
  || echo "✓ no hardcoded API keys"

# User-specific service instance URLs (PikaPod, ntfy, etc.)
grep -rInE 'https?://[a-z0-9-]+\.(pikapod\.net|example\.com|ngrok\.io)' "$SKILL_DIR" \
  || echo "✓ no personal instance URLs"

# User-specific paths and home dir
grep -rInE '(/home/[a-z]+/|~/Documents/Obsidian|/Users/[a-z]+/)' "$SKILL_DIR" \
  || echo "✓ no personal paths"

# Personal usernames in service APIs
grep -rInE '(USERNAME|USER|owner) = .[a-z]+.' "$SKILL_DIR" --include='*.py' \
  | grep -vE '"your_username"|username.*example' \
  || echo "✓ no hardcoded usernames"
```

Treat any hit as a leak to clean up. The grep filters for `@example.com` etc. are deliberate — those are valid placeholder values in README templates. If your real values are different, expand the filter to include your real domain so the grep doesn't false-positive on every legitimate reference.

For skills that explicitly need a real User-Agent string (e.g., MusicBrainz requires a contact per [their policy](https://musicbrainz.org/doc/MusicBrainz_API/Rate_limiting)), call it out in the README: "Before using, edit the User-Agent in the SKILL.md to your own contact." Don't ship a generic-but-invalid string that will get throttled.

### Pre-publish automation

The grep one-liners above are consolidated into a runnable script: `scripts/audit-skill-for-publish.sh`. It runs every check, prints pass/fail per check with a 5-line context preview on failure, and exits non-zero if anything fails. This is the right shape when you're auditing a batch of skills or running pre-commit hooks.

```bash
# Audit one skill before publishing
bash scripts/audit-skill-for-publish.sh /path/to/copied-out/skill

# Sweep every local skill (the right move after finding any leak — see "When
# you find one leak, sweep all local skills" pitfall above)
for d in ~/.hermes/skills/*/; do
  [ -d "$d" ] && echo "── $d ──" && bash scripts/audit-skill-for-publish.sh "$d" || true
done
```

The script never modifies files — review each hit, fix in source, re-run. False positives are possible (legitimate hex blobs, real flight numbers that are *supposed* to be in a worked example, etc.), so read every hit before deleting.

For the wider "I just found one leak, sweep all my local skills" workflow, use the wrapper at `scripts/sweep-all-local-skills.sh`. It runs the audit against every directory in `~/.hermes/skills/` (recursing one level for `category/skill/` layouts), aggregates pass/fail counts, and exits non-zero if any skill has at least one failure. Output is human-readable by default and `--json` for piping into other tools.

```bash
# After finding a leak in one skill, sweep all of them
bash scripts/sweep-all-local-skills.sh

# Or pipe to jq for further processing
bash scripts/sweep-all-local-skills.sh --json | jq '.failing_skills[].skill'

# Stop on first failure to inspect in place
bash scripts/sweep-all-local-skills.sh --stop-on-fail
```

For the README.md that ships alongside SKILL.md, the structural pattern used across the published-skill collection is in `templates/README.md`. Copy it as the starting point and fill in the placeholder sections; the section order is opinionated (What it does → Setup → Install → Usage → Output → Pitfalls → See also) and matches what GitHub readers expect from a scannable skill README.

## Skill Design Philosophy

### Two Design Patterns

Skills tend to fall into one of two patterns. Both are valid; they solve different problems.

**Pattern A — Capability primitives (tool wrappers):** Thin wrapper over a deterministic CLI or script. Logic lives in code. SKILL.md teaches the agent how to invoke it. Adds new capabilities (search, email, browser, API access). Reliability comes from shell tools, not prompts. Typically 30-80 lines, mostly command examples. Use when the bottleneck is "the agent can't do X."

**Pattern B — Process primitives (cognitive disciplines):** Encodes a methodology the agent should follow. Pure prompt engineering — no scripts needed. Adds structured workflows (TDD, code review, debugging loops, session handoff). Reliability comes from explicit procedure, checklists, validation loops. Use when the bottleneck is "the agent's output quality or process is bad."

A mature skill library uses both. Pattern A gives the agent better tools. Pattern B gives it better methods for using them.

### Description as Routing Contract

The description is the only thing the agent sees before deciding to load the skill. If your skill doesn't trigger, the description is wrong 95% of the time, not the body.

Include three elements:
1. **What** the skill does (one phrase)
2. **When** to use it (trigger phrases, situations)
3. **Differentiator** vs related skills (prevents routing conflicts)

Pattern: `"X via Y. Use for [situations]. [Differentiator: no Z required / faster than W / handles edge case V]."`

**Never summarize the full workflow in the description.** If the description contains a step-by-step summary of *how* the skill works, the agent tends to follow that summary and skip loading the body. Describe *what* and *when*, never *how*.

### Match Strictness to Task Fragility

Scale instruction rigidity to how costly a wrong move is:
- **Loose natural-language heuristics** when many approaches are valid (e.g. code review, research synthesis)
- **Pseudocode or templates** when there's a preferred pattern but variation is acceptable (e.g. report format, handoff template)
- **Exact scripts and strict step lists** when the workflow is fragile, error-prone, or consistency-critical (e.g. migrations, credential handling, deployments)

### Build Validation Loops

The single biggest output quality improvement: state a verify → fix → re-verify loop explicitly. Document skills need a visual QA pass before delivery. Code skills need tests pass + zero type errors. Data skills need schema validation before output.

### Compose Primitives, Don't Bundle Workflows

One skill = one capability or one discipline. Resist bundling concerns into "the X workflow." Multiple small skills combine at runtime; one large skill is rigid. If a skill does design + planning + implementation + testing + deployment, it's a framework, not a skill — split it.

## Skill Anti-Patterns

- **Don't re-teach what the model already knows.** Every line should provide context the model doesn't already have. No Python syntax tutorials. No "what is git." Challenge every paragraph.
- **Don't include human-facing docs inside the skill folder.** No README.md, CHANGELOG.md, or INSTALLATION_GUIDE.md. Skills are for agents.
- **Don't write vague descriptions.** Bad: "A helpful skill for documents." Good: "Fill PDF form fields, extract form data, flatten completed PDFs. Use when the user mentions PDF forms or programmatic field population."
- **Don't bundle library code.** Install via pip/npm. Don't paste source into the skill.
- **Don't write monolithic mega-skills.** If one skill does everything, you've built a framework, not a skill. Split it.
- **Don't assume the agent will infer.** Be explicit about every step that matters. Bad: "Then deploy it." Good: "Run `npm run deploy:staging` and wait for HTTP 200 from /healthz before reporting success."
- **Don't write style-only variants.** A skill that just changes tone belongs in user preferences or system prompt, not a skill.
- **Don't ignore failure modes.** For every workflow step that can fail, document what failure looks like and what to do. Happy-path-only skills break in production.
- **Don't include time-sensitive information.** "As of Q4 2024..." rots fast. Fetch live data via script or omit.

## Skill Ship Checklist

Before publishing or committing a skill:

- [ ] Frontmatter `name` matches folder name
- [ ] Description includes what + when + differentiator
- [ ] Description includes likely user trigger phrases
- [ ] No human-facing docs inside the skill folder
- [ ] No time-sensitive information
- [ ] Relative paths only (no hardcoded absolute paths)
- [ ] State-check before action where applicable
- [ ] Validation loop documented (if the skill produces output)
- [ ] Output format documented if relevant
- [ ] Tested with weak and strong models (or at least the target model)
- [ ] Tested for both correct triggering AND correct execution
- [ ] Skill does one thing (not bundled)
- [ ] Composes cleanly with related skills
- [ ] Version controlled

## Common Pitfalls

1. **Using `skill_manage(action='create')` for an in-repo skill.** It writes to `~/.hermes/skills/`, not the repo tree. Use `write_file` for in-repo creation.

2. **Leading whitespace before `---`.** The validator checks `content.startswith("---")`; any leading blank line or BOM fails validation.

3. **Description too generic.** Peer descriptions start with "Use when ..." and describe the *trigger class*, not the one task. "Use when debugging X" > "Debug X".

4. **Forgetting the author/license/metadata block.** Not validator-enforced, but every peer has it; omitting makes the skill look half-finished.

5. **Writing a skill that duplicates a peer.** Before creating, `ls skills/<category>/` and open 2-3 peers. Prefer extending an existing skill to creating a narrow sibling.

6. **Expecting the current session to see the new skill.** It won't. The skill loader is initialized at session start. Verify in a fresh session or via `skill_view` using the exact path.

7. **Linking to skills that don't exist in-repo.** `related_skills: [some-user-local-skill]` works for you but breaks for other clones. Prefer only in-repo links.

8. **Summarizing the workflow in the description.** If the description contains step-by-step instructions, the agent follows the summary and skips loading the body. Describe *what* and *when*, never *how*.

9. **Writing happy-path-only skills.** For every step that can fail, document what failure looks like and the recovery action. Skills without failure modes break in production.

10. **Bundling multiple concerns.** One skill = one capability or one discipline. A skill that does planning + implementation + testing is a framework, not a skill.

## Verification Checklist

- [ ] File is at `skills/<category>/<name>/SKILL.md` (not in `~/.hermes/skills/`)
- [ ] Frontmatter starts at byte 0 with `---`, closes with `\n---\n`
- [ ] `name`, `description`, `version`, `author`, `license`, `metadata.hermes.{tags, related_skills}` all present
- [ ] Name ≤ 64 chars, lowercase + hyphens
- [ ] Description ≤ 1024 chars and starts with "Use when ..."
- [ ] Total file ≤ 100,000 chars (aim for 8-15k)
- [ ] Structure: `# Title` → `## Overview` → `## When to Use` → body → `## Common Pitfalls` → `## Verification Checklist`
- [ ] `related_skills` references resolve in-repo (or are explicitly OK to be user-local)
- [ ] `git add skills/<category>/<name>/ && git commit` completed on the intended branch
