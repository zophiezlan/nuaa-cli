#!/usr/bin/env python3
"""
Readability checker for NUAA CLI documentation and templates.

Checks that text meets accessibility targets for plain language.
Based on NUAA accessibility guidelines.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


class ReadabilityChecker:
    """Check text readability against NUAA standards."""

    def __init__(self):
        self.issues: List[Tuple[str, str, int]] = []

    def check_file(self, file_path: Path) -> bool:
        """
        Check a markdown file for readability issues.

        Args:
            file_path: Path to the file to check

        Returns:
            True if file meets standards, False if issues found
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check sentence length
        self._check_sentence_length(content, file_path)

        # Check paragraph length
        self._check_paragraph_length(content, file_path)

        # Check acronyms are explained
        self._check_acronyms_explained(content, file_path)

        # Check for jargon
        self._check_jargon(content, file_path)

        # Check for passive voice (simplified check)
        self._check_passive_voice(content, file_path)

        return len(self.issues) == 0

    def _check_sentence_length(self, content: str, file_path: Path) -> None:
        """Check for overly long sentences (>20 words)."""
        # Split into sentences (simplified)
        sentences = re.split(r"[.!?]+", content)

        for i, sentence in enumerate(sentences):
            # Clean up
            sentence = sentence.strip()
            if not sentence:
                continue

            # Count words
            words = len(sentence.split())

            # Flag if too long (>25 words is definitely too long)
            if words > 25:
                self.issues.append(
                    (
                        str(file_path),
                        f"Sentence too long ({words} words, target <20)",
                        i + 1,
                    )
                )

    def _check_paragraph_length(self, content: str, file_path: Path) -> None:
        """Check for overly long paragraphs (>5 sentences)."""
        # Split into paragraphs
        paragraphs = content.split("\n\n")

        for i, para in enumerate(paragraphs):
            # Skip code blocks, headers, lists
            if para.startswith("#") or para.startswith("-") or para.startswith("`"):
                continue

            # Count sentences
            sentences = len(re.split(r"[.!?]+", para))

            if sentences > 6:
                self.issues.append(
                    (
                        str(file_path),
                        f"Paragraph too long ({sentences} sentences, target 2-5)",
                        i + 1,
                    )
                )

    def _check_acronyms_explained(self, content: str, file_path: Path) -> None:
        """Check that acronyms are explained on first use."""
        # Find acronyms (2+ uppercase letters)
        acronyms = re.findall(r"\b[A-Z]{2,}\b", content)

        # Common acronyms that don't need explanation
        common = {"NSW", "USA", "UK", "PDF", "URL", "API", "CLI", "AI"}

        for acronym in set(acronyms):
            if acronym in common:
                continue

            # Check if explained (acronym followed by text in parentheses)
            pattern = rf"{acronym}\s*\([^)]+\)"
            if not re.search(pattern, content):
                self.issues.append(
                    (
                        str(file_path),
                        f"Acronym '{acronym}' not explained on first use",
                        0,
                    )
                )

    def _check_jargon(self, content: str, file_path: Path) -> None:
        """Check for common jargon that should be explained."""
        jargon_terms = [
            "stakeholder",
            "deliverable",
            "leverage",
            "synergy",
            "paradigm",
            "optimize",
            "utilize",  # Use "use" instead
            "methodology",  # Often "method" is clearer
        ]

        content_lower = content.lower()

        for term in jargon_terms:
            if term in content_lower:
                # This is a warning, not an error (jargon can be acceptable with explanation)
                count = content_lower.count(term)
                if count > 3:  # Only flag if used frequently
                    self.issues.append(
                        (
                            str(file_path),
                            f"Jargon term '{term}' used {count} times - consider simpler alternative",
                            0,
                        )
                    )

    def _check_passive_voice(self, content: str, file_path: Path) -> None:
        """Check for passive voice (simplified detection)."""
        # Common passive voice patterns
        passive_patterns = [
            r"\bis\s+\w+ed\b",
            r"\bare\s+\w+ed\b",
            r"\bwas\s+\w+ed\b",
            r"\bwere\s+\w+ed\b",
            r"\bbeen\s+\w+ed\b",
        ]

        passive_count = 0
        for pattern in passive_patterns:
            passive_count += len(re.findall(pattern, content, re.IGNORECASE))

        # If more than 10% of sentences are passive, flag it
        total_sentences = len(re.split(r"[.!?]+", content))
        if total_sentences > 0:
            passive_ratio = passive_count / total_sentences

            if passive_ratio > 0.15:  # 15% threshold
                self.issues.append(
                    (
                        str(file_path),
                        f"High passive voice usage ({int(passive_ratio * 100)}%) - prefer active voice",
                        0,
                    )
                )

    def report(self) -> str:
        """Generate a report of all issues found."""
        if not self.issues:
            return "✓ All readability checks passed!"

        report = ["Readability Issues Found:", ""]

        for file_path, issue, line in self.issues:
            location = f" (line {line})" if line > 0 else ""
            report.append(f"  {file_path}{location}")
            report.append(f"    → {issue}")
            report.append("")

        return "\n".join(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check readability of documentation")
    parser.add_argument("files", nargs="+", help="Files to check")
    parser.add_argument(
        "--strict", action="store_true", help="Fail on any issues (exit code 1)"
    )

    args = parser.parse_args()

    checker = ReadabilityChecker()
    all_passed = True

    for file_path in args.files:
        path = Path(file_path)
        if path.suffix != ".md":
            continue

        if not checker.check_file(path):
            all_passed = False

    # Print report
    print(checker.report())

    # Exit with appropriate code
    if args.strict and not all_passed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
