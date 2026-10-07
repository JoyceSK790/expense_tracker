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
- Working: (nothing yet)
- Broken: (nothing yet)
- Working on now: requirements
