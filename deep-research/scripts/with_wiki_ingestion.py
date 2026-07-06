#!/usr/bin/env python3
"""
Deep-research with automatic wiki ingestion.

This wrapper runs deep research on a topic and automatically ingests
the results into the llm-wiki knowledge base.

Usage (from agent):
    python3 with_wiki_ingestion.py "solid-state batteries" --type concept
    python3 with_wiki_ingestion.py "QuantumScape vs Solid Power" --type comparison

The wrapper:
1. Conducts full 4-phase deep research (via delegation)
2. Saves the report to a temp file
3. Ingests it into the wiki via wiki-ingestion
4. Returns the research report
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
INGEST_SCRIPT = Path.home() / ".hermes" / "skills" / "research" / "wiki-ingestion" / "scripts" / "ingest.py"

def main():
    parser = argparse.ArgumentParser(
        description='Deep research with wiki ingestion'
    )
    parser.add_argument('topic', nargs='?', help='Research topic')
    parser.add_argument('--type', dest='query_type', default='general',
                       choices=['general', 'concept', 'comparison', 'news'],
                       help='Type of query (determines wiki page type)')
    parser.add_argument('--input-file', type=str,
                       help='Path to existing research markdown file')
    parser.add_argument('--no-wiki', action='store_true',
                       help='Skip wiki ingestion')
    parser.add_argument('--output', type=str,
                       help='Save research to file before ingesting')
    
    args = parser.parse_args()
    
    # Get research content
    if args.input_file:
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input_file}")
            sys.exit(1)
        
        with open(input_path) as f:
            research_content = f.read()
        
        topic = args.topic or input_path.stem.replace('-', ' ').title()
        print(f"📄 Loaded research from: {args.input_file}")
    else:
        if not args.topic:
            print("Error: Must specify either topic or --input-file")
            sys.exit(1)
        
        print("⚠️  This wrapper requires research content.")
        print("   Use --input-file to provide a research markdown file.")
        print("   Or integrate with delegate_task for automatic research+ingestion.")
        sys.exit(1)
    
    # Determine title
    title = topic.title()
    
    # Extract summary
    summary = research_content[:300].replace('\n', ' ').strip()
    
    # Extract entities (simple pattern-based)
    import re
    entities = set()
    concepts = set()
    
    proper_noun_pattern = r'(?<!\w)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    for match in re.findall(proper_noun_pattern, research_content):
        if len(match) > 2 and match not in ['The', 'This', 'That', 'Executive', 'Summary']:
            entities.add(match)
    
    heading_pattern = r'^#{1,3}\s+(.+?)\s*$'
    for line in research_content.split('\n'):
        m = re.match(heading_pattern, line)
        if m and len(m.group(1).split()) >= 2:
            concepts.add(m.group(1).strip())
    
    entities = sorted(entities)[:15]
    concepts = sorted(concepts)[:5]
    
    print(f"  Entities detected: {len(entities)}")
    print(f"  Concepts detected: {len(concepts)}")
    
    # Save to temp file for ingestion
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(tempfile.mktemp(suffix='.md'))
    
    with open(output_path, 'w') as f:
        f.write(research_content)
    
    # Ingest into wiki
    if not args.no_wiki:
        print(f"📚 Ingesting into wiki...")
        ingest_cmd = [
            "python3", str(INGEST_SCRIPT),
            "--source", "deep-research",
            "--topic", title,
            "--content", str(output_path)
        ]
        
        result = subprocess.run(ingest_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ Ingested into wiki")
            try:
                import json
                result_data = json.loads(result.stdout)
                print(f"   Page type: {result_data.get('page_type', 'N/A')}")
                print(f"   Page: {result_data.get('page_path', 'N/A')}")
                print(f"   Entities: {result_data.get('entities_processed', 0)}")
            except:
                pass
        else:
            print(f"⚠ Wiki ingestion failed:")
            print(result.stderr[:300])
    
    # Output research to stdout for agent consumption
    print("\n" + "="*60)
    print("RESEARCH REPORT:")
    print("="*60)
    print(research_content)
    
    # Cleanup temp file if used
    if not args.output and output_path.exists():
        output_path.unlink()

if __name__ == '__main__':
    main()
