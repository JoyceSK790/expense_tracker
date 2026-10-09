"""Student Expense Tracker - application entry point.

Opens the main window on the Home screen. All four screens work:
Home, Add, View (with search, Edit/Delete) and Reports.
"""

import tkinter as tk
from tkinter import ttk

import database
from screens.home_screen import HomeScreen
from screens.add_expense_screen import AddExpenseScreen
from screens.view_expenses_screen import ViewExpensesScreen
from screens.reports_screen import ReportsScreen


def main():
    database.init_db()

    root = tk.Tk()
    root.title("Student Expense Tracker")
    root.geometry("720x450")

    def show_home():
        home_screen.refresh()
        add_screen.pack_forget()
        view_screen.pack_forget()
        reports_screen.pack_forget()
        home_screen.pack(expand=True)

    def show_add_screen():
        add_screen.start_add()
        home_screen.pack_forget()
        view_screen.pack_forget()
        reports_screen.pack_forget()
        add_screen.pack(fill="both", expand=True)

    def show_view_screen():
        view_screen.show_all()
        home_screen.pack_forget()
        add_screen.pack_forget()
        reports_screen.pack_forget()
        view_screen.pack(fill="both", expand=True)

    def show_reports_screen():
        reports_screen.refresh()
        home_screen.pack_forget()
        add_screen.pack_forget()
        view_screen.pack_forget()
        reports_screen.pack(fill="both", expand=True)

    def show_edit_screen(expense):
        add_screen.start_edit(expense)
        view_screen.pack_forget()
        add_screen.pack(fill="both", expand=True)

    home_screen = HomeScreen(root,
                             on_add=lambda: show_add_screen(),
                             on_view=lambda: show_view_screen(),
                             on_reports=lambda: show_reports_screen())
    add_screen = AddExpenseScreen(root, on_cancel=lambda: show_home(),
                                  on_edit_done=lambda: show_view_screen())
    view_screen = ViewExpensesScreen(root, on_back=lambda: show_home(),
                                     on_edit=show_edit_screen)
    reports_screen = ReportsScreen(root, on_back=lambda: show_home())

    show_home()

    root.mainloop()


if __name__ == "__main__":
    main()
