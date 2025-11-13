#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

if [[ $# -gt 0 ]]; then
  PATH_ROOT="$1"
else
  if root=$(get_templates_root 2>/dev/null); then
    PATH_ROOT="$root"
  else
    echo "Could not locate NUAA templates under .nuaa/templates or nuaa-kit/templates." >&2
    exit 1
  fi
fi

if [[ ! -d "$PATH_ROOT" ]]; then
  echo "Template path not found: $PATH_ROOT" >&2
  exit 1
fi

error_found=0

while IFS= read -r -d '' file; do
  content="$(cat "$file")"
  # front matter detection
  if [[ $content =~ ^---[[:space:]]*.*status:[[:space:]]*final ]]; then
    # remove fenced code blocks (split by ```)
    awk 'BEGIN{FS="```"}{for(i=1;i<=NF;i+=2)printf "%s", $i}' "$file" > /tmp/_scan.md
    scan_text="$(cat /tmp/_scan.md)"
    # regex: brackets not followed by (
    if grep -P '\[[^\]]+\](?!\()' -q /tmp/_scan.md; then
      echo "Placeholder tokens found in FINAL document: $file" >&2
      error_found=1
    fi
    rm -f /tmp/_scan.md
  fi

done < <(find "$PATH_ROOT" -type f -name '*.md' -print0)

if [[ $error_found -eq 1 ]]; then
  exit 1
else
  echo "No placeholder tokens found in final documents."
fi
