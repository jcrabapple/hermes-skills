#!/bin/bash
# Setup script for answer-engine skill

set -e

echo "=== Answer Engine Setup ==="
echo

# Check SearXNG
echo "Testing SearXNG connection..."
if curl -s "https://searxng.snakepit.us/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if len(d.get('results', [])) > 0 else 1)" 2>/dev/null; then
    echo "✓ SearXNG is accessible"
else
    echo "✗ SearXNG connection failed"
    exit 1
fi
echo

# Check NanoGPT
echo "Checking NanoGPT API key..."
if [ -f ~/.config/nanogpt/.env ]; then
    if grep -q "NANOGPT_API_KEY" ~/.config/nanogpt/.env; then
        echo "✓ NanoGPT API key found"
        # Verify key actually works with a test embedding call
        API_KEY=$(grep NANOGPT_API_KEY ~/.config/nanogpt/.env | cut -d= -f2)
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "https://nano-gpt.com/api/v1/embeddings" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d '{"model":"text-embedding-3-small","input":"test"}' 2>/dev/null || echo "000")
        if [ "$HTTP_CODE" = "200" ]; then
            echo "✓ NanoGPT API key verified (embedding call successful)"
        elif [ "$HTTP_CODE" = "000" ]; then
            echo "⚠ NanoGPT API key found but could not reach API (network/DNS error)"
            echo "  Embeddings will fall back to keyword search"
        else
            echo "⚠ NanoGPT API key found but call returned HTTP $HTTP_CODE"
            echo "  Key may be invalid or expired — embeddings will fall back to keyword search"
        fi
    else
        echo "⚠ NanoGPT config exists but no API key found"
        echo "  Add to ~/.config/nanogpt/.env:"
        echo "  NANOGPT_API_KEY=your_key_here"
    fi
else
    echo "⚠ NanoGPT config not found"
    echo "  Create ~/.config/nanogpt/.env with:"
    echo "  NANOGPT_API_KEY=your_key_here"
    echo "  Semantic search will fall back to keyword-based search"
fi
echo

# Check Obsidian Research folder
echo "Checking Obsidian Research folder..."
if [ -d "$HOME/Documents/Obsidian Vault/Research" ]; then
    echo "✓ Research folder exists"
else
    echo "Creating Research folder..."
    mkdir -p "$HOME/Documents/Obsidian Vault/Research"
    echo "✓ Research folder created"
fi
echo

# Make scripts executable
echo "Setting script permissions..."
chmod +x ~/.hermes/skills/research/answer-engine/scripts/*.py
echo "✓ Scripts are executable"
echo

echo "=== Setup Complete ==="
echo
echo "To use answer-engine:"
echo "  1. Add NanoGPT API key if you want semantic file search"
echo "  2. Load skill: skill_view('answer-engine')"
echo "  3. Ask research questions!"
