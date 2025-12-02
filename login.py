import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import main
import unittest
from test_config import auto_tests_enabled

# Override PIN to return to home screen (To prevent unauthorized members from messing with the system)
OVERRIDE_PIN = "0000"  


class Login:
    def __init__(self, root, mode="staff", run_tests=True):
        """
        mode: "staff" or "member"
        run_tests: True in normal app usage, False when a unittest
                   creates a Login instance (to avoid recursion).
        """
        self.root = root
        self.mode = mode
        self.root.geometry("500x500")

        # Databases
        self.staff_conn = sqlite3.connect("staff.db")
        self.staff_cursor = self.staff_conn.cursor()

        self.member_conn = sqlite3.connect("members.db")
        self.member_cursor = self.member_conn.cursor()

        # Set UI based on user mode
        if self.mode == "staff":
            self.build_staff_login()
        elif self.mode == "member":
            self.build_member_login()

        # auto-run tests for this mode (only in real app, not inside tests)
        if run_tests:
            run_login_tests_for_mode(self.mode)

    # Staff Login Mode
    def build_staff_login(self):
        self.root.title("Staff Login")

        tk.Label(self.root, text="Staff Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Enter Username").pack(pady=10)
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=10)

        tk.Label(self.root, text="Enter Password").pack(pady=10)
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack(pady=10)

        tk.Button(self.root, text="Login", command=self.check_staff_login).pack(pady=20)

        tk.Button(self.root, text="Return Home", command=self.return_home).pack(pady=10)

    # Member Login Mode (Check-in)
    def build_member_login(self):
        self.root.title("Member Check-In")

        tk.Label(self.root, text="Member Check-In", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Enter Member ID").pack(pady=10)
        self.entry_member_id = tk.Entry(self.root)
        self.entry_member_id.pack(pady=10)

        tk.Button(self.root, text="Check In", command=self.check_member_login).pack(pady=20)

        tk.Button(self.root, text="Return Home", command=self.return_home).pack(pady=10)

    # Staff Login
    def check_staff_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both fields.")
            return

        self.staff_cursor.execute(
            "SELECT role FROM staff WHERE username=? AND password=?",
            (username, password)
        )
        result = self.staff_cursor.fetchone()

        if result:
            role = result[0]
            messagebox.showinfo("Success", f"Welcome {role}!")

            # Load the staff dashboard
            from main_page import GymInterface
            self.root.destroy()
            root = tk.Tk()
            GymInterface(root, role)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    # Member Login
    def check_member_login(self):
        member_id = self.entry_member_id.get().strip()

        if not member_id:
            messagebox.showerror("Error", "Please enter a member ID")
            return

        self.member_cursor.execute(
            "SELECT name FROM members WHERE id=?",
            (member_id,)
        )
        result = self.member_cursor.fetchone()

        if result:
            member_name = result[0]

            messagebox.showinfo("Check-In Successful", f"Welcome, {member_name}!")

            self.root.destroy()

            root = tk.Tk()
            from main_page import GymInterface
            GymInterface(root, member_name=member_name, member_username=member_id)
            root.mainloop()

        else:
            messagebox.showerror("Error", "Member not found.")

    # Return Home (Override PIN: 0000)
    def return_home(self):
        pin = simpledialog.askstring("PIN Required", "Enter override PIN:", show="*")
        if pin == OVERRIDE_PIN:
            self.root.destroy()
            root = tk.Tk()
            main.Landing(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect PIN!")


# Tests

class TestLogin(unittest.TestCase):
    def test_staff_mode_sets_title(self):
        root = tk.Tk()
        root.withdraw()  # hide test window
        Login(root, mode="staff", run_tests=False)
        self.assertEqual(root.title(), "Staff Login")
        root.destroy()

    def test_member_mode_sets_title(self):
        root = tk.Tk()
        root.withdraw()  # hide test window
        Login(root, mode="member", run_tests=False)
        self.assertEqual(root.title(), "Member Check-In")
        root.destroy()


def run_login_tests_for_mode(mode: str):
    """
    Run only the login tests relevant to the current mode.
    Called automatically from Login.__init__.
    """
    if not auto_tests_enabled():
        return

    loader = unittest.TestLoader()
    test_names = []

    if mode == "staff":
        test_names.append("login.TestLogin.test_staff_mode_sets_title")
    elif mode == "member":
        test_names.append("login.TestLogin.test_member_mode_sets_title")

    if not test_names:
        return

    suite = loader.loadTestsFromNames(test_names)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

