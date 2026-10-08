"""Add Expense screen.

Shows the form for adding an expense, and is reused (pre-filled)
for editing an existing one. All input validation happens here -
nothing reaches the database unless every field is valid.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import ttk, messagebox

import database


class AddExpenseScreen(ttk.Frame):
    """Form with Amount, Category, Date and Description fields.

    Add mode: Save stores a new expense and clears the form.
    Edit mode (started with start_edit): Save updates the expense,
    then on_edit_done is called. Cancel goes to on_cancel in add
    mode and on_edit_done in edit mode.
    """

    def __init__(self, parent, on_cancel, on_edit_done=None):
        super().__init__(parent, padding=20)
        self.on_cancel = on_cancel
        self.on_edit_done = on_edit_done
        self.edit_id = None  # None means "adding", an int means "editing"

        self.title_label = ttk.Label(self, text="Add Expense",
                                     font=("Helvetica", 14, "bold"))
        self.title_label.pack(pady=(0, 15))

        ttk.Label(self, text="Amount (naira):").pack(anchor="w")
        self.amount_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.amount_var).pack(fill="x", pady=(2, 10))

        ttk.Label(self, text="Category:").pack(anchor="w")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            self, textvariable=self.category_var,
            values=database.CATEGORIES, state="readonly")
        self.category_combo.pack(fill="x", pady=(2, 10))

        ttk.Label(self, text="Date (YYYY-MM-DD):").pack(anchor="w")
        self.date_var = tk.StringVar(value=date.today().isoformat())
        ttk.Entry(self, textvariable=self.date_var).pack(fill="x", pady=(2, 10))

        ttk.Label(self, text="Description (optional):").pack(anchor="w")
        self.description_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.description_var).pack(fill="x", pady=(2, 15))

        buttons = ttk.Frame(self)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Save",
                   command=self.save).pack(side="left", expand=True,
                                           fill="x", padx=(0, 5))
        ttk.Button(buttons, text="Cancel",
                   command=self.cancel).pack(side="left", expand=True,
                                             fill="x", padx=(5, 0))

    def start_edit(self, expense):
        """Switch to edit mode, pre-filling the form from the expense."""
        self.edit_id = expense["id"]
        self.title_label.configure(text="Edit Expense")
        self.amount_var.set(f"{database.kobo_to_naira(expense['amount_kobo']):.2f}")
        self.category_var.set(expense["category"])
        self.date_var.set(expense["date"])
        self.description_var.set(expense["description"])

    def start_add(self):
        """Switch back to add mode with an empty, reset form."""
        self.edit_id = None
        self.title_label.configure(text="Add Expense")
        self.clear_form()

    def save(self):
        amount_kobo = self.validate()
        if amount_kobo is None:
            return  # invalid - nothing is saved

        fields = (amount_kobo,
                  self.category_var.get().strip(),
                  self.date_var.get().strip(),
                  self.description_var.get().strip())

        if self.edit_id is None:
            database.add_expense(*fields)
            messagebox.showinfo("Saved", "Expense saved.")
            self.clear_form()
        else:
            database.update_expense(self.edit_id, *fields)
            messagebox.showinfo("Saved", "Expense saved.")
            self.on_edit_done()

    def cancel(self):
        if self.edit_id is None:
            self.on_cancel()
        else:
            self.on_edit_done()

    def validate(self):
        """Check every field. Return amount in kobo, or None after
        showing an error message."""
        raw_amount = self.amount_var.get().strip()
        if not raw_amount:
            self.show_error("Please enter an amount.")
            return None
        try:
            amount = Decimal(raw_amount)
        except InvalidOperation:
            self.show_error("Amount must be a number, e.g. 1500.50.")
            return None
        if not amount.is_finite():
            self.show_error("Amount must be a number, e.g. 1500.50.")
            return None
        if amount <= 0:
            self.show_error("Amount must be more than 0.")
            return None
        if amount.as_tuple().exponent < -2:
            self.show_error("Amount can have at most 2 decimal places.")
            return None

        raw_date = self.date_var.get().strip()
        try:
            expense_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            self.show_error("Date must be a valid date in YYYY-MM-DD format.")
            return None
        if expense_date > date.today():
            self.show_error("Date cannot be in the future.")
            return None

        category = self.category_var.get().strip()
        if category not in database.CATEGORIES:
            self.show_error("Please choose a category.")
            return None

        description = self.description_var.get().strip()
        if len(description) > 100:
            self.show_error("Description must be 100 characters or fewer.")
            return None

        return database.naira_to_kobo(amount)

    def show_error(self, message):
        messagebox.showerror("Invalid input", message)

    def clear_form(self):
        self.amount_var.set("")
        self.category_var.set("")
        self.description_var.set("")
        self.date_var.set(date.today().isoformat())
