"""
Test race condition handling in feature directory creation.

This test verifies that concurrent directory creation is handled
correctly without conflicts.
"""

import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest

from nuaa_cli.scaffold import _next_feature_dir, _ensure_nuaa_root


class TestRaceCondition:
    """Test concurrent directory creation."""

    def test_concurrent_feature_dir_creation(self):
        """Test that concurrent calls create unique directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            program_name = "test-program"
            num_workers = 10

            # Create directories concurrently
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = [
                    executor.submit(_next_feature_dir, program_name, root)
                    for _ in range(num_workers)
                ]

                results = []
                for future in as_completed(futures):
                    try:
                        feature_dir, num_str, slug = future.result()
                        results.append((feature_dir, num_str, slug))
                    except Exception as e:
                        pytest.fail(f"Concurrent directory creation failed: {e}")

            # Verify all directories are unique
            dir_paths = [r[0] for r in results]
            assert len(dir_paths) == len(set(dir_paths)), "Duplicate directories created"

            # Verify all directories exist
            for dir_path in dir_paths:
                assert dir_path.exists(), f"Directory {dir_path} does not exist"

            # Verify sequential numbering (001-010)
            num_strs = sorted([r[1] for r in results])
            expected = [f"{i:03d}" for i in range(1, num_workers + 1)]
            assert num_strs == expected, f"Expected {expected}, got {num_strs}"

    def test_concurrent_different_programs(self):
        """Test concurrent creation of different program directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            programs = ["program-a", "program-b", "program-c"]
            iterations = 3

            # Create directories for different programs concurrently
            with ThreadPoolExecutor(max_workers=len(programs) * iterations) as executor:
                futures = []
                for program in programs:
                    for _ in range(iterations):
                        futures.append(executor.submit(_next_feature_dir, program, root))

                results = []
                for future in as_completed(futures):
                    try:
                        feature_dir, num_str, slug = future.result()
                        results.append((feature_dir, num_str, slug))
                    except Exception as e:
                        pytest.fail(f"Concurrent directory creation failed: {e}")

            # Verify all directories are unique
            dir_paths = [r[0] for r in results]
            assert len(dir_paths) == len(set(dir_paths)), "Duplicate directories created"

            # Verify all directories exist
            for dir_path in dir_paths:
                assert dir_path.exists(), f"Directory {dir_path} does not exist"

            # Verify we have the correct number of directories
            nuaa_root = _ensure_nuaa_root(root)
            created_dirs = list(nuaa_root.iterdir())
            assert len(created_dirs) == len(programs) * iterations

    def test_max_retries_not_exceeded(self):
        """Test that normal operations don't exhaust retries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            # Create 50 directories sequentially
            for i in range(50):
                program_name = f"program-{i}"
                feature_dir, num_str, slug = _next_feature_dir(program_name, root)
                assert feature_dir.exists()
                assert num_str == f"{i+1:03d}"

            # Verify all directories were created
            nuaa_root = _ensure_nuaa_root(root)
            created_dirs = list(nuaa_root.iterdir())
            assert len(created_dirs) == 50

    def test_recovery_after_manual_creation(self):
        """Test that function recovers if directory is manually created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            nuaa_root = _ensure_nuaa_root(root)

            # Manually create 001-test
            manual_dir = nuaa_root / "001-test"
            manual_dir.mkdir(parents=True)

            # Try to create with same program name
            feature_dir, num_str, slug = _next_feature_dir("test", root)

            # Should create 002-test instead
            assert num_str == "002"
            assert feature_dir.name == "002-test"
            assert feature_dir.exists()

    def test_handles_gaps_in_numbering(self):
        """Test that function handles gaps in numbering correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            nuaa_root = _ensure_nuaa_root(root)

            # Create directories with gaps: 001, 003, 005
            for num in [1, 3, 5]:
                dir_path = nuaa_root / f"{num:03d}-program"
                dir_path.mkdir(parents=True)

            # Next directory should be 006 (highest + 1)
            feature_dir, num_str, slug = _next_feature_dir("new-program", root)
            assert num_str == "006"
            assert feature_dir.exists()
