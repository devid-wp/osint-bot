import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'shadow_graph.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Инициализация базы данных и создание таблиц."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица для хранения взаимодействий (кто кому ответил)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER,
            from_username TEXT,
            to_user_id INTEGER,
            to_username TEXT,
            chat_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Индексы ускорят поиск по базе, когда данных станет много
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_from_user ON interactions(from_user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_to_user ON interactions(to_user_id)')
    
    conn.commit()
    conn.close()

def log_interaction(from_id, from_user, to_id, to_user, chat_id):
    """Запись взаимодействия в БД."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (from_user_id, from_username, to_user_id, to_username, chat_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (from_id, from_user, to_id, to_user, chat_id))
    conn.commit()
    conn.close()