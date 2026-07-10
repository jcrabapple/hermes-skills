---
name: ai-context-generation
description: "Generate compact AI-readable context maps from codebases — tools like codesight, repomix, agentic-context that pre-compute project structure to save tokens in AI coding sessions."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [context-engineering, token-savings, codebase-analysis, AI-coding, codesight]
---

# AI Context Generation

Tools that scan a codebase and produce compact, AI-readable context maps (markdown, wiki, or MCP tool sets) so AI coding assistants understand the project without burning tokens on file exploration.

## When to Use

- User wants to generate a context map for an AI coding assistant (Claude Code, Cursor, Copilot, Codex, Aider, etc.)
- User wants blast-radius analysis before refactoring
- User wants to generate project config files (CLAUDE.md, .cursorrules, AGENTS.md) automatically
- User wants to reduce per-conversation token cost for AI-assisted development

## Tools

### codesight (npm)

`npx codesight` — Universal AI context generator. Zero dependencies, MIT, TypeScript. 1.1K+ stars.

**Strengths:**
- Import graph with per-file import counts (language-agnostic — works on Java, Python, JS/TS, etc.)
- Blast radius: `--blast <file>` shows affected files at 3 hops depth
- CI/CD workflow detection (GitHub Actions, secrets)
- Hot file identification (most-coupled files)
- MCP server mode with 13 tools (`--mcp`)
- One-shot config generation: `--init` produces CLAUDE.md, .cursorrules, codex.md, AGENTS.md
- Knowledge mode: `--mode knowledge <path>` maps markdown notes (Obsidian vaults, ADRs) into KNOWLEDGE.md
- Wiki generation: `--wiki` creates a .codesight/wiki/ knowledge base

**Limitations (web/TS-centric):**
- Route detection, schema/model extraction, component props, library exports, env var mapping are tuned for web frameworks (Express, Next.js, React, ORM models). Non-web projects (Android/Java, etc.) get 0 results for these categories.
- "Middleware" detection misclassifies non-web resources (e.g., Android drawable XML icons classified as middleware)
- Token savings claims are inflated for non-web projects (benchmark assumes extraction that didn't happen)
- No folder exclusion — scans everything including build dirs

**Commands:**
```bash
npx codesight                    # Basic scan → .codesight/CODESIGHT.md
npx codesight --blast <file>     # Blast radius: what breaks if you change a file
npx codesight --benchmark        # Token savings breakdown
npx codesight --init             # Generate CLAUDE.md, .cursorrules, codex.md, AGENTS.md
npx codesight --mcp              # Run as MCP server (13 tools)
npx codesight --wiki             # Generate wiki knowledge base
npx codesight --mode knowledge <path>  # Map markdown notes → KNOWLEDGE.md
npx codesight --profile <tool>   # Generate optimized config for a specific AI tool
npx codesight --open             # Open interactive HTML report in browser
```

**Output files (`.codesight/`):**
- `CODESIGHT.md` — combined context map (one file, full project understanding)
- `routes.md` — API routes with method, path, params (web only)
- `schema.md` — DB models with fields, types, keys, relations (web only)
- `components.md` — UI components with props (web only)
- `libs.md` — library exports with function signatures (web only)
- `config.md` — env vars, config files, key deps (web only)
- `middleware.md` — auth, CORS, rate limiting, etc. (web only)
- `graph.md` — import relationships and hot files (language-agnostic)
- `report.html` — interactive visual dashboard (with --html or --open)

## Pitfalls

1. **Check project type before expecting full results** — run `npx codesight --benchmark` first to see what detectors fired. If routes/models/components are all 0, the project type isn't supported for structural extraction.
2. **The import graph and blast radius are always useful** — even when structural extraction fails, the language-agnostic import graph tells you which files are safe to refactor and which touch everything.
3. **Clean up `.codesight/` if not integrating into workflow** — the directory is not gitignored by default. Decide whether to commit it or remove it.
4. **27K files scanned in ~15s** — fast for most projects, but no folder exclusion means build/dependency dirs are included.

## See Also

- `codebase-inspection` skill (pygount) — LOC counting and language breakdown, complementary but different purpose
