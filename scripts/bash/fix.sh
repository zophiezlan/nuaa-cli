#!/usr/bin/env bash
# Quick fix script - Auto-formats code and fixes common issues
# Usage: ./scripts/bash/fix.sh

set -e

echo "🔧 NUAA CLI Auto-Fix Script"
echo "============================"
echo ""

# Change to repo root
cd "$(dirname "$0")/../.."

echo "🎨 Step 1/3: Auto-formatting with black..."
black src/nuaa_cli tests scripts/python
echo "✅ Black formatting complete!"
echo ""

echo "🔍 Step 2/3: Auto-fixing with ruff..."
ruff check --fix src/nuaa_cli tests scripts/python || true
echo "✅ Ruff fixes complete!"
echo ""

echo "🔒 Step 3/3: Security scan..."
bandit -r src/nuaa_cli -f screen || true
echo "✅ Security scan complete!"
echo ""

echo "✨ All fixes applied!"
echo ""
echo "Next steps:"
echo "  • Review changes: git diff"
echo "  • Run tests: pytest"
echo "  • Commit changes: git add . && git commit -m 'fix: Apply auto-formatting and fixes'"
