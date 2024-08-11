# db/db.py
import sqlite3
from typing import Generator

DATABASE_URL = '/Users/asdf/Documents/Project_Unit/sanddeot/SANDDEOT-Server/db/server.db'

def get_db() -> Generator[sqlite3.Cursor, None, None]:
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    try:
        yield conn.cursor()
    finally:
        conn.commit()  # Fix here
        conn.close()
