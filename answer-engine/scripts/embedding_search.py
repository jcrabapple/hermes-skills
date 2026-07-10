#!/usr/bin/env python3
"""
Semantic search over Obsidian Research folder using NanoGPT API.
Usage: 
  - Embed file: embedding_search.py embed "filepath"
  - Search: embedding_search.py search "query"
  - Rebuild index: embedding_search.py rebuild
"""

import sys
import os
import json
import hashlib
from datetime import datetime

# NanoGPT API config
NANOGPT_API_KEY = os.environ.get('NANOGPT_API_KEY', '')
if not NANOGPT_API_KEY:
    # Load from .env file if not in environment
    try:
        with open(os.path.expanduser('~/.config/nanogpt/.env'), 'r') as f:
            for line in f:
                if line.startswith('NANOGPT_API_KEY='):
                    NANOGPT_API_KEY = line.strip().split('=', 1)[1]
                    break
    except FileNotFoundError:
        pass

NANOGPT_BASE_URL = 'https://nano-gpt.com/api/v1'
EMBEDDING_MODEL = 'text-embedding-3-small'  # Best price/performance, 1536 dims

OBSIDIAN_RESEARCH_DIR = os.path.expanduser("~/Documents/Obsidian Vault/Research")
INDEX_FILE = "/tmp/ae_embedding_index.json"

def get_embedding(text):
    """Get embedding vector from NanoGPT API."""
    import urllib.request
    import socket
    
    if not NANOGPT_API_KEY:
        print("NanoGPT API key not configured", file=sys.stderr)
        return None
    
    payload = json.dumps({
        'model': EMBEDDING_MODEL,
        'input': text[:8191]  # Truncate to model limit (text-embedding-3-small max)
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{NANOGPT_BASE_URL}/embeddings",
        data=payload,
        headers={
            'Authorization': f'Bearer {NANOGPT_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data['data'][0]['embedding']
    except urllib.error.HTTPError as e:
        print(f"Embedding API HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Embedding API connection error: {e}", file=sys.stderr)
        return None
    except socket.gaierror as e:
        print(f"Embedding API DNS resolution failed: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Embedding API error: {e}", file=sys.stderr)
        return None

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    import math
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

def load_index():
    """Load embedding index from disk."""
    try:
        with open(INDEX_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'files': [], 'embeddings': {}}

def save_index(index):
    """Save embedding index to disk."""
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)

def file_hash(filepath):
    """Calculate file hash for change detection."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def embed_file(filepath):
    """Embed a single file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    embedding = get_embedding(content)
    if embedding is None:
        return None
    
    return {
        'path': filepath,
        'hash': file_hash(filepath),
        'embedding': embedding,
        'embedded_at': datetime.now().isoformat()
    }

def rebuild_index():
    """Rebuild embedding index for all files in Research folder."""
    if not os.path.exists(OBSIDIAN_RESEARCH_DIR):
        print(f"Research directory not found: {OBSIDIAN_RESEARCH_DIR}")
        return
    
    index = {'files': [], 'embeddings': {}}
    
    for filename in os.listdir(OBSIDIAN_RESEARCH_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(OBSIDIAN_RESEARCH_DIR, filename)
            print(f"Embedding: {filename}")
            
            file_data = embed_file(filepath)
            if file_data:
                index['files'].append(filepath)
                index['embeddings'][filepath] = file_data['embedding']
    
    save_index(index)
    print(f"Indexed {len(index['files'])} files")

def search(query, top_k=5):
    """Search for similar documents."""
    query_embedding = get_embedding(query)
    if query_embedding is None:
        print("Semantic search unavailable. Use keyword search instead.", file=sys.stderr)
        return []
    
    index = load_index()
    if not index['embeddings']:
        print("Index is empty. Run 'rebuild' first.")
        return []
    
    # Calculate similarities
    similarities = []
    for filepath, embedding in index['embeddings'].items():
        sim = cosine_similarity(query_embedding, embedding)
        similarities.append((filepath, sim))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top results
    results = []
    for filepath, score in similarities[:top_k]:
        if score > 0.5:  # Threshold for relevance
            results.append({'path': filepath, 'score': score})
    
    return results

def embed_new_file(filepath):
    """Embed a new file and add to index."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    index = load_index()
    
    # Check if already indexed
    if filepath in index['embeddings']:
        # Check if file changed
        if file_hash(filepath) == index['files'].get(filepath, {}).get('hash'):
            print("File unchanged, skipping")
            return
    
    file_data = embed_file(filepath)
    if file_data:
        index['files'].append(filepath)
        index['embeddings'][filepath] = file_data['embedding']
        save_index(index)
        print(f"Embedded: {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: embedding_search.py [embed|search|rebuild] ...", file=sys.stderr)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'embed':
        if len(sys.argv) < 3:
            print("Usage: embedding_search.py embed 'filepath'", file=sys.stderr)
            sys.exit(1)
        embed_new_file(sys.argv[2])
    
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("Usage: embedding_search.py search 'query'", file=sys.stderr)
            sys.exit(1)
        results = search(sys.argv[2])
        print(json.dumps(results, indent=2))
    
    elif cmd == 'rebuild':
        rebuild_index()
    
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
