import tkinter as tk
import unittest

import login
from test_config import auto_tests_enabled


class Landing:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Manager")
        self.root.geometry("500x500")

        tk.Label(root, text="Welcome to the Gym Manager", font=("Arial", 20)).pack(pady=40)

        tk.Button(
            root,
            text="Staff Login",
            font=("Arial", 18),
            width=20,
            command=self.open_staff_login
        ).pack(pady=20)

        tk.Button(
            root,
            text="Member Login",
            font=("Arial", 18),
            width=20,
            command=self.open_member_login
        ).pack(pady=20)

    def open_staff_login(self):
        self.root.destroy()
        root = tk.Tk()
        login.Login(root, mode="staff")
        root.mainloop()

    def open_member_login(self):
        self.root.destroy()
        root = tk.Tk()
        login.Login(root, mode="member")
        root.mainloop()


# Tests

class TestLanding(unittest.TestCase):
    def test_title_is_gym_manager(self):
        root = tk.Tk()
        root.withdraw()  # hide test window
        Landing(root)
        self.assertEqual(root.title(), "Gym Manager")
        root.destroy()

    def test_has_staff_and_member_buttons(self):
        root = tk.Tk()
        root.withdraw()  # hide test window
        Landing(root)

        # grab all Button widgets and their text
        btn_texts = [
            w.cget("text")
            for w in root.winfo_children()
            if isinstance(w, tk.Button)
        ]

        self.assertIn("Staff Login", btn_texts)
        self.assertIn("Member Login", btn_texts)

        root.destroy()


def run_landing_tests():
    """Run Landing tests if global toggle is ON."""
    if not auto_tests_enabled():
        return

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLanding)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)




if __name__ == "__main__":
    # run tests automatically when app starts
    run_landing_tests()

    root = tk.Tk()
    Landing(root)
    root.mainloop()
