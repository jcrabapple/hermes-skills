#!/usr/bin/env bash
# audit-skill-for-publish.sh
# Run a battery of leak/authorship checks against a skill directory BEFORE
# committing it to a public repo. Pass/fail per check. Exits 1 if any
# check fails, 0 if all clean.
#
# Usage:
#   bash scripts/audit-skill-for-publish.sh <path/to/skill-dir>
#
# Designed to be run from the skill's own directory (e.g. before
# `git add` on a new skill export), or against a copied-out skill
# directory. The checks are conservative — false positives are possible,
# so review each hit. The script never modifies files.

set -uo pipefail

SKILL_DIR="${1:?usage: audit-skill-for-publish.sh <skill-dir>}"
if [[ ! -d "$SKILL_DIR" ]]; then
  echo "error: not a directory: $SKILL_DIR" >&2
  exit 2
fi

# Files to scan: markdown, python, shell, javascript, yaml, json
INCLUDES=(--include='*.md' --include='*.py' --include='*.sh' \
          --include='*.bash' --include='*.js' --include='*.mjs' \
          --include='*.ts' --include='*.yaml' --include='*.yml' \
          --include='*.json' --include='*.toml' --include='*.txt')

fail_count=0
pass_count=0
results=()

check() {
  local name="$1"
  shift
  if "$@" 2>/dev/null | grep -q .; then
    echo "  ✗ $name"
    "$@" 2>/dev/null | head -5 | sed 's/^/      /'
    fail_count=$((fail_count + 1))
    results+=("FAIL $name")
  else
    echo "  ✓ $name"
    pass_count=$((pass_count + 1))
    results+=("PASS $name")
  fi
}

echo "Auditing: $SKILL_DIR"
echo "── Authorship / upstream signals ──"

# 1. LICENSE file with non-MIT / non-self copyright
check "LICENSE references another author" \
  bash -c "find '$SKILL_DIR' -maxdepth 1 -name LICENSE -exec grep -lE 'Copyright.*[0-9]{4}.*([A-Z][a-z]+ [A-Z][a-z]+|Matt|Van Horn|MIT License)' {} \;"

# 2. Frontmatter author/homepage/repository pointing to another maintainer
check "SKILL.md frontmatter names another author" \
  grep -rInE '^(author|homepage|repository):\s*(mvanhorn|heredotnow|nexu-io|openai|anthropic|[a-z0-9-]+/[a-z0-9-]+-skill)' \
    "$SKILL_DIR" "${INCLUDES[@]}"

# 3. npx skills add / pip install hint suggesting a specific installer
check "SKILL.md references an upstream installer" \
  grep -rInE '(npx skills add|pip install .*skill|claude plugin install)' \
    "$SKILL_DIR" "${INCLUDES[@]}"

# 4. Bundled vendor dir (suggests vendored third-party)
check "Bundled vendor/ or node_modules/ directory" \
  bash -c "find '$SKILL_DIR' -maxdepth 2 -type d \( -name vendor -o -name node_modules \) | head -3"

echo
echo "── Personal data leaks ──"

# 5. Personal email addresses (filters out the common placeholders)
check "Personal email address" \
  grep -rInE '[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.(com|us|to|net|org|io)' \
    "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE '(@example\.com|@example\.org|@your-domain|@contact|@hermes|@your-email|@hermesagent|@anthropic\.com|@openai\.com|@github\.com|@noreply)'

# 6. Hardcoded API keys (common shapes)
check "Hardcoded API key (sk-, pk-, hex blobs)" \
  grep -rInE '(sk-[a-zA-Z0-9]{16,}|pk_(live|test)_[a-zA-Z0-9]+|sk_(live|test)_[a-zA-Z0-9]{16,}|[a-f0-9]{32,})' \
    "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE '(example|sample|placeholder|your[_-]?key)'

# 7. Common API key variable assignments with literal values
check "API key / secret variable with literal value" \
  grep -rInE '(API[_-]?KEY|SECRET|TOKEN|PASSWORD)\s*=\s*["'\''][a-zA-Z0-9]{16,}["'\'']' \
    "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE 'os\.environ|process\.env|\$\{?[A-Z_]+\}?'

# 8. User-specific service instance URLs (PikaPod, ngrok, custom domains)
check "User-specific instance URL" \
  grep -rInE 'https?://[a-z0-9-]+\.(pikapod\.net|ngrok\.io|ngrok-free\.app|localtunnel\.me|trycloudflare\.com)' \
    "$SKILL_DIR" "${INCLUDES[@]}"

# 9. Personal filesystem paths
check "Personal filesystem path" \
  grep -rInE '(/home/[a-z]+/|/Users/[A-Za-z]+/|~?/Documents/[A-Z][a-z]+)' \
    "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE '(~/.hermes|~/.config|~/.local|~/Documents)'

# 10. Hardcoded usernames in service APIs (Last.fm, GitHub, etc.)
check "Service API username hardcoded" \
  grep -rInE 'USERNAME\s*=\s*["'\''][a-z][a-z0-9_-]+["'\'']' \
    "$SKILL_DIR" --include='*.py' --include='*.sh' --include='*.js' \
  | grep -vE 'os\.environ|process\.env|your_username|placeholder'

# 11. Real flight numbers in worked examples (UA#### / AA#### / DL#### / etc.)
check "Real flight number in worked example" \
  grep -rInE '\b(UA|AA|DL|WN|AS|HA|B6|NK|F9)[0-9]{3,4}\b' \
    "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE '(UA123|AA456|DL789)'  # known-safe example patterns

# 12. Real car rental confirmation numbers (long all-digit, in trip context)
check "Possible car rental / booking confirmation #" \
  grep -rInE '(rental|reservation|confirmation|booking).*#[0-9]{6,}' \
    "$SKILL_DIR" "${INCLUDES[@]}"

# 13. Phone numbers — including partial-redaction forms like +140****8075
# which still leak area code + last 4. Catch any +1 with 8+ digit-or-asterisk
# chars in any of the common US/Canada formats.
check "Phone number (full or partial-redaction form)" \
  grep -rInE '\+1[0-9*()\s.-]{8,18}' "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE '(\+1-XXX|\+1-REDACTED|\+1-555-555-5555|555-01[0-9]{2}-[0-9]{4})'

# 14. Personal service inbox IDs (AgentMail and similar). The inbox part
# before @ is a stable identifier that's effectively a username — if
# `herman-the-hermes-agent@agentmail.to` appears in worked examples, every
# downstream user sees it.
check "Personal service inbox ID" \
  grep -rInE '[a-z][a-z0-9._-]+@agentmail\.to' "$SKILL_DIR" "${INCLUDES[@]}" \
  | grep -vE '(inbox@agentmail|you@agentmail|your-inbox@agentmail|user@agentmail|example@agentmail)'

# 15. Public-facing personal URLs (Cloudflare tunnels, custom tunnels, etc.)
# These identify the user even if the host changes. pgs.sh / snakepit.us
# hosts are user-named tunnels, not anonymous ones.
check "Personal public-facing URL (tunnel, pgs.sh, snakepit, etc.)" \
  grep -rInE 'https?://[a-z0-9-]+\.(pgs\.sh|snakepit\.[a-z]+|trycloudflare\.com|heredotnow\.com)' \
    "$SKILL_DIR" "${INCLUDES[@]}"

echo
echo "── Done ──"
echo "  Passed: $pass_count"
echo "  Failed: $fail_count"

if [[ $fail_count -gt 0 ]]; then
  echo
  echo "Action: review each hit above. Replace literal values with env-var"
  echo "lookups (os.environ['FOO'], \$FOO, process.env.FOO) or placeholders."
  echo "Re-run after fixes. Exits 1 on any failure."
  exit 1
fi

exit 0
