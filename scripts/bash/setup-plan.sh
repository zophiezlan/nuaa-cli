#!/usr/bin/env bash

set -e

# Parse command line arguments
JSON_MODE=false
ARGS=()

for arg in "$@"; do
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --help|-h) 
            echo "Usage: $0 [--json]"
            echo "  --json    Output results in JSON format"
            echo "  --help    Show this help message"
            exit 0 
            ;;
        *) 
            ARGS+=("$arg") 
            ;;
    esac
done

# Get script directory and load common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get all paths and variables from common functions
eval $(get_feature_paths)

# Check if we're on a proper feature branch (only for git repos)
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# Ensure the feature directory exists
mkdir -p "$FEATURE_DIR"

# Copy program design template if it exists
TEMPLATE="$(resolve_template_path 'program-design.md' "$REPO_ROOT")"
if [[ -f "$TEMPLATE" ]]; then
    cp "$TEMPLATE" "$DESIGN"
    echo "Copied program design template to $DESIGN"
else
    echo "Warning: Program design template not found at $TEMPLATE"
    # Create a basic design file if template doesn't exist
    touch "$DESIGN"
fi

# Output results
if $JSON_MODE; then
    printf '{"PROPOSAL":"%s","DESIGN":"%s","FEATURE_DIR":"%s","BRANCH":"%s","HAS_GIT":"%s"}\n' \
        "$PROPOSAL" "$DESIGN" "$FEATURE_DIR" "$CURRENT_BRANCH" "$HAS_GIT"
else
    echo "PROPOSAL: $PROPOSAL"
    echo "DESIGN: $DESIGN" 
    echo "FEATURE_DIR: $FEATURE_DIR"
    echo "BRANCH: $CURRENT_BRANCH"
    echo "HAS_GIT: $HAS_GIT"
fi

