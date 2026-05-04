import csv

with open("MOCK_DATA.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["first_name"], row["last_name"])
