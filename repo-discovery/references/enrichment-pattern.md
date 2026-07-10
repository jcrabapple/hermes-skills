# GitHub Trending Enrichment Pattern

## Problem
When scraping GitHub trending pages (or search results), you typically get only repository names (`owner/repo`), not full metadata. This causes quality filters to reject all repos as "dead" (0 stars, no description).

## Solution: Two-Phase Enrichment

### Phase 1: Scrape Names
```python
def scrape_trending():
    """Scrape trending pages for repo names."""
    # Returns list of {full_name: "owner/repo", source: "trending-daily"}
    pass
```

### Phase 2: Enrich with Metadata
```python
def enrich_trending_repos(trending_repos):
    """Fetch metadata from GitHub API for scraped repos."""
    enriched = []
    failed = 0
    
    for repo_info in trending_repos:
        full_name = repo_info["full_name"]
        url = f"https://api.github.com/repos/{full_name}"
        
        try:
            wait_for_rate_limit()
            
            req = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github+json"
            })
            
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                enriched_repo = {
                    "full_name": data.get("full_name", ""),
                    "description": (data.get("description") or "").strip(),
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                    "language": data.get("language") or "",
                    "topics": data.get("topics", []),
                    "created_at": data.get("created_at", ""),
                    "pushed_at": data.get("pushed_at", ""),
                    "license": data.get("license", {}).get("spdx_id", "") if data.get("license") else "",
                    "html_url": data.get("html_url", ""),
                    "source": repo_info.get("source", "trending"),
                }
                enriched.append(enriched_repo)
                
        except Exception as e:
            failed += 1
            print(f"WARN: Failed to enrich {full_name}: {e}")
    
    print(f"ENRICH: {len(enriched)}/{len(trending_repos)} succeeded, {failed} failed")
    return enriched
```

## Rate Limiting

```python
# GitHub API rate limits:
# - Unauthenticated: 60 requests/hour
# - Authenticated: 5000 requests/hour
# - Search API: 30 requests/minute (stricter)

def wait_for_rate_limit():
    """Throttle requests to avoid hitting rate limits."""
    # Track timestamps, sleep if needed
    pass
```

## Auth Handling

```python
def get_github_token():
    """Get GitHub token, handle gracefully if not available."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    
    # Try gh CLI
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        # gh CLI not installed — continue without auth
        pass
    except Exception as e:
        print(f"WARN: gh auth failed: {e}")
    
    print("WARN: No GitHub token available. Rate limited to 60 req/hour.")
    return None
```

## Common Pitfalls

1. **Missing enrichment step**: All trending repos filtered as "dead_repo" (0 stars)
2. **Hard crash on missing gh CLI**: Use try/except for FileNotFoundError
3. **Not tracking new vs. enriched**: Count repos actually added to results, not just fetched
4. **Sequential API calls**: For large scans, use asyncio + aiohttp for parallel requests
5. **Infinite retry loops**: Set timeout and max retries per request

## Testing

```python
# Test enrichment with a known repo
test_repos = [
    {"full_name": "bytedance/deer-flow", "source": "test"}
]
enriched = enrich_trending_repos(test_repos)
assert len(enriched) == 1
assert enriched[0]["stars"] > 0
print(f"✓ Enriched: {enriched[0]['full_name']} ({enriched[0]['stars']} stars)")
```
