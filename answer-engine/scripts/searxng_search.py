#!/usr/bin/env python3
"""
Query SearXNG instance and return JSON results.
Usage: python searxng_search.py "search query"
"""

import sys
import urllib.parse
import urllib.request
import json
import time

SEARXNG_BASE = "https://searxng.snakepit.us"

def search(query, max_results=10):
    """Query SearXNG and return results list."""
    encoded = urllib.parse.quote_plus(query)
    url = f"{SEARXNG_BASE}/search?q={encoded}&format=json&pageno=1"
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 Hermes-Agent/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            
        results = []
        for item in data.get('results', [])[:max_results]:
            results.append({
                'title': item.get('title', 'No title'),
                'url': item.get('url', ''),
                'content': item.get('content', ''),
                'engine': item.get('engine', 'unknown'),
                'score': item.get('score', 0)
            })
        return results
        
    except Exception as e:
        print(f"Error querying SearXNG: {e}", file=sys.stderr)
        return []

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python searxng_search.py 'search query'", file=sys.stderr)
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    results = search(query)
    print(json.dumps(results, indent=2))
