#!/usr/bin/env python3.14
"""
Create a Deezer playlist from a list of tracks.

Uses deezer-python-gql (ARL cookie auth) for playlist creation + search.

Input: JSON with {"title": "...", "description": "...", "tracks": [{"title": "...", "artist": "..."}, ...]}
Output: Playlist URL and match summary.

Usage:
  echo '{"title":"My Mix","description":"","tracks":[{"title":"Get Lucky","artist":"Daft Punk"}]}' | python3.14 ~/.hermes/scripts/deezer_create_playlist.py

Or with Infisical:
  infisical run --projectId <YOUR_PROJECT_ID> --env dev -- python3.14 scripts/deezer_create_playlist.py
"""

import asyncio
import json
import os
import sys
from difflib import SequenceMatcher


def get_arl():
    """Get Deezer ARL from env (Infisical injection) or secrets file."""
    arl = os.environ.get("DEEZER_ARL")
    if arl:
        return arl
    # Fallback: read from Infisical secret file
    secret_path = os.path.expanduser("~/.hermes/secrets/deezer_arl")
    if os.path.exists(secret_path):
        with open(secret_path) as f:
            return f.read().strip()
    raise RuntimeError(
        "DEEZER_ARL not found. Set via env (Infisical) or ~/.hermes/secrets/deezer_arl"
    )


def parse_input() -> dict:
    """Read playlist spec from stdin or --input file."""
    if len(sys.argv) > 1 and sys.argv[1] == "--input":
        with open(sys.argv[2]) as f:
            return json.load(f)
    return json.load(sys.stdin)


def score_match(query_title, query_artist, result_title, result_artist):
    """Score a search result against the query. Returns 0-1."""
    # Normalize
    def norm(s):
        return s.lower().strip()

    qt = norm(query_title)
    qa = norm(query_artist)
    rt = norm(result_title)
    ra = norm(result_artist)

    title_score = SequenceMatcher(None, qt, rt).ratio()
    artist_score = SequenceMatcher(None, qa, ra).ratio()

    # Heavy weight on title match, artist is secondary
    return 0.7 * title_score + 0.3 * artist_score


def get_artist_name(node) -> str:
    """Extract primary artist name from a track node's contributors."""
    if hasattr(node, "contributors") and node.contributors:
        for edge in node.contributors.edges:
            if hasattr(edge.node, "name"):
                return edge.node.name
    return ""


async def find_best_match(client, title, artist) -> dict | None:
    """Search Deezer for the best matching track. Returns {id, title, artist, link} or None."""
    query = f"{title} {artist}"
    try:
        results = await client.search(query=query)
    except Exception as e:
        print(f"  ⚠️  Search error for '{title} - {artist}': {e}", file=sys.stderr)
        return None

    # Search returns results.results.tracks.edges (GraphQL connection pattern)
    if not hasattr(results, "results"):
        return None
    sr = results.results
    if not hasattr(sr, "tracks") or not hasattr(sr.tracks, "edges"):
        return None

    edges = sr.tracks.edges
    if not edges:
        return None

    # Score all candidates
    scored = []
    for edge in edges:
        node = edge.node
        if node is None:
            continue
        r_title = node.title
        r_artist = get_artist_name(node)
        r_id = node.id
        s = score_match(title, artist, r_title, r_artist)
        scored.append(
            {
                "id": r_id,
                "title": r_title,
                "artist": r_artist,
                "score": s,
                "link": f"https://www.deezer.com/track/{r_id}",
            }
        )

    if not scored:
        return None

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]

    if best["score"] < 0.5:
        return None  # Too low confidence

    return best


async def create_playlist(arl: str, spec: dict):
    """Main flow: search tracks, create playlist, add matches."""
    from deezer_python_gql import DeezerGQLClient

    client = DeezerGQLClient(arl=arl)
    try:
        title = spec["title"]
        description = spec.get("description", "")
        tracks = spec["tracks"]

        print(f"🎵 Creating playlist: **{title}**")
        print(f"   {len(tracks)} tracks to find...")
        print()

        # Step 1: Search for all tracks
        matches = []
        misses = []
        for i, track in enumerate(tracks):
            t_title = track["title"]
            t_artist = track["artist"]
            print(f"   [{i+1}/{len(tracks)}] Searching: {t_title} — {t_artist}...", end=" ")

            match = await find_best_match(client, t_title, t_artist)
            if match:
                print(f"✅ {match['title']} — {match['artist']} (score: {match['score']:.2f})")
                matches.append(match)
            else:
                print("❌ No match found")
                misses.append(track)

            # Rate limiting: small delay between searches
            await asyncio.sleep(0.2)

        if not matches:
            print("\n❌ No tracks could be matched. Aborting.")
            return None

        # Step 2: Create the playlist
        print(f"\n📝 Creating playlist '{title}'...")
        playlist_result = await client.create_playlist(
            title=title,
            description=description or f"Created by Hermes Agent — {len(matches)} tracks",
            is_private=False,
            is_collaborative=False,
        )
        playlist_id = playlist_result.playlist.id
        print(f"   Playlist ID: {playlist_id}")

        # Step 3: Add tracks in batches
        track_ids = [m["id"] for m in matches]
        batch_size = 50
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i : i + batch_size]
            print(f"   Adding tracks {i+1}-{min(i+batch_size, len(track_ids))}...")
            await client.add_tracks_to_playlist(playlist_id, batch)

        playlist_url = f"https://www.deezer.com/playlist/{playlist_id}"

        # Summary
        print(f"\n{'='*50}")
        print(f"✅ Playlist created: {playlist_url}")
        print(f"   Matched: {len(matches)} tracks")
        if misses:
            print(f"   Missed:  {len(misses)} tracks")
            for m in misses:
                print(f"     • {m['title']} — {m['artist']}")

        return {
            "playlist_url": playlist_url,
            "playlist_id": playlist_id,
            "matched": len(matches),
            "missed": len(misses),
            "missed_tracks": misses,
            "tracks": [
                {"title": m["title"], "artist": m["artist"], "link": m["link"]}
                for m in matches
            ],
        }

    finally:
        await client.close()


def main():
    spec = parse_input()

    if not spec.get("title"):
        print("❌ Missing 'title' in input", file=sys.stderr)
        sys.exit(1)
    if not spec.get("tracks"):
        print("❌ Missing 'tracks' in input", file=sys.stderr)
        sys.exit(1)

    arl = get_arl()
    result = asyncio.run(create_playlist(arl, spec))

    if result:
        # Output JSON result for programmatic use
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
