import pytest
from pathlib import Path
from privyc import filter_rows, get_columns, get_headers, iter_csv, read_csv

FIXTURE = Path(__file__).parent / "fixtures" / "sample.csv"


def test_get_headers():
    assert get_headers(FIXTURE) == ["id", "first_name", "last_name", "city", "gender"]


def test_read_csv_returns_list_of_dicts():
    rows = read_csv(FIXTURE)
    assert isinstance(rows, list)
    assert len(rows) == 4
    assert rows[0] == {
        "id": "1",
        "first_name": "Alice",
        "last_name": "Smith",
        "city": "NYC",
        "gender": "Female",
    }


def test_iter_csv_yields_dicts():
    gen = iter_csv(FIXTURE)
    first = next(gen)
    assert first["first_name"] == "Alice"
    second = next(gen)
    assert second["first_name"] == "Bob"


def test_get_columns_returns_only_requested():
    rows = get_columns(FIXTURE, ["first_name", "last_name"])
    assert rows[0] == {"first_name": "Alice", "last_name": "Smith"}
    assert "city" not in rows[0]
    assert "id" not in rows[0]


def test_get_columns_raises_on_missing_column():
    with pytest.raises(KeyError):
        get_columns(FIXTURE, ["nonexistent"])


def test_filter_rows_single_condition():
    rows = filter_rows(FIXTURE, city="NYC")
    assert len(rows) == 2
    assert all(r["city"] == "NYC" for r in rows)


def test_filter_rows_multiple_conditions():
    rows = filter_rows(FIXTURE, city="NYC", gender="Female")
    assert len(rows) == 2
    assert all(r["city"] == "NYC" and r["gender"] == "Female" for r in rows)


def test_filter_rows_no_match():
    rows = filter_rows(FIXTURE, city="London")
    assert rows == []


def test_encoding_parameter(tmp_path):
    csv_file = tmp_path / "latin.csv"
    csv_file.write_bytes("name,note\nJosé,café\n".encode("latin-1"))
    rows = read_csv(csv_file, encoding="latin-1")
    assert rows[0]["name"] == "José"


def test_pathlib_and_string_paths():
    assert read_csv(str(FIXTURE)) == read_csv(FIXTURE)
