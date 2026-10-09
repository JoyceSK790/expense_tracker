# Manual Test Checklist

Run on the finished app after Stage 5. All items tested by hand.

| Situation | Expected result | Passed? |
|---|---|---|
| Save with empty fields | Clear error, nothing saved | Yes |
| Amount abc or negative | Rejected with message | Yes |
| Add a valid expense | Appears in the list | Yes |
| Edit an expense | Change shows and persists | Yes |
| Delete with confirmation | Removed; cancel keeps it | Yes |
| Search and filter | Only matching records shown | Yes |
| Summary totals | Match hand calculation | Yes |
| Close and reopen the app | All data still there | Yes |

## Extra cases tested during development
- NaN, Infinity and -Infinity as the amount (found a crash, fixed with is_finite)
- Amount with more than 2 decimal places, impossible dates, future dates, description over 100 characters
- Edit and Delete on a filtered table act on the right row and keep the filters
- Searching for % or _ matches only descriptions that contain those characters (found a bug, fixed with escape_like)
- Reports refresh after adding and deleting an expense

## Automated tests
23 pytest tests in tests/test_database.py, run with: python -m pytest tests/ -v
