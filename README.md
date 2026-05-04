# csv-reader

A lightweight Python library for reading and querying CSV files. Zero external dependencies — built entirely on Python's standard library.

## Features

- Read a CSV into a list of dicts in one call
- Iterate row-by-row for memory-efficient handling of large files
- Select only the columns you need
- Filter rows by column value
- Inspect headers without reading the full file
- Full type annotations (`py.typed` marker included)
- Works with `str` paths, `pathlib.Path`, and custom encodings

## Installation

### From PyPI

```bash
pip install csv-reader
```

> **Before publishing:** verify the name `csv-reader` is available on [pypi.org](https://pypi.org). If it's taken, update the `name` field in `pyproject.toml`.

### From GitHub (without publishing to PyPI)

```bash
pip install git+https://github.com/yourusername/csv-reader.git
```

### For local development

```bash
git clone https://github.com/yourusername/csv-reader.git
cd csv-reader
pip install -e ".[dev]"
```

The `[dev]` extras install `pytest` and `pytest-cov`.

---

## Quick Start

```python
from csv_reader import read_csv, iter_csv, get_headers, get_columns, filter_rows

# Read all rows
rows = read_csv("data.csv")
# [{"id": "1", "first_name": "Alice", "last_name": "Smith", ...}, ...]

# Get column names only
headers = get_headers("data.csv")
# ["id", "first_name", "last_name", "email", "gender", "ip_address"]

# Keep only specific columns
names = get_columns("data.csv", ["first_name", "last_name"])
# [{"first_name": "Alice", "last_name": "Smith"}, ...]

# Filter by one or more column values
women_in_nyc = filter_rows("data.csv", gender="Female", city="NYC")

# Stream rows without loading the whole file into memory
for row in iter_csv("data.csv"):
    print(row["first_name"], row["last_name"])
```

---

## API Reference

All functions accept a `path` (either a `str` or `pathlib.Path`) and an optional `encoding` argument (default: `"utf-8"`).

> **Note on types:** every cell value is always a `str`, because CSV is a text format. Convert to `int`, `float`, etc. after reading if needed.

---

### `read_csv`

```python
def read_csv(path: str | Path, encoding: str = "utf-8") -> list[dict[str, str]]
```

Reads the entire CSV file and returns all rows as a list of dicts.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | — | Path to the CSV file |
| `encoding` | `str` | `"utf-8"` | File encoding |

**Returns:** `list[dict[str, str]]` — one dict per row, keys are the header column names.

**Example**

```python
rows = read_csv("users.csv")
print(rows[0])
# {"id": "1", "first_name": "Alice", "last_name": "Smith"}

print(rows[0]["first_name"])  # "Alice"
print(len(rows))              # number of data rows (excludes header)
```

---

### `iter_csv`

```python
def iter_csv(path: str | Path, encoding: str = "utf-8") -> Iterator[dict[str, str]]
```

Yields rows one at a time as dicts. The file is opened and streamed, so the full contents are never loaded into memory. Use this for large files where `read_csv` would be too slow or consume too much RAM.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | — | Path to the CSV file |
| `encoding` | `str` | `"utf-8"` | File encoding |

**Returns:** `Iterator[dict[str, str]]`

**Example**

```python
for row in iter_csv("large_file.csv"):
    process(row)
```

You can also use it with built-in functions that accept iterables:

```python
import itertools

first_100 = list(itertools.islice(iter_csv("data.csv"), 100))
```

---

### `get_headers`

```python
def get_headers(path: str | Path, encoding: str = "utf-8") -> list[str]
```

Returns the column names from the CSV header row without reading any data rows. Useful for inspecting a file before deciding which columns to use.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | — | Path to the CSV file |
| `encoding` | `str` | `"utf-8"` | File encoding |

**Returns:** `list[str]` — column names in the order they appear in the file.

**Example**

```python
headers = get_headers("users.csv")
# ["id", "first_name", "last_name", "email", "gender", "ip_address"]

if "email" in headers:
    emails = get_columns("users.csv", ["email"])
```

---

### `get_columns`

```python
def get_columns(
    path: str | Path,
    columns: list[str],
    encoding: str = "utf-8",
) -> list[dict[str, str]]
```

Reads all rows but returns only the specified columns. The result has the same row count as the file; only the keys in each dict are reduced.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | — | Path to the CSV file |
| `columns` | `list[str]` | — | Column names to include |
| `encoding` | `str` | `"utf-8"` | File encoding |

**Returns:** `list[dict[str, str]]`

**Raises:** `KeyError` if any name in `columns` does not exist as a header in the file.

**Example**

```python
names = get_columns("users.csv", ["first_name", "last_name"])
# [{"first_name": "Alice", "last_name": "Smith"}, ...]

# Extract a single column as a flat list
emails = [row["email"] for row in get_columns("users.csv", ["email"])]
```

---

### `filter_rows`

```python
def filter_rows(
    path: str | Path,
    encoding: str = "utf-8",
    **filters: str,
) -> list[dict[str, str]]
```

Returns all rows where every keyword argument matches the corresponding column value exactly (case-sensitive string equality).

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | — | Path to the CSV file |
| `encoding` | `str` | `"utf-8"` | File encoding |
| `**filters` | `str` | — | `column=value` pairs to match |

**Returns:** `list[dict[str, str]]` — only matching rows, with all columns present.

**Notes**
- All comparisons are against string values (e.g. use `"1"` not `1`).
- Filtering on a column that does not exist in the file silently returns no rows (the `dict.get` call returns `None`).
- Multiple filters are combined with AND logic. For OR logic, call `filter_rows` twice and combine the results.

**Example**

```python
# Single condition
women = filter_rows("users.csv", gender="Female")

# Multiple conditions (AND)
nyc_women = filter_rows("users.csv", gender="Female", city="NYC")

# OR logic: combine two calls
from_la_or_chicago = (
    filter_rows("users.csv", city="LA") +
    filter_rows("users.csv", city="Chicago")
)
```

---

## Common Patterns

### Convert a column to a specific type

```python
rows = read_csv("scores.csv")
scores = [int(row["score"]) for row in rows]
average = sum(scores) / len(scores)
```

### Write filtered results to a new CSV

```python
import csv
from csv_reader import filter_rows, get_headers

rows = filter_rows("users.csv", gender="Female")
headers = get_headers("users.csv")

with open("women.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
```

### Handle non-UTF-8 files

```python
rows = read_csv("legacy_export.csv", encoding="latin-1")
```

---

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=csv_reader --cov-report=term-missing
```

---

## Publishing to PyPI

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Build the distribution:
   ```bash
   python -m build
   ```

3. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

   You will need a [PyPI account](https://pypi.org/account/register/) and an API token.

---

## License

MIT — see [LICENSE](LICENSE).
