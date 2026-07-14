---
name: yolo-dev
description: Run AI coding agents on disposable repo clones. The agent works on a clone — it can't touch your real repo. An optional container (Podman or Docker) provides build/test isolation. You review the diff and decide what (if anything) to apply.
category: software-development
version: 1.0.0
author: Jason Crabtree
license: MIT
metadata:
  hermes:
    tags: [sandbox, podman, docker, coding-agent, safety, diff-review]
    related_skills: [podman-helper, subagent-driven-development]
dependencies:
  - podman-helper
---

# yolo-dev: Disposable Sandbox Coding

Run AI coding agents on disposable repo clones. The agent works on a clone — it can't touch your real repo. An optional container (Podman or Docker) provides build/test isolation. You review the diff and decide what (if anything) to apply.

## Philosophy

> Sandboxes fail. Review gates don't.

The clone provides filesystem isolation. The optional container provides process isolation for builds/tests. But the real safety comes from the workflow: **clone → modify → diff → review → apply**. You're always the gatekeeper.

## Container Runtime

The skill auto-detects the available container runtime. Precedence: **Podman > Docker**. If neither is available, the container phase is skipped and builds/tests run directly in the sandbox (still filesystem-isolated from the real repo).

```bash
# Auto-detection (run once at the start of a yolo session)
if command -v podman &>/dev/null; then
  CONTAINER_RUNTIME="podman"
  SELINUX_LABEL=":Z"          # SELinux relabeling (Podman on Fedora/RHEL)
elif command -v docker &>/dev/null; then
  CONTAINER_RUNTIME="docker"
  SELINUX_LABEL=""            # Docker doesn't use SELinux labels
else
  CONTAINER_RUNTIME=""
fi
```

| Runtime | SELinux Label | Build Command | Notes |
|---|---|---|---|
| Podman | `:Z` required | `podman build` | Rootless by default |
| Docker | No label | `docker build` | May need `sudo` |
| None | N/A | N/A | Builds/tests run in sandbox directly |

## Commands

### `yolo run <task-name> <repo-path> [prompt]`

Clone the repo into a sandbox, delegate the coding task to a Hermes subagent, capture the diff.

### `yolo diff <task-name>`

Show the saved diff from a previous run. If the task has a summary file, show that too.

### `yolo apply <task-name> [--all] [--file <glob>]`

Apply saved changes to the original repo. Without flags, shows diff and asks for confirmation via `clarify`. With `--all`, applies everything. With `--file`, applies only matching files.

### `yolo list`

List all saved tasks with their status (pending review, applied, discarded).

### `yolo clean <task-name>`

Remove the sandbox directory for a task.

## Run Workflow (detailed)

### Phase 1: Setup

```bash
# Create task directory
SANDBOX=~/.hermes/yolo/tasks/<task-name>
mkdir -p "$SANDBOX"

# Clone the repo (shallow, to save space)
git clone --depth 1 <repo-path> "$SANDBOX/repo"
```

If the user didn't provide a prompt, ask: "What should the agent do?"

### Phase 2: Run the Agent

The coding work is done by a `delegate_task` subagent working directly on the sandbox clone. No external API key or CLI tool needed — just Hermes itself.

```python
delegate_task(
    goal="<user-prompt>",
    context="""Working directory: $SANDBOX/repo
This is a disposable clone of <repo-path>. Make changes here.

Rules:
- Modify files in this directory to complete the task
- Run tests/builds to verify your changes work
- Use git diff to confirm what changed
- Do NOT commit anything — just make the file changes

The real repo is at <repo-path>. You're working on a clone — changes will be reviewed before applying.""",
    role="leaf"
)
```

**Why delegate_task instead of a CLI coding agent**:
- No external API key needed — uses the same model as the parent session
- No rate limits, no auth issues, no sunsetted free tiers
- The subagent can run builds/tests directly or via container
- Simpler, fewer dependencies, always available

### Phase 3: Optional Container for Build/Test

For projects that need build/test isolation, optionally spin up a container (Podman or Docker):

```bash
# Only if you want process isolation for builds/tests
$CONTAINER_RUNTIME run -d --name "yolo-<task-name>" --rm \
  -v "$SANDBOX/repo:/workspace$SELINUX_LABEL" \
  -w /workspace \
  yolo-sandbox \
  sleep infinity

# Tell the subagent: "Run builds/tests with: $CONTAINER_RUNTIME exec yolo-<task-name> <command>"
```

### Phase 4: Capture & Summarize

After the subagent completes:

```bash
# Capture the diff
git -C "$SANDBOX/repo" diff > "$SANDBOX/diff.patch"
git -C "$SANDBOX/repo" diff --stat > "$SANDBOX/diff-stat.txt"
```

Present to user as:
```
## yolo run: <task-name> ✓

**Repo**: <repo-path>
**Prompt**: <user-prompt>

### Changes
[git diff --stat output]

Full diff: yolo diff <task-name>
Apply:      yolo apply <task-name>
Discard:    yolo clean <task-name>
```

### Phase 5: Cleanup

If container was used, stop it:
```bash
$CONTAINER_RUNTIME stop "yolo-<task-name>" 2>/dev/null || true
```

## Diff Workflow

```bash
SANDBOX=~/.hermes/yolo/tasks/<task-name>

# Show stat summary
cat "$SANDBOX/diff-stat.txt"

# Show full diff (paginate if long)
read_file "$SANDBOX/diff.patch"
```

## Apply Workflow

### Without flags (interactive confirmation)

Show diff, ask user via `clarify` with choices: "Apply all", "Apply specific files", "Discard".

### With `--all`

```bash
cd <original-repo-path>
git apply ~/.hermes/yolo/tasks/<task-name>/diff.patch
```

**Safety check**: Before applying, verify the working tree is clean:
```bash
cd <original-repo-path> && git diff --quiet && git diff --cached --quiet
```
If dirty, warn the user and abort.

### With `--file <glob>`

```bash
# Filter diff to only matching files, then apply
cd <original-repo-path>
git apply --include="<glob>" ~/.hermes/yolo/tasks/<task-name>/diff.patch
```

### After apply

Ask user if they want to commit immediately or review in editor.

## Optional Sandbox Container Image

For build/test isolation, use the `yolo-sandbox` image (pre-built, ~875MB). Build once with your available runtime:

```bash
# Podman
podman build -t yolo-sandbox \
  -f ./references/Dockerfile ./references/

# Docker
docker build -t yolo-sandbox \
  -f ./references/Dockerfile ./references/
```

The Dockerfile is runtime-agnostic and works with both Podman and Docker.

Includes: Node.js 22, Python 3, git, curl, gcc, build-essential. See `references/Dockerfile`.

## Storage

All tasks live under `~/.hermes/yolo/tasks/`:

```
~/.hermes/yolo/tasks/
├── fix-login-bug/
│   ├── repo/              # Cloned repo (after agent modifications)
│   ├── diff.patch         # The diff
│   ├── diff-stat.txt      # Stat summary
│   └── metadata.json      # {task-name, repo-path, prompt, timestamp, status}
├── refactor-auth/
│   └── ...
```

`metadata.json` structure:
```json
{
  "task_name": "fix-login-bug",
  "repo_path": "/home/user/projects/myapp",
  "prompt": "Fix the OAuth redirect loop in login",
  "created": "2026-07-14T15:30:00-04:00",
  "status": "pending-review",
  "files_changed": 3,
  "insertions": 41,
  "deletions": 4
}
```

## Pitfalls

1. **Large repos**: `git clone --depth 1` keeps it fast, but monorepos may need `--filter=blob:none`. Consider asking before cloning repos >500MB.

2. **Dirty working tree**: Never `git apply` to a repo with uncommitted changes. Always check first.

3. **Binary files**: `git diff` doesn't handle binary files well. If the agent modifies images or binaries, the diff will be empty. Warn the user.

4. **SELinux `:Z` (Podman only)**: Always use `:Z` on bind mounts with Podman on Fedora/RHEL, or the container can't write to the workspace. Docker doesn't need this — the auto-detection handles it via `$SELINUX_LABEL`.

5. **Docker may need `sudo`**: Unlike Podman (rootless by default), Docker typically requires `sudo docker` unless the user is in the `docker` group. The subagent may need to prefix commands with `sudo` when using Docker.

6. **Subagent context limits**: The subagent doesn't have the full repo in context. For large codebases, include relevant file paths or architecture notes in the context field.

7. **Task name collisions**: If a task name already exists, ask the user whether to overwrite or choose a new name.

8. **Build/test isolation**: By default, the subagent runs build/test commands on the host (in the sandbox clone). For untrusted code or projects with risky build scripts, use the optional container.

## Error Recovery

These are common failure modes and what to do about them:

| Failure | Symptoms | Recovery |
|---|---|---|
| **Clone fails** | Network error, disk full, permission denied | Verify the repo path exists and is readable. For remote repos, check network/DNS. If disk is full, suggest `yolo clean` on old tasks. |
| **Subagent timeout** | `delegate_task` returns no result after 2+ minutes | Check if the task was too broad — suggest a narrower prompt. The sandbox clone is still intact; run `yolo diff <task>` to see partial work. |
| **Subagent error** | Subagent returns status=failed | Read the subagent's summary for the specific error. Common causes: missing build tools, syntax errors in generated code, test failures. The sandbox clone has the broken state — inspect with `git -C $SANDBOX/repo diff`. |
| **Apply conflicts** | `git apply` fails with "patch does not apply" | The real repo has diverged from the clone (new commits landed). Options: (a) `git apply --reject` to apply what fits, manually resolve `.rej` files; (b) re-run `yolo run` to get a fresh clone; (c) apply the patch to the specific commit the clone was made from and cherry-pick. |
| **Container won't start** | `podman run` / `docker run` fails | Check if the image exists (`$CONTAINER_RUNTIME images yolo-sandbox`). Build it if missing. Check port conflicts if the project needs network. SELinux denials: verify `:Z` on volume mount. |
| **Container build/test failure** | Build commands return non-zero inside container | The container may be missing language-specific dependencies. Install them inside the container (`$CONTAINER_RUNTIME exec yolo-<task> dnf install -y <pkg>`) and retry. |

## Implementation Notes for the Agent
1. Load this skill + podman-helper (if container needed)
2. Parse `<task-name>`, `<repo-path>`, and optional `[prompt]`
3. If no prompt provided, ask the user: "What should the agent do?"
4. Create task directory and clone repo
5. Delegate the task to a subagent via `delegate_task`
6. After subagent completes, capture `git diff`
7. Generate summary + diff preview
8. Offer next steps: `yolo diff`, `yolo apply`, or `yolo clean`

When the user invokes `yolo diff`:
1. Check if task exists in ~/.hermes/yolo/tasks/<task-name>/
2. Show diff-stat.txt, then the full diff

When the user invokes `yolo apply`:
1. Check if task exists
2. Verify original repo is clean (`git diff --quiet`)
3. If dirty, abort with warning
4. Apply patch (all or filtered)
5. Ask if user wants to commit

When the user invokes `yolo list`:
1. List all directories in ~/.hermes/yolo/tasks/
2. Parse metadata.json from each
3. Show table: task name, repo, date, status, files changed

When the user invokes `yolo clean`:
1. Confirm with user
2. `rm -rf ~/.hermes/yolo/tasks/<task-name>/`

## Verification

After building the skill:
- `yolo run` should create a task directory, clone a repo, and produce a diff
- `yolo diff` should show the saved diff
- `yolo apply` should apply changes to the original repo
- No changes should leak to the original repo without explicit apply
