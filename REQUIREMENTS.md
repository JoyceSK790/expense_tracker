# Requirements: Student Expense & Budget Tracker

## Problem
Students often spend money without knowing where it goes. This app lets one student record expenses and see where the money went.

## Must do
- Add, view, edit and delete expenses
- Search and filter expenses (description text, category, date range)
- Show a spending summary: total, this month, and per category

## Each expense stores
- Amount: positive number, up to 2 decimals, saved as whole kobo
- Category: one of 8 fixed choices (Food, Transport, School fees, Books and supplies, Entertainment, Airtime and data, Health, Other)
- Date: YYYY-MM-DD, defaults to today, cannot be in the future
- Description: optional, up to 100 characters

## Screens (one window, buttons switch between them)
- Home: total and this month's spending, buttons to the other screens
- Add Expense: the form; Edit reuses it pre-filled
- View Expenses: table (newest first) with filters, Apply and Clear buttons, Edit and Delete (Delete asks to confirm)
- Reports: total, this month, total per category (numbers only)

## Rules
- Invalid input shows a clear error and saves nothing
- Amounts shown in naira with thousands separators
- One user, no login, data stored locally in SQLite

## Not included
Income, budgets, savings goals, charts, export, receipts, multiple users
