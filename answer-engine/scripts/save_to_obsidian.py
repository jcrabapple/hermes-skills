#!/usr/bin/env python3
"""
Save research results to Obsidian vault.
Usage: save_to_obsidian.py "query" "content" "references"
"""

import sys
import os
import re
from datetime import datetime

def slugify(text):
    """Convert text to safe filename."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text).strip('-')
    return text[:50]  # Limit length

def save_research(query, content, references):
    """Save research to Obsidian Research folder."""
    vault_path = os.path.expanduser("~/Documents/Obsidian Vault/Research")
    
    # Ensure directory exists
    os.makedirs(vault_path, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(query)
    filename = f"{timestamp}-{slug}.md"
    filepath = os.path.join(vault_path, filename)
    
    # Build markdown content
    markdown = f"""# {query}

*Research Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S ET')}*

---

{content}

---

## References

{references}

---

## Metadata

- **Query**: {query}
- **Timestamp**: {datetime.now().isoformat()}
- **Sources**: See References above

"""
    
    # Write file
    with open(filepath, 'w') as f:
        f.write(markdown)
    
    return filepath

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: save_to_obsidian.py 'query' 'content' 'references'", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    content = sys.argv[2]
    references = sys.argv[3]
    
    filepath = save_research(query, content, references)
    print(f"Saved to: {filepath}")
    
    # ─────────────────────────────────────────────────────────────────
    # Also ingest into llm-wiki for compounding knowledge
    # ─────────────────────────────────────────────────────────────────
    try:
        import subprocess
        wiki_ingest = os.path.expanduser(
            "~/.hermes/skills/research/wiki-ingestion/scripts/ingest.py"
        )
        if os.path.exists(wiki_ingest):
            subprocess.run([
                "python3", wiki_ingest,
                "--source", "answer-engine",
                "--file", filepath
            ], check=False, timeout=30)
            print(f"✓ Also ingested into wiki")
    except Exception as e:
        # Non-fatal — research is already saved to Obsidian
        print(f"⚠ Wiki ingestion skipped: {e}")
