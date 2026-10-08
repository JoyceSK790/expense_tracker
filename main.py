"""Student Expense Tracker - application entry point.

Opens the main window. Add, View (with Edit/Delete) work;
Reports is wired up in a later stage.
"""

import tkinter as tk
from tkinter import ttk

import database
from screens.add_expense_screen import AddExpenseScreen
from screens.view_expenses_screen import ViewExpensesScreen


def main():
    database.init_db()

    root = tk.Tk()
    root.title("Student Expense Tracker")
    root.geometry("600x400")

    home = ttk.Frame(root, padding=20)
    home.pack(expand=True)

    ttk.Label(home, text="Student Expense Tracker",
              font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

    def show_home():
        add_screen.pack_forget()
        view_screen.pack_forget()
        home.pack(expand=True)

    def show_add_screen():
        add_screen.start_add()
        view_screen.pack_forget()
        home.pack_forget()
        add_screen.pack(fill="both", expand=True)

    def show_view_screen():
        view_screen.refresh()
        add_screen.pack_forget()
        home.pack_forget()
        view_screen.pack(fill="both", expand=True)

    def show_edit_screen(expense):
        add_screen.start_edit(expense)
        view_screen.pack_forget()
        add_screen.pack(fill="both", expand=True)

    add_screen = AddExpenseScreen(root, on_cancel=lambda: show_home(),
                                  on_edit_done=lambda: show_view_screen())
    view_screen = ViewExpensesScreen(root, on_back=lambda: show_home(),
                                     on_edit=show_edit_screen)

    ttk.Button(home, text="Add Expense",
               command=show_add_screen).pack(fill="x", pady=5)
    ttk.Button(home, text="View Expenses",
               command=show_view_screen).pack(fill="x", pady=5)
    ttk.Button(home, text="Reports",
               command=lambda: print("Reports - coming soon")).pack(fill="x", pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
