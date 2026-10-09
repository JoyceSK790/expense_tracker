"""Home screen.

Shows total spending and this month's spending, with buttons to
the other screens. Figures are reloaded from the database every
time the screen is shown.
"""

import tkinter as tk
from tkinter import ttk

import database


class HomeScreen(ttk.Frame):
    """App landing page: two totals and navigation buttons."""

    def __init__(self, parent, on_add, on_view, on_reports):
        super().__init__(parent, padding=20)
        self.on_add = on_add
        self.on_view = on_view
        self.on_reports = on_reports

        ttk.Label(self, text="Student Expense Tracker",
                  font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        self.total_var = tk.StringVar()
        self.month_var = tk.StringVar()

        summary = ttk.Frame(self)
        summary.pack(pady=(0, 20))
        ttk.Label(summary, text="Total spending:").grid(row=0, column=0,
                                                        sticky="w")
        ttk.Label(summary, textvariable=self.total_var,
                  font=("Helvetica", 12, "bold")).grid(
            row=0, column=1, sticky="e", padx=(15, 0))
        ttk.Label(summary, text="This month:").grid(row=1, column=0,
                                                    sticky="w")
        ttk.Label(summary, textvariable=self.month_var,
                  font=("Helvetica", 12, "bold")).grid(
            row=1, column=1, sticky="e", padx=(15, 0))

        ttk.Button(self, text="Add Expense",
                   command=self.on_add).pack(fill="x", pady=5)
        ttk.Button(self, text="View Expenses",
                   command=self.on_view).pack(fill="x", pady=5)
        ttk.Button(self, text="Reports",
                   command=self.on_reports).pack(fill="x", pady=5)

    def refresh(self):
        """Reload both figures from the database."""
        self.total_var.set(self.format_naira(database.get_total_spending()))
        self.month_var.set(self.format_naira(database.get_month_spending()))

    @staticmethod
    def format_naira(amount_kobo):
        """Format integer kobo as naira with thousands separator."""
        return f"{database.kobo_to_naira(amount_kobo):,.2f}"
