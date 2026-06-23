#!/usr/bin/env bash
# discover.sh — Search GitHub for contribution opportunities via gh CLI
#
# Outputs JSON array of candidate repos to stdout.
# Strategy: keyword searches via GitHub Search API, sorted by stars ascending
# (low stars = high opportunity for visibility). Filters by activity and age.
#
# Usage:
#   ./discover.sh [--max-results N] [--languages lang1,lang2] [--keywords kw1,kw2]
#                 [--max-stars N] [--min-stars N] [--created-days N] [--pushed-days N]
#
# Defaults: 30 results, 0-1000 stars, created in last 120 days, pushed in last 30 days

set -euo pipefail

MAX_RESULTS=30
LANGUAGES="TypeScript,Python"
KEYWORDS="mcp server,agent sdk,developer tools,api sdk,automation workflow,llm tooling,ai agent,open source sdk,cli tool framework,developer workflow"
MAX_STARS=1000
MIN_STARS=0
CREATED_DAYS=120
PUSHED_DAYS=30

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-results)  MAX_RESULTS="$2"; shift 2;;
    --languages)    LANGUAGES="$2"; shift 2;;
    --keywords)     KEYWORDS="$2"; shift 2;;
    --max-stars)    MAX_STARS="$2"; shift 2;;
    --min-stars)    MIN_STARS="$2"; shift 2;;
    --created-days) CREATED_DAYS="$2"; shift 2;;
    --pushed-days)  PUSHED_DAYS="$2"; shift 2;;
    *) echo "Unknown option: $1" >&2; exit 1;;
  esac
done

IFS=',' read -ra LANG_ARRAY <<< "$LANGUAGES"
IFS=',' read -ra KEYWORD_ARRAY <<< "$KEYWORDS"

CREATED_AFTER=$(date -d "${CREATED_DAYS} days ago" +%Y-%m-%d)
PUSHED_AFTER=$(date -d "${PUSHED_DAYS} days ago" +%Y-%m-%d)

ALL_RESULTS="[]"

for lang in "${LANG_ARRAY[@]}"; do
  for kw in "${KEYWORD_ARRAY[@]}"; do
    # URL-encode the keyword (replace spaces with +)
    ENCODED_KW=$(echo "$kw" | sed 's/ /+/g')

    # GitHub Search API: sort by stars ascending to surface small repos
    # Use stars:N..M range syntax (stars:>=N doesn't work reliably)
    STAR_FILTER="stars:${MIN_STARS}..${MAX_STARS}"
    ENDPOINT="/search/repositories?q=${ENCODED_KW}+language:${lang}+${STAR_FILTER}+created:>${CREATED_AFTER}+pushed:>${PUSHED_AFTER}&sort=stars&order=asc&per_page=10"

    RESULT=$(gh api "$ENDPOINT" \
      --jq '.items' \
      2>/dev/null || echo '[]')

    if [[ "$RESULT" != "[]" && -n "$RESULT" ]]; then
      ALL_RESULTS=$(echo "$ALL_RESULTS" | jq -c --argjson new "$RESULT" '. + $new')
    fi
  done
done

# Deduplicate, filter, transform, sort by stars ascending, take top N
echo "$ALL_RESULTS" | jq -c '
  unique_by(.full_name)
  | map(select(.archived == false))
  | map({
      name: (.full_name | split("/") | .[1]),
      fullName: .full_name,
      description: (.description // ""),
      url: .html_url,
      stars: .stargazers_count,
      forks: .forks_count,
      openIssues: .open_issues_count,
      createdAt: .created_at,
      updatedAt: .updated_at,
      pushedAt: .pushed_at,
      language: (.language // ""),
      topics: (.topics // []),
      license: (.license.name // "None")
    })
  | sort_by(.stars)
  | .[0:'"${MAX_RESULTS}"']
'
