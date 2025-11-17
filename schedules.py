import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Schedules:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedules")
        self.root.geometry("500x500")

        self.button_schedules = tk.Button(root, text="View Class Schedules", command=self.view_schedules)
        self.button_schedules.pack(pady=10)

        self.button_edit = tk.Button(root, text="Edit Schedules", command=self.edit_schedules)
        self.button_edit.pack(pady=10)

    def view_schedules(self):
        pass

    def edit_schedules(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Schedules(root)
    root.mainloop()