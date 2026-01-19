import csv
from pathlib import Path
from vars import RAW_DATA_DIR

def reorder_csv_rows(input_csv: Path, output_csv: Path):
    # Step 1: read all rows into memory
    rows = []
    with input_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Step 2: build parent->children map and row lookup
    children_map = {}  # parent_id -> list of child rows
    row_map = {}       # id -> row
    roots = []

    for row in rows:
        row_id = row['id']
        parent_id = row['parent_id'].strip() if row['parent_id'] else None
        row_map[row_id] = row
        if not parent_id:
            roots.append(row)
        else:
            children_map.setdefault(parent_id, []).append(row)

    # Step 3: do a depth-first search (DFS)/topological sort
    ordered_rows = []

    def dfs(row):
        if row in ordered_rows:
            return
        parent_id = row['parent_id'].strip() if row['parent_id'] else None
        if parent_id and parent_id in row_map:
            dfs(row_map[parent_id])
        if row not in ordered_rows:
            ordered_rows.append(row)

    for row in rows:
        dfs(row)

    # Step 4: write reordered CSV
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns) # pyright: ignore[reportArgumentType]
        writer.writeheader()
        for row in ordered_rows:
            writer.writerow(row)

    print(f"Reordered {input_csv.name} → {output_csv.name}, {len(ordered_rows)} rows")

# Example usage
input_path = Path(f"{RAW_DATA_DIR}/themes.csv")
output_path = Path(f"{RAW_DATA_DIR}/themes_reordered.csv")
reorder_csv_rows(input_path, output_path)
