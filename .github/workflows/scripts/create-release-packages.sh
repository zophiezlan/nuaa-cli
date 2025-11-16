#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build NUAA Project template release archives for each supported AI assistant and script type.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS and/or SCRIPTS env vars to limit what gets built.
#     AGENTS  : space or comma separated subset of: claude gemini copilot cursor-agent qwen opencode windsurf codex amp (default: all)
#     SCRIPTS : space or comma separated subset of: sh ps (default: both)
#   Examples:
#     AGENTS=claude SCRIPTS=sh $0 v0.2.0
#     AGENTS="copilot,gemini" $0 v0.2.0
#     SCRIPTS=ps $0 v0.2.0

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  sed -E \
    -e 's@(/?)memory/@.nuaa/memory/@g' \
    -e 's@(/?)scripts/@.nuaa/scripts/@g' \
    -e 's@(/?)templates/@.nuaa/templates/@g'
}

generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  mkdir -p "$output_dir"
  for template in nuaa-kit/commands/*.md; do
    [[ -f "$template" ]] || continue
    local name description script_command agent_script_command body
    name=$(basename "$template" .md)

    # Normalize line endings
    file_content=$(tr -d '\r' < "$template")

    # Extract description and script command from YAML frontmatter
    description=$(printf '%s\n' "$file_content" | awk '/^description:/ {sub(/^description:[[:space:]]*/, ""); print; exit}')
    script_command=$(printf '%s\n' "$file_content" | awk -v sv="$script_variant" '/^[[:space:]]*'"$script_variant"':[[:space:]]*/ {sub(/^[[:space:]]*'"$script_variant"':[[:space:]]*/, ""); print; exit}')

    if [[ -z $script_command ]]; then
      echo "Warning: no script command found for $script_variant in $template" >&2
      script_command="(Missing script command for $script_variant)"
    fi

    # Extract agent_script command from YAML frontmatter if present
    agent_script_command=$(printf '%s\n' "$file_content" | awk '
      /^agent_scripts:$/ { in_agent_scripts=1; next }
      in_agent_scripts && /^[[:space:]]*'"$script_variant"':[[:space:]]*/ {
        sub(/^[[:space:]]*'"$script_variant"':[[:space:]]*/, "")
        print
        exit
      }
      in_agent_scripts && /^[a-zA-Z]/ { in_agent_scripts=0 }
    ')

    # Replace {SCRIPT} placeholder with the script command
    body=$(printf '%s\n' "$file_content" | sed "s|{SCRIPT}|${script_command}|g")

    # Replace {AGENT_SCRIPT} placeholder with the agent script command if found
    if [[ -n $agent_script_command ]]; then
      body=$(printf '%s\n' "$body" | sed "s|{AGENT_SCRIPT}|${agent_script_command}|g")
    fi

    # Remove the scripts: and agent_scripts: sections from frontmatter while preserving YAML structure
    body=$(printf '%s\n' "$body" | awk '
      /^---$/ { print; if (++dash_count == 1) in_frontmatter=1; else in_frontmatter=0; next }
      in_frontmatter && /^scripts:$/ { skip_scripts=1; next }
      in_frontmatter && /^agent_scripts:$/ { skip_scripts=1; next }
      in_frontmatter && /^[a-zA-Z].*:/ && skip_scripts { skip_scripts=0 }
      in_frontmatter && skip_scripts && /^[[:space:]]/ { next }
      { print }
    ')

    # Apply other substitutions
    body=$(printf '%s\n' "$body" | sed "s/{ARGS}/$arg_format/g" | sed "s/__AGENT__/$agent/g" | rewrite_paths)

    case $ext in
      toml)
        body=$(printf '%s\n' "$body" | sed 's/\\/\\\\/g')
        { echo "description = \"$description\""; echo; echo "prompt = \"\"\""; echo "$body"; echo "\"\"\""; } > "$output_dir/nuaa.$name.$ext" ;;
      md)
        echo "$body" > "$output_dir/nuaa.$name.$ext" ;;
      agent.md)
        echo "$body" > "$output_dir/nuaa.$name.$ext" ;;
    esac
  done
}

generate_copilot_prompts() {
  local agents_dir=$1 prompts_dir=$2
  mkdir -p "$prompts_dir"

  # Generate a .prompt.md file for each .agent.md file
  for agent_file in "$agents_dir"/nuaa.*.agent.md; do
    [[ -f "$agent_file" ]] || continue

    local basename=$(basename "$agent_file" .agent.md)
    local prompt_file="$prompts_dir/${basename}.prompt.md"

    {
      printf '%s\n' '---'
      printf 'agent: %s\n' "$basename"
      printf 'version: %s\n' "$NEW_VERSION"
      printf 'generated_from: .github/agents/%s.agent.md\n' "$basename"
      printf '%s\n\n' '---'
      cat "$agent_file"
    } > "$prompt_file"
  done
}

build_variant() {
  local agent=$1 script=$2
  local base_dir="$GENRELEASES_DIR/sdd-${agent}-package-${script}"
  echo "Building $agent ($script) package..."
  mkdir -p "$base_dir"

  # Copy base structure but filter scripts by variant
  NUAA_DIR="$base_dir/.nuaa"
  mkdir -p "$NUAA_DIR"

  [[ -d memory ]] && { cp -r memory "$NUAA_DIR/"; echo "Copied memory -> .nuaa"; }

  # Only copy the relevant script variant directory
  if [[ -d scripts ]]; then
    mkdir -p "$NUAA_DIR/scripts"
    case $script in
      sh)
        [[ -d scripts/bash ]] && { cp -r scripts/bash "$NUAA_DIR/scripts/"; echo "Copied scripts/bash -> .nuaa/scripts"; }
        # Copy any script files that aren't in variant-specific directories
        find scripts -maxdepth 1 -type f -exec cp {} "$NUAA_DIR/scripts/" \; 2>/dev/null || true
        ;;
      ps)
        [[ -d scripts/powershell ]] && { cp -r scripts/powershell "$NUAA_DIR/scripts/"; echo "Copied scripts/powershell -> .nuaa/scripts"; }
        # Copy any script files that aren't in variant-specific directories
        find scripts -maxdepth 1 -type f -exec cp {} "$NUAA_DIR/scripts/" \; 2>/dev/null || true
        ;;
    esac
  fi

  [[ -d nuaa-kit/templates ]] && { mkdir -p "$NUAA_DIR/templates"; find nuaa-kit/templates -type f -not -name "vscode-settings.json" -exec cp {} "$NUAA_DIR/templates/" \; ; echo "Copied nuaa-kit/templates -> .nuaa/templates"; }

  # NOTE: We substitute {ARGS} internally. Outward tokens differ intentionally:
  #   * Markdown/prompt (claude, copilot, cursor-agent, opencode): $ARGUMENTS
  #   * TOML (gemini, qwen): {{args}}
  # This keeps formats readable without extra abstraction.

      generate_commands q md "$ARGUMENTS" "$base_dir/.amazonq/prompts" "$script" ;;
  esac

  # Dynamically handle agent properties from JSON
  local agent_format
  agent_format=$(jq -r --arg agent "$agent" '.[$agent].format' "$AGENTS_JSON_PATH")

  local arg_placeholder
  if [[ "$agent_format" == "TOML" ]]; then
    arg_placeholder="{{args}}"
  else
    arg_placeholder="\$ARGUMENTS"
  fi

  local output_dir
  output_dir="$base_dir/$(jq -r --arg agent "$agent" '.[$agent].folder' "$AGENTS_JSON_PATH")"
  mkdir -p "$output_dir"

  generate_commands "$agent" "${agent_format,,}" "$arg_placeholder" "$output_dir" "$script"

  # Special handling for certain agents
  if [[ "$agent" == "copilot" ]]; then
    generate_copilot_prompts "$output_dir" "$base_dir/.github/prompts"
    mkdir -p "$base_dir/.vscode"
    [[ -f templates/vscode-settings.json ]] && cp templates/vscode-settings.json "$base_dir/.vscode/settings.json"
  elif [[ "$agent" == "gemini" ]]; then
    [[ -f agent_templates/gemini/GEMINI.md ]] && cp agent_templates/gemini/GEMINI.md "$base_dir/GEMINI.md"
  elif [[ "$agent" == "qwen" ]]; then
    [[ -f agent_templates/qwen/QWEN.md ]] && cp agent_templates/qwen/QWEN.md "$base_dir/QWEN.md"
  fi

  # Create zip archive (prefer zip, fallback to 7z if available)
  (
    cd "$base_dir"
    if command -v zip >/dev/null 2>&1; then
      zip -r "../nuaa-template-${agent}-${script}-${NEW_VERSION}.zip" .
    elif command -v 7z >/dev/null 2>&1; then
      7z a -tzip "../nuaa-template-${agent}-${script}-${NEW_VERSION}.zip" . >/dev/null
    else
      echo "Error: neither 'zip' nor '7z' is available. Install one of them and retry." >&2
      exit 1
    fi
  )
  echo "Created $GENRELEASES_DIR/nuaa-template-${agent}-${script}-${NEW_VERSION}.zip"
}

# --- Agent and script variant selection ---
AGENTS_JSON_PATH="src/nuaa_cli/agents.json"
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. It is required to read agent configuration." >&2
    exit 1
fi
if [[ ! -f "$AGENTS_JSON_PATH" ]]; then
  echo "Error: Agent configuration file not found at $AGENTS_JSON_PATH" >&2
  exit 1
fi

# Use jq to get all agent keys from the JSON file
ALL_AGENTS=($(jq -r 'keys | .[]' "$AGENTS_JSON_PATH"))
ALL_SCRIPTS=(sh ps)

norm_list() {
  # convert comma+space separated -> space separated unique while preserving order of first occurrence
  tr ',\n' '  ' | awk '{for(i=1;i<=NF;i++){if(!seen[$i]++){printf((out?" ":"") $i)}}}END{printf("\n")}'
}

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=("$@")
  local ok=1
  for it in "${items[@]}"; do
    local found=0
    for a in "${allowed[@]}"; do [[ $it == "$a" ]] && { found=1; break; }; done
    if [[ $found -eq 0 ]]; then
      echo "Error: unknown $type '$it' (allowed: ${allowed[*]})" >&2
      ok=0
    fi
  done
  return $ok
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' "$AGENTS" | norm_list)
  validate_subset agent ALL_AGENTS "${AGENT_LIST[@]}" || exit 1
else
  AGENT_LIST=("${ALL_AGENTS[@]}")
fi

if [[ -n ${SCRIPTS:-} ]]; then
  mapfile -t SCRIPT_LIST < <(printf '%s' "$SCRIPTS" | norm_list)
  validate_subset script ALL_SCRIPTS "${SCRIPT_LIST[@]}" || exit 1
else
  SCRIPT_LIST=("${ALL_SCRIPTS[@]}")
fi

echo "Agents: ${AGENT_LIST[*]}"
echo "Scripts: ${SCRIPT_LIST[*]}"

for agent in "${AGENT_LIST[@]}"; do
  for script in "${SCRIPT_LIST[@]}"; do
    build_variant "$agent" "$script"
  done
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/nuaa-template-*-"${NEW_VERSION}".zip
