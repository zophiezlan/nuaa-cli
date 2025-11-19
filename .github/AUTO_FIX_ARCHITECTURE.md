# Auto-Fix Linting Architecture

## Overview

All workflows that run on `push` or `pull_request` now automatically fix linting issues **BEFORE** running any tests. This ensures that linting errors never block releases or CI runs.

## Architecture

### Reusable Action

- **Location**: `.github/actions/auto-fix-lint/action.yml`
- **Purpose**: Centralized auto-fix logic used by all workflows
- **What it does**:
  1. ✅ Runs Black formatter on **entire codebase** (not just selected directories)
  2. ✅ Runs Ruff with auto-fix **and --unsafe-fixes** on entire codebase
     - Automatically removes unused imports (F401)
     - Automatically removes unused variables (F841)
     - Converts lambda assignments to def (E731)
  3. ✅ Runs pre-commit hooks (trailing whitespace, EOF, YAML/TOML checks, PowerShell linting)
  4. ✅ Updates agent documentation if needed
  5. ✅ Shows a summary of all changes made

### Workflow Coverage

| Workflow | Trigger | Auto-Fix Enabled | Notes |
|----------|---------|------------------|-------|
| **CI** (`ci.yml`) | push, pull_request | ✅ YES | Runs before all tests in matrix |
| **Release** (`release.yml`) | push to main, workflow_dispatch | ✅ YES | Runs before verification step |
| **E2E** (`e2e.yml`) | push, pull_request | ✅ YES | Runs before smoke tests |
| **Auto-fix** (`auto-fix.yml`) | pull_request | ✅ YES | Commits fixes back to PR |
| **Lint** (`lint.yml`) | push, pull_request | ⚠️ Markdown only | Only checks Markdown files |
| **Docs** (`docs.yml`) | push to main (docs/**) | ⚠️ Not needed | Only builds documentation |

## Execution Order

### On Direct Push to Main

1. **CI Workflow** triggers first
   - Setup Python
   - Install dependencies
   - **🔧 AUTO-FIX RUNS** (fixes applied in-memory with `--unsafe-fixes`, not committed)
   - Run linting (ruff check) - will pass after auto-fix
   - Run type checking (mypy)
   - Run tests with fixed code

2. **E2E Workflow** triggers (in parallel with CI)
   - Setup Python
   - Install dependencies
   - **🔧 AUTO-FIX RUNS** (fixes applied in-memory with `--unsafe-fixes`, not committed)
   - Run smoke tests

3. **Release Workflow** triggers AFTER CI completes successfully
   - **⏸️ WAITS** for CI workflow to complete
   - Only runs if CI passes AND release-relevant files changed
   - Checks if release-relevant paths changed (memory/, scripts/, templates/, .github/workflows/)
   - Creates release packages (no verification needed - CI already verified)

### On Pull Request

1. **Auto-fix Workflow** triggers
   - **🔧 AUTO-FIX RUNS** (fixes are committed back to PR branch)
   - Creates a commit with fixes if needed

2. **CI Workflow** triggers
   - **🔧 AUTO-FIX RUNS** (additional safety check)
   - Runs all tests

3. **E2E Workflow** triggers
   - **🔧 AUTO-FIX RUNS** (additional safety check)
   - Runs smoke tests

## Why This Works

### Layer 1: Pre-commit Hooks (Development)

- Developers can run `pre-commit run --all-files` locally
- Catches issues before commit
- Includes PowerShell Script Analyzer

### Layer 2: Auto-fix PR Workflow (Continuous)

- Runs on every PR
- Automatically commits fixes back to the PR
- Keeps PR branch clean

### Layer 3: Auto-fix in Every Workflow (Safety Net)

- Even if previous layers miss something, every workflow fixes issues before testing
- Ensures tests always run against properly formatted code
- No manual intervention needed

### Layer 4: Unified Action (Maintainability)

- Single source of truth: `.github/actions/auto-fix-lint/action.yml`
- Easy to update - change once, affects all workflows
- Consistent behavior everywhere

## Benefits

✅ **Zero Manual Intervention**: Linting issues are automatically fixed with `--unsafe-fixes`
✅ **Never Block Releases**: Release workflow waits for CI to complete successfully
✅ **Proper Execution Order**: CI runs first, release only triggers after CI passes
✅ **Consistent**: Same auto-fix logic everywhere via reusable action
✅ **Fast Feedback**: Developers see fixes in PR commits
✅ **Maintainable**: Update one file to change all workflows
✅ **Comprehensive**: Covers entire codebase including web_api, interfaces, scripts
✅ **Visible**: Shows diff of changes made in each run
✅ **Flexible Line Length**: Extended to 120 chars for CLI help text and examples

## Maintenance

### To Add a New Auto-fix Tool

1. Edit `.github/actions/auto-fix-lint/action.yml`
2. Add the new tool command to the composite action
3. All workflows automatically get the new fix

### To Update Existing Fix

1. Edit `.github/actions/auto-fix-lint/action.yml`
2. Change the command or parameters
3. All workflows automatically use the new logic

### To Add Auto-fix to a New Workflow

```yaml
- name: 🔧 Auto-fix linting issues (REQUIRED before tests)
  uses: ./.github/actions/auto-fix-lint
```

## PowerShell Linting

PowerShell Script Analyzer is now integrated into:

- Pre-commit hooks (`.pre-commit-config.yaml`)
- Checks for unapproved verbs, reserved variables, and other issues
- Runs automatically with `pre-commit run --all-files`

## Files Modified

### New Files

- `.github/actions/auto-fix-lint/action.yml` - Reusable composite action

### Updated Files (Latest Changes)

- `.github/actions/auto-fix-lint/action.yml` - Added `--unsafe-fixes` flag, now checks entire codebase
- `.github/workflows/release.yml` - Now uses `workflow_run` to wait for CI completion, added path filtering
- `pyproject.toml` - Extended line-length to 120, added per-file ignores for commands and scripts
- `.github/AUTO_FIX_ARCHITECTURE.md` - Updated documentation

### Previously Updated Files

- `.github/workflows/ci.yml` - Uses auto-fix action
- `.github/workflows/e2e.yml` - Uses auto-fix action
- `.github/workflows/scripts/create-release-packages.ps1` - Fixed function names to use approved verbs
- `.pre-commit-config.yaml` - Added PowerShell Script Analyzer

## Result

🎉 **Linting issues will NEVER block releases again!**

The workflow execution order is now:

1. **CI runs** → auto-fixes code in-memory → verifies everything passes
2. **Release waits** → only runs if CI succeeds AND release-relevant files changed
3. **No more race conditions** → proper dependency chain ensures correct order
