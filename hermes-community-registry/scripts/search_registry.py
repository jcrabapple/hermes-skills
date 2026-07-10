#!/usr/bin/env python3
"""Search the babylondreams.de Hermes Community Registry.

Fetches data.json once, then filters by keyword (substring match across
name + description + author), type, category, or author. Prints a
human-readable table by default; JSON with full records when --json.

Exit codes:
  0 — search completed (including zero-result searches, which are valid)
  1 — network/parsing failure
  2 — usage error
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from typing import Any

DATA_URL = "https://babylondreams.de/hermes-registry/data.json"


def fetch_data(url: str = DATA_URL) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch {url}: {exc}") from exc


def filter_entries(
    entries: list[dict[str, Any]],
    *,
    keyword: str | None = None,
    entry_type: str | None = None,
    category: str | None = None,
    author: str | None = None,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    kw = (keyword or "").lower().strip()

    for entry in entries:
        if entry_type and entry.get("type", "").lower() != entry_type.lower():
            continue
        if category and entry.get("category", "").lower() != category.lower():
            continue
        if author:
            a = entry.get("author", "") or ""
            if author.lower() not in a.lower():
                continue
        if kw:
            blob = " ".join(
                str(entry.get(field, "") or "")
                for field in ("name", "description", "author", "category", "slug")
            )
            if kw not in blob.lower():
                continue
        out.append(entry)

    out.sort(key=lambda e: (e.get("author", "") or "", e.get("name", "") or ""))
    return out


def print_table(entries: list[dict[str, Any]]) -> None:
    if not entries:
        print("No results.", file=sys.stderr)
        return

    print(f"Found {len(entries)} entr{'y' if len(entries)==1 else 'ies'}:\n")
    for e in entries:
        name = e.get("name", "")
        etype = e.get("type", "")
        category = e.get("category", "")
        author = e.get("author", "")
        description = e.get("description", "") or ""
        url = e.get("repo_url") or e.get("url") or ""
        if len(description) > 180:
            description = description[:177] + "..."
        print(f"  {name}")
        print(f"    type={etype}  category={category}  author={author}")
        print(f"    desc: {description}")
        print(f"    url : {url}")
        print()


def print_json(entries: list[dict[str, Any]]) -> None:
    json.dump(entries, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def list_values(entries: list[dict[str, Any]], *, type_order: list[str] | None = None) -> None:
    from collections import Counter

    print("=== TYPES ===")
    type_counts = Counter(e.get("type", "") for e in entries)
    seen: set[str] = set()
    if type_order:
        for t in type_order:
            if t in type_counts:
                print(f"  {t:14} {type_counts[t]}")
                seen.add(t)
    for t, c in type_counts.most_common():
        if t not in seen:
            print(f"  {t:14} {c}")

    print("\n=== CATEGORIES ===")
    cat_counts = Counter(e.get("category", "") for e in entries)
    for c, n in cat_counts.most_common():
        print(f"  {c:14} {n}")

    print(f"\nTotal entries: {len(entries)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search the babylondreams.de Hermes Community Registry.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --keyword sqlite
  %(prog)s --type skill --category memory
  %(prog)s --author Hypercubed
  %(prog)s --keyword "code review" --json
  %(prog)s --list-values
""",
    )
    parser.add_argument(
        "--keyword", "-k", default=None,
        help="Substring to match in name / description / author / category / slug (case-insensitive)",
    )
    parser.add_argument("--type", dest="entry_type", default=None, help="Filter by type (e.g. skill, plugin, tool)")
    parser.add_argument("--category", default=None, help="Filter by category (e.g. memory, devops)")
    parser.add_argument("--author", default=None, help="Substring match against author field")
    parser.add_argument("--json", action="store_true", help="Output full JSON records instead of human-readable table")
    parser.add_argument(
        "--list-values", action="store_true",
        help="Print the full list of types and categories present in current data, then exit",
    )
    parser.add_argument(
        "--url", default=DATA_URL,
        help=f"data.json URL (default: {DATA_URL})",
    )
    args = parser.parse_args(argv)

    try:
        data = fetch_data(args.url)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    entries = data.get("entries", []) if isinstance(data, dict) else data

    if args.list_values:
        type_order = data.get("type_order") if isinstance(data, dict) else None
        list_values(entries, type_order=type_order)
        return 0

    if not any([args.keyword, args.entry_type, args.category, args.author]):
        # No filters → list everything (but warn)
        print(f"Notice: no filters provided. Listing all {len(entries)} entries.", file=sys.stderr)

    results = filter_entries(
        entries,
        keyword=args.keyword,
        entry_type=args.entry_type,
        category=args.category,
        author=args.author,
    )

    if args.json:
        print_json(results)
    else:
        print_table(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
