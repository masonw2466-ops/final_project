import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Staff:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff")
        self.root.geometry("500x500")

        self.conn = sqlite3.connect("staff.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

        self.button_add = tk.Button(root, text="Add Staff", command=self.add_staff)
        self.button_add.pack(pady=10)

        self.button_edit = tk.Button(root, text="Edit Staff", command=self.edit_staff)
        self.button_edit.pack(pady=10)

        self.button_remove = tk.Button(root, text="Remove Staff", command=self.remove_staff)
        self.button_remove.pack(pady=10)

        self.button_close = tk.Button(root, text="Close", command=self.close)
        self.button_close.pack(pady=10)


    def add_staff(self):
        AddWindow(self)

    def edit_staff(self):
        EditWindow(self)

    def remove_staff(self):
        RemoveWindow(self)

    def close(self):
        self.root.destroy()


class AddWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Add Staff")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Enter Staff name:").pack(pady=5)
        self.entry_name = tk.Entry(self.win)
        self.entry_name.pack(pady=5)

        tk.Label(self.win, text="Enter Staff phone").pack(pady=5)
        self.entry_phone = tk.Entry(self.win)
        self.entry_phone.pack(pady=10)

        tk.Label(self.win, text="Enter Staff email").pack(pady=5)
        self.entry_email = tk.Entry(self.win)
        self.entry_email.pack(pady=10)

        tk.Label(self.win, text="Enter Staff username").pack(pady=5)
        self.entry_username = tk.Entry(self.win)
        self.entry_username.pack(pady=10)

        tk.Label(self.win, text="Enter Staff password").pack(pady=5)
        self.entry_password = tk.Entry(self.win, show="*")
        self.entry_password.pack(pady=10)

        tk.Label(self.win, text="Select Staff Role").pack(pady=5)
        self.role = ttk.Combobox(
            self.win,
            values=["Employee", "Manager"]
        )
        self.role.pack(pady=5)
        # Find some sort of selector for this option

        tk.Button(self.win, text="Save",
                  command=self.save_staff).pack(pady=5)
        tk.Button(self.win, text="Close",
                  command=self.win.destroy).pack(pady=5)

    def save_staff(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        username = self.entry_username.get()
        role = self.role.get()
        password = self.entry_password.get()

        if not name or not phone or not email or not username or not role or not password:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # For testing, just show the data (later you save to DB)
        messagebox.showinfo(
            "Staff Saved",
            f"Name: {name}\nPhone: {phone}\nEmail: {email}\nRole: {role}"
        )
        conn = self.main_app.conn
        cursor = self.main_app.cursor
        cursor.execute(
            "INSERT INTO staff (name, phone, email, role, username, password) VALUES (?, ?, ?, ?, ?, ?)",
            (name, phone, email, role, username, password)
        )
        conn.commit()
        self.win.destroy()

class EditWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Edit Staff")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Select Staff to Edit:").pack(pady=10)

        # Dropdown list
        self.staff_dropdown = ttk.Combobox(self.win)
        self.staff_dropdown.pack(pady=5)

        # Load member list from DB
        self.load_staff_list()

        # When selecting a member → load into input fields
        self.staff_dropdown.bind("<<ComboboxSelected>>", self.load_staff_data)

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

        tk.Label(self.win, text="Username").pack(pady=5)
        self.entry_username = tk.Entry(self.win)
        self.entry_username.pack()

        tk.Label(self.win, text="Password").pack(pady=5)
        self.entry_password = tk.Entry(self.win, show="*")
        self.entry_password.pack()

        tk.Label(self.win, text="Role").pack(pady=5)
        self.staff_type = ttk.Combobox(
            self.win,
            values=["Employee", "Manager"]
        )
        self.staff_type.pack()

        # Save Button
        tk.Button(self.win, text="Save Changes",
                  command=self.save_changes).pack(pady=15)

    def load_staff_list(self):
        cursor = self.main_app.cursor
        cursor.execute("SELECT id, name, role FROM staff")
        rows = cursor.fetchall()

        # Format:  "1 - John Smith (Premium)"
        formatted = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
        self.staff_dropdown["values"] = formatted

    def load_staff_data(self, event=None):
        selected = self.staff_dropdown.get()
        staff_id = selected.split(" - ")[0]

        cursor = self.main_app.cursor
        cursor.execute("SELECT name, phone, email, role, username, password FROM staff WHERE id=?", (staff_id,))
        data = cursor.fetchone()

        if data:
            self.current_id = staff_id
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.staff_type.set("")

            self.entry_name.insert(0, data[0])
            self.entry_phone.insert(0, data[1])
            self.entry_email.insert(0, data[2])
            self.staff_type.set(data[3])
            self.entry_username.delete(0, tk.END)
            self.entry_username.insert(0, data[4])
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, data[5])

    def save_changes(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        role = self.staff_type.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor = self.main_app.cursor
        cursor.execute("""
            UPDATE staff
            SET name=?, phone=?, email=?, role=?, username=?, password=?
            WHERE id=?
        """, (name, phone, email, role, username, password, self.current_id))

        self.main_app.conn.commit()
        messagebox.showinfo("Success", "Staff updated successfully!")
        self.win.destroy()

class RemoveWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Remove Member")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Select Member to Remove:").pack(pady=10)

        # Dropdown list
        self.staff_dropdown = ttk.Combobox(self.win)
        self.staff_dropdown.pack(pady=5)

        # Load member list from DB
        self.load_staff_list()

        # Remove button
        tk.Button(self.win, text="Remove Member", command=self.remove_staff).pack(pady=10)

    def load_staff_list(self):
        cursor = self.main_app.cursor
        cursor.execute("SELECT id, name, role FROM staff")
        rows = cursor.fetchall()
        formatted = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
        self.staff_dropdown["values"] = formatted

    def remove_staff(self):
        selected = self.staff_dropdown.get()
        if not selected:
            messagebox.showerror("Error", "Please select a member to remove.")
            return
        staff_id = selected.split(" - ")[0]
        cursor = self.main_app.cursor
        cursor.execute("DELETE FROM staff WHERE id=?", (staff_id,))
        self.main_app.conn.commit()
        messagebox.showinfo("Success", "Member removed successfully!")
        self.win.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Staff(root)
    root.mainloop()