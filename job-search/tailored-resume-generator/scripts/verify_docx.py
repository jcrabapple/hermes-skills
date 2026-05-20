#!/usr/bin/env python3
"""Verify a DOCX file has no markdown syntax artifacts.

Scans all paragraphs for `**text**`, `*text*`, `[text](url)`, and other
markdown syntax that may have leaked through DOCX conversion.

Usage:
    source /tmp/.venv/bin/activate
    python3 scripts/verify_docx.py <path/to/resume.docx>

Exit codes:
    0 — clean (no artifacts found)
    1 — artifacts found
    2 — file not found or unreadable
"""

import re
import sys

try:
    from docx import Document
except ImportError:
    print("❌ python-docx not installed. Run: uv pip install python-docx")
    sys.exit(2)

# Patterns that should never appear in clean DOCX output
MARKDOWN_PATTERNS = {
    "bold markers": r'\*\*[^*]+\*\*',           # **text**
    "single star markers": r'(?<!\*)\*[^*\s]+\*',  # *text* (not **)
    "markdown links": r'\[([^\]]+)\]\(([^)]+)\)',  # [text](url)
    "code backticks": r'`[^`]+`',                 # `code`
    "markdown headers": r'^#{1,6}\s',            # # Header
    "markdown HR": r'^---+$',                    # ---
}

# But some patterns have exceptions — allow these
ALLOWED_SINGLE_STARS = [
    'Best in class',  # brand name
]


def is_allowed_star(text: str, match) -> bool:
    """Return True if a single-star match is actually legitimate content."""
    word = text[match.start():match.end()].strip('*')
    return word.lower() in [a.lower() for a in ALLOWED_SINGLE_STARS]


def verify(path: str) -> int:
    try:
        doc = Document(path)
    except Exception as e:
        print(f"❌ Cannot open file: {e}")
        return 2

    issues = []

    for i, para in enumerate(doc.paragraphs):
        text = para.text
        if not text:
            continue

        for label, pattern in MARKDOWN_PATTERNS.items():
            for match in re.finditer(pattern, text, re.MULTILINE):
                # Skip allowed exceptions for single-star patterns
                if label == "single star markers" and is_allowed_star(text, match):
                    continue
                snippet = text[max(0, match.start()-10):match.end()+10]
                issues.append(f"  Para {i:3d} | {label:20s} | ...{snippet.strip()}...")

    if issues:
        print(f"⚠️  Found {len(issues)} markdown artifact(s) in {path}:")
        for issue in issues:
            print(issue)
        print("\nFix: Check the build script uses _add_rich() for bold markers,")
        print("      and that skill lines are handled before generic bullets.")
        return 1
    else:
        print(f"✓  Clean — no markdown artifacts in {path}")
        return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/resume.docx>")
        sys.exit(2)
    sys.exit(verify(sys.argv[1]))
