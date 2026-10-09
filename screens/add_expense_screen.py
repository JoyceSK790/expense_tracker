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

        # Make the layout grid-based and tidy
        self.columnconfigure(0, weight=0)  # label column
        self.columnconfigure(1, weight=1)  # field column

        self.title_label = ttk.Label(
            self, text="Add Expense", font=("Helvetica", 14, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Row counter for the form
        r = 1

        # Amount
        ttk.Label(self, text="Amount (naira):").grid(
            row=r, column=0, sticky="w", padx=(0, 10), pady=(0, 6)
        )
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(self, textvariable=self.amount_var)
        self.amount_entry.grid(row=r, column=1, sticky="ew", pady=(0, 6))

        r += 1

        # Category
        ttk.Label(self, text="Category:").grid(
            row=r, column=0, sticky="w", padx=(0, 10), pady=(0, 6)
        )
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=database.CATEGORIES,
            state="readonly",
        )
        self.category_combo.grid(row=r, column=1, sticky="ew", pady=(0, 6))

        r += 1

        # Date
        ttk.Label(self, text="Date (YYYY-MM-DD):").grid(
            row=r, column=0, sticky="w", padx=(0, 10), pady=(0, 6)
        )
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.date_entry = ttk.Entry(self, textvariable=self.date_var)
        self.date_entry.grid(row=r, column=1, sticky="ew", pady=(0, 6))

        r += 1

        # Description
        ttk.Label(self, text="Description (optional):").grid(
            row=r, column=0, sticky="w", padx=(0, 10), pady=(0, 6)
        )
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(self, textvariable=self.description_var)
        self.description_entry.grid(row=r, column=1, sticky="ew", pady=(0, 15))

        r += 1

        # Bind Enter to Save (same as clicking Save)
        # Bind to the Entry widgets so Enter behaves naturally in them.
        self.amount_entry.bind("<Return>", lambda _e: self.save())
        self.date_entry.bind("<Return>", lambda _e: self.save())
        self.description_entry.bind("<Return>", lambda _e: self.save())
        # Category is a combobox; Enter behavior can vary, so we bind it too.
        self.category_combo.bind("<Return>", lambda _e: self.save())

        # Buttons
        buttons = ttk.Frame(self)
        buttons.grid(row=r, column=0, columnspan=2, sticky="ew")
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)

        self.save_button = ttk.Button(buttons, text="Save", command=self.save)
        self.save_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ttk.Button(buttons, text="Cancel", command=self.cancel).grid(
            row=0, column=1, sticky="ew", padx=(5, 0)
        )

        # Put cursor in Amount field when the screen opens
        self.after(0, self.amount_entry.focus_set)

    def start_edit(self, expense):
        """Switch to edit mode, pre-filling the form from the expense."""
        self.edit_id = expense["id"]
        self.title_label.configure(text="Edit Expense")
        self.save_button.configure(text="Save Changes")
        self.amount_var.set(f"{database.kobo_to_naira(expense['amount_kobo']):.2f}")
        self.category_var.set(expense["category"])
        self.date_var.set(expense["date"])
        self.description_var.set(expense["description"])

    def start_add(self):
        """Switch back to add mode with an empty, reset form."""
        self.edit_id = None
        self.title_label.configure(text="Add Expense")
        self.save_button.configure(text="Save")
        self.clear_form()
        self.after(0, self.amount_entry.focus_set)

    def save(self):
        amount_kobo = self.validate()
        if amount_kobo is None:
            return  # invalid - nothing is saved

        fields = (
            amount_kobo,
            self.category_var.get().strip(),
            self.date_var.get().strip(),
            self.description_var.get().strip(),
        )

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
