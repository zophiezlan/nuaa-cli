"""Tests for utility functions."""

import shutil

from nuaa_cli.utils import StepTracker, check_tool
from nuaa_cli.scaffold import _slugify


def test_step_tracker_basic_flow():
    """Test basic StepTracker operations."""
    tracker = StepTracker("Test Steps")

    # Add steps
    tracker.add("step1", "First step")
    tracker.add("step2", "Second step")

    assert len(tracker.steps) == 2
    assert tracker.steps[0]["status"] == "pending"

    # Start a step
    tracker.start("step1", "in progress")
    assert tracker.steps[0]["status"] == "running"
    assert tracker.steps[0]["detail"] == "in progress"

    # Complete a step
    tracker.complete("step1", "done")
    assert tracker.steps[0]["status"] == "done"

    # Error a step
    tracker.error("step2", "failed")
    assert tracker.steps[1]["status"] == "error"


def test_step_tracker_skip():
    """Test skipping steps."""
    tracker = StepTracker("Test Steps")
    tracker.add("optional", "Optional step")
    tracker.skip("optional", "not needed")

    assert tracker.steps[0]["status"] == "skipped"
    assert tracker.steps[0]["detail"] == "not needed"


def test_step_tracker_render():
    """Test rendering tracker to tree."""
    tracker = StepTracker("Test Title")
    tracker.add("test", "Test step")
    tracker.complete("test", "finished")

    tree = tracker.render()
    assert tree is not None
    assert "Test Title" in str(tree.label)


def test_step_tracker_refresh_callback():
    """Test attach_refresh callback."""
    tracker = StepTracker("Test")
    callback_called = []

    def refresh_cb():
        callback_called.append(True)

    tracker.attach_refresh(refresh_cb)
    tracker.add("step1", "Step 1")

    # Should have triggered refresh
    assert len(callback_called) > 0


def test_check_tool_git_found():
    """Test check_tool finds git (if installed)."""
    # Git is usually available in CI/dev environments
    if shutil.which("git"):
        result = check_tool("git", tracker=None)
        assert result is True


def test_check_tool_nonexistent():
    """Test check_tool with non-existent tool."""
    tool_name = "this-tool-definitely-does-not-exist-12345"
    result = check_tool(tool_name, tracker=None)
    assert result is False


def test_check_tool_with_tracker():
    """Test check_tool updates tracker."""
    tracker = StepTracker("Tools")
    tracker.add("git", "Git")

    if shutil.which("git"):
        result = check_tool("git", tracker=tracker)
        assert result is True
        # Should have updated the tracker
        assert any(s["status"] in ["done", "running"] for s in tracker.steps)


def test_slugify_basic():
    """Test slugify with basic strings."""
    assert _slugify("Hello World") == "hello-world"
    assert _slugify("Test-Project") == "test-project"
    assert _slugify("Multiple   Spaces") == "multiple-spaces"


def test_slugify_special_chars():
    """Test slugify removes special characters."""
    assert _slugify("Test@Project!") == "testproject"
    assert _slugify("Hello (World)") == "hello-world"
    assert _slugify("Test & Project") == "test-project"


def test_slugify_unicode():
    """Test slugify with unicode characters."""
    # Should handle basic unicode
    result = _slugify("Café")
    assert "caf" in result.lower()


def test_slugify_empty():
    """Test slugify with empty string."""
    result = _slugify("")
    # Empty string defaults to 'feature'
    assert result == "feature"


def test_slugify_numbers():
    """Test slugify preserves numbers."""
    assert _slugify("Project 2024") == "project-2024"
    assert _slugify("123 Test") == "123-test"
