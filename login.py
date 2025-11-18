import tkinter as tk
from tkinter import messagebox
import sqlite3

staff_status = None  

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x500")

        self.staff_conn = sqlite3.connect("staff.db")
        self.staff_cursor = self.staff_conn.cursor()

        self.member_conn = sqlite3.connect("members.db")
        self.member_cursor = self.member_conn.cursor()

        # Adds the prompt asking for ID
        self.label_prompt_id = tk.Label(root, text="Enter Username or ID")
        self.label_prompt_id.pack(pady=10)

        # Adds the box to place ID
        self.entry_id = tk.Entry(root)
        self.entry_id.pack(pady=10)

        # Adds prompt asking for passcode
        self.label_prompt_passcode = tk.Label(root, text="Enter Passcode")
        self.label_prompt_passcode.pack(pady=10)
        
        # Place passcode here
        self.entry_passcode = tk.Entry(root)
        self.entry_passcode.pack(pady=10)

        # Submits informaiton and calls a checker
        self.button_submit = tk.Button(root, text="Submit", command=self.check_login)
        self.button_submit.pack(pady=10)

        # Left empty to start but will display message if done wrong
        self.label_output = tk.Label(root, text="")
        self.label_output.pack(pady=10)

    def check_login(self):
        global staff_status

        username = self.entry_id.get().strip()
        password = self.entry_passcode.get().strip()

        if username == "" or password == "":
            self.label_output.config(text="Please enter both ID and password.", fg="red")
            return

        # Check staff database
        try:
            self.staff_cursor.execute(
                "SELECT role FROM staff WHERE username=? AND password=?",
                (username, password)
            )
            staff_result = self.staff_cursor.fetchone()
        except Exception as e:
            self.label_output.config(text=f"Staff DB error: {e}", fg="red")
            return

        if staff_result:
            staff_status = staff_result[0]
            messagebox.showinfo("Login Successful", f"Welcome {staff_status}!")
            self.root.destroy()

            import main_page
            root = tk.Tk()
            main_page.GymInterface(root, staff_status)
            root.mainloop()
            return

        # Check member database
        try:
            self.member_cursor.execute(
                "SELECT name FROM members WHERE username=? AND password=?",
                (username, password)
            )
            member_result = self.member_cursor.fetchone()
        except Exception as e:
            self.label_output.config(text=f"Member DB error: {e}", fg="red")
            return

        if member_result:
            member_name = member_result[0]
            messagebox.showinfo("Login Successful", f"Welcome {member_name}!")
            self.root.destroy()

            # Placeholder for member portal
            messagebox.showinfo("Member Page", "Member login successful. Member portal not yet implemented.")
            return

        self.label_output.config(text="Invalid ID or password", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()