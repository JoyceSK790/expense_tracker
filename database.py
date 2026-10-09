"""SQLite storage for the Student Expense Tracker.

No Tkinter here - this module only talks to the database.
Money is stored as integer kobo; use naira_to_kobo / kobo_to_naira
to convert.
"""

import sqlite3
from datetime import date

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


def get_expense_by_id(expense_id, db_path=DEFAULT_DB):
    """Return one expense as a dict, or None if no row has that id."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, amount_kobo, category, date, description"
        " FROM expenses WHERE id = ?",
        (expense_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_expense(expense_id, amount_kobo, category, date, description,
                   db_path=DEFAULT_DB):
    """Update an existing expense, matched by id."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE expenses SET amount_kobo = ?, category = ?, date = ?,"
        " description = ? WHERE id = ?",
        (amount_kobo, category, date, description, expense_id),
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id, db_path=DEFAULT_DB):
    """Delete one expense, matched by id."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def escape_like(text):
    """Escape the LIKE wildcards % and _ so they match literally."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_expenses(text=None, category=None, date_from=None, date_to=None,
                    db_path=DEFAULT_DB):
    """Return expenses matching ALL given conditions, newest first.

    - text: matches anywhere in the description (case-insensitive)
    - category: must match exactly
    - date_from / date_to: 'YYYY-MM-DD' strings, inclusive
    - a blank or None value means "no limit" for that condition
    """
    query = ("SELECT id, amount_kobo, category, date, description"
             " FROM expenses")
    conditions = []
    params = []

    if text:
        conditions.append("description LIKE ? ESCAPE '\\'")
        params.append(f"%{escape_like(text)}%")
    if category:
        conditions.append("category = ?")
        params.append(category)
    if date_from:
        conditions.append("date >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("date <= ?")
        params.append(date_to)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY date DESC, id DESC"

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]



def get_total_spending(db_path=DEFAULT_DB):
    """Return the sum of all expenses in kobo, or 0 if there are none."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount_kobo), 0) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_month_spending(db_path=DEFAULT_DB):
    """Return the sum for the current calendar month in kobo, or 0.

    Matches the same month AND year as today, e.g. '2026-10'.
    """
    month = date.today().strftime("%Y-%m")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(amount_kobo), 0) FROM expenses"
        " WHERE strftime('%Y-%m', date) = ?",
        (month,),
    )
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_totals_by_category(db_path=DEFAULT_DB):
    """Return a list of (category, total_kobo) for categories that
    have expenses, highest total first."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(amount_kobo) FROM expenses"
        " GROUP BY category ORDER BY SUM(amount_kobo) DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
