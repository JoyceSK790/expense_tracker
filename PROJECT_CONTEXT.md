# PROJECT: Student Expense & Budget Tracker

## GOAL
Desktop app for students to record and understand their spending.

## TECH
Python 3, Tkinter (ttk), SQLite (sqlite3), pytest

## FILES
- main.py - Application entry point
- database.py - SQLite database operations
- screens/ - User interface screens
- tests/ - Automated tests
- PROJECT_CONTEXT.md - Project information
- PROMPT_LOG.md - Record of AI prompts and development decisions
- README.md - Project documentation
- REQUIREMENTS.md - System requirements
- .gitignore - Files excluded from Git

## RULES
- Keep the application simple and beginner-friendly.
- Use SQLite for local data storage.
- Validate user input before saving data.
- Keep database logic separate from the user interface.
- Test important database operations.

- Inspect existing code before changing anything.
- Do not rewrite working parts unnecessarily.
- Change only what I ask. Explain before editing.
- Use parameterized SQL queries (question-mark placeholders, never f-strings).
- Store money as integer kobo, display as naira.
- No Tkinter in database.py. No SQL in screens/.

## STATUS
- Working: Stage 1 (main.py opens a window with three buttons); Stage 2 (database.py has init_db, add_expense, get_all_expenses, CATEGORIES, naira_to_kobo, kobo_to_naira, tested and data survives restart); Stage 3 (screens/add_expense_screen.py: Add Expense form with validation, saves to database, main.py shows it from the Add Expense button and calls init_db); Stage 4a (screens/view_expenses_screen.py: ttk.Treeview table of all expenses newest first, amounts in naira with thousands separator, refresh() reloads from the database each time the screen opens, Back to Home button; main.py wires it to the View Expenses button); Stage 4b (database.py has get_expense_by_id, update_expense, delete_expense; View Expenses has Edit and Delete buttons that match rows by database id; Delete asks for confirmation; Edit reuses the Add Expense form pre-filled via start_edit and start_add; full add, view, edit, delete working and tested); Stage 5a (database.py has search_expenses(text, category, date_from, date_to) with escape_like so % and _ match literally; View Expenses has a filter bar with text search, category dropdown, From and To dates, Apply and Clear buttons, a No expenses found message, and opens unfiltered via show_all; Edit and Delete still work on filtered rows and keep the filters after a delete; tested); Stage 5b (database.py has get_total_spending, get_month_spending, get_totals_by_category, all SQL SUM with COALESCE so empty gives 0; screens/reports_screen.py shows total, this month and per-category totals in naira, reloads on open via refresh; main.py wires the Reports button; totals checked by hand and the screen refreshes after add and delete); Day 10 testing (tests/test_database.py has 23 pytest tests using temporary databases, all passing, run with python -m pytest tests/ -v; MANUAL_TESTS.md checklist all passed); Day 11 (screens/home_screen.py Home screen shows total and this month figures, reloaded every time it is shown; Add Expense form polished with a grid layout, Save Changes in edit mode, Enter key saves, cursor starts in Amount; main.py uses HomeScreen; all tested)
- Broken: (nothing yet)
- Working on now: nothing. Project complete and published (README with screenshots, 23 pytest tests, manual checklist, 12 prompt log entries)

## PLAN (accepted)
- screens/app.py: window controller, swaps the four screens
- screens/home_screen.py, add_expense_screen.py, view_expenses_screen.py, reports_screen.py: one file per screen, UI only
- database.py functions: init_db, add_expense, update_expense, delete_expense, get_expense_by_id, get_all_expenses, search_expenses(text, category, date_from, date_to), get_total_spending, get_month_spending, get_totals_by_category
- database.py also holds CATEGORIES (8 fixed) and naira_to_kobo / kobo_to_naira
- Table expenses: id (INTEGER PRIMARY KEY AUTOINCREMENT), amount_kobo (INTEGER NOT NULL), category (TEXT NOT NULL), date (TEXT NOT NULL, YYYY-MM-DD), description (TEXT)
- Validation lives in add_expense_screen.py
- Categories: Food, Transport, School fees, Books and supplies, Entertainment, Airtime and data, Health, Other











