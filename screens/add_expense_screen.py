"""Add Expense screen.

Shows the form for adding an expense (Edit mode reuses this form
in a later stage). All input validation happens here - nothing
reaches the database unless every field is valid.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import ttk, messagebox

import database


class AddExpenseScreen(ttk.Frame):
    """Form with Amount, Category, Date and Description fields."""

    def __init__(self, parent, on_cancel):
        super().__init__(parent, padding=20)
        self.on_cancel = on_cancel

        ttk.Label(self, text="Add Expense",
                  font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

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
                   command=self.on_cancel).pack(side="left", expand=True,
                                                fill="x", padx=(5, 0))

    def save(self):
        amount_kobo = self.validate()
        if amount_kobo is None:
            return  # invalid - nothing is saved

        database.add_expense(
            amount_kobo,
            self.category_var.get().strip(),
            self.date_var.get().strip(),
            self.description_var.get().strip(),
        )
        messagebox.showinfo("Saved", "Expense saved.")
        self.clear_form()

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
