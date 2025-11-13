#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Calculate the next version based on the latest git tag and output GitHub Actions variables
# Usage: get-next-version.sh

# Get the latest tag, or use v0.0.0 if no tags exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "latest_tag=$LATEST_TAG" >> $GITHUB_OUTPUT

if [ "$LATEST_TAG" = "v0.0.0" ] && [ -f "pyproject.toml" ]; then
	# Seed initial release version from pyproject.toml when no tags exist
	PY_VER=$(grep -E '^version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"' pyproject.toml | sed -E 's/.*"([0-9]+\.[0-9]+\.[0-9]+)".*/\1/' || true)
	if [ -n "$PY_VER" ]; then
		NEW_VERSION="v$PY_VER"
		echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
		echo "No tags found. Using pyproject.toml version: $NEW_VERSION"
		exit 0
	fi
fi

# Extract version number and increment from latest tag
VERSION=$(echo $LATEST_TAG | sed 's/v//')
IFS='.' read -ra VERSION_PARTS <<< "$VERSION"
MAJOR=${VERSION_PARTS[0]:-0}
MINOR=${VERSION_PARTS[1]:-0}
PATCH=${VERSION_PARTS[2]:-0}

# Increment patch version from latest tag
PATCH=$((PATCH + 1))
NEW_VERSION="v$MAJOR.$MINOR.$PATCH"

echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
echo "New version will be: $NEW_VERSION"
