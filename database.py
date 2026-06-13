# database.py
import sqlite3
import re
import pandas as pd

DB_PATH = "nf_buildathon.db"

def check_security(sql_query: str) -> bool:
    """
    Tokenizes the query string to verify no write, modify, 
    or destructive commands are being passed.
    """
    forbidden_keywords = {"insert", "update", "delete", "drop", "alter", "truncate", "create", "replace"}
    # Strip string and match words only
    tokens = set(re.findall(r'\b\w+\b', sql_query.lower()))
    
    # If any forbidden keyword intersects with our query tokens, block execution
    if tokens.intersection(forbidden_keywords):
        return False
    return True

def run_query(sql_query: str):
    """
    Executes a SELECT query safely against the read-only SQLite URI interface.
    """
    if not check_security(sql_query):
        return {
            "status": "error", 
            "message": "Security Exception: Write, Modify, or Structural DDL commands are strictly blocked."
        }
    
    try:
        # 'mode=ro' acts as an engine-level lock preventing database mutation
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return {"status": "success", "data": df}
    except Exception as e:
        return {"status": "error", "message": str(e)}