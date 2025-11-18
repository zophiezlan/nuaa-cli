#!/usr/bin/env python3
"""
Stigmatizing language detector for NUAA CLI.

Detects and flags stigmatizing, ableist, and non-inclusive language
in documentation and templates.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class StigmaLinter:
    """Detect stigmatizing and non-inclusive language."""

    def __init__(self):
        self.issues: List[Tuple[str, str, int, str]] = []

        # Stigmatizing terms with suggestions
        self.stigma_patterns: Dict[str, str] = {
            # Drug-related stigma
            r"\baddicts?\b": "people who use drugs / people with substance use disorder",
            r"\bjunkies?\b": "people who use drugs",
            r"\bcrackheads?\b": "people who use drugs",
            r"\bclean\b.*\b(sobriety|sober)": "not currently using / specify context",
            r"\bdirty\b.*\b(urine|test)": "positive test result",
            r"\babuse\b.*\b(drugs|substances)": "drug use / substance use",
            r"\bsubstance abusers?\b": "people who use drugs",
            # Disease/condition stigma
            r"\bsuffering from\b": "living with / experiencing",
            r"\bvictims? of\b.*\b(overdose|HIV|HCV)": "person who experienced / person living with",
            r"\binfected with\b": "living with / diagnosed with",
            r"\bHIV/AIDS\b": "HIV (AIDS is a late-stage condition)",
            # Gender/sexuality stigma
            r"\btransgenders?\b": "trans and gender diverse people",
            r"\bhomosexuals?\b": "LGBTIQ+ people / gay and lesbian people",
            r"\bhe or she\b": "they / people",
            # Ableist language
            r"\bcrazy\b": "unusual / unexpected / distressing",
            r"\binsane\b": "extreme / intense",
            r"\blame\b": "ineffective / poor / substandard",
            r"\bdumb\b": "unclear / confusing",
            r"\bstupid\b": "confusing / poorly designed",
            r"\bblind to\b": "unaware of / not seeing",
            r"\bdeaf to\b": "ignoring / not hearing",
            # Criminalization language
            r"\billegal drug users?\b": "people who use drugs (avoid criminalization)",
            r"\bcriminals?\b.*\b(drugs|users)": "people who use drugs",
        }

        # Binary gender assumptions
        self.binary_gender_patterns = [
            r"\bhe/she\b",
            r"\bhis/her\b",
            r"\bhim/her\b",
            r"\bmale or female\b",
            r"\bmen and women\b",  # Should include "and gender diverse people"
        ]

        # Ableist metaphors
        self.ableist_metaphors = [
            r"\bfalling on deaf ears\b",
            r"\bturning a blind eye\b",
            r"\bcrippled by\b",
            r"\bwheelchair-bound\b",  # Use "wheelchair user"
            r"\bconfined to a wheelchair\b",
        ]

    def check_file(self, file_path: Path) -> bool:
        """
        Check a file for stigmatizing language.

        Args:
            file_path: Path to the file to check

        Returns:
            True if no issues found, False otherwise
        """
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, start=1):
            # Check stigmatizing terms
            for pattern, suggestion in self.stigma_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(
                        (
                            str(file_path),
                            f"Stigmatizing language detected",
                            line_num,
                            f"Consider using: {suggestion}",
                        )
                    )

            # Check binary gender assumptions
            for pattern in self.binary_gender_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(
                        (
                            str(file_path),
                            "Binary gender assumption detected",
                            line_num,
                            "Use gender-inclusive language (they/them, or 'people of all genders')",
                        )
                    )

            # Check ableist metaphors
            for pattern in self.ableist_metaphors:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(
                        (
                            str(file_path),
                            "Ableist metaphor detected",
                            line_num,
                            "Use alternative phrasing that doesn't reference disability",
                        )
                    )

        return len(self.issues) == 0

    def report(self) -> str:
        """Generate a report of all issues found."""
        if not self.issues:
            return "✓ No stigmatizing language detected!"

        report = ["❌ Stigmatizing Language Issues Found:", ""]

        grouped_issues: Dict[str, List[Tuple[int, str, str]]] = {}

        for file_path, issue_type, line_num, suggestion in self.issues:
            if file_path not in grouped_issues:
                grouped_issues[file_path] = []
            grouped_issues[file_path].append((line_num, issue_type, suggestion))

        for file_path, issues in grouped_issues.items():
            report.append(f"File: {file_path}")
            for line_num, issue_type, suggestion in issues:
                report.append(f"  Line {line_num}: {issue_type}")
                report.append(f"    → {suggestion}")
                report.append("")

        report.append("---")
        report.append(
            "Please review the NUAA accessibility guidelines: nuaa-kit/accessibility-guidelines.md"
        )
        report.append("For terminology guidance, see: nuaa-kit/glossary.md")

        return "\n".join(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check for stigmatizing and non-inclusive language"
    )
    parser.add_argument("files", nargs="+", help="Files to check")
    parser.add_argument(
        "--strict", action="store_true", help="Fail on any issues (exit code 1)"
    )

    args = parser.parse_args()

    linter = StigmaLinter()
    all_passed = True

    for file_path in args.files:
        path = Path(file_path)

        # Check markdown, text, and template files
        if path.suffix in (".md", ".txt", ".template"):
            if not linter.check_file(path):
                all_passed = False

    # Print report
    print(linter.report())

    # Exit with appropriate code
    if args.strict and not all_passed:
        print("\n⚠ Build failed due to stigmatizing language.")
        print("This is a critical accessibility issue that must be addressed.")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
