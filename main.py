"""Student Expense Tracker - application entry point (Stage 1).

Opens the main window with navigation buttons.
Screen swapping and the database are added in later stages.
"""

import tkinter as tk
from tkinter import ttk

import database
from screens.add_expense_screen import AddExpenseScreen


def main():
    database.init_db()

    root = tk.Tk()
    root.title("Student Expense Tracker")
    root.geometry("400x350")

    home = ttk.Frame(root, padding=20)
    home.pack(expand=True)

    ttk.Label(home, text="Student Expense Tracker",
              font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

    add_screen = AddExpenseScreen(root, on_cancel=lambda: show_home())

    def show_add_screen():
        home.pack_forget()
        add_screen.pack(fill="both", expand=True)

    def show_home():
        add_screen.pack_forget()
        home.pack(expand=True)

    ttk.Button(home, text="Add Expense",
               command=show_add_screen).pack(fill="x", pady=5)
    ttk.Button(home, text="View Expenses",
               command=lambda: print("View Expenses - coming soon")).pack(fill="x", pady=5)
    ttk.Button(home, text="Reports",
               command=lambda: print("Reports - coming soon")).pack(fill="x", pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
