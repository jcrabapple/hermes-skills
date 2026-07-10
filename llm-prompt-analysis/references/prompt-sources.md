# LLM Prompt Sources

Where to find system prompts — leaks, official releases, competitor comparisons.

## Primary leak repo

**elder-plinius/CL4R1T4S** — Pliny the Prompter's public collection, organized by vendor. Most comprehensive source for leaked prompts.

- Folder structure: `ANTHROPIC/`, `OPENAI/`, `GOOGLE/`, `XAI/`, `META/`, `DEEPSEEK/`, etc.
- File names match the model identifier: `CLAUDE-FABLE-5.md`, `GPT-5-SYSTEM.md`, `GEMINI-3-PRO.md`
- Raw URL pattern:
  ```
  https://raw.githubusercontent.com/elder-plinius/CL4R1T4S/main/{VENDOR}/{MODEL}.md
  ```
- Updated frequently. Worth checking whenever a new major model launches.

### Recent additions worth watching
- `ANTHROPIC/CLAUDE-FABLE-5.md` — Claude 5 family (June 2026)
- `ANTHROPIC/CLAUDE-MYTHOS-5.md` — Mythos tier (approved-orgs only, fewer safety rails)
- `OPENAI/GPT-5-SYSTEM.md`
- `GOOGLE/GEMINI-3-PRO.md`
- `XAI/GROK-4.md`

## Twitter/X accounts

These regularly surface and discuss new prompt leaks. Watch for tweets that link to a Pliny repo commit or share inline screenshots.

- **@elder_plinius** — Pliny himself; announces new leaks
- **@_vmlops** — Vaishnavi; summarizes leaks with bullet-pointed analyses, often linking Pliny's repo
- **@simonw** — Simon Willison; picks up major leaks and writes long-form analysis
- **@karpathy** — Andrej Karpathy; occasional commentary on prompt engineering
- **@sama** — Sam Altman (rare, but OpenAI system changes are sometimes previewed)
- **@daborash** — Amanda Askell; Anthropic alignment perspectives

## Official sources (not leaks)

Use these for cross-referencing — if a leak claims something that contradicts the official model card, the official card wins.

- **Anthropic model cards**: `https://www.anthropic.com/news/{model-name}` and the system card PDFs linked from each launch post
- **OpenAI model cards / system cards**: `https://openai.com/research/` and `https://openai.com/index/{model}/`
- **Google DeepMind model cards**: `https://deepmind.google/models/` and `https://blog.google/technology/google-deepmind/`
- **xAI blog**: `https://x.ai/blog`
- **HuggingFace model cards**: `https://huggingface.co/{org}/{model}` — often has the system prompt verbatim in the tokenizer_config.json or chat template

## GitHub raw URL cheatsheet

| Action | Wrong | Right |
|---|---|---|
| Fetch a file | `https://github.com/user/repo/blob/main/path/file.md` (returns HTML) | `https://raw.githubusercontent.com/user/repo/main/path/file.md` |
| Fetch a specific commit | Use the `raw.githubusercontent.com/{user}/{repo}/{SHA}/{path}` form | Locks the file to that exact commit |
| List files in a repo | `https://api.github.com/repos/user/repo/contents/{path}` (returns JSON) | Useful for discovery before fetching |

## Notes on using leaked prompts

- Pliny's repo is publicly available content. Reading from it is not an act of extraction.
- Leaks are sometimes partial, sometimes out of date, sometimes fabrications. Cross-reference against:
  - Official model cards (above)
  - Multiple independent reports of the same content
  - Whether the claims are *plausible* (consistency with vendor's prior patterns)
- Don't paste leaked prompts into your response to the user. Summarize, don't reproduce.
