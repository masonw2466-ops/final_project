import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import unittest
from test_config import auto_tests_enabled


class Schedules:
    def __init__(self, root, member_mode=False, member_username=None, run_tests=True):
        self.root = root
        self.member_mode = member_mode
        self.member_username = member_username

        self.root.title("Class Schedules")
        self.root.geometry("600x500")

        self.conn = sqlite3.connect("class-schedule.db")
        self.cursor = self.conn.cursor()

        # Tables
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT NOT NULL,
                instructor TEXT NOT NULL,
                day TEXT NOT NULL,
                time TEXT NOT NULL,
                capacity INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER,
                member_username TEXT
            )
        """)

        self.conn.commit()

        mode = "member" if self.member_mode else "staff"

        if self.member_mode:
            self.build_member_view()
        else:
            self.build_staff_view()

        # auto-run tests when this screen is opened (but not from tests)
        if run_tests:
            run_schedules_tests_for_mode(mode)

    # Staff tools
    def build_staff_view(self):
        tk.Button(self.root, text="View All Classes", command=self.view_classes).pack(pady=10)
        tk.Button(self.root, text="Add Class", command=self.add_class).pack(pady=10)
        tk.Button(self.root, text="Edit Class", command=self.edit_class).pack(pady=10)
        tk.Button(self.root, text="Delete Class", command=self.delete_class).pack(pady=10)

    def view_classes(self):
        win = tk.Toplevel(self.root)
        win.title("Class List")

        tree = ttk.Treeview(win, columns=("name", "instr", "day", "time", "cap"), show="headings")
        for col, title in zip(("name", "instr", "day", "time", "cap"),
                              ("Class", "Instructor", "Day", "Time", "Capacity")):
            tree.heading(col, text=title)
        tree.pack(fill="both", expand=True)

        self.cursor.execute("SELECT class_name, instructor, day, time, capacity FROM schedules")
        for row in self.cursor.fetchall():
            tree.insert("", tk.END, values=row)

    def add_class(self):
        win = tk.Toplevel(self.root)
        win.title("Add Class")
        win.geometry("400x400")

        labels = ["Class Name", "Instructor", "Day", "Time", "Capacity"]
        entries = {}

        for label in labels:
            tk.Label(win, text=label).pack(pady=5)
            e = tk.Entry(win)
            e.pack(pady=5)
            entries[label] = e

        def save():
            data = [entries[l].get() for l in labels]
            if "" in data:
                messagebox.showerror("Error", "All fields required")
                return
            self.cursor.execute(
                "INSERT INTO schedules (class_name, instructor, day, time, capacity) VALUES (?, ?, ?, ?, ?)",
                data
            )
            self.conn.commit()
            win.destroy()

        tk.Button(win, text="Save Class", command=save).pack(pady=20)

    def edit_class(self):
        win = tk.Toplevel(self.root)
        win.title("Edit Class")
        win.geometry("400x450")

        tk.Label(win, text="Select Class").pack(pady=5)
        dropdown = ttk.Combobox(win)
        dropdown.pack(pady=5)

        self.cursor.execute("SELECT id, class_name FROM schedules")
        data = self.cursor.fetchall()
        dropdown["values"] = [f"{d[0]} - {d[1]}" for d in data]

        labels = ["Class Name", "Instructor", "Day", "Time", "Capacity"]
        entries = {l: tk.Entry(win) for l in labels}

        for l, entry in entries.items():
            tk.Label(win, text=l).pack(pady=5)
            entry.pack(pady=5)

        def load(event=None):
            class_id = dropdown.get().split(" - ")[0]
            self.cursor.execute(
                "SELECT class_name, instructor, day, time, capacity FROM schedules WHERE id=?",
                (class_id,)
            )
            vals = self.cursor.fetchone()
            if not vals:
                return
            for i, lab in enumerate(labels):
                entries[lab].delete(0, tk.END)
                entries[lab].insert(0, vals[i])
            win.class_id = class_id

        dropdown.bind("<<ComboboxSelected>>", load)

        def save():
            values = [entries[l].get() for l in labels]
            self.cursor.execute(
                "UPDATE schedules SET class_name=?, instructor=?, day=?, time=?, capacity=? WHERE id=?",
                (*values, win.class_id)
            )
            self.conn.commit()
            win.destroy()

        tk.Button(win, text="Save Changes", command=save).pack(pady=15)

    def delete_class(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Class")

        tk.Label(win, text="Select Class").pack(pady=10)
        dropdown = ttk.Combobox(win)
        dropdown.pack(pady=10)

        self.cursor.execute("SELECT id, class_name FROM schedules")
        data = self.cursor.fetchall()
        dropdown["values"] = [f"{d[0]} - {d[1]}" for d in data]

        def delete():
            class_id = dropdown.get().split(" - ")[0]
            self.cursor.execute("DELETE FROM schedules WHERE id=?", (class_id,))
            self.conn.commit()
            win.destroy()

        tk.Button(win, text="Delete", command=delete).pack(pady=20)

    # Member tools
    def build_member_view(self):
        tk.Label(self.root, text="Class Schedule", font=("Arial", 20)).pack(pady=15)

        tk.Button(self.root, text="Join a Class", command=self.member_join_class).pack(pady=10)
        tk.Button(self.root, text="Leave a Class", command=self.member_leave_class).pack(pady=10)
        tk.Button(self.root, text="View Schedule", command=self.member_view_schedule).pack(pady=10)

    def member_view_schedule(self):
        win = tk.Toplevel(self.root)
        win.title("Class Schedule")

        self.cursor.execute("""
            SELECT s.id, s.class_name, s.day, s.time, s.capacity,
            (SELECT COUNT(*) FROM enrollment WHERE class_id=s.id)
            FROM schedules s
        """)
        rows = self.cursor.fetchall()

        for cid, name, day, time, cap, count in rows:
            tk.Label(
                win,
                text=f"{name} — {day} @ {time}  ({count}/{cap} enrolled)",
                font=("Arial", 12),
                justify="left"
            ).pack(pady=4, anchor="w")

    def member_join_class(self):
        win = tk.Toplevel(self.root)
        win.title("Join Class")

        tk.Label(win, text="Choose Class").pack(pady=10)
        dropdown = ttk.Combobox(win)
        dropdown.pack(pady=10)

        self.cursor.execute("SELECT id, class_name FROM schedules")
        classes = self.cursor.fetchall()
        dropdown["values"] = [f"{c[0]} - {c[1]}" for c in classes]

        def join():
            class_id = dropdown.get().split(" - ")[0]

            # Check class capacity
            self.cursor.execute("SELECT capacity FROM schedules WHERE id=?", (class_id,))
            cap = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(*) FROM enrollment WHERE class_id=?", (class_id,))
            count = self.cursor.fetchone()[0]

            if count >= cap:
                messagebox.showerror("Full", "This class is full.")
                return

            # Member already enrolled in selected class
            self.cursor.execute(
                "SELECT 1 FROM enrollment WHERE class_id=? AND member_username=?",
                (class_id, self.member_username)
            )
            if self.cursor.fetchone():
                messagebox.showinfo("Already Enrolled", "You are already enrolled.")
                return

            self.cursor.execute(
                "INSERT INTO enrollment (class_id, member_username) VALUES (?, ?)",
                (class_id, self.member_username)
            )
            self.conn.commit()

            messagebox.showinfo("Success", "You joined the class!")
            win.destroy()

        tk.Button(win, text="Join", command=join).pack(pady=20)

    def member_leave_class(self):
        win = tk.Toplevel(self.root)
        win.title("Leave Class")

        tk.Label(win, text="Choose Class to Leave").pack(pady=10)
        dropdown = ttk.Combobox(win)
        dropdown.pack(pady=10)

        self.cursor.execute("""
            SELECT s.id, s.class_name
            FROM schedules s
            JOIN enrollment e ON e.class_id = s.id
            WHERE e.member_username=?
        """, (self.member_username,))
        data = self.cursor.fetchall()

        dropdown["values"] = [f"{d[0]} - {d[1]}" for d in data]

        def leave():
            class_id = dropdown.get().split(" - ")[0]
            self.cursor.execute(
                "DELETE FROM enrollment WHERE class_id=? AND member_username=?",
                (class_id, self.member_username)
            )
            self.conn.commit()

            messagebox.showinfo("Success", "You left the class.")
            win.destroy()

        tk.Button(win, text="Leave", command=leave).pack(pady=20)


# Tests

class TestSchedules(unittest.TestCase):
    def test_staff_view_title(self):
        root = tk.Tk()
        root.withdraw()
        Schedules(root, member_mode=False, run_tests=False)
        self.assertEqual(root.title(), "Class Schedules")
        root.destroy()

    def test_member_view_has_join_button(self):
        root = tk.Tk()
        root.withdraw()
        app = Schedules(root, member_mode=True, member_username="testuser", run_tests=False)

        button_texts = [
            w.cget("text")
            for w in app.root.winfo_children()
            if isinstance(w, tk.Button)
        ]
        self.assertIn("Join a Class", button_texts)
        root.destroy()


def run_schedules_tests_for_mode(mode: str):
    if not auto_tests_enabled():
        return

    loader = unittest.TestLoader()
    test_names = []

    if mode == "staff":
        test_names.append("schedules.TestSchedules.test_staff_view_title")
    elif mode == "member":
        test_names.append("schedules.TestSchedules.test_member_view_has_join_button")

    if not test_names:
        return

    suite = loader.loadTestsFromNames(test_names)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    root = tk.Tk()
    Schedules(root)
    root.mainloop()
