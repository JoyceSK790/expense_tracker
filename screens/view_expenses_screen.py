"""View Expenses screen.

Shows expenses in a table (ttk.Treeview), newest first, with a
filter bar (text, category, date range). Filters are applied only
when Apply is pressed. Each row's Treeview item id is the expense's
database id, so Edit and Delete always act on the right expense
regardless of its position in the table.
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

import database

ALL_CATEGORIES = "All categories"


class ViewExpensesScreen(ttk.Frame):
    """Filterable table of expenses with Edit, Delete, Back to Home."""

    COLUMNS = ("date", "category", "description", "amount")

    def __init__(self, parent, on_back, on_edit):
        super().__init__(parent, padding=20)
        self.on_back = on_back
        self.on_edit = on_edit

        ttk.Label(self, text="View Expenses",
                  font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        # Filter bar
        filters = ttk.Frame(self)
        filters.pack(fill="x", pady=(0, 10))

        self.search_var = tk.StringVar()
        ttk.Entry(filters, textvariable=self.search_var,
                  width=18).grid(row=0, column=0, padx=(0, 5))
        self.search_var.set("Search description")

        self.category_var = tk.StringVar(value=ALL_CATEGORIES)
        ttk.Combobox(filters, textvariable=self.category_var,
                     values=[ALL_CATEGORIES] + database.CATEGORIES,
                     state="readonly", width=20).grid(row=0, column=1,
                                                      padx=(0, 5))

        ttk.Label(filters, text="From:").grid(row=0, column=2)
        self.from_var = tk.StringVar()
        ttk.Entry(filters, textvariable=self.from_var,
                  width=11).grid(row=0, column=3, padx=(2, 5))
        ttk.Label(filters, text="To:").grid(row=0, column=4)
        self.to_var = tk.StringVar()
        ttk.Entry(filters, textvariable=self.to_var,
                  width=11).grid(row=0, column=5, padx=(2, 5))

        ttk.Button(filters, text="Apply",
                   command=self.apply_filters).grid(row=0, column=6,
                                                    padx=(5, 0))
        ttk.Button(filters, text="Clear",
                   command=self.clear_filters).grid(row=0, column=7,
                                                    padx=(5, 0))

        # Table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=self.COLUMNS,
                                 show="headings", selectmode="browse")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("amount", text="Amount")
        self.tree.column("date", width=100, anchor="w")
        self.tree.column("category", width=140, anchor="w")
        self.tree.column("description", width=180, anchor="w")
        self.tree.column("amount", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status_var = tk.StringVar()
        ttk.Label(self, textvariable=self.status_var,
                  foreground="gray").pack(anchor="w", pady=(5, 0))

        buttons = ttk.Frame(self)
        buttons.pack(pady=(10, 0))
        ttk.Button(buttons, text="Edit",
                   command=self.edit_selected).pack(side="left", padx=5)
        ttk.Button(buttons, text="Delete",
                   command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(buttons, text="Back to Home",
                   command=self.on_back).pack(side="left", padx=5)

    # ---- filtering ----

    def show_all(self):
        """Reset every filter and show all expenses (used when the
        screen is opened)."""
        self.search_var.set("")
        self.category_var.set(ALL_CATEGORIES)
        self.from_var.set("")
        self.to_var.set("")
        self.refresh()

    def clear_filters(self):
        """Reset every filter and show all expenses."""
        self.show_all()

    def apply_filters(self):
        """Validate the dates, then reload the table with filters."""
        if not self.valid_date_range():
            return  # error already shown
        self.refresh()

    def valid_date_range(self):
        """Check the From/To entries. Return True if both are blank or
        valid YYYY-MM-DD dates with From not after To; otherwise show
        an error and return False."""
        from_text = self.from_var.get().strip()
        to_text = self.to_var.get().strip()

        from_date = None
        to_date = None
        if from_text:
            try:
                from_date = datetime.strptime(from_text, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror(
                    "Invalid date",
                    "From date must be a valid date in YYYY-MM-DD format.")
                return False
        if to_text:
            try:
                to_date = datetime.strptime(to_text, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror(
                    "Invalid date",
                    "To date must be a valid date in YYYY-MM-DD format.")
                return False
        if from_date and to_date and from_date > to_date:
            messagebox.showerror("Invalid date range",
                                 "From date cannot be after To date.")
            return False
        return True

    # ---- table ----

    def refresh(self):
        """Reload the table using the current filter values."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        category = self.category_var.get()
        expenses = database.search_expenses(
            text=self.search_var.get().strip() or None,
            category=None if category == ALL_CATEGORIES else category,
            date_from=self.from_var.get().strip() or None,
            date_to=self.to_var.get().strip() or None,
        )

        for expense in expenses:
            naira = database.kobo_to_naira(expense["amount_kobo"])
            # The Treeview item id IS the database id.
            self.tree.insert("", "end", iid=str(expense["id"]), values=(
                expense["date"],
                expense["category"],
                expense["description"],
                f"{naira:,.2f}",
            ))

        if not expenses:
            self.status_var.set("No expenses found")
        else:
            self.status_var.set("")

    # ---- edit / delete (unchanged behaviour) ----

    def selected_expense_id(self):
        """Return the database id of the selected row, or None after
        asking the user to select one."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("No selection",
                                "Please select an expense first.")
            return None
        return int(selection[0])

    def edit_selected(self):
        expense_id = self.selected_expense_id()
        if expense_id is None:
            return
        expense = database.get_expense_by_id(expense_id)
        if expense is not None:
            self.on_edit(expense)

    def delete_selected(self):
        expense_id = self.selected_expense_id()
        if expense_id is None:
            return
        confirmed = messagebox.askyesno(
            "Confirm delete", "Delete this expense? This cannot be undone.")
        if not confirmed:
            return  # cancel keeps the expense
        database.delete_expense(expense_id)
        self.refresh()  # keep the current filters
