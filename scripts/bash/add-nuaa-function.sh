#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-v0.2.0}"
REF="$VERSION"
if [[ "$VERSION" == "latest" ]]; then
  REF="main"
fi

BASH_RC="$HOME/.bashrc"
ZSH_RC="$HOME/.zshrc"

add_fn() {
  local rc="$1"
  [[ -f "$rc" ]] || return 0
  if ! grep -q "function nuaa" "$rc" 2>/dev/null; then
    cat >> "$rc" <<EOF

# NUAA CLI (added by add-nuaa-function.sh on $(date -Is))
function nuaa() {
  uvx --from "git+https://github.com/zophiezlan/nuaa-cli@${REF}" nuaa "$@"
}
EOF
    echo "Added 'nuaa' function to $rc"
  else
    # Update existing definition (simple append a fresh one)
    cat >> "$rc" <<EOF

# NUAA CLI (refreshed by add-nuaa-function.sh on $(date -Is))
function nuaa() {
  uvx --from "git+https://github.com/zophiezlan/nuaa-cli@${REF}" nuaa "$@"
}
EOF
    echo "Updated 'nuaa' function in $rc"
  fi
}

add_fn "$BASH_RC"
add_fn "$ZSH_RC"

echo "Open a new shell (or 'source ~/.bashrc' / 'source ~/.zshrc') then run: nuaa version"
