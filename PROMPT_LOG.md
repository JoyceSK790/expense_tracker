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

## Entry 8: Stage 5a Search and filter (Day 8)
Prompt: Pasted PROJECT_CONTEXT.md, database.py and view_expenses_screen.py. Asked for search_expenses in database.py with parameterized SQL, and a filter bar on the View Expenses screen with Apply and Clear, date validation, a No expenses found message, and Edit and Delete still working on filtered rows.
Result: The filters, dates, Apply and Clear, and Edit and Delete on filtered rows all worked. I wrote a 9-line test for search_expenses and ran 15 manual tests. All passed after one fix.
AI mistakes:
- Searching for % or _ matched every expense, because they are LIKE wildcards and the search text was not escaped. Kimi said 8 checks passed but never tested this case. My own test caught it.
- Fixed it with a debugging prompt (what happened, results, code, expected). The fix was an escape_like helper plus ESCAPE in the query, and the query stayed parameterized.
- Kimi's explanation said _ matches every non-empty description. That is true for my test data, but a blank description would not match, so the explanation was slightly loose.
- Pre-filled the search box with the real text Search description, instead of a placeholder. It is cleared when the screen opens, so I left it.

## Entry 9: Stage 5b Reports (Day 9)
Prompt: Pasted PROJECT_CONTEXT.md, database.py and main.py. Asked for get_total_spending, get_month_spending and get_totals_by_category in database.py using SQL SUM (not Python or UI maths), returning 0 not None when empty, plus a Reports screen that reloads on open and a Reports button in main.py.
Result: The database functions were correct. I tested them on a throwaway database with hand-calculated totals, including traps for the same month last year and the last day of last month. After one fix, the screen showed totals that matched my own arithmetic, and it refreshed after adding and deleting an expense.
AI mistakes:
- The app crashed at startup with TclError: unknown option -background. Kimi read the background colour from a ttk.Frame, which has no background option. It said all checks pass, but it had only tested the database functions, never the window. My run caught it.
- Fixed it with a debugging prompt (what happened, error, code, expected). The fix was removing the background argument and using borderwidth=0.
- Kimi's explanation blamed tk.Text and my platform, but the failing call was cget on the ttk.Frame, so the diagnosis was muddled even though the fix was right.

## Entry 10: pytest tests (Day 10)
Prompt: Pasted PROJECT_CONTEXT.md and database.py. Asked for pytest tests that use a temporary database for every test, check specific values, build the month-test dates from today's date, and include the % and _ search cases. Told it not to modify database.py.
Result: The tests were good. All 23 passed on my computer. To check they could really fail, I broke database.py on purpose (month total counting every month) and one test failed, then I restored the file and confirmed 23 passed again.
AI mistakes:
- Said 22 tests would pass, but the file has 23. It stated a number it had not counted.
- Said it verified the assertions with a plain harness because pytest was not installed in its sandbox. I could not see that, so the run on my own computer was what counted.
- No bugs in the tests themselves. The prompt rules (temporary database, specific values, dates built from today) prevented the usual weak-test problems.

## Entry 11: Home screen and polish (Day 11)
Prompt 1: Pasted PROJECT_CONTEXT.md, main.py and database.py. Asked for screens/home_screen.py showing total spending and this month in naira using the existing database functions, reloading every time Home is shown, and main.py using it.
Result 1: Worked first time. The figures matched my hand-checked totals and stayed current after adding, editing and deleting an expense.
Prompt 2: Pasted PROJECT_CONTEXT.md and add_expense_screen.py. Asked to improve layout and usability of that screen only, keeping all behaviour and method names.
Result 2: Worked. I tested both add mode and edit mode and everything passed.
AI mistakes:
- Mentioned a screens/app.py file that does not exist in my project. It came from the old plan in my context file, because I put the screen switching in main.py.
- Did not centre the form, which I asked for. It admitted this itself. I left it because it is only cosmetic.
- Kimi was overloaded when I sent the polish prompt, so I had to retry.

## Entry 12: README tidy (Day 12)
Prompt: Wrote the README myself (intro and known limitations in my own words), then asked an AI tool to tidy only the wording, without adding or removing facts, commands, links or image paths.
Result: Kimi was overloaded, so I used ChatGPT. It fixed real typos in my intro (helps helps, keeps record, keep account) and kept all the headings, commands, the clone link, image paths and the 23-test number. I compared with git diff before accepting anything.
AI mistakes:
- Added a compliment to my Known limitations (it is very easy to understand when viewed), which is not a limitation and made the section less honest.
- Changed can be tested manually on Windows only, which changes what I did (I tested on Windows only). I rewrote the whole section as an honest bullet list myself.
- Its list of changes was accurate for the typos, but I only trusted it after checking the diff.
