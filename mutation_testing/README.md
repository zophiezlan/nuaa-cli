# Mutation Testing

This directory contains configuration for mutation testing with `mutmut`.

## What is Mutation Testing?

Mutation testing introduces small changes (mutations) to your code to verify that your tests can detect them. If a test suite doesn't catch a mutation, it indicates a gap in test coverage or test quality.

## Setup

Install mutmut:

```bash
pip install mutmut
```

## Running Mutation Tests

### Basic Usage

```bash
# Run mutation testing on all code
mutmut run

# Run on specific file or directory
mutmut run --paths-to-mutate=src/nuaa_cli/utils.py

# Run with specific test command
mutmut run --runner="pytest tests/test_utils.py"
```

### Viewing Results

```bash
# Show summary
mutmut results

# Show detailed results
mutmut show

# Show specific mutant
mutmut show 42

# Generate HTML report
mutmut html
```

### Working with Mutants

```bash
# Show mutants that survived (not caught by tests)
mutmut results --status survived

# Apply a specific mutant to see what changed
mutmut apply 42

# Restore original code
mutmut apply --restore
```

## Configuration

The `.mutmut_config` file contains settings:

- `paths_to_mutate`: Which code to mutate
- `exclude_patterns`: What to skip
- `runner`: Test command to use
- `use_coverage`: Only mutate covered lines

## Interpreting Results

### Mutant Status

- **Killed**: Test caught the mutation ✅ (Good!)
- **Survived**: Mutation not caught ❌ (Test gap!)
- **Timeout**: Test took too long
- **Suspicious**: Unclear result

### Score Calculation

```
Mutation Score = (Killed / Total) × 100%
```

Target: **> 80%** mutation score for high-quality test suites

## Example Workflow

```bash
# 1. Run full mutation test suite
mutmut run

# 2. Check results
mutmut results
# Output: Killed: 150, Survived: 20, Timeout: 2

# 3. Investigate survivors
mutmut results --status survived

# 4. View specific mutant
mutmut show 15

# 5. Add tests to catch the mutant

# 6. Re-run on specific file
mutmut run --paths-to-mutate=src/nuaa_cli/utils.py

# 7. Generate HTML report
mutmut html
# Report saved to html/index.html
```

## Common Mutations

Mutmut introduces these types of mutations:

1. **Arithmetic Operators**

   ```python
   # Original: x + y
   # Mutation: x - y, x * y, x / y
   ```

2. **Comparison Operators**

   ```python
   # Original: x > y
   # Mutation: x < y, x >= y, x == y
   ```

3. **Boolean Operators**

   ```python
   # Original: x and y
   # Mutation: x or y, not (x and y)
   ```

4. **Return Values**

   ```python
   # Original: return True
   # Mutation: return False, return None
   ```

5. **String Mutations**

   ```python
   # Original: "hello"
   # Mutation: "", "XX"
   ```

6. **Number Mutations**

   ```python
   # Original: 42
   # Mutation: 43, 41, 0
   ```

## Performance Tips

### Speed Up Mutation Testing

1. **Use Coverage Data**

   ```bash
   # Only mutate covered code
   pytest --cov=src/nuaa_cli --cov-report=
   mutmut run --use-coverage
   ```

2. **Parallel Execution**

   ```bash
   # Run 4 workers in parallel
   mutmut run --use-coverage --parallelize 4
   ```

3. **Test Specific Modules**

   ```bash
   # Focus on specific files
   mutmut run --paths-to-mutate=src/nuaa_cli/utils.py,src/nuaa_cli/validation.py
   ```

4. **Cache Results**

   ```bash
   # Reuse previous results
   mutmut run --use-coverage --cache-only-mutants-that-failed
   ```

## CI/CD Integration

### GitHub Actions

```yaml
name: Mutation Testing
on: [pull_request]

jobs:
  mutmut:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install mutmut

      - name: Run mutation tests
        run: |
          mutmut run --use-coverage --parallelize 4

      - name: Check mutation score
        run: |
          mutmut results
          # Fail if mutation score < 80%
          SCORE=$(mutmut results | grep -oP 'Score: \K[0-9.]+')
          if (( $(echo "$SCORE < 80" | bc -l) )); then
            echo "Mutation score too low: $SCORE%"
            exit 1
          fi
```

## Best Practices

1. **Start Small**: Begin with critical modules (utils, validation, security)
2. **Set Thresholds**: Define minimum mutation score (e.g., 80%)
3. **Regular Runs**: Run mutation tests on CI for new code
4. **Fix Survivors**: Investigate and add tests for survived mutants
5. **Track Progress**: Monitor mutation score over time

## Troubleshooting

### Tests Hang

```bash
# Increase timeout multiplier
mutmut run --test-time-multiplier=3.0
```

### Too Many Timeouts

```bash
# Skip timeouts
mutmut run --skip-timeout
```

### Memory Issues

```bash
# Reduce parallelization
mutmut run --parallelize 2
```

## Example Output

```
Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.
🙁 Survived.         This means your tests needs to be expanded.
🔇 Skipped.          Skipped.

Results:
Killed: 187 (93.5%)
Survived: 13 (6.5%)
Timeout: 0 (0.0%)
Suspicious: 0 (0.0%)

Mutation Score: 93.5%
```

## Recommended Modules to Test

Priority order for mutation testing:

1. **Security-critical** (High priority)
   - `src/nuaa_cli/utils.py` (input validation)
   - `src/nuaa_cli/download.py` (ZIP extraction)

2. **Core functionality** (Medium priority)
   - `src/nuaa_cli/git_utils.py`
   - `src/nuaa_cli/scaffold.py`

3. **Commands** (Lower priority)
   - `src/nuaa_cli/commands/*.py`

## Resources

- [Mutmut Documentation](https://mutmut.readthedocs.io/)
- [Mutation Testing Wikipedia](https://en.wikipedia.org/wiki/Mutation_testing)
- [PyCon Talk on Mutation Testing](https://www.youtube.com/watch?v=jwB3Nn4hR1o)
