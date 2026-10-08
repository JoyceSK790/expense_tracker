"""Student Expense Tracker - application entry point (Stage 1).

Opens the main window with navigation buttons.
Screen swapping and the database are added in later stages.
"""

import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title("Student Expense Tracker")
    root.geometry("400x250")

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)

    ttk.Label(frame, text="Student Expense Tracker",
              font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

    ttk.Button(frame, text="Add Expense",
               command=lambda: print("Add Expense - coming soon")).pack(fill="x", pady=5)
    ttk.Button(frame, text="View Expenses",
               command=lambda: print("View Expenses - coming soon")).pack(fill="x", pady=5)
    ttk.Button(frame, text="Reports",
               command=lambda: print("Reports - coming soon")).pack(fill="x", pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
