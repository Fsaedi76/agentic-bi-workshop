
# src/tools/sql_tool.py
import sqlite3

def run_sql(query: str):
    """
    Very simple SQL tool for workshop use.
    Expects SELECT-only queries on the local SQLite DB: src/data/sales.sqlite
    Returns dict with columns and rows for the agent to format.
    """
    # Safety guard: only allow SELECT statements in the workshop
    normalized = query.strip().lower()
    if not normalized.startswith("select"):
        return {"error": "Only SELECT queries are allowed in this workshop."}

    conn = sqlite3.connect("src/data/sales.sqlite")
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        return {"columns": cols, "rows": rows}
    except Exception as e:
        return {"error": f"SQL error: {e}"}
    finally:
        conn.close()
