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
