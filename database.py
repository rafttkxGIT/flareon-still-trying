import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            channel_id TEXT NOT NULL,
            message TEXT NOT NULL,
            interval INTEGER NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auto_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
