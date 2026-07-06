# Mixture of Agents (MoA) Parallel Decomposition

Pattern for decomposing a complex analysis into independent dimensions, dispatching parallel `delegate_task` subagents, and synthesizing results into one comprehensive deliverable.

## When to Use

- Task has **3+ independent dimensions** that can be researched in parallel
- User is actively waiting but a single sequential research path would be slow
- The deliverable is a **comprehensive plan, audit, or comparison** (not a quick lookup)
- Each dimension would benefit from its own dedicated context window

## When NOT to Use

- Dimensions are dependent (one must complete before the next can start)
- Quick lookup (2-3 searches) — do it inline
- Only 1-2 dimensions — use a single delegation or inline research
- The task requires interactive user steering between steps

## The Pattern

### Step 1: Decompose

Identify 3-5 independent dimensions. Each becomes one subagent's scope.

**Example (modernizing an unmaintained project):**
- Agent 1: Codebase technical analysis (clone repo, audit deps/architecture)
- Agent 2: Bug/issue investigation (GitHub issues, security, CVEs)
- Agent 3: Upstream compatibility research (API changes, breaking changes)

### Step 2: Dispatch All Agents in Parallel

Batch all `delegate_task` calls in a **single assistant turn** so they run concurrently. Each agent gets:
- A specific, self-contained goal (the subagent has no conversation history)
- Enough context to work independently
- Appropriate toolsets (e.g. `["terminal", "web"]` for analysis that needs cloning + searching)
- `role="leaf"` (default — these are focused workers, no further delegation needed)

**Key:** Give each agent enough background context about the project/domain in the `context` field, since they start with a blank slate.

### Step 3: Track Progress

Create a todo list tracking each agent's status. Update it as each async batch result arrives:

```
todo([
  {"id": "agent-1", "content": "Codebase analysis agent — waiting", "status": "in_progress"},
  {"id": "agent-2", "content": "Bugs/issues agent — waiting", "status": "in_progress"},
  {"id": "agent-3", "content": "API compat agent — waiting", "status": "in_progress"},
  {"id": "synthesis", "content": "Synthesize findings", "status": "pending"},
])
```

As each `[ASYNC DELEGATION BATCH COMPLETE]` message arrives, mark that agent complete and give the user a brief status update. Don't wait for all agents — start synthesizing as soon as all are back.

### Step 4: Synthesize

Once all agents report back:
1. Read any files they created (agents may save findings to files)
2. Identify cross-cutting themes, contradictions, and gaps
3. Write the synthesized deliverable as a single comprehensive document
4. Save to a file for the user
5. Present a summary in the conversation with the file path

### Step 5: Validate

Check for:
- Contradictions between agents (e.g., one says "supports v2 API" and another says "only v1")
- Gaps (dimensions that no agent covered)
- Subagent self-reports that need verification (e.g., "file written" — verify the file exists)

## Template: Dispatch Prompts

Each agent's goal should be self-contained with:
1. What to analyze
2. Specific questions to answer
3. Expected output format
4. Any resources to consult (repo URL, docs URL, etc.)

```
delegate_task(
  goal="Perform a comprehensive technical analysis of [PROJECT] at [URL]. Clone the repo and analyze: [specific questions]. Report back a structured analysis with [output format]. Be thorough and specific — cite actual file paths and version numbers.",
  context="[PROJECT] is [brief description]. Repo at [URL]. [Any relevant background the agent needs].",
  toolsets=["terminal", "web"],
  role="leaf"
)
```

## Template: Synthesis Document Structure

```
# [Project] Modernization Plan
## Executive Summary
## Strategic Decision (paths evaluated, recommendation with rationale)
## Target Tech Stack (table: component | current | target | rationale)
## Compatibility Matrix (table: change | version | impact | action)
## Bug Fixes (table: issue | description | fix approach)
## Design & Redesign (principles, UI/UX modernization)
## Architecture (project structure, state management, offline/caching)
## Implementation Roadmap (phases with checkboxes)
## Risk Assessment (table: risk | likelihood | impact | mitigation)
## Success Criteria (checkboxes)
## Appendix: [Full audit tables, API change logs, etc.]
```

## Key Advantages Over Sequential Research

- **Speed:** N agents in parallel vs 1 agent doing N dimensions sequentially
- **Context isolation:** Each agent gets a clean context window for its dimension — no cross-contamination
- **Depth:** Each agent can go deep on its dimension without worrying about context budget for other dimensions
- **Incremental delivery:** Results stream back as async batches — user sees progress
- **Cross-validation:** Synthesis step catches contradictions between independent analyses

## Pitfalls

- **Don't dispatch dependent agents in parallel.** If Agent 2 needs Agent 1's results, run them sequentially.
- **Don't forget the synthesis step.** Three agent reports ≠ a plan. The synthesis is where the value is.
- **Verify file claims.** If an agent says "file written to /path," check it exists before telling the user.
- **Agent duration varies.** In practice: codebase analysis (~3min), web research (~4-9min), API docs research (~9min). Don't block on the fastest agent — start synthesizing when all are back.
- **Cost.** 3 parallel subagents cost ~3x a single agent. Use for high-value deliverables, not quick lookups.
