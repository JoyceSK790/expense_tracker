"""SQLite storage for the Student Expense Tracker.

No Tkinter here - this module only talks to the database.
Money is stored as integer kobo; use naira_to_kobo / kobo_to_naira
to convert.
"""

import sqlite3

CATEGORIES = [
    "Food",
    "Transport",
    "School fees",
    "Books and supplies",
    "Entertainment",
    "Airtime and data",
    "Health",
    "Other",
]

DEFAULT_DB = "expenses.db"


def naira_to_kobo(amount_naira):
    """Convert a naira amount (e.g. 500.50) to whole kobo (50050)."""
    return int(round(amount_naira * 100))


def kobo_to_naira(amount_kobo):
    """Convert whole kobo (e.g. 50050) back to naira (500.5)."""
    return amount_kobo / 100


def init_db(db_path=DEFAULT_DB):
    """Create the database file and expenses table if they do not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount_kobo INTEGER NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_expense(amount_kobo, category, date, description, db_path=DEFAULT_DB):
    """Insert one expense. date is a 'YYYY-MM-DD' string.

    Returns the id of the new row.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount_kobo, category, date, description)"
        " VALUES (?, ?, ?, ?)",
        (amount_kobo, category, date, description),
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_all_expenses(db_path=DEFAULT_DB):
    """Return all expenses as a list of dicts, newest first.

    Each dict has keys: id, amount_kobo, category, date, description.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, amount_kobo, category, date, description"
        " FROM expenses ORDER BY date DESC, id DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
