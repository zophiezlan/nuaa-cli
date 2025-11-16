#!/bin/bash

# Exit immediately on error, treat unset variables as an error, and fail if any command in a pipeline fails.
set -euo pipefail

# Ensure jq is available early (used for manifest-driven installs)
if ! command -v jq >/dev/null 2>&1; then
    echo -e "\n📦 Installing jq..."
    sudo apt-get update -y >/dev/null 2>&1 || true
    sudo apt-get install -y jq >/dev/null 2>&1 || true
fi

# Load agent manifest (if available) to determine which CLIs to install
AGENTS_JSON_PATH="src/nuaa_cli/agents.json"
if command -v jq >/dev/null 2>&1 && [ -f "$AGENTS_JSON_PATH" ]; then
    JQ_PRESENT=1
else
    JQ_PRESENT=0
fi

requires_cli() {
    # Usage: requires_cli <agent_key>
    local key="$1"
    if [ "$JQ_PRESENT" -eq 1 ]; then
        jq -e -r --arg k "$key" '.[$k].requires_cli // false' "$AGENTS_JSON_PATH" >/dev/null 2>&1
        return $?
    fi
    # If jq/manifest not present, default to installing (return true) to preserve previous behavior
    return 0
}

# Function to run a command and show logs only on error
run_command() {
    local command_to_run="$*"
    local output
    local exit_code

    # Capture all output (stdout and stderr)
    output=$(eval "$command_to_run" 2>&1) || exit_code=$?
    exit_code=${exit_code:-0}

    if [ $exit_code -ne 0 ]; then
        echo -e "\033[0;31m[ERROR] Command failed (Exit Code $exit_code): $command_to_run\033[0m" >&2
        echo -e "\033[0;31m$output\033[0m" >&2

        exit $exit_code
    fi
}

# Installing CLI-based AI Agents

if requires_cli copilot; then
echo -e "\n🤖 Installing Copilot CLI..."
run_command "npm install -g @github/copilot@latest"
echo "✅ Done"
fi

if requires_cli claude; then
echo -e "\n🤖 Installing Claude CLI..."
run_command "npm install -g @anthropic-ai/claude-code@latest"
echo "✅ Done"
fi

if requires_cli codex; then
echo -e "\n🤖 Installing Codex CLI..."
run_command "npm install -g @openai/codex@latest"
echo "✅ Done"
fi

if requires_cli gemini; then
echo -e "\n🤖 Installing Gemini CLI..."
run_command "npm install -g @google/gemini-cli@latest"
echo "✅ Done"
fi

if requires_cli auggie; then
echo -e "\n🤖 Installing Augie CLI..."
run_command "npm install -g @augmentcode/auggie@latest"
echo "✅ Done"
fi

if requires_cli qwen; then
echo -e "\n🤖 Installing Qwen Code CLI..."
run_command "npm install -g @qwen-code/qwen-code@latest"
echo "✅ Done"
fi

if requires_cli opencode; then
echo -e "\n🤖 Installing OpenCode CLI..."
run_command "npm install -g opencode-ai@latest"
echo "✅ Done"
fi

if requires_cli q; then
echo -e "\n🤖 Installing Amazon Q CLI..."
# 👉🏾 https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-verify-download.html

run_command "curl --proto '=https' --tlsv1.2 -sSf 'https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip' -o 'q.zip'"
run_command "curl --proto '=https' --tlsv1.2 -sSf 'https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip.sig' -o 'q.zip.sig'"
cat > amazonq-public-key.asc << 'EOF'
-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEZig60RYJKwYBBAHaRw8BAQdAy/+G05U5/EOA72WlcD4WkYn5SInri8pc4Z6D
BKNNGOm0JEFtYXpvbiBRIENMSSBUZWFtIDxxLWNsaUBhbWF6b24uY29tPoiZBBMW
CgBBFiEEmvYEF+gnQskUPgPsUNx6jcJMVmcFAmYoOtECGwMFCQPCZwAFCwkIBwIC
IgIGFQoJCAsCBBYCAwECHgcCF4AACgkQUNx6jcJMVmef5QD/QWWEGG/cOnbDnp68
SJXuFkwiNwlH2rPw9ZRIQMnfAS0A/0V6ZsGB4kOylBfc7CNfzRFGtovdBBgHqA6P
zQ/PNscGuDgEZig60RIKKwYBBAGXVQEFAQEHQC4qleONMBCq3+wJwbZSr0vbuRba
D1xr4wUPn4Avn4AnAwEIB4h+BBgWCgAmFiEEmvYEF+gnQskUPgPsUNx6jcJMVmcF
AmYoOtECGwwFCQPCZwAACgkQUNx6jcJMVmchMgEA6l3RveCM0YHAGQaSFMkguoAo
vK6FgOkDawgP0NPIP2oA/jIAO4gsAntuQgMOsPunEdDeji2t+AhV02+DQIsXZpoB
 =f8yY
-----END PGP PUBLIC KEY BLOCK-----
EOF
run_command "gpg --batch --import amazonq-public-key.asc"
run_command "gpg --verify q.zip.sig q.zip"
run_command "unzip -q q.zip"
run_command "chmod +x ./q/install.sh"
run_command "./q/install.sh --no-confirm"
run_command "rm -rf ./q q.zip q.zip.sig amazonq-public-key.asc"
echo "✅ Done"
fi

if requires_cli codebuddy; then
echo -e "\n🤖 Installing CodeBuddy CLI..."
run_command "npm install -g @tencent-ai/codebuddy-code@latest"
echo "✅ Done"
fi

# Installing UV (Python package manager)
echo -e "\n🐍 Installing UV - Python Package Manager..."
run_command "pipx install uv"
echo "✅ Done"

# Install pre-commit and set up hooks for this repo
echo -e "\n🧰 Installing pre-commit and enabling hooks..."
run_command "pipx install pre-commit"
if [ -d ".git" ]; then
    run_command "pre-commit install"
fi
echo "✅ Done"

# Installing DocFx (for documentation site)
echo -e "\n📚 Installing DocFx..."
run_command "dotnet tool update -g docfx"
echo "✅ Done"

echo -e "\n🧹 Cleaning cache..."
run_command "sudo apt-get autoclean"
run_command "sudo apt-get clean"

echo "✅ Setup completed. Happy coding! 🚀"
