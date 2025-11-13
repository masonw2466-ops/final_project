import tkinter as tk
from tkinter import messagebox

class GymInterface:
    def __init__(self, root, staff_status):
        self.root = root
        self.staff_status = staff_status
        self.root.title("Staff Dashboard")
        self.root.geometry("500x500")

        # Lets employee add gym member
        self.button_add_member = tk.Button(root, text="Add Member", command=self.add_member)
        self.button_add_member.pack(pady=10)

        # Lets staff edit member info
        self.button_edit_member = tk.Button(root, text="Edit Member", command=self.edit_member)
        self.button_edit_member.pack(pady=10)

        # Lets staff edit or see class schedule
        self.button_class_schedule = tk.Button(root, text="Class Schedule", command=self.class_schedule)
        self.button_class_schedule.pack(pady=10)

        # Lets staff see maintenance logs
        self.button_maintenance_logs = tk.Button(root, text="Maintenance Logs", command=self.maintenance_logs)
        self.button_maintenance_logs.pack(pady=10)

        # Adds extra options for the manager
        if self.staff_status == "Manager":
            self.button_manage_staff = tk.Button(root, text="Manage Staff", command=self.manage_staff)
            self.button_manage_staff.pack(pady=10)

        self.button_loggout = tk.Button(root, text="Loggout", command=self.loggout)
        self.button_loggout.pack(pady=10)

    # Adds the method for adding members
    def add_member(self):
        pass

    # Adds method for editing members
    def edit_member(self):
        pass
    
    # Adds method for the class schedules
    def class_schedule(self):
        pass
    
    # Allows you to change and update maintenance logs
    def maintenance_logs(self):
        pass

    # Allows manager to add and fire staff
    def manage_staff(self):
        pass

    def loggout(self):
        messagebox.showinfo("Loggout Successful", "Loggout Successful")
        self.root.destroy()

        #Reloads the login page
        import login
        root = tk.Tk()
        login.Login(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GymInterface(root, "Employee")
    root.mainloop()