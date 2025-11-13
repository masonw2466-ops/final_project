import tkinter as tk
from tkinter import messagebox

class Members:
    def __init__(self, root):
        self.root = root
        self.root.title("Members")
        self.root.geometry("500x500")

        self.button_add = tk.Button(root, text="Add Member", command=self.add_member)
        self.button_add.pack(pady=10)

        self.button_edit = tk.Button(root, text="Edit Member", command=self.edit_member)
        self.button_edit.pack(pady=10)

        self.button_remove = tk.Button(root, text="Remove Member", command=self.remove_member)
        self.button_remove.pack(pady=10)


    def add_member(self):
        AddWindow(self)

    def edit_member(self):
        pass

    def remove_member(self):
        pass


class AddWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Add Member")
        self.win.geometry("300x200")

        tk.Label(self.win, text="Enter Member name:").pack(pady=10)
        self.entry_name = tk.Entry(self.win)
        self.entry_name.pack(pady=5)

        tk.Label(self.win, text="Enter Member phone").pack(pady=10)
        self.entry_phone = tk.Entry(self.win)
        self.entry_phone.pack(pady=10)

        tk.Label(self.win, text="Enter Member email").pack(pady=10)
        self.entry_email = tk.Entry(self.win)
        self.entry_email.pack(pady=10)

        tk.Label(self.win, text="Enter Membership Type").pack(pady=10)
        # Find some sort of selector for this option

        tk.Button(self.win, text="Save",
                  command=self.save_member).pack(pady=5)
        tk.Button(self.win, text="Close",
                  command=self.win.destroy).pack(pady=5)

    def save_member(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Members(root)
    root.mainloop()