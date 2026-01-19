from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "dataset" / "lego.db"
SCHEMA_PATH = BASE_DIR / "sql" / "build_tables.sql"
RAW_DATA_DIR = BASE_DIR / "dataset" / "raw"
QNA_LOG = BASE_DIR / "qnas.txt"

CSV_SOURCE_MAP = {
    'themes': 'themes_reordered.csv'
    }

# FK-safe load order
CSV_LOAD_ORDER = [
    # no dependencies
    "themes.csv",
    "part_categories.csv",
    "colors.csv",
    "parts.csv",
    "sets.csv",
    "minifigs.csv",
    
    # inventories
    "inventories.csv",
    
    # inventory children
    "inventory_sets.csv",
    "inventory_minifigs.csv",
    "inventory_parts.csv",
    
    # remaining relationship
    "elements.csv",
    "part_relationships.csv",
    ]

SYSTEM_PROMPT = """
You are a SQL assistant.

Given a SQLite database schema and a natural language question,
write the correct SQL query to answer it.

Rules:
- Use only tables and columns from the schema
- SQLite syntax only
- Do not hallucinate tables or columns
- Do not modify the database
- Return ONLY the SQL query
- No markdown, no explanations

If the question cannot be answered using ONLY the given database schema,
return exactly this string (and nothing else):

HIGH_REASONING_QUESTION
"""
