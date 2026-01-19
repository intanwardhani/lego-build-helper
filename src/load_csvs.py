import sqlite3
import csv
from pathlib import Path
from fix_inventory import load_inventory_parts
from vars import DB_PATH, RAW_DATA_DIR, CSV_LOAD_ORDER, CSV_SOURCE_MAP

def load_csv(conn, table_name, csv_file):
    with csv_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames

        placeholders = ", ".join("?" for _ in columns)
        column_list = ", ".join(columns)

        sql = f"""
            INSERT INTO {table_name} ({column_list})
            VALUES ({placeholders})
        """

        rows = [
            tuple(row[col] if row[col] != "" else None for col in columns)
            for row in reader
        ]

        ### debug ###
        # for row in rows:
        #     try:
        #         conn.execute(sql, row)
        #     except sqlite3.IntegrityError as e:
        #         print(f"FK failed on table '{table_name}', row:", row)
        #         raise
        ### end debug ###

        conn.executemany(sql, rows)

    print(f"Loaded {csv_file.name} ({len(rows)} rows)")

def create_indexes(conn):
    print("Creating indexes...")

    conn.executescript("""
        CREATE INDEX IF NOT EXISTS idx_inventory_parts_part
            ON inventory_parts (part_num);

        CREATE INDEX IF NOT EXISTS idx_inventory_parts_color
            ON inventory_parts (color_id);

        CREATE INDEX IF NOT EXISTS idx_inventory_parts_inventory
            ON inventory_parts (inventory_id);

        CREATE INDEX IF NOT EXISTS idx_inventory_parts_part_color
            ON inventory_parts (part_num, color_id);

        CREATE INDEX IF NOT EXISTS idx_elements_part
            ON elements (part_num);

        CREATE INDEX IF NOT EXISTS idx_elements_color
            ON elements (color_id);

        CREATE INDEX IF NOT EXISTS idx_elements_part_color
            ON elements (part_num, color_id);

        CREATE INDEX IF NOT EXISTS idx_parts_category
            ON parts (part_cat_id);

        CREATE INDEX IF NOT EXISTS idx_colors_is_trans
            ON colors (is_trans);

        CREATE INDEX IF NOT EXISTS idx_inventories_set
            ON inventories (set_num);
    """)

    print("Indexes created.")

def load_all_csvs():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run build_database.py first.")

    with sqlite3.connect(DB_PATH) as conn:
        # REQUIRED for SQLite
        conn.execute("PRAGMA foreign_keys = ON;")

        # Big speed-up for bulk loads
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")

        print("Beginning CSV load...")

        # One transaction for all inserts (FAST)
        
        with conn:
            for csv_name in CSV_LOAD_ORDER:
                table_name = Path(csv_name).stem

                # resolve actual csv source
                source_csv = CSV_SOURCE_MAP.get(table_name, csv_name)
                csv_path = RAW_DATA_DIR / source_csv
                
                if table_name == "inventory_parts":
                    load_inventory_parts(conn, csv_path)
                else:
                    load_csv(conn, table_name, csv_path)
                
                # logging
                if source_csv != csv_name:
                    print(f"Using {source_csv} for table {table_name}")

        create_indexes(conn)

        print("All CSVs loaded successfully.")

if __name__ == "__main__":
    load_all_csvs()
