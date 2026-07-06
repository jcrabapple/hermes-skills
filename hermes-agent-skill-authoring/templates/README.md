<!--
README template for skills published to a public skill-collection repo
(e.g. your-username/hermes-skills). Use this as the starting point when
authoring README.md for a new exported skill.

The SKILL.md is the agent-facing doc; the README.md is the human-facing
doc for GitHub visitors. They are distinct artifacts with different
audiences. Don't merge them.

Sections below are ordered for scannability. The order is opinionated;
a "What it does" at the top lets a reader decide whether to keep
reading in 5 seconds. "Pitfalls" near the end is for the implementer
who's already decided to use it.

The placeholder lines marked DELETE-ME are scaffolding for the author
to remove before committing.
-->

# <Skill Name>

<One-sentence description of what the skill does and the trigger class
it handles. Lead with the verb.>

<!-- DELETE-ME: if the skill depends on external services, name them
in this opening sentence so the README is self-describing when shared
out of context. -->

## What it does

<2-4 bullet list or short table of the skill's concrete capabilities.
Each bullet should be specific enough that a reader knows whether the
skill covers their use case.>

| <thing 1> | <description> |
| <thing 2> | <description> |
| <thing 3> | <description> |

## Setup

### Required

- <binary, library, or service dependency #1>
- <env var or config file>
- <companion skill that must be installed>

### Optional but recommended

- <dependency that improves the experience but isn't required>

<!-- DELETE-ME: if the skill needs env vars, list them here with their
purpose. README is a better home than SKILL.md for env-var docs because
users find READMEs via search engines; SKILL.md is agent-only. -->

```bash
EXAMPLE_API_KEY=...          # https://example.com/signup
EXAMPLE_USERNAME=...         # your account username
```

## Install

```bash
git clone https://github.com/<owner>/<skill-collection>.git
cp -r <skill-collection>/<skill-name> ~/.hermes/skills/<category>/
```

<!-- DELETE-ME: if the skill is installable via an alternative mechanism
(official installer, package manager), prefer that and link it. -->

## Usage

Triggers on: "<trigger phrase 1>", "<trigger phrase 2>", "<trigger 3>".

<One paragraph on the typical usage flow, or a short example.>

<!-- DELETE-ME: if the skill is designed for a specific cron pattern,
include it. -->

```python
cronjob(action="create", schedule="<when>",
        prompt="Run the <skill-name> skill.")
```

## Output

<If the skill produces a specific deliverable — an email, a file, a
URL — show a small example of the output. This is the single most
useful section for a reader deciding whether to install.>

## Pitfalls

- <Pitfall 1> — <why it bites + how to avoid>
- <Pitfall 2>

<!-- DELETE-ME: the full pitfall list lives in SKILL.md. The README
should only carry the 3-5 that a human reader needs to know to use the
skill successfully. Implementation gotchas belong in SKILL.md, not
README. -->

## See also

- [<companion-skill>](../<companion-skill>/) — <one-line relationship>
- [<external-doc-or-skill>](<url>) — <one-line description>
