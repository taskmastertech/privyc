# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run a single test
pytest tests/test_reader.py::test_filter_rows_single_condition

# Run tests with coverage
pytest --cov=privyc --cov-report=term-missing

# Build distribution packages (requires: pip install build)
python -m build

# Publish to PyPI (requires: pip install twine + PyPI API token)
twine upload dist/*
```

## Architecture

```
src/privyc/       ← installable package (src layout keeps it off sys.path during dev)
  __init__.py         ← public API: re-exports the five functions + __version__
  reader.py           ← all logic lives here
  py.typed            ← PEP 561 marker; tells type checkers this package has annotations
tests/
  fixtures/sample.csv ← self-contained test fixture (do not rely on MOCK_DATA.csv in tests)
  test_reader.py
examples/
  read_names.py       ← original use-case rewritten using the package
```

### Public API (five functions)

| Function | Returns | Notes |
|---|---|---|
| `read_csv(path, encoding)` | `list[dict]` | Loads full file |
| `iter_csv(path, encoding)` | `Iterator[dict]` | Streams row-by-row |
| `get_headers(path, encoding)` | `list[str]` | Reads header row only |
| `get_columns(path, columns, encoding)` | `list[dict]` | Raises `KeyError` on missing column |
| `filter_rows(path, encoding, **filters)` | `list[dict]` | AND logic; string equality only |

All cell values are always `str`. `iter_csv` is the core primitive — the other functions build on it.

## Packaging notes

- Package name on PyPI: `privyc` (verify availability before publishing)
- Import name: `privyc`
- `pyproject.toml` uses the `src/` layout with `setuptools`
- Before bumping the version, update it in both `pyproject.toml` and `src/privyc/__init__.py`
