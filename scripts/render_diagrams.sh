#!/usr/bin/env bash
# Render Mermaid diagrams (*.mmd) to SVG using mermaid-cli (mmdc).
# Requires: npm install -g @mermaid-js/mermaid-cli

set -euo pipefail

if ! command -v mmdc >/dev/null 2>&1; then
  echo "mmdc (mermaid-cli) not found. Install with: npm install -g @mermaid-js/mermaid-cli" >&2
  exit 1
fi

for src in $(find . -name "*.mmd"); do
  out="${src%.mmd}.svg"
  echo "Rendering $src -> $out"
  mmdc -i "$src" -o "$out"
done
