import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import main
import sqlite3
import unittest
from test_config import auto_tests_enabled


class GymInterface:
    def __init__(self, root, staff_status=None, member_name=None, member_username=None, run_tests=True):
        self.root = root
        self.staff_status = staff_status
        self.member_name = member_name
        self.member_username = member_username
        self.timeout_id = None

        self.root.geometry("500x500")

        mode = None
        if self.staff_status is not None:
            self.build_staff_dashboard()
            mode = "staff"
        elif self.member_name is not None:
            self.build_member_dashboard()
            mode = "member"

        if run_tests and mode is not None:
            run_gyminterface_tests_for_mode(mode)

    def build_staff_dashboard(self):
        self.root.title("Staff Dashboard")

        tk.Label(self.root, text=f"Welcome, {self.staff_status}", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Manage Members", width=20, command=self.edit_member).pack(pady=10)
        tk.Button(self.root, text="Manage Class Schedules", width=20, command=self.class_schedule).pack(pady=10)
        tk.Button(self.root, text="Maintenance Logs", width=20, command=self.maintenance_logs).pack(pady=10)

        if self.staff_status == "Manager":
            tk.Button(self.root, text="Manage Staff", width=20, command=self.manage_staff).pack(pady=10)

        tk.Button(self.root, text="Logout", width=20, command=self.logout).pack(pady=20)

    def build_member_dashboard(self):
        self.root.title("Member Dashboard")

        tk.Label(self.root, text=f"Welcome, {self.member_name}!", font=("Arial", 24)).pack(pady=25)
        tk.Label(self.root, text="You are checked in. Enjoy your workout!", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="View My Membership Info", command=self.open_membership_info).pack(pady=15)
        tk.Button(self.root, text="Change Membership", command=self.change_membership).pack(pady=15)
        tk.Button(self.root, text="View Class Schedule", command=self.open_class_schedule_view).pack(pady=15)

        tk.Button(self.root, text="Logout", width=20, command=self.logout).pack(pady=20)

        self.start_timeout()

    def cancel_timeout(self):
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)
            self.timeout_id = None

    def start_timeout(self):
        self.cancel_timeout()
        self.timeout_id = self.root.after(7000, self.member_timeout)

    def open_membership_info(self):
        self.cancel_timeout()

        conn = sqlite3.connect("members.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT membership, email, phone FROM members WHERE name=?",
            (self.member_name,)
        )
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "Membership data not found.")
            self.start_timeout()
            return

        membership, email, phone = result

        messagebox.showinfo(
            "Membership Info",
            f"Name: {self.member_name}\n"
            f"Membership: {membership}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Renewal Date: 12/31/2025\n"
        )

        self.start_timeout()

    def open_class_schedule_view(self):
        self.cancel_timeout()

        win = tk.Toplevel(self.root)
        import schedules
        schedules.Schedules(
            win,
            member_mode=True,
            member_username=self.member_username
        )

        win.protocol("WM_DELETE_WINDOW", lambda: (win.destroy(), self.start_timeout()))

    def change_membership(self):
        self.cancel_timeout()
        EditMembershipWindow(self)

    def member_timeout(self):
        try:
            self.root.destroy()
        except:
            pass
        from login import Login
        new = tk.Tk()
        Login(new, mode="member")
        new.mainloop()

    def edit_member(self):
        import members
        new = tk.Toplevel(self.root)
        members.Members(new)

    def class_schedule(self):
        import schedules
        new = tk.Toplevel(self.root)
        schedules.Schedules(new)

    def maintenance_logs(self):
        new = tk.Toplevel(self.root)
        MaintenanceLogsWindow(new, self.staff_status)

    def manage_staff(self):
        import staff
        new = tk.Toplevel(self.root)
        staff.Staff(new)

    def logout(self):
        messagebox.showinfo("Logout Successful", "Logout Successful")
        self.root.destroy()
        root = tk.Tk()
        main.Landing(root)
        root.mainloop()


class EditMembershipWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Edit Membership")
        self.win.geometry("500x700")

        tk.Label(self.win, text="Membership options").pack(pady=10)

        tk.Label(self.win, text="Membership Type").pack(pady=5)
        self.membership_type = ttk.Combobox(
            self.win,
            values=["Basic", "Premium", "VIP", "Student", "Family"]
        )
        self.membership_type.pack()

        tk.Button(self.win, text="Save Changes", command=self.save_changes).pack(pady=15)

    def save_changes(self):
        new_membership = self.membership_type.get()

        if not new_membership:
            messagebox.showerror("Error", "Please select a membership type.")
            return

        conn = sqlite3.connect("members.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE members SET membership=? WHERE id=?",
            (new_membership, self.main_app.member_username)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Membership type updated!")
        self.win.destroy()
        self.main_app.start_timeout()


class MaintenanceLogsWindow:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.root.title("Maintenance Logs")
        self.root.geometry("800x350")

        conn = sqlite3.connect("maintenance.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment TEXT,
                issue TEXT,
                resolved INTEGER,
                notes TEXT
            )
        """)
        conn.commit()
        conn.close()

        self.tree = ttk.Treeview(self.root, columns=("equip", "issue", "resolved", "notes"), show="headings")
        self.tree.heading("equip", text="Equipment")
        self.tree.heading("issue", text="Issue")
        self.tree.heading("resolved", text="Resolved")
        self.tree.heading("notes", text="Notes")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Log", command=self.add_log).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Log", command=self.edit_log).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Mark Resolved", command=self.mark_resolved).grid(row=0, column=2, padx=5)

        if self.role == "Manager":
            tk.Button(btn_frame, text="Delete Log", command=self.delete_log).grid(row=0, column=3, padx=5)

        self.load_logs()

    def load_logs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("maintenance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, equipment, issue, resolved, notes FROM logs")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            resolved_text = "Yes" if r[3] == 1 else "No"
            self.tree.insert("", tk.END, iid=r[0], values=(r[1], r[2], resolved_text, r[4]))

    def add_log(self):
        LogEditor(self, mode="add")

    def edit_log(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a log to edit.")
            return
        LogEditor(self, mode="edit", log_id=selected)

    def mark_resolved(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a log.")
            return

        conn = sqlite3.connect("maintenance.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE logs SET resolved=1 WHERE id=?", (selected,))
        conn.commit()
        conn.close()

        self.load_logs()

    def delete_log(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a log.")
            return

        conn = sqlite3.connect("maintenance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logs WHERE id=?", (selected,))
        conn.commit()
        conn.close()

        self.load_logs()


class LogEditor:
    def __init__(self, parent, mode, log_id=None):
        self.parent = parent
        self.mode = mode
        self.log_id = log_id

        self.win = tk.Toplevel(parent.root)
        self.win.title("Edit Log" if mode == "edit" else "Add Log")
        self.win.geometry("400x300")

        tk.Label(self.win, text="Equipment").pack()
        self.entry_equipment = tk.Entry(self.win)
        self.entry_equipment.pack()

        tk.Label(self.win, text="Issue").pack()
        self.entry_issue = tk.Entry(self.win)
        self.entry_issue.pack()

        tk.Label(self.win, text="Notes").pack()
        self.entry_notes = tk.Entry(self.win)
        self.entry_notes.pack()

        if mode == "edit":
            conn = sqlite3.connect("maintenance.db")
            cursor = conn.cursor()
            cursor.execute("SELECT equipment, issue, notes FROM logs WHERE id=?", (log_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                self.entry_equipment.insert(0, row[0])
                self.entry_issue.insert(0, row[1])
                self.entry_notes.insert(0, row[2])

        tk.Button(self.win, text="Save", command=self.save).pack(pady=10)

    def save(self):
        equip = self.entry_equipment.get().strip()
        issue = self.entry_issue.get().strip()
        notes = self.entry_notes.get().strip()

        if self.mode == "add":
            conn = sqlite3.connect("maintenance.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (equipment, issue, resolved, notes) VALUES (?, ?, 0, ?)",
                           (equip, issue, notes))
            conn.commit()
            conn.close()

        else:
            conn = sqlite3.connect("maintenance.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE logs SET equipment=?, issue=?, notes=? WHERE id=?",
                           (equip, issue, notes, self.log_id))
            conn.commit()
            conn.close()

        self.win.destroy()
        self.parent.load_logs()


class TestGymInterface(unittest.TestCase):
    def test_staff_dashboard_title(self):
        root = tk.Tk()
        root.withdraw()
        GymInterface(root, staff_status="Employee", run_tests=False)
        self.assertEqual(root.title(), "Staff Dashboard")
        root.destroy()

    def test_member_dashboard_title(self):
        root = tk.Tk()
        root.withdraw()
        GymInterface(root, member_name="John Doe", member_username="1", run_tests=False)
        self.assertEqual(root.title(), "Member Dashboard")
        root.destroy()


def run_gyminterface_tests_for_mode(mode: str):
    if not auto_tests_enabled():
        return

    loader = unittest.TestLoader()
    test_names = []

    if mode == "staff":
        test_names.append("main_page.TestGymInterface.test_staff_dashboard_title")
    elif mode == "member":
        test_names.append("main_page.TestGymInterface.test_member_dashboard_title")

    if not test_names:
        return

    suite = loader.loadTestsFromNames(test_names)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    root = tk.Tk()
    GymInterface(root, staff_status="Employee")
    root.mainloop()
