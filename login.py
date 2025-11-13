import tkinter as tk
from tkinter import messagebox

staff_status = None  

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x500")

        # Adds the prompt asking for ID
        self.label_prompt_id = tk.Label(root, text="Enter Employee ID")
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

    # Method for checking that the login exists
    def check_login(self):
        global staff_status

        employee_id = self.entry_id.get().strip()
        password = self.entry_passcode.get().strip()

        # fake data: id -> {password, role}
        staff_data = {
            "001": {"password": "1234", "role": "Manager"},
            "002": {"password": "abcd", "role": "Employee"},
            "003": {"password": "pass", "role": "Employee"},
        }

        if employee_id == "" or password == "":
            self.label_output.config(text="Please enter both ID and password.", fg="red")
            return

        if employee_id in staff_data and staff_data[employee_id]["password"] == password:
            staff_status = staff_data[employee_id]["role"]
            messagebox.showinfo("Login Successful", f"Welcome {staff_status}!")
            self.root.destroy()

            # import and open main page
            import main_page
            root = tk.Tk()
            main_page.GymInterface(root, staff_status)
            root.mainloop()

        else:
            self.label_output.config(text="Invalid ID or password", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()