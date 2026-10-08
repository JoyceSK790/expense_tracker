"""View Expenses screen.

Shows every expense in a table (ttk.Treeview), newest first.
The table is rebuilt from the database every time the screen
is opened, so new expenses appear immediately. Each row's
Treeview item id is the expense's database id, so Edit and
Delete always act on the right expense regardless of its
position in the table.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import database


class ViewExpensesScreen(ttk.Frame):
    """Table of all expenses with Edit, Delete and Back to Home."""

    COLUMNS = ("date", "category", "description", "amount")

    def __init__(self, parent, on_back, on_edit):
        super().__init__(parent, padding=20)
        self.on_back = on_back
        self.on_edit = on_edit

        ttk.Label(self, text="View Expenses",
                  font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

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
        self.tree.column("description", width=200, anchor="w")
        self.tree.column("amount", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        buttons = ttk.Frame(self)
        buttons.pack(pady=(15, 0))
        ttk.Button(buttons, text="Edit",
                   command=self.edit_selected).pack(side="left", padx=5)
        ttk.Button(buttons, text="Delete",
                   command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(buttons, text="Back to Home",
                   command=self.on_back).pack(side="left", padx=5)

    def refresh(self):
        """Reload all expenses from the database into the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in database.get_all_expenses():
            naira = database.kobo_to_naira(expense["amount_kobo"])
            # The Treeview item id IS the database id.
            self.tree.insert("", "end", iid=str(expense["id"]), values=(
                expense["date"],
                expense["category"],
                expense["description"],
                f"{naira:,.2f}",
            ))

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
        self.refresh()
