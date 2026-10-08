# Prompt Log

## Entry 1: Requirements session (Day 1)
Prompt: Asked Kimi to ask me questions one at a time to define requirements, no code.
Result: Kimi asked 13 questions and gave a requirements list, which I rewrote in my own words in REQUIREMENTS.md.
AI mistakes:
- Asked several questions in one message (Questions 4, 5 and 11) even though I said one at a time.
- Said the app had two screens (Home and Reports) when it has four.
- Offered extra features (income, budgets, charts, export) that I cut to keep the app small.
- Kept asking after it had enough to write the list, so I told it to stop.

## Entry 2: Planning session (Day 2)
Prompt: Pasted my requirements and asked Kimi for a file structure, database table, and screen list, with no code.
Result: Kimi gave a sensible plan. I asked for four changes and it applied all of them.
AI mistakes:
- Named the screens folder ui/ instead of screens/ because I did not paste PROJECT_CONTEXT.md into the chat.
- Added models.py, which was unnecessary for a small app.
- Named the date column expense_date instead of date.
- Left out init_db() and get_expense_by_id(), which the app needs.

## Entry 3: Stage 1 basic window (Day 3)
Prompt: Pasted PROJECT_CONTEXT.md and asked for only main.py with a window titled Student Expense Tracker and three buttons that print messages.
Result: Worked first time. Window opens and all three buttons print to the console. I changed a button label myself to check I could control the code.
AI mistakes:
- Added a bold title label I did not ask for (harmless, so I kept it).

## Entry 4: Stage 2 database (Day 4)
Prompt: Pasted PROJECT_CONTEXT.md and asked for database.py only, with init_db, add_expense, get_all_expenses, the categories and the kobo helpers, plus a terminal test script.
Result: database.py was correct first time: parameterized queries, integer kobo, no Tkinter. I tested it and confirmed 2 saved expenses were still there in a fresh Python session.
AI mistakes:
- Named the test script test_database.py, which would clash with my pytest file in tests/. I renamed it try_database.py.
- The test script deleted the database at the end, so it never checked that data survives a restart. I added that check myself.

## Entry 5: Stage 3 Add Expense form (Day 5)
Prompt: Pasted PROJECT_CONTEXT.md, main.py and database.py. Asked for screens/add_expense_screen.py with validation, using the decimal module for the amount, and minimal changes to main.py.
Result: The form worked and database.py was left untouched. I tested 11 kinds of bad input and saved 1500.50 as 150050 kobo.
AI mistakes:
- Typing NaN or Infinity as the amount crashed the app with a TypeError. Decimal accepts those values, and the decimal-places check could not compare a string with a number. My validation tests caught it, not the AI.
- Fixed it with a debugging prompt (what happened, error, code, expected). The fix was amount.is_finite(), checked before the other amount rules.
- Kimi's explanation was slightly wrong: it said both NaN and Infinity hit the exponent line first, but NaN fails earlier, on the <= 0 check. The fix still covered both.
- Showed main.py as a diff instead of the full file, and listed screens/__init__.py as new when it already existed.

## Entry 6: Stage 4a View Expenses table (Day 6)
Prompt: Pasted PROJECT_CONTEXT.md, main.py and database.py. Asked for screens/view_expenses_screen.py with a Treeview table, newest first, amounts in naira, reloading from the database on open, and no edit or delete. Asked for the full main.py, not a diff.
Result: Worked first time. The table showed my saved expenses with correct amounts (150050 kobo shown as 1,500.50), and a new expense appeared without restarting the app.
AI mistakes:
- Widened the window to 600x400 without being asked (reasonable, so I kept it).
- Left an unused import (tkinter as tk) in the new screen file.
- No real bugs this stage. The refresh-on-open instruction in my prompt prevented the common stale-table problem.

## Entry 7: Stage 4b Edit and Delete (Day 7)
Prompt: Pasted PROJECT_CONTEXT.md and all four code files. Asked for get_expense_by_id, update_expense and delete_expense in database.py, Edit and Delete buttons on the View screen matching rows by database id, a confirmation before delete, and Edit reusing the Add Expense form. Asked for full files, not diffs.
Result: Worked first time. I tested the new database functions on a throwaway database first, then ran 11 manual tests (no selection, editing the second row, cancel, invalid edits, Add mode after Edit, delete with No and Yes). All passed.
AI mistakes:
- Said its database checks passed, but I could not see them, so I tested the functions myself before trusting that.
- No real bugs this stage. Telling it to match rows by id (not position) and to refresh after changes in the prompt prevented the common problems.
