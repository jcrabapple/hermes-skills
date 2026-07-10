---
name: teaching-workspace
description: "Teach the user a new skill or concept through a structured workspace with lessons, reference docs, and learning records. Use when the user asks to learn something new, wants lessons, says 'teach me', 'help me learn', 'I want to understand', or references ongoing learning (Spanish lessons, coding skills, exam prep). Creates a stateful workspace that persists across sessions. Triggers on: teach me, learn, lessons, study guide, learning workspace, education."
version: 1.0.0
author: Hermes Agent (adapted from davidondrej/skills)
license: MIT
metadata:
  hermes:
    tags: [teaching, learning, education, lessons, study, spanish, college-prep]
    related_skills: [college-prep, spanish-teacher, article-writing]
---

# Teaching Workspace

A stateful teaching system that persists across sessions. The user learns a topic over multiple sessions using a structured workspace directory with lessons, reference docs, and learning records.

## When to Use

- User asks to learn a new skill or concept ("teach me Python", "I want to learn Spanish")
- User references ongoing learning ("continue my Spanish lessons", "what's next in my Python course")
- User wants structured study materials for an exam or certification
- User wants to build knowledge systematically rather than ad-hoc Q&A

**NOT for:** Quick one-off questions ("what does X mean?"). Just answer directly.

## Be Concise

Keep every chat message short, direct, and free of filler. State what you did, what's next, and the single most important thing for the user to do — nothing more. The teaching happens in the lessons and reference documents, not in long chat replies.

## The Workspace

Treat a dedicated directory as the teaching workspace. Default: `~/Documents/Learning/<topic>/`. State of the user's learning is captured in:

| File/Dir | Purpose |
|---|---|
| `MISSION.md` | Why the user wants to learn this topic. Grounds all teaching. |
| `RESOURCES.md` | Curated list of high-quality external resources. |
| `NOTES.md` | Scratchpad for user preferences and working notes. |
| `reference/` | Compressed reference docs — cheat sheets, syntax, glossaries. Revisit-able. |
| `lessons/` | Self-containedlesson files (HTML or markdown). Primary unit of teaching. |
| `learning-records/` | Records of what the user has learned, like ADRs for education. |

### File Formats

**MISSION.md:**
```markdown
# Learning Mission: <Topic>

## Why
<User's stated reason for learning — in their words>

## Current State
<Where they are now — beginner, intermediate, etc.>

## Success Looks Like
<What "done" looks like — pass an exam, build a project, hold a conversation>

## Mission History
- <date>: Mission updated from <old> to <new>
```

**Learning Records** (`learning-records/0001-<slug>.md`):
```markdown
# 0001: <Key Insight or Lesson Title>

**Date:** <date>
**Source:** <lesson number, resource, or session>

## What Was Learned
<2-3 sentences>

## Key Insights
- <non-obvious takeaway 1>
- <non-obvious takeaway 2>

## Gaps Identified
- <what the user still needs to learn>

## Next Steps
- <what this enables next>
```

## Philosophy

To learn at a deep level, the user needs three things:

1. **Knowledge** — captured from high-quality, high-trust resources
2. **Skills** — acquired through interactive lessons based on the knowledge
3. **Wisdom** — comes from interacting with other learners and practitioners

### Fluency vs Storage Strength

Distinguish between two types of learning:

- **Fluency strength:** In-the-moment retrieval of knowledge. Gives an illusory sense of mastery.
- **Storage strength:** Long-term retention. The real goal.

Design lessons that build storage strength through:
- **Retrieval practice** (recall from memory, not re-reading)
- **Spacing** (distribute practice over time — don't cram all lessons in one session)
- **Interleaving** (mix related topics in practice — for skills practice only)

## Lessons

A lesson is the primary unit of teaching — one self-contained file saved to `./lessons/` titled `0001-<slug>.md` (or `.html` for rich formatting), incrementing each time.

Each lesson:
- **Short and completable quickly.** Learners' working memory is small. Stay within it.
- **One tangible win.** The user should be able to do something they couldn't before.
- **Directly tied to the mission.** If it doesn't serve the mission, it doesn't belong.
- **In the zone of proximal development.** Challenging enough to grow, not so hard they're lost.

### Lesson Structure

```markdown
# Lesson N: <Title>

**Prerequisite:** <prior lesson or none>
**Estimated time:** <X minutes>
**Mission link:** <how this serves the mission>

## Concept
<Brief explanation of what this lesson teaches. Concise.>

## Knowledge
<The specific knowledge needed for this skill. Don't teach everything — only what's required for this lesson's skill.>

## Practice
<Interactive exercise or real-world task. This is where the learning happens — make it active, not passive reading.>

### Exercises
1. <exercise with clear expected output>
2. <exercise building on #1>

## Check Your Understanding
- <question 1>
- <question 2>

## What's Next
<One sentence preview of the next lesson.>

## Resources
- <link to primary source for deeper reading>
```

## The Teaching Loop

### Starting a New Topic

1. **Clarify the mission.** Ask why the user wants to learn this. What's the end goal? Create `MISSION.md`.
2. **Assess current level.** Ask what they already know. Create the first learning record.
3. **Gather resources.** Search for high-quality learning resources. Populate `RESOURCES.md`. Don't trust parametric knowledge — verify resources exist and are good.
4. **Create the first lesson.** Start at the zone of proximal development.
5. **Save the workspace.** Tell the user the directory path.

### Continuing an Existing Topic

1. **Read MISSION.md** — ground in the user's stated purpose.
2. **Read learning-records/** — understand what's been learned. These inform where to go next.
3. **Read NOTES.md** — check for user preferences.
4. **Identify the next lesson** based on:
   - What the mission requires
   - What's been learned so far (learning records)
   - Zone of proximal development
5. **Create the next lesson.**
6. **After the lesson, create a learning record** capturing what was learned and what's next.

### Question Dynamics

- **One question at a time.** Never dump multiple questions in a single message.
- **Domain-discovery, not confirmation.** "What's the one thing that, if true, makes everything else obvious?" beats "Do you already know X?"
- **Concrete over abstract.** "What's the hardest part of writing a function?" beats "Tell me about your challenges."

## Reference Documents

While creating lessons, also create reference docs in `./reference/`. These are the compressed essence of lessons — designed for quick lookup, not sequential reading.

Good reference doc types:
- **Syntax cheat sheets** for programming languages
- **Glossaries** for any topic with its own vocabulary
- **Algorithm summaries** and flowcharts for processes
- **Conjugation tables** for languages
- **Formula sheets** for math/science

Reference docs will be revisited far more often than lessons. Make them beautiful, scannable, and complete.

## Cross-Session Continuity

The workspace persists across sessions. When the user returns:

1. `session_search(query="teaching <topic>")` or check for the workspace directory
2. Read the workspace files to reconstruct state
3. Resume from where you left off

The learning records are the key — they tell you exactly what the user knows and what's next. No re-asking, no starting over.

## Common Pitfalls

1. **Teaching without understanding the mission.** If MISSION.md is empty or vague, lessons drift. Always clarify the mission first.
2. **Cramming too much into one lesson.** If a lesson takes more than ~15 minutes to complete, split it.
3. **Passive learning.** Reading without doing doesn't build storage strength. Every lesson must have an active practice component.
4. **Ignoring learning records.** If you don't record what was learned, the next session can't pick up intelligently.
5. **Re-teaching what the model knows.** Don't write a Python tutorial from scratch. Point to Resources, create targeted lessons that fill the specific gaps.
6. **Not verifying resources.** "I think there's a good course at..." — verify the resource exists and is high quality before recommending it.
7. **Skipping the practice exercises.** The exercises ARE the lesson. The explanation is just the setup for the exercises.

## Verification Checklist

- [ ] `MISSION.md` exists and captures the user's stated purpose
- [ ] `RESOURCES.md` has at least 3 verified, high-quality resources
- [ ] Each lesson has a practice/exercise component
- [ ] Each lesson creates or updates a learning record
- [ ] `NOTES.md` captures user preferences as they emerge
- [ ] Lesson numbering is sequential and correct
- [ ] The next lesson is identified at the end of each session
