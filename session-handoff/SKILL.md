---
name: session-handoff
description: "Compact the current session into a structured handoff document for a fresh agent or delegate_task subagent. Use when hitting context limits, switching focus, ending a work session, partitioning work across fresh contexts, or preparing a delegate_task goal that needs full session context. Triggers on: handoff, session handoff, context handoff, summarize for fresh agent, prepare for new session."
version: 1.0.0
author: Hermes Agent (adapted from davidondrej/skills)
license: MIT
metadata:
  hermes:
    tags: [handoff, session, context, delegation, continuity]
    related_skills: [subagent-driven-development, writing-plans, hermes-agent-skill-authoring]
---

# Session Handoff

Write a complete handoff that lets a fresh agent, delegate_task subagent, or new session continue the work without re-asking, re-discovering, or repeating mistakes.

## Core Principles

1. **State, not instructions.** Describe what *is true*, not what the next agent *should do*. Write "Auth endpoint is implemented; logout is not yet started" — never "Implement logout next." The fresh agent decides actions; you give it ground truth.

2. **Reference, don't duplicate.** Do not paste content already captured in other artifacts (plans, ADRs, issues, commits, diffs, design docs). Point to them by path or URL. Handoffs that re-embed everything become bloated and stale.

3. **Capture the "why".** Decisions and rejected approaches are the most valuable and least recoverable information. Code shows *what*; only you remember *why* and *what failed*.

4. **Trust nothing blindly.** Frame all claims as context to verify against the actual code, not facts to accept.

5. **Redact secrets.** Strip API keys, tokens, passwords, and PII. Reference where credentials live (e.g. "env var OPENROUTER_API_KEY" or "~/.hermes/secrets/token") — never their values.

6. **Be ruthless.** Every line must be something the next agent cannot trivially get by reading the code or project config. Cut anything obvious, redundant, or explanatory.

## When to Use

- **Context limits approaching:** Session is long, compress before losing context
- **delegate_task with complex context:** Subagent needs full background but can't see your conversation
- **Ending a work session:** Save state so tomorrow's session can pick up
- **Partitioning work:** Split a large task across multiple fresh sessions
- **Session crash recovery:** Reconstruct what was happening

**NOT for:** Simple task delegation (just write a good goal in delegate_task). This is for complex, multi-step work where session state matters.

## Procedure

1. If a project config file exists (CLAUDE.md / AGENTS.md / .cursorrules), read it first. Do **not** restate anything already covered there — the handoff is session-specific only.

2. If using `session_search`, check for prior handoff files. Update rather than starting from scratch.

3. Fill in every section of the template below. Omit a section only if it is genuinely empty (e.g. no blockers) — mark it `None`.

4. Output the filled template as a single fenced code block so it can be copy-pasted.

5. Save to a file outside the working tree: `/tmp/handoff-<project>-<date>.md` or `HANDOFF.md` in the project root if the user prefers an in-repo record.

## Output Format

```
# HANDOFF: <short title of the work>
Generated: <timestamp> · Session focus: <one line>

## 1. Goal
<What we are ultimately trying to accomplish. 1-3 sentences. The "north star" so the next agent never loses the plot.>

## 2. Background / Context
<The motivation and constraints driving this work. Why it's being done now, who it's for, any hard requirements. Skip anything already in the project config.>

## 3. Current State
<Factual status of the work. What is DONE, what is PARTIAL, what is NOT STARTED.
Phrase as status, not actions:
- DONE: OAuth login flow (Google provider), tests passing locally
- PARTIAL: Session persistence — store wired up, refresh logic missing
- NOT STARTED: Logout endpoint>

## 4. Key Decisions (and why)
<The choices made and the reasoning. This is the highest-value section.
- Chose passport.js over custom OAuth — more community support, less surface area
- Stored tokens in httpOnly cookies, not localStorage — XSS mitigation>

## 5. Traps & Dead Ends
<Approaches already tried that FAILED, and things the next agent will be tempted to do wrong. Saves the next agent from repeating expensive mistakes.
- Tried mocking the DB in integration tests — flaky, abandoned for a test container
- Do NOT bump the SDK to v3 — it breaks the streaming API we rely on>

## 6. Relevant Files & Pointers
<Files that matter, with line ranges and WHAT specifically is there — not just what the file is. Reference external artifacts instead of pasting them.
- src/auth/oauth.ts:L40-L88 — provider config + token exchange
- docs/adr/0007-auth.md — full rationale (do not duplicate here)
- PR #142 — in-progress session work
- Issue #150 — logout requirements>

## 7. Open Work (status, with dependencies)
<What remains, described as state and ordering — NOT as a command list.
- Logout endpoint is not yet implemented
- Session persistence depends on the logout endpoint existing first
- E2E auth tests are blocked until both above are complete>

## 8. Environment & Setup
<Only if non-obvious. Tool versions, env vars needed, special run commands, anything the next agent needs to actually execute the work. Skip if standard.>

---
## Prompt for the Fresh Agent
<If this handoff will be fed to a delegate_task subagent or pasted into a new Hermes session, include this ready-to-use prompt. Use declarative statements ("X is complete", "Y has not been started"), never imperatives. End with:>

Before responding, read every file listed under "Relevant Files & Pointers" above.
Do not summarize, paraphrase, or claim you already have context — actually read each
file. Treat every claim in this handoff as context to verify against the code, not
facts to trust blindly. Then wait for my instructions before taking any action.
```

## Using with delegate_task

When dispatching a complex subagent that needs full session context, embed the handoff in the `context` field:

```python
delegate_task(
    goal="Continue implementing the auth feature. Read the handoff context first.",
    context="""# HANDOFF: Auth feature
... (paste handoff content here) ...""",
    toolsets=['terminal', 'file']
)
```

The handoff is especially valuable for `delegate_task` because subagents have **no memory of your conversation** — they start completely fresh. The handoff is the only context they get.

## Using with session_search

If you're ending a session and want tomorrow's session to pick up:

1. Save the handoff to `/tmp/handoff-<project>-<date>.md`
2. The next session can find it via `session_search(query="handoff auth")` or you can tell the user the file path to paste.

## Common Pitfalls

1. **Writing instructions instead of state.** "Fix the bug in auth.py" is an instruction. "auth.py has a known bug at L42 where empty passwords pass validation (see Issue #150)" is state. Always write state.

2. **Re-embedding code or docs.** Don't paste the plan, the ADR, or the diff. Point to them. The handoff is a map, not a copy.

3. **Forgetting rejected approaches.** "We tried X and it failed because Y" is more valuable than "we chose Z." The next agent WILL try X again if you don't warn them.

4. **Including secrets.** Even in a `/tmp/` file, secrets can leak. Reference env vars or secret file paths, never values.

5. **Being too verbose.** Every line must be non-obvious. If the next agent could figure it out from `ls` or `git log`, it doesn't belong here.

6. **Not saving to a file.** If the handoff only lives in the chat, it's lost when the session ends. Always write it to a file.

## Verification Checklist

- [ ] Handoff saved to a file (not just in chat)
- [ ] Every section filled or marked `None`
- [ ] No secrets or credentials included
- [ ] No re-embedded code or docs (only references)
- [ ] Decisions include the "why"
- [ ] At least one trap/dead-end documented
- [ ] Fresh agent could continue without asking a single question
