import sqlite3
from datetime import datetime

# Initialize database and table
def init_db():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("init_db: chat_log table ensured ✅")


# Save a chat message
def save_message(session_id, role, message):
    print(f"save_message: Saving message for session_id={session_id}")
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_log (session_id, role, message, timestamp) VALUES (?, ?, ?, ?)",
        (session_id, role, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    print("save_message: Message saved ✅")



def get_sessions():
    print("get_sessions: Opening DB connection...")
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT session_id FROM chat_log ORDER BY timestamp DESC")
    return [row[0] for row in cursor.fetchall()]

def load_messages(session_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, message FROM chat_log WHERE session_id = ? ORDER BY timestamp", (session_id,))

    rows = cursor.fetchall()
    return [{"name": row[0], "msg": row[1]} for row in rows]

