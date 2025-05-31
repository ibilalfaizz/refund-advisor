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

# Get all chat history
def get_chat_history():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("SELECT role, message, timestamp FROM chat_log ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return rows

# Clear chat history (optional, if you want a reset button)
def clear_chat_history():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute("DELETE FROM chat_log")
    conn.commit()
    conn.close()

def get_all_sessions():
    with sqlite3.connect("chat_history.db") as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT session_id FROM chat_log ORDER BY id DESC")
        sessions = [row[0] for row in c.fetchall()]
    return sessions

def get_chat_history(session_id=None):
    with sqlite3.connect("chat_history.db") as conn:
        c = conn.cursor()
        if session_id:
            c.execute(
                "SELECT role, message, timestamp FROM chat_log WHERE session_id = ? ORDER BY id ASC",
                (session_id,)
            )
        else:
            c.execute("SELECT role, message, timestamp FROM chat_log ORDER BY id ASC")
        return c.fetchall()

