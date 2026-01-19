"""
While trying to load data into the inventory_parts table in lego.db, i got an error:

sqlite3.IntegrityError: UNIQUE constraint failed: 
inventory_parts.inventory_id, inventory_parts.part_num, inventory_parts.color_id

This is because the data inventory_parts have multiple duplicate rows with different
quantity values. For example, a Lego piece with the same part number and colour id appears
once in row 1 with quantity = 2 and once again in row 2 with quantity = 1. Thus, the correct
data should be for that piece to appear only in one row with quantity = 3. 

Therefore, this code works to aggregate those pseudo-duplicated rows by adding the quantity
values.
"""

import csv
import sqlite3
from collections import defaultdict
from pathlib import Path

def load_inventory_parts(conn, csv_file: Path):
    """
    Load inventory_parts CSV into SQLite, handling:
    - duplicate rows (same inventory_id, part_num, color_id)
    - summing quantity
    - normalizing boolean is_spare
    - preserving img_url
    """
    table_name = "inventory_parts"

    def bool_to_int(val):
        if isinstance(val, str):
            val_lower = val.strip().lower()
            return 1 if val_lower == "true" else 0
        return int(val or 0)

    # Aggregation dict
    # key: (inventory_id, part_num, color_id)
    # value: dict with quantity, is_spare, img_url
    aggregated = defaultdict(lambda: {"quantity": 0, "is_spare": 0, "img_url": None})

    with csv_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Key for uniqueness
            try:
                inventory_id = int(row["inventory_id"])
                part_num = row["part_num"].strip()
                color_id = int(row["color_id"])
            except Exception as e:
                print(f"Skipping invalid row: {row} ({e})")
                continue

            key = (inventory_id, part_num, color_id)

            # Quantity sum
            quantity = row.get("quantity")
            aggregated[key]["quantity"] += int(quantity) if quantity else 0

            # Boolean normalization for is_spare
            aggregated[key]["is_spare"] = max(
                aggregated[key]["is_spare"],
                bool_to_int(row.get("is_spare"))
            )

            # Preserve img_url if available
            aggregated[key]["img_url"] = row.get("img_url")

    # Prepare rows for insertion
    rows_to_insert = [
        (
            inventory_id,
            part_num,
            color_id,
            data["quantity"],
            data["is_spare"],
            data["img_url"]
        )
        for (inventory_id, part_num, color_id), data in aggregated.items()
    ]

    # FK-safe bulk insert
    sql = f"""
        INSERT INTO {table_name}
        (inventory_id, part_num, color_id, quantity, is_spare, img_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    try:
        conn.executemany(sql, rows_to_insert)
    except sqlite3.IntegrityError as e:
        print("FK constraint failed during inventory_parts load")
        raise

    print(f"Loaded {csv_file.name} → {table_name} ({len(rows_to_insert)} aggregated rows)")

