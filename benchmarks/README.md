# Performance Benchmarks

This directory contains performance benchmarking tools for the NUAA CLI.

## Running Benchmarks

```bash
# Run all benchmarks
python benchmarks/performance.py

# Or use make command (if configured)
make benchmark
```

## Benchmark Suite

The benchmark suite measures performance of:

1. **Slugify** - String slugification for directory names
2. **Input Validation** - Program name validation and sanitization
3. **JSON Merge** - Deep merging of configuration files
4. **Template Loading** - Template file loading from disk

## Results

Benchmark results are saved to `benchmark_results.json` and displayed in a formatted table:

```
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Benchmark          ┃ Iterations ┃  Min (s) ┃  Mean (s) ┃  Max (s) ┃ StdDev (s) ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Slugify            │        100 │   0.0001 │    0.0001 │   0.0003 │     0.0000 │
│ Input Validation   │        100 │   0.0002 │    0.0003 │   0.0008 │     0.0001 │
│ JSON Merge         │         50 │   0.0015 │    0.0018 │   0.0035 │     0.0004 │
│ Template Loading   │         10 │   0.0005 │    0.0008 │   0.0012 │     0.0002 │
└────────────────────┴────────────┴──────────┴───────────┴──────────┴────────────┘
```

## Interpreting Results

- **Min**: Fastest execution time
- **Mean**: Average execution time
- **Max**: Slowest execution time
- **StdDev**: Standard deviation (consistency indicator)

Lower times and lower standard deviation indicate better performance and consistency.

## Adding New Benchmarks

Create a new benchmark function:

```python
def benchmark_my_feature(iterations: int = 10) -> Dict[str, Any]:
    """Benchmark my feature."""
    from nuaa_cli.my_module import my_function

    def run():
        my_function(args)

    bench = Benchmark("My Feature")
    return bench.run(run, iterations=iterations)
```

Add it to `run_all_benchmarks()`:

```python
benchmarks = [
    # ... existing benchmarks
    ("My Feature", benchmark_my_feature, 50),
]
```

## Performance Targets

Target performance benchmarks:

- **Slugify**: < 0.001s mean
- **Input Validation**: < 0.001s mean
- **JSON Merge**: < 0.005s mean
- **Template Loading**: < 0.002s mean

## Continuous Monitoring

Benchmark results can be tracked over time to detect performance regressions:

```bash
# Run benchmarks and save results with timestamp
python benchmarks/performance.py > benchmarks/results_$(date +%Y%m%d).txt
```
