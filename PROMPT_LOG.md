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
