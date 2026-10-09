"""Reports screen.

Shows spending totals: all-time total, current month, and a
per-category breakdown. Numbers only, no charts. All figures are
reloaded from the database every time the screen is opened.
"""

import tkinter as tk
from tkinter import ttk

import database


class ReportsScreen(ttk.Frame):
    """Summary figures with a Back to Home button."""

    def __init__(self, parent, on_back):
        super().__init__(parent, padding=20)
        self.on_back = on_back

        ttk.Label(self, text="Reports",
                  font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        self.total_var = tk.StringVar()
        self.month_var = tk.StringVar()

        summary = ttk.Frame(self)
        summary.pack(fill="x", pady=(0, 15))
        ttk.Label(summary, text="Total spending:").grid(row=0, column=0,
                                                        sticky="w")
        ttk.Label(summary, textvariable=self.total_var,
                  font=("Helvetica", 11, "bold")).grid(row=0, column=1,
                                                     sticky="e", padx=(10, 0))
        ttk.Label(summary, text="This month:").grid(row=1, column=0,
                                                    sticky="w")
        ttk.Label(summary, textvariable=self.month_var,
                  font=("Helvetica", 11, "bold")).grid(row=1, column=1,
                                                     sticky="e", padx=(10, 0))
        summary.columnconfigure(1, weight=1)

        ttk.Label(self, text="Total per category:",
                  font=("Helvetica", 11, "bold")).pack(anchor="w")

        self.category_list = tk.Text(self, height=10, width=40,
                                     state="disabled", relief="flat",
                                     borderwidth=0)
        self.category_list.pack(fill="both", expand=True, pady=(5, 15))

        ttk.Button(self, text="Back to Home",
                   command=self.on_back).pack()

    def refresh(self):
        """Reload all figures from the database."""
        self.total_var.set(self.format_naira(database.get_total_spending()))
        self.month_var.set(self.format_naira(database.get_month_spending()))

        totals = database.get_totals_by_category()
        self.category_list.configure(state="normal")
        self.category_list.delete("1.0", "end")
        if totals:
            for category, total_kobo in totals:
                line = f"{category:<24}{self.format_naira(total_kobo):>14}\n"
                self.category_list.insert("end", line)
        else:
            self.category_list.insert(
                "end", "No expenses yet. Add some to see totals here.")
        self.category_list.configure(state="disabled")

    @staticmethod
    def format_naira(amount_kobo):
        """Format integer kobo as naira with thousands separator."""
        return f"{database.kobo_to_naira(amount_kobo):,.2f}"
