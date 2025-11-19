import tkinter as tk
import login 




class Landing:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym System - Landing")
        self.root.geometry("500x500")

        tk.Label(root, text="Welcome to the Gym System", font=("Arial", 20)).pack(pady=40)

        # 'Staff Login' Button
        tk.Button(
            root,
            text="Staff Login",
            font=("Arial", 18),
            width=20,
            command=self.open_staff_login
        ).pack(pady=20)

        # 'Member Login' Button
        tk.Button(
            root,
            text="Member Login",
            font=("Arial", 18),
            width=20,
            command=self.open_member_login
        ).pack(pady=20)

    # Open staff login page
    def open_staff_login(self):
        self.root.destroy()
        root = tk.Tk()
        login.Login(root, mode="staff")
        root.mainloop()

    # Open member login page
    def open_member_login(self):
        self.root.destroy()
        root = tk.Tk()
        login.Login(root, mode="member")
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    Landing(root)
    root.mainloop()
