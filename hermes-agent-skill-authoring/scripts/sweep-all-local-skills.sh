#!/usr/bin/env bash
# sweep-all-local-skills.sh
# Run audit-skill-for-publish.sh against every skill in a skills root
# (default: ~/.hermes/skills/) and aggregate pass/fail counts. This is
# the "When you find one leak, sweep all local skills" workflow in
# script form — one bad pattern in one skill usually means the same
# pattern is sitting in 5-10 other skills, and you want a single run
# that names them all.
#
# Usage:
#   bash scripts/sweep-all-local-skills.sh                  # scan ~/.hermes/skills/
#   bash scripts/sweep-all-local-skills.sh /path/to/skills  # custom root
#   bash scripts/sweep-all-local-skills.sh --stop-on-fail   # exit on first hit
#   bash scripts/sweep-all-local-skills.sh --json           # machine-readable output
#
# Output: per-skill pass/fail counts, then an aggregate summary listing
# the skills that have at least one failure. Exits non-zero if any skill
# failed. This script never modifies files.

set -uo pipefail

SKILLS_ROOT="${HOME}/.hermes/skills"
STOP_ON_FAIL=0
JSON_OUTPUT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stop-on-fail) STOP_ON_FAIL=1; shift ;;
    --json)         JSON_OUTPUT=1; shift ;;
    -h|--help)
      sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# //; s/^#//'
      exit 0
      ;;
    *) SKILLS_ROOT="$1"; shift ;;
  esac
done

if [[ ! -d "$SKILLS_ROOT" ]]; then
  echo "error: not a directory: $SKILLS_ROOT" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT="$SCRIPT_DIR/audit-skill-for-publish.sh"
if [[ ! -x "$AUDIT" && ! -f "$AUDIT" ]]; then
  echo "error: audit script not found at $AUDIT" >&2
  echo "  (this wrapper expects to live next to audit-skill-for-publish.sh)" >&2
  exit 2
fi

total_skills=0
total_failures=0
skills_with_failures=()
total_passed=0
total_failed=0

# Per-skill JSON accumulator (only used in --json mode)
json_entries=()

for d in "$SKILLS_ROOT"/*/; do
  # Defensive: glob may not match if dir is empty
  [[ -d "$d" ]] || continue
  skill_name="$(basename "$d")"
  # Skip hidden / backup / cache dirs
  case "$skill_name" in
    .*|backup*|backups*|node_modules*|__pycache__*|dist*|*.bak) continue ;;
  esac
  # Only scan dirs that have a SKILL.md (skips category-level dirs in
  # layout that uses <category>/<skill>/SKILL.md)
  if [[ ! -f "$d/SKILL.md" ]]; then
    # Could be a category dir containing sub-skills — recurse one level
    for sub in "$d"/*/; do
      [[ -d "$sub" ]] || continue
      sub_name="$(basename "$sub")"
      case "$sub_name" in
        .*|backup*|backups*|node_modules*|__pycache__*|dist*) continue ;;
      esac
      if [[ -f "$sub/SKILL.md" ]]; then
        :  # fall through to scan this sub-skill below by adjusting d
        d="$sub"
        skill_name="${skill_name}/${sub_name}"
        break
      fi
    done
    [[ -f "$d/SKILL.md" ]] || continue
  fi

  total_skills=$((total_skills + 1))

  if [[ $JSON_OUTPUT -eq 0 ]]; then
    echo "── $skill_name ──"
  fi

  # Run audit; capture output and exit code
  output=$("$AUDIT" "$d" 2>&1)
  exit_code=$?

  pass_count=$(echo "$output" | grep -c "^  ✓ " || true)
  fail_count=$(echo "$output" | grep -c "^  ✗ " || true)
  total_passed=$((total_passed + pass_count))
  total_failed=$((total_failed + fail_count))

  if [[ $JSON_OUTPUT -eq 1 ]]; then
    # Capture failing-check names for JSON
    failed_names=$(echo "$output" | grep "^  ✗ " | sed 's/^  ✗ //' | jq -R . | jq -s . 2>/dev/null || echo '[]')
    json_entries+=("{\"skill\": $(echo "$skill_name" | jq -R .), \"passed\": $pass_count, \"failed\": $fail_count, \"failing_checks\": $failed_names}")
  else
    if [[ $fail_count -gt 0 ]]; then
      # Show the failed-check lines so the user can see what hit
      echo "$output" | grep "^  ✗ " | sed 's/^/    /' | head -20
    fi
    if [[ $fail_count -gt 20 ]]; then
      echo "    ... and $((fail_count - 20)) more"
    fi
  fi

  if [[ $exit_code -ne 0 ]]; then
    total_failures=$((total_failures + 1))
    skills_with_failures+=("$skill_name")
    if [[ $STOP_ON_FAIL -eq 1 && $JSON_OUTPUT -eq 0 ]]; then
      echo
      echo "First failure in: $skill_name. Stopping."
      echo
      echo "$output"
      exit 1
    fi
  fi
done

if [[ $JSON_OUTPUT -eq 1 ]]; then
  # Emit JSON
  printf '{\n'
  printf '  "skills_root": %s,\n' "$(echo "$SKILLS_ROOT" | jq -R .)"
  printf '  "skills_scanned": %d,\n' "$total_skills"
  printf '  "skills_clean": %d,\n' "$((total_skills - total_failures))"
  printf '  "skills_with_failures": %d,\n' "$total_failures"
  printf '  "total_checks_passed": %d,\n' "$total_passed"
  printf '  "total_checks_failed": %d,\n' "$total_failed"
  printf '  "failing_skills": [\n'
  for i in "${!json_entries[@]}"; do
    if [[ $i -lt $((${#json_entries[@]} - 1)) ]]; then
      printf '    %s,\n' "${json_entries[$i]}"
    else
      printf '    %s\n' "${json_entries[$i]}"
    fi
  done
  printf '  ]\n'
  printf '}\n'
else
  echo
  echo "── Summary ──"
  echo "  Skills scanned:        $total_skills"
  echo "  Skills clean:          $((total_skills - total_failures))"
  echo "  Skills with failures:  $total_failures"
  echo "  Total checks passed:   $total_passed"
  echo "  Total checks failed:   $total_failed"
  if [[ $total_failures -gt 0 ]]; then
    echo
    echo "  Failing skills:"
    for s in "${skills_with_failures[@]}"; do
      echo "    - $s"
    done
    echo
    echo "  To drill into one: bash $AUDIT $SKILLS_ROOT/<skill>"
  else
    echo
    echo "  ✓ all skills clean"
  fi
fi

if [[ $total_failures -gt 0 ]]; then
  exit 1
fi
exit 0
