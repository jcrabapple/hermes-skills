#!/usr/bin/env python3
"""
Track sources and generate citations for research answers.
Usage: 
  - Add sources: citation_tracker.py add "Title" "URL"
  - Generate refs: citation_tracker.py generate
"""

import sys
import json

def load_sources():
    """Load existing sources from temp file."""
    try:
        with open('/tmp/ae_sources.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_sources(sources):
    """Save sources to temp file."""
    with open('/tmp/ae_sources.json', 'w') as f:
        json.dump(sources, f, indent=2)

def add_source(title, url):
    """Add a new source."""
    sources = load_sources()
    # Check for duplicates
    for src in sources:
        if src['url'] == url:
            return src['id']
    
    new_id = len(sources) + 1
    sources.append({'id': new_id, 'title': title, 'url': url})
    save_sources(sources)
    return new_id

def generate_references():
    """Generate formatted references section."""
    sources = load_sources()
    if not sources:
        return "No sources tracked."
    
    lines = []
    for src in sorted(sources, key=lambda x: x['id']):
        lines.append(f"[{src['id']}] {src['title']} - {src['url']}")
    return '\n'.join(lines)

def clear_sources():
    """Clear all tracked sources."""
    save_sources([])
    return "Sources cleared."

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: citation_tracker.py [add|generate|clear] ...", file=sys.stderr)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'add':
        if len(sys.argv) < 4:
            print("Usage: citation_tracker.py add 'Title' 'URL'", file=sys.stderr)
            sys.exit(1)
        title = sys.argv[2]
        url = sys.argv[3]
        cid = add_source(title, url)
        print(f"Added source [{cid}]")
    
    elif cmd == 'generate':
        print(generate_references())
    
    elif cmd == 'clear':
        print(clear_sources())
    
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
