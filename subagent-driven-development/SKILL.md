---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## The 5-Part Contract for Autonomous Subagent Loops

When dispatching an implementer subagent for a non-trivial task, structure the context as a 5-part contract. This prevents drift, scope creep, and reward-hacking in autonomous execution.

### The Contract

1. **Objective** — one sentence, one concrete outcome. Not a backlog.
2. **Constraints** — what must NOT change (public API, files, libs, conventions). Forbid scope creep explicitly: "Do not refactor unrelated code. Do not add dependencies."
3. **Validation command** — the exact shell command that proves progress (`pytest -q`, `pnpm test`, `npm run build`, etc.). After each change, the subagent runs this.
4. **Stop condition** — verifiable: "Stop when X passes" OR "when further changes need human/product input." Must be concrete and testable.
5. **Documentation** — one sentence instructing the subagent to write concise, targeted docs for every change (new `.md` files or updates to existing docs).

### Critical Additions

- **Forbid reward-hacking explicitly.** Add: "Do not delete, skip, weaken, or narrow tests to make the goal pass." Without this, subagents may game the stop condition by weakening tests rather than fixing the underlying issue.
- **Tell the subagent what to read first.** List the specific files/paths to read before starting work. This grounds the subagent in the actual codebase, not assumptions.
- **Ask it to work in checkpoints.** "Work in checkpoints and log progress briefly" gives you visibility into what happened when reviewing the result.
- **Tell it when to pause.** "If a change requires architecture decisions, pause and report instead of proceeding."

### Template

```
**Objective:** <one-sentence objective>
**Read first:** <files/PLAN.md/issue links>
**Constraints:** <what not to change, libs, conventions. Do not refactor unrelated code. Do not add dependencies.>
**Validate:** `<exact command>` after each change
**Document:** Write concise, targeted documentation for all changes — create new `.md` files or update existing docs as needed.
**Checkpoints:** Work in checkpoints and log progress briefly.
**Reward-hacking prohibition:** Do not delete, skip, weaken, or narrow tests to make the goal pass.
**Stop when:** <verifiable condition>, OR when further changes require human/product input.
```

### Example (migration task)

```
**Objective:** Migrate this project from Pydantic v1 to v2.
**Read first:** pyproject.toml, src/, tests/
**Constraints:** no public API changes; keep imports backwards-compatible via shims if needed; no new dependencies. Do not refactor unrelated code.
**Validate:** `pytest -q` after each change
**Document:** Write concise, targeted documentation for all changes.
**Checkpoints:** Work in checkpoints; log progress briefly.
**Reward-hacking prohibition:** Do not delete, skip, weaken, or narrow tests to make the goal pass.
**Stop when:** full suite passes with zero deprecation warnings, OR when a change requires architecture decisions.
```

### The Meta-Prompting Trick

Hand-written goals under-specify. For complex tasks, ask a second AI session (a separate `delegate_task` subagent, or a browser-based session like Claude/ChatGPT with the codebase loaded) to:
1. Inspect the codebase
2. Surface hidden assumptions, constraints, and edge cases
3. Emit a structured 5-part contract using the template above

Paste that contract into the implementer subagent's context. This is an order-of-magnitude improvement over writing the contract yourself, because the inspecting session catches constraints you missed.

### Handling Subagent Failure

**Delegate first, but always have a fallback plan.** When a task is complex enough to warrant delegation but the user is waiting for results, attempt delegation and automatically fall back to inline execution if the subagent fails.

**Delegate first, but always have a fallback plan.** When a task is complex enough to warrant delegation but the user is waiting for results, attempt delegation and automatically fall back to inline execution if the subagent fails.

### Failure Modes to Handle

| Failure Type | Symptoms | Recovery |
|--------------|----------|----------|
| API malformed data | "Upstream emitted malformed tool call data" | Fall back to inline immediately |
| Rate limiting | 429 errors, timeouts | Retry with backoff or fallback |
| Subagent crash | Exit code non-zero, empty results | Fall back to inline |
| Tool limitations | Subagent lacks needed tools | Use inline from start |
| Infinite loops | Max iterations hit without progress | Fall back with partial results |

### Pattern

```python
result = delegate_task(goal="...", skills=["relevant-skill"], toolsets=["web", "terminal"])

if result.get('error') or result.get('status') != 'completed':
    # Fallback: execute inline with same approach
    # Inform user: "Delegation failed, doing it directly instead"
    ...
```

## Subagent Output Verification

**After EVERY `delegate_task` where the subagent was expected to create files:**

1. Run `find <directory> -type f -name "*.ext"` to confirm files exist
2. Run `wc -l <files>` to verify content length > 0
3. If missing, read the subagent's summary/output to extract the intended content
4. Write the file directly yourself — don't re-delegate

**Do NOT trust the subagent's self-reported summary about files written.** Always verify with filesystem commands in YOUR context, not delegated context.

### Recovery Pattern
When a subagent write fails but the tool trace shows the intended content:
1. Extract the content from the subagent's tool trace response
2. Write the file directly using `write_file`
3. Do NOT re-delegate the same task — it will likely fail the same way

## Task Granularity

**Each task = 2-5 minutes of focused work.**

**Too big:**
- "Implement user authentication system"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"

## Red Flags — Never Do These

- Start implementation without a plan
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues

## Handling Issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails a Task

- Dispatch a new fix subagent with specific instructions about what went wrong
- Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```

**Quality is not an accident. It's the result of systematic process.**
