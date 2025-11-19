"""
Performance benchmarks for NUAA CLI.

This module provides performance benchmarking utilities to measure
and track the performance of key CLI operations.
"""

import time
from pathlib import Path
from typing import Callable, Dict, List, Any
import statistics
import json

from rich.console import Console
from rich.table import Table


class Benchmark:
    """Performance benchmark utilities."""

    def __init__(self, name: str):
        """
        Initialize a benchmark.

        Args:
            name: Name of the benchmark
        """
        self.name = name
        self.results: List[float] = []

    def run(self, func: Callable, iterations: int = 10, warmup: int = 2) -> Dict[str, Any]:
        """
        Run a benchmark function multiple times and collect results.

        Args:
            func: Function to benchmark
            iterations: Number of iterations to run
            warmup: Number of warmup iterations (not counted)

        Returns:
            Dictionary with benchmark statistics
        """
        # Warmup runs
        for _ in range(warmup):
            func()

        # Actual benchmark runs
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append(end - start)

        self.results = times

        return {
            "name": self.name,
            "iterations": iterations,
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
            "total": sum(times),
        }


class BenchmarkSuite:
    """Suite of benchmarks for NUAA CLI."""

    def __init__(self):
        """Initialize the benchmark suite."""
        self.benchmarks: List[Dict[str, Any]] = []
        self.console = Console()

    def add_result(self, result: Dict[str, Any]):
        """
        Add a benchmark result to the suite.

        Args:
            result: Benchmark result dictionary
        """
        self.benchmarks.append(result)

    def display_results(self):
        """Display benchmark results in a formatted table."""
        table = Table(title="NUAA CLI Performance Benchmarks")

        table.add_column("Benchmark", style="cyan", no_wrap=True)
        table.add_column("Iterations", justify="right", style="magenta")
        table.add_column("Min (s)", justify="right", style="green")
        table.add_column("Mean (s)", justify="right", style="yellow")
        table.add_column("Max (s)", justify="right", style="red")
        table.add_column("StdDev (s)", justify="right", style="blue")

        for result in self.benchmarks:
            table.add_row(
                result["name"],
                str(result["iterations"]),
                f"{result['min']:.4f}",
                f"{result['mean']:.4f}",
                f"{result['max']:.4f}",
                f"{result['stdev']:.4f}",
            )

        self.console.print(table)

    def save_results(self, output_file: Path):
        """
        Save benchmark results to a JSON file.

        Args:
            output_file: Path to output JSON file
        """
        with open(output_file, "w") as f:
            json.dump(self.benchmarks, f, indent=2)

        self.console.print(f"[green]Benchmark results saved to {output_file}[/green]")


def benchmark_template_loading(iterations: int = 10) -> Dict[str, Any]:
    """
    Benchmark template file loading performance.

    Args:
        iterations: Number of iterations to run

    Returns:
        Benchmark results
    """
    from nuaa_cli.scaffold import _load_template

    def load_template():
        try:
            _load_template("program-design.md")
        except Exception:
            pass  # Template may not exist in test environment

    bench = Benchmark("Template Loading")
    return bench.run(load_template, iterations=iterations)


def benchmark_slugify(iterations: int = 100) -> Dict[str, Any]:
    """
    Benchmark slugify performance.

    Args:
        iterations: Number of iterations to run

    Returns:
        Benchmark results
    """
    from nuaa_cli.scaffold import _slugify

    def slugify():
        _slugify("Test Program Name with Spaces and 123 Numbers!")

    bench = Benchmark("Slugify")
    return bench.run(slugify, iterations=iterations)


def benchmark_input_validation(iterations: int = 100) -> Dict[str, Any]:
    """
    Benchmark input validation performance.

    Args:
        iterations: Number of iterations to run

    Returns:
        Benchmark results
    """
    from nuaa_cli.utils import validate_program_name
    from rich.console import Console

    console = Console(file=None)  # Suppress output

    def validate():
        try:
            validate_program_name("Test Program Name", console)
        except Exception:
            pass

    bench = Benchmark("Input Validation")
    return bench.run(validate, iterations=iterations)


def benchmark_json_merge(iterations: int = 50) -> Dict[str, Any]:
    """
    Benchmark JSON merging performance.

    Args:
        iterations: Number of iterations to run

    Returns:
        Benchmark results
    """
    import tempfile
    from nuaa_cli.download import merge_json_files
    from rich.console import Console

    console = Console(file=None)

    # Create temporary JSON files
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f1:
        json.dump({"key1": "value1", "nested": {"a": 1, "b": 2}}, f1)
        file1 = Path(f1.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f2:
        json.dump({"key2": "value2", "nested": {"b": 3, "c": 4}}, f2)
        file2 = Path(f2.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f3:
        output = Path(f3.name)

    def merge():
        try:
            merge_json_files(file1, file2, output, verbose=False, console=console)
        except Exception:
            pass

    bench = Benchmark("JSON Merge")
    result = bench.run(merge, iterations=iterations)

    # Cleanup
    file1.unlink(missing_ok=True)
    file2.unlink(missing_ok=True)
    output.unlink(missing_ok=True)

    return result


def run_all_benchmarks(iterations: int = 10) -> BenchmarkSuite:
    """
    Run all available benchmarks.

    Args:
        iterations: Number of iterations per benchmark

    Returns:
        BenchmarkSuite with all results
    """
    suite = BenchmarkSuite()
    console = Console()

    console.print("[bold cyan]Running NUAA CLI Performance Benchmarks...[/bold cyan]\n")

    # Run benchmarks
    benchmarks = [
        ("Slugify", benchmark_slugify, 100),
        ("Input Validation", benchmark_input_validation, 100),
        ("JSON Merge", benchmark_json_merge, 50),
        ("Template Loading", benchmark_template_loading, 10),
    ]

    for name, func, iters in benchmarks:
        console.print(f"Running: {name}...", style="yellow")
        result = func(iterations=iters)
        suite.add_result(result)

    console.print("\n[bold green]Benchmarks Complete![/bold green]\n")
    return suite


if __name__ == "__main__":
    # Run benchmarks when executed directly
    suite = run_all_benchmarks()
    suite.display_results()

    # Save results
    output_file = Path("benchmark_results.json")
    suite.save_results(output_file)
