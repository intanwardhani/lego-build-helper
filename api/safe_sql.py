from pathlib import Path
from api.load_db import get_connection, get_schema
from api.call_api import nl_to_sql
from src.vars import QNA_LOG

FORBIDDEN_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE",
    "DROP", "ALTER", "TRUNCATE", "CREATE"
}

HIGH_REASONING_MESSAGE = (
    "This is a high-reasoning question outside the limit of the current database. "
    "Please rephrase your question."
)

def execute_sql(conn, sql: str):
    upper_sql = sql.upper()
    if any(keyword in upper_sql for keyword in FORBIDDEN_KEYWORDS):
        raise ValueError("Unsafe SQL detected")

    cursor = conn.cursor()
    cursor.execute(sql)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    return columns, rows


def rows_to_natural_language(columns, rows) -> str:
    if not rows:
        return "No results found."

    if len(columns) == 1:
        return f"The answer is {rows[0][0]}."

    lines = []
    for row in rows:
        parts = [f"{col}: {val}" for col, val in zip(columns, row)]
        lines.append("; ".join(parts))

    return "Here are the results:\n" + "\n".join(lines)


def log_qna(question: str, sql: str | None, answer: str):
    with open(QNA_LOG, "a", encoding="utf-8") as f:
        f.write("Q: " + question + "\n")
        if sql:
            f.write("SQL: " + sql + "\n")
        f.write("A: " + answer + "\n")
        f.write("-" * 50 + "\n")


def answer_question(question: str):
    conn = get_connection()
    try:
        schema = get_schema(conn)
        sql = nl_to_sql(schema, question)

        if sql == "HIGH_REASONING_QUESTION":
            log_qna(question, None, HIGH_REASONING_MESSAGE)
            return {
                "question": question,
                "sql": None,
                "answer": HIGH_REASONING_MESSAGE
            }

        columns, rows = execute_sql(conn, sql)
        answer = rows_to_natural_language(columns, rows)

        log_qna(question, sql, answer)

        return {
            "question": question,
            "sql": sql,
            "answer": answer
        }

    finally:
        conn.close()
