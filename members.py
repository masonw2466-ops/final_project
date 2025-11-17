import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Members:
    def __init__(self, root):
        self.root = root
        self.root.title("Members")
        self.root.geometry("500x500")

        self.conn = sqlite3.connect("members.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                membership TEXT NOT NULL
            )
        """)
        self.conn.commit()

        self.button_add = tk.Button(root, text="Add Member", command=self.add_member)
        self.button_add.pack(pady=10)

        self.button_edit = tk.Button(root, text="Edit Member", command=self.edit_member)
        self.button_edit.pack(pady=10)

        self.button_remove = tk.Button(root, text="Remove Member", command=self.remove_member)
        self.button_remove.pack(pady=10)

        self.button_close = tk.Button(root, text="Close", command=self.close)
        self.button_close.pack(pady=10)


    def add_member(self):
        AddWindow(self)

    def edit_member(self):
        EditWindow(self)

    def remove_member(self):
        RemoveWindow(self)

    def close(self):
        self.root.destroy()


class AddWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Add Member")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Enter Member name:").pack(pady=10)
        self.entry_name = tk.Entry(self.win)
        self.entry_name.pack(pady=5)

        tk.Label(self.win, text="Enter Member phone").pack(pady=10)
        self.entry_phone = tk.Entry(self.win)
        self.entry_phone.pack(pady=10)

        tk.Label(self.win, text="Enter Member email").pack(pady=10)
        self.entry_email = tk.Entry(self.win)
        self.entry_email.pack(pady=10)

        tk.Label(self.win, text="Select Membership Type").pack(pady=10)
        self.membership_type = ttk.Combobox(
            self.win,
            values=["Basic", "Premium", "VIP", "Student", "Family"]
        )
        self.membership_type.pack(pady=5)
        # Find some sort of selector for this option

        tk.Button(self.win, text="Save",
                  command=self.save_member).pack(pady=5)
        tk.Button(self.win, text="Close",
                  command=self.win.destroy).pack(pady=5)

    def save_member(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        membership = self.membership_type.get()

        if not name or not phone or not email or not membership:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # For testing, just show the data (later you save to DB)
        messagebox.showinfo(
            "Member Saved",
            f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMembership: {membership}"
        )
        conn = self.main_app.conn
        cursor = self.main_app.cursor
        cursor.execute(
            "INSERT INTO members (name, phone, email, membership) VALUES (?, ?, ?, ?)",
            (name, phone, email, membership)
        )
        conn.commit()
        self.win.destroy()

class EditWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Edit Member")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Select Member to Edit:").pack(pady=10)

        # Dropdown list
        self.member_dropdown = ttk.Combobox(self.win)
        self.member_dropdown.pack(pady=5)

        # Load member list from DB
        self.load_member_list()

        # When selecting a member → load into input fields
        self.member_dropdown.bind("<<ComboboxSelected>>", self.load_member_data)

        # Editable fields
        tk.Label(self.win, text="Name").pack(pady=5)
        self.entry_name = tk.Entry(self.win)
        self.entry_name.pack()

        tk.Label(self.win, text="Phone").pack(pady=5)
        self.entry_phone = tk.Entry(self.win)
        self.entry_phone.pack()

        tk.Label(self.win, text="Email").pack(pady=5)
        self.entry_email = tk.Entry(self.win)
        self.entry_email.pack()

        tk.Label(self.win, text="Membership Type").pack(pady=5)
        self.membership_type = ttk.Combobox(
            self.win,
            values=["Basic", "Premium", "VIP", "Student", "Family"]
        )
        self.membership_type.pack()

        # Save Button
        tk.Button(self.win, text="Save Changes",
                  command=self.save_changes).pack(pady=15)

    def load_member_list(self):
        cursor = self.main_app.cursor
        cursor.execute("SELECT id, name, membership FROM members")
        rows = cursor.fetchall()

        # Format:  "1 - John Smith (Premium)"
        formatted = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
        self.member_dropdown["values"] = formatted

    def load_member_data(self, event=None):
        selected = self.member_dropdown.get()
        member_id = selected.split(" - ")[0]

        cursor = self.main_app.cursor
        cursor.execute("SELECT name, phone, email, membership FROM members WHERE id=?", (member_id,))
        data = cursor.fetchone()

        if data:
            self.current_id = member_id
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.membership_type.set("")

            self.entry_name.insert(0, data[0])
            self.entry_phone.insert(0, data[1])
            self.entry_email.insert(0, data[2])
            self.membership_type.set(data[3])

    def save_changes(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        membership = self.membership_type.get()

        cursor = self.main_app.cursor
        cursor.execute("""
            UPDATE members
            SET name=?, phone=?, email=?, membership=?
            WHERE id=?
        """, (name, phone, email, membership, self.current_id))

        self.main_app.conn.commit()
        messagebox.showinfo("Success", "Member updated successfully!")
        self.win.destroy()

class RemoveWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Remove Member")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Select Member to Remove:").pack(pady=10)

        # Dropdown list
        self.member_dropdown = ttk.Combobox(self.win)
        self.member_dropdown.pack(pady=5)

        # Load member list from DB
        self.load_member_list()

        # Remove button
        tk.Button(self.win, text="Remove Member", command=self.remove_member).pack(pady=10)

    def load_member_list(self):
        cursor = self.main_app.cursor
        cursor.execute("SELECT id, name, membership FROM members")
        rows = cursor.fetchall()
        formatted = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
        self.member_dropdown["values"] = formatted

    def remove_member(self):
        selected = self.member_dropdown.get()
        if not selected:
            messagebox.showerror("Error", "Please select a member to remove.")
            return
        member_id = selected.split(" - ")[0]
        cursor = self.main_app.cursor
        cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
        self.main_app.conn.commit()
        messagebox.showinfo("Success", "Member removed successfully!")
        self.win.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Members(root)
    root.mainloop()