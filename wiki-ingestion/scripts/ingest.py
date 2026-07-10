#!/usr/bin/env python3
"""
Ingest research outputs into llm-wiki.

Supported sources:
  - answer-engine: Research markdown files from ~/Documents/Obsidian Vault/Research/
  - weekly-blog: Research drafts before blog condensation
"""

import argparse
import os
import re
import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ─────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────

DEFAULT_WIKI_PATH = os.path.expanduser("~/wiki")
RESEARCH_DIR = os.path.expanduser("~/Documents/Obsidian Vault/Research")

# ─────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text).strip('-')
    return text[:60]

def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def append_file(path: str, content: str) -> None:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm_raw = content[3:end].strip()
            body = content[end+3:].lstrip('\n')
            metadata = {}
            for line in fm_raw.split('\n'):
                if ':' in line and not line.startswith('#'):
                    key, _, val = line.partition(':')
                    metadata[key.strip()] = val.strip().strip('"').strip("'")
            return metadata, body
    return {}, content

def extract_title(content: str) -> str:
    for line in content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled"

def extract_section(content: str, heading: str) -> Optional[str]:
    pattern = rf'^##+\s+{re.escape(heading)}\s*$'
    lines = content.split('\n')
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return None
    result = []
    for line in lines[start:]:
        if line.startswith('#') and line.strip() != '':
            break
        result.append(line)
    return '\n'.join(result).strip()

# ─────────────────────────────────────────────────────────────────
# Entity extraction
# ─────────────────────────────────────────────────────────────────

def extract_entities_simple(content: str) -> Tuple[List[str], List[str]]:
    entities = set()
    concepts = set()
    
    proper_noun_pattern = r'(?<!\w)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    matches = re.findall(proper_noun_pattern, content)
    
    stopwords = {
        # Articles/demonstratives
        'The', 'This', 'That', 'These', 'Those', 'Such', 'Each', 'Every', 'Both', 'Either',
        # Section headers
        'Executive', 'Summary', 'Key', 'Findings', 'Detailed', 'Analysis',
        'Introduction', 'Background', 'Conclusion', 'References', 'Metadata',
        'Research', 'Date', 'Query', 'Timestamp', 'Sources', 'Notes',
        # Days/months
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December',
        # Timezones
        'ET', 'PT', 'UTC', 'EST', 'EDT', 'CST', 'MST', 'PST',
        # Common verbs that get capitalized
        'Is', 'Are', 'Was', 'Were', 'Be', 'Being', 'Been',
        'Have', 'Has', 'Had', 'Do', 'Does', 'Did',
        'Will', 'Would', 'Should', 'Could', 'May', 'Might', 'Can',
        'Make', 'Makes', 'Made', 'Get', 'Gets', 'Got',
        'Take', 'Takes', 'Took', 'See', 'Sees', 'Saw',
        'Look', 'Looks', 'Looked', 'Come', 'Comes', 'Came',
        'Want', 'Wants', 'Wanted', 'Need', 'Needs', 'Needed',
        'Use', 'Uses', 'Used', 'Find', 'Finds', 'Found',
        'Give', 'Gives', 'Gave', 'Put', 'Puts', 'Say', 'Says', 'Said',
        'Go', 'Goes', 'Went', 'Know', 'Knows', 'Knew',
        # Common nouns that aren't entities
        'Bottom', 'Line', 'Top', 'Bottom', 'Number', 'Numbers',
        'Percent', 'Percentage', 'Year', 'Years', 'Month', 'Months',
        'Day', 'Days', 'Time', 'Times', 'Hour', 'Hours',
        'Question', 'Questions', 'Answer', 'Answers',
        'Problem', 'Problems', 'Solution', 'Solutions',
        'Challenge', 'Challenges', 'Controversy', 'Controversies',
        'Implication', 'Implications', 'Impact', 'Impacts',
        'Factor', 'Factors', 'Reason', 'Reasons',
        'Example', 'Examples', 'Case', 'Cases', 'Study', 'Studies',
        'Report', 'Reports', 'Paper', 'Papers', 'Article', 'Articles',
        'Source', 'Sources', 'Reference', 'References',
        'Data', 'Point', 'Points', 'Statistic', 'Statistics',
        'Figure', 'Figures', 'Table', 'Tables',
        'Section', 'Sections', 'Chapter', 'Chapters',
        'Part', 'Parts', 'Piece', 'Pieces',
        'Type', 'Types', 'Kind', 'Kinds',
        'Version', 'Versions', 'Edition', 'Editions',
        'Release', 'Releases', 'Update', 'Updates',
        'News', 'Update', 'Updates', 'Announcement', 'Announcements',
        # Technology/generic terms
        'Technology', 'Technologies', 'System', 'Systems',
        'Method', 'Methods', 'Process', 'Processes',
        'Approach', 'Approaches', 'Strategy', 'Strategies',
        'Technique', 'Techniques', 'Mechanism', 'Mechanisms',
        'Device', 'Devices', 'Tool', 'Tools',
        'Product', 'Products', 'Service', 'Services',
        'Feature', 'Features', 'Function', 'Functions',
        'Capability', 'Capabilities',
        # Companies/orgs often have these words but they're not entities by themselves
        'Inc', 'Inc.', 'Corp', 'Corp.', 'Ltd', 'Ltd.', 'LLC', 'LLC.',
        'Company', 'Companies', 'Corporation', 'Corporations',
        'Organization', 'Organizations', 'Group', 'Groups',
        'Team', 'Teams', 'Lab', 'Labs', 'Laboratory', 'Laboratories',
        'Institute', 'Institutes', 'Center', 'Centers', 'Centre', 'Centres',
        'University', 'Universities', 'College', 'Colleges',
        'Department', 'Departments', 'Division', 'Divisions',
        # Geographic
        'North', 'South', 'East', 'West', 'Central',
        'City', 'Cities', 'State', 'States', 'Country', 'Countries',
        'Region', 'Regions', 'Area', 'Areas',
        # Units
        'Kilogram', 'Kilograms', 'Meter', 'Meters', 'Liter', 'Liters',
        'Watt', 'Watts', 'Volt', 'Volts', 'Ampere', 'Amperes',
        'Hertz', 'Hertz', 'Ohm', 'Ohms',
        # Academic/research
        'Paper', 'Papers', 'Study', 'Studies', 'Research', 'Researcher',
        'Scientist', 'Scientists', 'Professor', 'Professors',
        'Doctor', 'Doctors', 'PhD', 'Ph.D.',
        'Journal', 'Journals', 'Conference', 'Conferences',
        'Proceedings', 'Publication', 'Publications',
        # Common in research papers
        'Abstract', 'Introduction', 'Method', 'Methods', 'Methodology',
        'Result', 'Results', 'Discussion', 'Discussions',
        'Conclusion', 'Conclusions', 'Summary', 'Summaries',
        'Future', 'Future Work', 'Ongoing', 'Currently',
        'Previous', 'Prior', 'Existing', 'Existing Work',
        'Related', 'Related Work', 'Literature', 'Literature Review',
        # Misc
        'Yes', 'No', 'Maybe', 'Perhaps',
        'Good', 'Bad', 'Better', 'Worse', 'Best', 'Worst',
        'High', 'Low', 'Higher', 'Lower', 'Highest', 'Lowest',
        'Large', 'Small', 'Larger', 'Smaller', 'Largest', 'Smallest',
        'Fast', 'Slow', 'Faster', 'Slower', 'Fastest', 'Slowest',
        'New', 'Old', 'Newer', 'Older', 'Newest', 'Oldest',
        'Young', 'Old', 'Younger', 'Older', 'Youngest', 'Oldest',
        'First', 'Second', 'Third', 'Fourth', 'Fifth',
        'Last', 'Next', 'Previous', 'Current',
        'Overall', 'Generally', 'Typically', 'Usually',
        'Often', 'Sometimes', 'Rarely', 'Never', 'Always',
        'Many', 'Much', 'Few', 'Several', 'Multiple',
        'Some', 'Any', 'All', 'None', 'Most', 'Least',
        'Various', 'Various', 'Different', 'Similar',
        'Important', 'Important', 'Critical', 'Critical',
        'Significant', 'Significant', 'Major', 'Major',
        'Minor', 'Minor', 'Primary', 'Primary', 'Secondary', 'Secondary',
    }
    
    for match in matches:
        if match not in stopwords and len(match) > 2:
            entities.add(match)
    
    heading_pattern = r'^#{1,3}\s+(.+?)\s*$'
    for line in content.split('\n'):
        m = re.match(heading_pattern, line)
        if m:
            heading = m.group(1).strip()
            if len(heading.split()) >= 2:
                concepts.add(heading)
    
    wikilink_pattern = r'\[\[([^\]]+)\]\]'
    for match in re.findall(wikilink_pattern, content):
        entities.add(match)
    
    return sorted(entities), sorted(concepts)

# ─────────────────────────────────────────────────────────────────
# Wiki page operations
# ─────────────────────────────────────────────────────────────────

def read_wiki_page(wiki_path: str, page_name: str) -> Optional[str]:
    safe_name = page_name.lower().replace(' ', '-')
    for subdir in ['entities', 'concepts', 'comparisons', 'queries']:
        p = os.path.join(wiki_path, subdir, f"{safe_name}.md")
        if os.path.exists(p):
            with open(p) as f:
                return f.read()
    return None

def create_wiki_page(
    wiki_path: str,
    page_type: str,
    title: str,
    content: str,
    metadata: Dict,
    cross_refs: List[str]
) -> str:
    safe_name = slugify(title)
    page_dir = os.path.join(wiki_path, page_type)
    os.makedirs(page_dir, exist_ok=True)
    filepath = os.path.join(page_dir, f"{safe_name}.md")
    
    today = date.today().isoformat()
    frontmatter = f"""---
title: "{title}"
created: {today}
updated: {today}
type: {page_type}
tags: {json.dumps(metadata.get('tags', []))}
sources:
  - type: {metadata.get('source_type', 'unknown')}
    reference: "{metadata.get('reference', title)}"
    date: {today}
---
"""
    
    body = f"# {title}\n\n"
    if metadata.get('summary'):
        body += f"*{metadata['summary']}*\n\n"
    body += "---\n\n"
    body += content + "\n\n"
    
    if cross_refs:
        body += "## Related\n\n"
        for ref in cross_refs[:10]:
            body += f"- [[{ref}]]\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + "\n" + body)
    
    return filepath

def update_wiki_page(
    wiki_path: str,
    page_type: str,
    title: str,
    new_content: str,
    additional_refs: List[str] = None
) -> str:
    safe_name = slugify(title)
    filepath = None
    for subdir in ['entities', 'concepts', 'comparisons', 'queries']:
        p = os.path.join(wiki_path, subdir, f"{safe_name}.md")
        if os.path.exists(p):
            filepath = p
            break
    
    if not filepath:
        raise FileNotFoundError(f"Page not found: {title}")
    
    with open(filepath) as f:
        existing = f.read()
    
    metadata, body = parse_frontmatter(existing)
    metadata['updated'] = date.today().isoformat()
    
    updated_body = body.rstrip() + "\n\n---\n\n" + new_content
    
    if additional_refs:
        if "## Related" in updated_body:
            updated_body = updated_body.replace(
                "## Related\n",
                "## Related\n" + ''.join(f"- [[{r}]]\n" for r in additional_refs)
            )
        else:
            updated_body += "\n\n## Related\n\n"
            for ref in additional_refs[:10]:
                updated_body += f"- [[{ref}]]\n"
    
    new_frontmatter = '---\n'
    for k, v in metadata.items():
        if k == 'tags':
            new_frontmatter += f'{k}: {json.dumps(v)}\n'
        else:
            new_frontmatter += f'{k}: {v}\n'
    new_frontmatter += '---\n'
    
    with open(filepath, 'w') as f:
        f.write(new_frontmatter + "\n" + updated_body)
    
    return filepath

def update_index(wiki_path: str, new_pages: List[Tuple[str, str, str]]) -> None:
    index_path = os.path.join(wiki_path, "index.md")
    with open(index_path) as f:
        index = f.read()
    
    sections = {}
    current_section = None
    lines = index.split('\n')
    
    for line in lines:
        if line.startswith('## '):
            current_section = line[3:].strip()
            sections[current_section] = []
        elif line.startswith('- ') and current_section:
            m = re.match(r'- \[\[([^\]]+)\]\] — (.+)', line)
            if m:
                sections[current_section].append((m.group(1), m.group(2)))
    
    section_map = {
        'entity': 'Entities',
        'concept': 'Concepts',
        'comparison': 'Comparisons',
        'query': 'Queries',
    }
    
    for page_type, title, summary in new_pages:
        section_name = section_map.get(page_type, page_type.capitalize() + 's')
        if section_name not in sections:
            sections[section_name] = []
        
        exists = any(t.lower() == title.lower() for t, _ in sections[section_name])
        if not exists:
            sections[section_name].append((title, summary))
            sections[section_name].sort(key=lambda x: x[0])
    
    new_index = "# Wiki Index\n\n"
    new_index += "> Content catalog. Every wiki page listed under its type with a one-line summary.\n"
    new_index += "> Last updated: " + date.today().isoformat() + " | Total pages: " + str(sum(len(v) for v in sections.values())) + "\n\n"
    
    for section in ['Entities', 'Concepts', 'Comparisons', 'Queries']:
        if section in sections:
            new_index += f"## {section}\n\n"
            for title, summary in sections[section]:
                new_index += f"- [[{title}]] — {summary}\n"
            new_index += "\n"
    
    with open(index_path, 'w') as f:
        f.write(new_index)

def update_log(wiki_path: str, action: str, subject: str, details: List[str] = None) -> None:
    log_path = os.path.join(wiki_path, "log.md")
    today = date.today().isoformat()
    
    entry = f"## [{today}] {action} | {subject}\n"
    if details:
        for detail in details:
            entry += f"- {detail}\n"
    entry += "\n"
    
    append_file(log_path, entry)
    
    with open(log_path) as f:
        lines = f.readlines()
    
    entry_count = sum(1 for line in lines if line.startswith('## ['))
    if entry_count > 500:
        import shutil
        year = today[:4]
        archive_name = f"log-{year}.md"
        shutil.move(log_path, os.path.join(wiki_path, archive_name))
        with open(log_path, 'w') as f:
            f.write("# Wiki Log\n\n")
            f.write("> Chronological record. Rotated: " + today + "\n\n")

# ─────────────────────────────────────────────────────────────────
# Source-specific ingestion
# ─────────────────────────────────────────────────────────────────

def ingest_answer_engine_file(filepath: str, wiki_path: str) -> Dict:
    content = read_file(filepath)
    metadata, body = parse_frontmatter(content)
    
    title = extract_title(content)
    summary = extract_section(content, 'Executive Summary') or metadata.get('Query', title)
    
    entities, concepts = extract_entities_simple(body)
    
    print(f"  Ingesting: {title}")
    print(f"  Entities: {len(entities)}, Concepts: {len(concepts)}", file=sys.stderr)
    
    created_pages = []
    
    query_metadata = {
        'source_type': 'answer-engine',
        'reference': metadata.get('Query', title),
        'summary': summary,
        'tags': ['research', 'query']
    }
    
    cross_refs = entities[:5] + concepts[:3]
    
    query_path = create_wiki_page(
        wiki_path=wiki_path,
        page_type='query',
        title=title,
        content=body,
        metadata=query_metadata,
        cross_refs=cross_refs
    )
    created_pages.append(('query', title, summary[:100]))
    print(f"  ✓ Query page: query/{os.path.basename(query_path)}", file=sys.stderr)
    
    for entity in entities[:15]:
        existing = read_wiki_page(wiki_path, entity)
        if existing:
            update_wiki_page(
                wiki_path=wiki_path,
                page_type='entity',
                title=entity,
                new_content=f"\n> Referenced in: [[{title}]] ({date.today().isoformat()})",
                additional_refs=[title]
            )
        else:
            entity_content = f"**Mentioned in research:** [[{title}]]\n\n*No detailed information available yet.*"
            entity_metadata = {
                'source_type': 'auto-created',
                'reference': f'Mentioned in "{title}"',
                'tags': ['entity', 'auto-created']
            }
            create_wiki_page(
                wiki_path=wiki_path,
                page_type='entity',
                title=entity,
                content=entity_content,
                metadata=entity_metadata,
                cross_refs=[title]
            )
            created_pages.append(('entity', entity, f'Mentioned in {title}'))
    
    update_index(wiki_path, created_pages)
    update_log(
        wiki_path,
        action='ingest',
        subject=f'answer-engine | {title}',
        details=[
            f'Query page created',
            f'Entities processed: {len(entities[:15])}',
            f'Source: {os.path.basename(filepath)}'
        ]
    )
    
    return {
        'status': 'success',
        'query_page': query_path,
        'entities_processed': len(entities[:15]),
        'created_pages': created_pages
    }

def ingest_weekly_blog_research(topic: str, research_content: str, wiki_path: str) -> Dict:
    title = topic.title()
    summary = f"Weekly research deep dive on {topic}"
    
    entities, concepts = extract_entities_simple(research_content)
    
    created_pages = []
    
    concept_metadata = {
        'source_type': 'weekly-blog',
        'reference': f'Weekly research: {topic}',
        'summary': summary,
        'tags': ['weekly-blog', 'research', 'deep-dive']
    }
    
    cross_refs = entities[:5] + concepts[:3]
    
    concept_path = create_wiki_page(
        wiki_path=wiki_path,
        page_type='concept',
        title=title,
        content=research_content,
        metadata=concept_metadata,
        cross_refs=cross_refs
    )
    created_pages.append(('concept', title, summary[:100]))
    
    update_index(wiki_path, created_pages)
    update_log(
        wiki_path,
        action='ingest',
        subject=f'weekly-blog | {title}',
        details=[f'Concept page created', f'Entities: {len(entities)}']
    )
    
    return {
        'status': 'success',
        'concept_page': concept_path,
        'entities_processed': len(entities)
    }

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

def ingest_last30days_report(filepath: str, wiki_path: str) -> Dict:
    """Ingest a last30days research report into the wiki."""
    content = read_file(filepath)
    
    # Extract topic from the report
    topic_match = re.match(r'# (.+) - Last 30 Days Research Report', content)
    if not topic_match:
        topic_match = re.search(r'## Research Results: (.+)', content)
    title = topic_match.group(1).strip() if topic_match else "Last 30 Days Research"
    
    # Extract the "What I learned" synthesis section
    # last30days output has "What I learned:" followed by patterns
    learned_section = extract_section(content, 'What I learned') or extract_section(content, 'Research Results')
    
    # If not found, try to extract the summary from the beginning
    if not learned_section:
        # Get first substantial paragraph after headers
        lines = content.split('\n')
        summary_lines = []
        for line in lines:
            if line.startswith('#') or line.startswith('==') or line.startswith('**'):
                continue
            if len(line.strip()) > 50:
                summary_lines.append(line)
            if len(summary_lines) >= 3:
                break
        summary = ' '.join(summary_lines)[:300]
    else:
        summary = learned_section[:300]
    
    # Extract entities from the content (tools, people, companies)
    entities, concepts = extract_entities_simple(content)
    
    print(f"  Ingesting last30days: {title}")
    print(f"  Entities: {len(entities)}, Concepts: {len(concepts)}", file=sys.stderr)
    
    created_pages = []
    
    # Create query page with the full report
    query_metadata = {
        'source_type': 'last30days',
        'reference': f'Last 30 days research: {title}',
        'summary': summary,
        'tags': ['research', 'last30days', 'social-sentiment']
    }
    
    # Cross-refs: top entities + concepts
    cross_refs = entities[:5] + concepts[:3]
    
    query_path = create_wiki_page(
        wiki_path=wiki_path,
        page_type='query',
        title=title,
        content=content,
        metadata=query_metadata,
        cross_refs=cross_refs
    )
    created_pages.append(('query', title, summary[:100]))
    print(f"  ✓ Query page: query/{os.path.basename(query_path)}", file=sys.stderr)
    
    # Process entities (create/update)
    for entity in entities[:15]:
        existing = read_wiki_page(wiki_path, entity)
        if existing:
            update_wiki_page(
                wiki_path=wiki_path,
                page_type='entity',
                title=entity,
                new_content=f"\n> Mentioned in last30days research: [[{title}]] ({date.today().isoformat()})",
                additional_refs=[title]
            )
        else:
            entity_content = f"**Mentioned in last30days research:** [[{title}]]\n\n*No detailed information available yet.*"
            entity_metadata = {
                'source_type': 'auto-created',
                'reference': f'Mentioned in "{title}"',
                'tags': ['entity', 'auto-created']
            }
            create_wiki_page(
                wiki_path=wiki_path,
                page_type='entity',
                title=entity,
                content=entity_content,
                metadata=entity_metadata,
                cross_refs=[title]
            )
            created_pages.append(('entity', entity, f'Mentioned in {title}'))
    
    update_index(wiki_path, created_pages)
    update_log(
        wiki_path,
        action='ingest',
        subject=f'last30days | {title}',
        details=[
            f'Query page created',
            f'Entities processed: {len(entities[:15])}',
            f'Source: {os.path.basename(filepath)}'
        ]
    )
    
    return {
        'status': 'success',
        'query_page': query_path,
        'entities_processed': len(entities[:15]),
        'created_pages': created_pages
    }



def ingest_deep_research(topic: str, research_content: str, wiki_path: str, query_type: str = 'general') -> Dict:
    """Ingest deep-research output into the wiki."""
    title = topic.title()
    
    # Extract summary from executive summary or first section
    summary = extract_section(research_content, 'Executive Summary') or research_content[:300]
    
    entities, concepts = extract_entities_simple(research_content)
    
    print(f"  Ingesting deep-research: {title}")
    print(f"  Query type: {query_type}")
    print(f"  Entities: {len(entities)}, Concepts: {len(concepts)}", file=sys.stderr)
    
    created_pages = []
    
    # Determine page type based on query_type
    if query_type in ['comparison', 'vs', 'versus']:
        page_type = 'comparison'
        tags = ['research', 'deep-research', 'comparison']
    else:
        page_type = 'concept'
        tags = ['research', 'deep-research', 'concept']
    
    cross_refs = entities[:5] + concepts[:3]
    
    page_path = create_wiki_page(
        wiki_path=wiki_path,
        page_type=page_type,
        title=title,
        content=research_content,
        metadata={
            'source_type': 'deep-research',
            'reference': f'Deep research: {topic}',
            'summary': summary,
            'tags': tags
        },
        cross_refs=cross_refs
    )
    created_pages.append((page_type, title, summary[:100]))
    print(f"  ✓ {page_type.capitalize()} page: {page_type}/{os.path.basename(page_path)}")
    
    # Process entities
    for entity in entities[:15]:
        existing = read_wiki_page(wiki_path, entity)
        if existing:
            update_wiki_page(
                wiki_path=wiki_path,
                page_type='entity',
                title=entity,
                new_content=f"\n> Referenced in deep research: [[{title}]] ({date.today().isoformat()})",
                additional_refs=[title]
            )
        else:
            entity_content = f"**Mentioned in deep research:** [[{title}]]\n\n*No detailed information available yet.*"
            entity_metadata = {
                'source_type': 'auto-created',
                'reference': f'Mentioned in "{title}"',
                'tags': ['entity', 'auto-created']
            }
            create_wiki_page(
                wiki_path=wiki_path,
                page_type='entity',
                title=entity,
                content=entity_content,
                metadata=entity_metadata,
                cross_refs=[title]
            )
            created_pages.append(('entity', entity, f'Mentioned in {title}'))
    
    update_index(wiki_path, created_pages)
    update_log(
        wiki_path,
        action='ingest',
        subject=f'deep-research | {title}',
        details=[
            f'{page_type.capitalize()} page created',
            f'Entities processed: {len(entities[:15])}',
            f'Query type: {query_type}'
        ]
    )
    
    return {
        'status': 'success',
        'page_path': page_path,
        'page_type': page_type,
        'entities_processed': len(entities[:15]),
        'created_pages': created_pages
    }


def main():
    parser = argparse.ArgumentParser(description='Ingest research into wiki')
    parser.add_argument('--source', required=True,
                        choices=['answer-engine', 'weekly-blog', 'last30days', 'deep-research'],
                        help='Source skill')
    parser.add_argument('--wiki-path', default=DEFAULT_WIKI_PATH,
                        help='Path to wiki (default: ~/wiki)')
    parser.add_argument('--file', help='Source file to ingest')
    parser.add_argument('--date', help='Process all files from date (today, yesterday, YYYY-MM-DD)')
    parser.add_argument('--topic', help='Topic name (for weekly-blog)')
    parser.add_argument('--content', help='Content file (for weekly-blog)')
    
    args = parser.parse_args()
    
    wiki_path = os.path.expanduser(args.wiki_path)
    
    if not os.path.exists(wiki_path):
        print(f"Error: Wiki not found at {wiki_path}")
        sys.exit(1)
    
    print(f"Ingesting to wiki: {wiki_path}")
    
    if args.source == 'answer-engine':
        if args.file:
            result = ingest_answer_engine_file(args.file, wiki_path)
            print(json.dumps(result, indent=2))
        elif args.date:
            target_date = None
            if args.date == 'today':
                target_date = date.today()
            elif args.date == 'yesterday':
                target_date = date.today() - timedelta(days=1)
            else:
                target_date = date.fromisoformat(args.date)
            
            processed = []
            for fname in sorted(os.listdir(RESEARCH_DIR)):
                if fname.startswith(target_date.isoformat()):
                    fpath = os.path.join(RESEARCH_DIR, fname)
                    print(f"\nProcessing {fname}...")
                    result = ingest_answer_engine_file(fpath, wiki_path)
                    processed.append(result)
            
            print(f"\nProcessed {len(processed)} files")
        else:
            print("Error: Must specify --file or --date for answer-engine source")
            sys.exit(1)
    
    elif args.source == 'weekly-blog':
        if args.topic and args.content:
            content = read_file(args.content)
            result = ingest_weekly_blog_research(args.topic, content, wiki_path)
            print(json.dumps(result, indent=2))
        else:
            print("Error: weekly-blog requires --topic and --content")
            sys.exit(1)
    
    elif args.source == 'last30days':
        if args.file:
            result = ingest_last30days_report(args.file, wiki_path)
            print(json.dumps(result, indent=2))
        else:
            print("Error: last30days requires --file")
            sys.exit(1)
    
    elif args.source == 'deep-research':
        if args.file:
            content = read_file(args.file)
            topic = extract_title(content) or args.file.split('/')[-1].replace('.md', '').replace('-', ' ').title()
            query_type = 'comparison' if ' vs ' in content.lower() or ' versus ' in content.lower() else 'general'
            result = ingest_deep_research(topic, content, wiki_path, query_type)
            print(json.dumps(result, indent=2))
        elif args.topic and args.content:
            content = read_file(args.content)
            query_type = 'comparison' if ' vs ' in args.topic or ' versus ' in args.topic else 'general'
            result = ingest_deep_research(args.topic, content, wiki_path, query_type)
            print(json.dumps(result, indent=2))
        else:
            print("Error: deep-research requires --file OR --topic and --content")
            sys.exit(1)
    
    else:
        print(f"Source '{args.source}' not yet implemented")
        sys.exit(1)

if __name__ == '__main__':
    main()
