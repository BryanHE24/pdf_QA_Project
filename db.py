import sqlite3

def get_connection():
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
