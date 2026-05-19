#!/usr/bin/env python3
"""
Valyu API CLI — search, extract, answer, research.

Usage:
  valyu.py search "query" [--type web|proprietary|news|all] [--sources preset|domain|dataset_id] [--max-results 5] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
  valyu.py extract URL [URL ...] [--effort auto|normal|high] [--summary]
  valyu.py answer "question" [--sources ...]
  valyu.py research "topic" [--sources ...]

Environment:
  VALYU_API_KEY — required, read from ~/.hermes/.env if not already set.

Exit codes:
  0 = success (JSON on stdout)
  1 = error (error message on stderr)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API_BASE = "https://api.valyu.ai/v1"


def load_api_key() -> str:
    key = os.environ.get("VALYU_API_KEY")
    if key:
        return key
    env_file = Path.home() / ".hermes" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("VALYU_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: VALYU_API_KEY not found in env or ~/.hermes/.env", file=sys.stderr)
    sys.exit(1)


def api_post(endpoint: str, payload: dict) -> dict:
    url = f"{API_BASE}/{endpoint}"
    data = json.dumps(payload).encode()
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", load_api_key())
    try:
        with urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def cmd_search(args):
    payload = {
        "query": args.query,
        "max_num_results": args.max_results,
        "search_type": args.type,
        "relevance_threshold": args.relevance_threshold,
    }
    if args.sources:
        payload["included_sources"] = [s.strip() for s in args.sources.split(",")]
    if args.start_date:
        payload["start_date"] = args.start_date
    if args.end_date:
        payload["end_date"] = args.end_date
    if args.instructions:
        payload["instructions"] = args.instructions
    if args.response_length:
        payload["response_length"] = args.response_length
    if args.fast:
        payload["fast_mode"] = True

    result = api_post("search", payload)
    print(json.dumps(result, indent=2))


def cmd_extract(args):
    payload = {
        "urls": args.urls,
        "response_length": args.response_length,
    }
    if args.effort:
        payload["extract_effort"] = args.effort
    if args.summary:
        if isinstance(args.summary, str):
            payload["summary"] = args.summary
        else:
            payload["summary"] = True

    result = api_post("contents", payload)
    print(json.dumps(result, indent=2))


def cmd_answer(args):
    payload = {"query": args.query}
    if args.sources:
        payload["included_sources"] = [s.strip() for s in args.sources.split(",")]

    result = api_post("answer", payload)
    print(json.dumps(result, indent=2))


def cmd_research(args):
    payload = {"query": args.query}
    if args.sources:
        payload["included_sources"] = [s.strip() for s in args.sources.split(",")]

    result = api_post("deepresearch", payload)
    task_id = result.get("task_id") or result.get("id")
    if not task_id:
        print(json.dumps(result, indent=2))
        return

    print(f"Research task started: {task_id}", file=sys.stderr)
    print("Polling for results...", file=sys.stderr)

    # Poll until complete
    api_key = load_api_key()
    for attempt in range(60):  # max 5 minutes
        time.sleep(5)
        poll_req = Request(f"{API_BASE}/deepresearch/{task_id}", method="GET")
        poll_req.add_header("X-API-Key", api_key)
        try:
            with urlopen(poll_req, timeout=30) as resp:
                status_result = json.loads(resp.read())
                state = status_result.get("status", "").lower()
                if state in ("completed", "done", "finished"):
                    print(json.dumps(status_result, indent=2))
                    return
                elif state in ("failed", "error", "cancelled"):
                    print(json.dumps(status_result, indent=2))
                    sys.exit(1)
                else:
                    print(f"  status: {state} (attempt {attempt + 1}/60)", file=sys.stderr)
        except HTTPError as e:
            print(f"  poll error: HTTP {e.code}", file=sys.stderr)

    print("ERROR: Research timed out after 5 minutes", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Valyu API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search web + proprietary sources")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--type", dest="type", default="all",
                          choices=["all", "web", "proprietary", "news"],
                          help="Search type (default: all)")
    p_search.add_argument("--sources", default=None,
                          help="Comma-separated source presets/domains/dataset IDs")
    p_search.add_argument("--max-results", type=int, default=5,
                          help="Max results (1-20, default: 5)")
    p_search.add_argument("--relevance-threshold", type=float, default=0.5,
                          help="Min relevance score 0-1 (default: 0.5)")
    p_search.add_argument("--start-date", default=None,
                          help="Filter results published on or after (YYYY-MM-DD)")
    p_search.add_argument("--end-date", default=None,
                          help="Filter results published on or before (YYYY-MM-DD)")
    p_search.add_argument("--instructions", default=None,
                          help="Natural language ranking instructions (max 500 chars)")
    p_search.add_argument("--response-length", default=None,
                          choices=["short", "medium", "large", "max"],
                          help="Content length per result")
    p_search.add_argument("--fast", action="store_true",
                          help="Fast mode: skip LLM reranking, web-only")

    # extract
    p_extract = sub.add_parser("extract", help="Extract content from URLs")
    p_extract.add_argument("urls", nargs="+", help="URLs to extract (up to 50)")
    p_extract.add_argument("--effort", default="auto",
                           choices=["auto", "normal", "high"],
                           help="Extraction effort (auto/normal/high)")
    p_extract.add_argument("--summary", nargs="?", const=True, default=False,
                           help="AI summary (optionally pass instructions)")
    p_extract.add_argument("--response-length", default="short",
                           choices=["short", "medium", "large", "max"],
                           help="Content length per URL")

    # answer
    p_answer = sub.add_parser("answer", help="AI-synthesized answer with citations")
    p_answer.add_argument("query", help="Question to answer")
    p_answer.add_argument("--sources", default=None,
                          help="Comma-separated source presets/domains/dataset IDs")

    # research
    p_research = sub.add_parser("research", help="Deep research report (async)")
    p_research.add_argument("query", help="Research topic")
    p_research.add_argument("--sources", default=None,
                            help="Comma-separated source presets/domains/dataset IDs")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "answer":
        cmd_answer(args)
    elif args.command == "research":
        cmd_research(args)


if __name__ == "__main__":
    main()
