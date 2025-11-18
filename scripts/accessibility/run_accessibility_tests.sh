#!/usr/bin/env bash
#
# Comprehensive accessibility testing suite for NUAA CLI
# Run this before commits to ensure accessibility standards are met
#

set -e

echo "🌍 NUAA CLI Accessibility Test Suite"
echo "======================================"
echo ""

# Colors for output (with fallback for NO_COLOR)
if [ -z "$NO_COLOR" ]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    GREEN=''
    RED=''
    YELLOW=''
    BLUE=''
    NC=''
fi

ERRORS=0
WARNINGS=0

# Function to print test results
print_result() {
    local status=$1
    local message=$2

    if [ "$status" == "PASS" ]; then
        echo -e "${GREEN}✓${NC} $message"
    elif [ "$status" == "FAIL" ]; then
        echo -e "${RED}✗${NC} $message"
        ((ERRORS++))
    elif [ "$status" == "WARN" ]; then
        echo -e "${YELLOW}⚠${NC} $message"
        ((WARNINGS++))
    else
        echo -e "${BLUE}ℹ${NC} $message"
    fi
}

# Test 1: Readability Check
echo ""
echo "Test 1: Readability Check"
echo "-------------------------"

if [ -f "scripts/accessibility/check_readability.py" ]; then
    if python3 scripts/accessibility/check_readability.py README.md nuaa-kit/QUICKSTART.md docs/*.md 2>&1 | grep -q "All readability checks passed"; then
        print_result "PASS" "Documentation meets readability standards"
    else
        print_result "WARN" "Some readability issues found (see details above)"
    fi
else
    print_result "WARN" "Readability checker not found"
fi

# Test 2: Stigmatizing Language Check
echo ""
echo "Test 2: Stigmatizing Language Check"
echo "-----------------------------------"

if [ -f "scripts/accessibility/lint_stigma.py" ]; then
    if python3 scripts/accessibility/lint_stigma.py README.md nuaa-kit/**/*.md docs/**/*.md 2>&1 | grep -q "No stigmatizing language detected"; then
        print_result "PASS" "No stigmatizing language detected"
    else
        print_result "FAIL" "Stigmatizing language found - must be fixed"
    fi
else
    print_result "WARN" "Stigma linter not found"
fi

# Test 3: Check for Alt Text in Images
echo ""
echo "Test 3: Image Alt Text Check"
echo "----------------------------"

# Find markdown images without alt text
MISSING_ALT=$(find . -name "*.md" -type f -exec grep -Hn '!\[\](' {} \; | wc -l)

if [ "$MISSING_ALT" -eq 0 ]; then
    print_result "PASS" "All images have alt text"
else
    print_result "FAIL" "Found $MISSING_ALT images without alt text"
fi

# Test 4: Heading Hierarchy Check
echo ""
echo "Test 4: Heading Hierarchy Check"
echo "-------------------------------"

# Check for heading skips (simplified check)
HEADING_ISSUES=0

for file in README.md nuaa-kit/README.md docs/*.md; do
    if [ -f "$file" ]; then
        # Check if file has ## before any #
        if grep -q "^##" "$file" && ! grep -q "^#[^#]" "$file" 2>/dev/null; then
            ((HEADING_ISSUES++))
        fi
    fi
done

if [ "$HEADING_ISSUES" -eq 0 ]; then
    print_result "PASS" "Heading hierarchy is correct"
else
    print_result "WARN" "Possible heading hierarchy issues in $HEADING_ISSUES files"
fi

# Test 5: Acronym Expansion Check
echo ""
echo "Test 5: Acronym Expansion Check"
echo "-------------------------------"

# List of acronyms that should be explained (simplified check)
ACRONYMS=("NUAA" "NSP" "BBV" "HCV" "OST" "PWUD")
UNEXPLAINED=0

for acronym in "${ACRONYMS[@]}"; do
    if grep -q "$acronym" README.md && ! grep -q "$acronym (.*)" README.md; then
        # This is a simplified check, might have false positives
        : # Skip for now
    fi
done

print_result "INFO" "Acronym check completed (manual review recommended)"

# Test 6: Color-Only Meaning Check
echo ""
echo "Test 6: Color-Only Meaning Check"
echo "--------------------------------"

# Check for references to color without additional context
COLOR_REFS=$(grep -ri "see.*red\|see.*green\|see.*blue" docs/ nuaa-kit/ | wc -l)

if [ "$COLOR_REFS" -eq 0 ]; then
    print_result "PASS" "No color-only instructions found"
else
    print_result "WARN" "Found $COLOR_REFS potential color-only references"
fi

# Test 7: Translation Completeness
echo ""
echo "Test 7: Translation Completeness"
echo "--------------------------------"

if [ -d "locales" ]; then
    # Count number of msgid in template
    if [ -f "locales/nuaa_cli.pot" ]; then
        TOTAL_STRINGS=$(grep -c "^msgid" locales/nuaa_cli.pot || echo "0")
        print_result "INFO" "Found $TOTAL_STRINGS translatable strings"

        # Check each language
        for lang_dir in locales/*/; do
            if [ -d "$lang_dir" ]; then
                lang=$(basename "$lang_dir")
                po_file="$lang_dir/LC_MESSAGES/nuaa_cli.po"

                if [ -f "$po_file" ]; then
                    TRANSLATED=$(grep -c "^msgstr \"[^\"]\+\"" "$po_file" || echo "0")
                    PERCENT=$((TRANSLATED * 100 / TOTAL_STRINGS))

                    if [ "$PERCENT" -ge 80 ]; then
                        print_result "PASS" "$lang: $PERCENT% translated ($TRANSLATED/$TOTAL_STRINGS)"
                    elif [ "$PERCENT" -ge 50 ]; then
                        print_result "WARN" "$lang: $PERCENT% translated ($TRANSLATED/$TOTAL_STRINGS)"
                    else
                        print_result "INFO" "$lang: $PERCENT% translated ($TRANSLATED/$TOTAL_STRINGS)"
                    fi
                fi
            fi
        done
    else
        print_result "INFO" "Translation template not yet generated"
    fi
else
    print_result "INFO" "Translations not yet initialized"
fi

# Test 8: Accessibility Documentation Exists
echo ""
echo "Test 8: Accessibility Documentation"
echo "-----------------------------------"

REQUIRED_DOCS=(
    "ACCESSIBILITY_ENHANCEMENT_PLAN.md"
    "CULTURAL_SAFETY_FRAMEWORK.md"
    "TRANSLATION_GUIDE.md"
    "docs/accessibility/KEYBOARD_SHORTCUTS.md"
    "nuaa-kit/accessibility-guidelines.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        print_result "PASS" "Found: $doc"
    else
        print_result "FAIL" "Missing: $doc"
    fi
done

# Test 9: Code Accessibility Features
echo ""
echo "Test 9: Code Accessibility Features"
echo "-----------------------------------"

if [ -f "src/nuaa_cli/accessibility/__init__.py" ]; then
    print_result "PASS" "Accessibility module exists"
else
    print_result "FAIL" "Accessibility module missing"
fi

if [ -f "src/nuaa_cli/i18n/__init__.py" ]; then
    print_result "PASS" "Internationalization module exists"
else
    print_result "FAIL" "Internationalization module missing"
fi

if [ -f "src/nuaa_cli/commands/onboard.py" ]; then
    print_result "PASS" "Onboarding wizard exists"
else
    print_result "FAIL" "Onboarding wizard missing"
fi

# Test 10: Keyboard Accessibility
echo ""
echo "Test 10: Keyboard Navigation Documentation"
echo "------------------------------------------"

if grep -q "Ctrl+C\|Escape\|Arrow keys" docs/accessibility/KEYBOARD_SHORTCUTS.md 2>/dev/null; then
    print_result "PASS" "Keyboard shortcuts documented"
else
    print_result "WARN" "Keyboard shortcuts documentation incomplete"
fi

# Summary
echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo ""

if [ "$ERRORS" -eq 0 ]; then
    print_result "PASS" "All critical tests passed!"
else
    print_result "FAIL" "$ERRORS critical issues found"
fi

if [ "$WARNINGS" -gt 0 ]; then
    print_result "WARN" "$WARNINGS warnings (should be addressed)"
fi

echo ""
echo "Accessibility compliance: $((100 - (ERRORS + WARNINGS) * 5))%"
echo ""

# Exit with error if critical issues found
if [ "$ERRORS" -gt 0 ]; then
    echo "❌ Accessibility tests failed. Please fix critical issues before committing."
    exit 1
else
    echo "✅ Accessibility tests passed!"
    exit 0
fi
