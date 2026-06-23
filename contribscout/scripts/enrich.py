#!/usr/bin/env python3
"""enrich.py — Enrich discovered repos with contribution-relevant signals.

Reads JSON array from stdin (discover.sh output), fetches for each repo:
- README content and size
- Open issues with labels (good first issue, help wanted)
- CONTRIBUTING.md presence
- Recent PR merge rate (last 10 PRs)
- Number of unique contributors
- Recent commit activity (last 10 commits)

Outputs enriched JSON to stdout.

Usage:
    ./discover.sh | python enrich.py [--max-repos N] [--timeout SECS]

Requires: gh CLI (authenticated), jq
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any


def gh_api(endpoint: str, timeout: int = 10) -> dict | list | None:
    """Call GitHub API via gh CLI. Returns parsed JSON or None on failure."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint, "--jq", "."],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout) if result.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def gh_search_issues(query: str, timeout: int = 10) -> list[dict]:
    """Search GitHub issues/PRs via gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "search", "issues", query, "--limit", "10", "--json",
             "number,title,state,createdAt,updatedAt,labels,url,comments"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            return []
        return json.loads(result.stdout) if result.stdout.strip() else []
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return []


def check_file_exists(full_name: str, path: str) -> bool:
    """Check if a file exists in the repo root via gh api."""
    result = gh_api(f"repos/{full_name}/contents/{path}")
    return result is not None


def enrich_repo(repo: dict) -> dict:
    """Enrich a single repo with contribution signals."""
    full_name = repo["fullName"]
    enriched = {**repo}

    # 1. README content (first 3000 chars for analysis)
    readme_data = gh_api(f"repos/{full_name}/readme")
    if readme_data and "content" in readme_data:
        import base64
        try:
            readme_raw = base64.b64decode(readme_data["content"]).decode("utf-8", errors="replace")
            enriched["readmeContent"] = readme_raw[:3000]
            enriched["readmeSize"] = len(readme_raw)
            enriched["readmeQuality"] = (
                "strong" if len(readme_raw) > 2000
                else "basic" if len(readme_raw) > 500
                else "thin" if len(readme_raw) > 100
                else "missing"
            )
        except Exception:
            enriched["readmeContent"] = ""
            enriched["readmeSize"] = 0
            enriched["readmeQuality"] = "missing"
    else:
        enriched["readmeContent"] = ""
        enriched["readmeSize"] = 0
        enriched["readmeQuality"] = "missing"

    # 2. CONTRIBUTING.md presence
    enriched["hasContributing"] = check_file_exists(full_name, "CONTRIBUTING.md")

    # 3. Open issues with contribution-friendly labels
    good_first_issues = gh_search_issues(
        f"repo:{full_name} is:issue is:open label:\"good first issue\""
    )
    help_wanted = gh_search_issues(
        f"repo:{full_name} is:issue is:open label:\"help wanted\""
    )

    enriched["goodFirstIssues"] = [
        {"number": i.get("number"), "title": i.get("title"), "url": i.get("url"),
         "comments": i.get("comments", 0)}
        for i in good_first_issues[:5]
    ]
    enriched["helpWantedIssues"] = [
        {"number": i.get("number"), "title": i.get("title"), "url": i.get("url"),
         "comments": i.get("comments", 0)}
        for i in help_wanted[:5]
    ]

    # 4. Recent PRs (merge rate — saturation signal)
    recent_prs = gh_search_issues(f"repo:{full_name} is:pr sort:updated")
    merged_prs = [p for p in recent_prs if p.get("state") == "CLOSED"]
    open_prs = [p for p in recent_prs if p.get("state") == "OPEN"]

    enriched["recentPrs"] = {
        "total": len(recent_prs),
        "merged": len(merged_prs),
        "open": len(open_prs),
        "sample": [
            {"number": p.get("number"), "title": p.get("title"),
             "state": p.get("state"), "url": p.get("url")}
            for p in recent_prs[:5]
        ]
    }

    # 5. Contributor count
    contributors = gh_api(f"repos/{full_name}/contributors?per_page=100")
    enriched["contributorCount"] = len(contributors) if isinstance(contributors, list) else 0

    # 6. Recent commits (activity signal)
    commits = gh_api(f"repos/{full_name}/commits?per_page=10")
    if isinstance(commits, list) and commits:
        enriched["recentCommitCount"] = len(commits)
        enriched["lastCommitDate"] = commits[0].get("commit", {}).get("author", {}).get("date", "")
        enriched["lastCommitMessage"] = commits[0].get("commit", {}).get("message", "")[:200]
    else:
        enriched["recentCommitCount"] = 0
        enriched["lastCommitDate"] = ""
        enriched["lastCommitMessage"] = ""

    # 7. Computed signals
    contribution_signals = 0
    if enriched["hasContributing"]:
        contribution_signals += 1
    if enriched["goodFirstIssues"]:
        contribution_signals += 1
    if enriched["helpWantedIssues"]:
        contribution_signals += 1
    if enriched["readmeQuality"] in ("basic", "strong"):
        contribution_signals += 1
    if enriched["openIssues"] > 0:
        contribution_signals += 1

    enriched["contributionSignalCount"] = contribution_signals

    # Saturation: contributor count relative to project size
    # For low-star repos (<50), saturation is inherently low (room to stand out)
    # For larger repos, use contributor-to-star ratio
    if repo["stars"] < 50:
        enriched["saturationLevel"] = "low"
    elif enriched["contributorCount"] > 0 and repo["stars"] > 0:
        ratio = enriched["contributorCount"] / max(repo["stars"], 1)
        enriched["saturationLevel"] = (
            "high" if ratio > 0.3 or repo["stars"] > 3000
            else "medium" if ratio > 0.1 or repo["stars"] > 500
            else "low"
        )
    else:
        enriched["saturationLevel"] = "unknown"

    return enriched


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enrich discovered repos with contribution signals."
    )
    parser.add_argument("--max-repos", type=int, default=10,
                        help="Max repos to enrich (default 10)")
    parser.add_argument("--timeout", type=int, default=120,
                        help="Overall timeout in seconds (default 120)")
    args = parser.parse_args()

    try:
        repos = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: invalid JSON on stdin", file=sys.stderr)
        return 1

    if not isinstance(repos, list) or not repos:
        print("[]")
        return 0

    # Take the bottom N (lowest stars = highest opportunity)
    repos = repos[:args.max_repos]

    enriched_results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_repo = {
            executor.submit(enrich_repo, repo): repo for repo in repos
        }

        for future in as_completed(future_to_repo):
            if time.time() - start_time > args.timeout:
                break

            repo = future_to_repo[future]
            try:
                result = future.result(timeout=30)
                enriched_results.append(result)
                print(f"  ✓ {repo['fullName']}: "
                      f"{result['contributionSignalCount']} signals, "
                      f"{result['contributorCount']} contributors, "
                      f"{result['saturationLevel']} saturation",
                      file=sys.stderr)
            except Exception as e:
                print(f"  ✗ {repo['fullName']}: {e}", file=sys.stderr)

    # Sort by contribution signal count (descending), then stars (ascending)
    enriched_results.sort(
        key=lambda r: (-r.get("contributionSignalCount", 0), r.get("stars", 0))
    )

    json.dump(enriched_results, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
