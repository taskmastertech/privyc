"""Original use-case rewritten using the csv_reader package."""
from privyc import get_columns

for row in get_columns("MOCK_DATA.csv", ["first_name", "last_name"]):
    print(row["first_name"], row["last_name"])
