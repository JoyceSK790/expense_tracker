"""View Expenses screen.

Shows every expense in a table (ttk.Treeview), newest first.
The table is rebuilt from the database every time the screen
is opened, so new expenses appear immediately. Edit and Delete
are added in a later stage.
"""

import tkinter as tk
from tkinter import ttk

import database


class ViewExpensesScreen(ttk.Frame):
    """Table of all expenses with a Back to Home button."""

    COLUMNS = ("date", "category", "description", "amount")

    def __init__(self, parent, on_back):
        super().__init__(parent, padding=20)
        self.on_back = on_back

        ttk.Label(self, text="View Expenses",
                  font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=self.COLUMNS,
                                 show="headings")
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

        ttk.Button(self, text="Back to Home",
                   command=self.on_back).pack(pady=(15, 0))

    def refresh(self):
        """Reload all expenses from the database into the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in database.get_all_expenses():
            naira = database.kobo_to_naira(expense["amount_kobo"])
            self.tree.insert("", "end", values=(
                expense["date"],
                expense["category"],
                expense["description"],
                f"{naira:,.2f}",
            ))
