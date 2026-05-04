from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator


def get_headers(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """Return column names without reading the entire file."""
    with open(path, newline="", encoding=encoding) as f:
        return next(csv.reader(f))


def iter_csv(
    path: str | Path, encoding: str = "utf-8"
) -> Iterator[dict[str, str]]:
    """Yield rows one at a time as dicts (memory-efficient for large files)."""
    with open(path, newline="", encoding=encoding) as f:
        yield from csv.DictReader(f)


def read_csv(
    path: str | Path, encoding: str = "utf-8"
) -> list[dict[str, str]]:
    """Read all rows and return them as a list of dicts.

    Each dict maps column name → cell value (always a string).
    """
    return list(iter_csv(path, encoding))


def get_columns(
    path: str | Path,
    columns: list[str],
    encoding: str = "utf-8",
) -> list[dict[str, str]]:
    """Return rows containing only the specified columns.

    Raises KeyError if any column name is not present in the file.
    """
    return [{col: row[col] for col in columns} for row in iter_csv(path, encoding)]


def filter_rows(
    path: str | Path,
    encoding: str = "utf-8",
    **filters: str,
) -> list[dict[str, str]]:
    """Return rows where every column=value keyword argument matches exactly.

    Example::

        filter_rows("data.csv", gender="Female", city="NYC")
    """
    return [
        row
        for row in iter_csv(path, encoding)
        if all(row.get(k) == v for k, v in filters.items())
    ]
