import tkinter as tk
from tkinter import messagebox
import landing   # for going “home” after timeout


class GymInterface:
    def __init__(self, root, staff_status=None, member_name=None):
        self.root = root
        self.staff_status = staff_status
        self.member_name = member_name

        self.root.geometry("500x500")

        # Load dashboard based on user role ("Staff","Member")
        if self.staff_status is not None:
            self.build_staff_dashboard()

        elif self.member_name is not None:
            self.build_member_dashboard()



    # Staff dashboard
    def build_staff_dashboard(self):
        self.root.title("Staff Dashboard")

        tk.Label(self.root, text=f"Welcome, {self.staff_status}", font=("Arial", 18)).pack(pady=20)

        # Members
        tk.Button(self.root, text="Manage Members", width=20,
                  command=self.edit_member).pack(pady=10)

        # Class schedules
        tk.Button(self.root, text="Manage Class Schedules", width=20,
                  command=self.class_schedule).pack(pady=10)

        # Maintenance logs
        tk.Button(self.root, text="Maintenance Logs", width=20,
                  command=self.maintenance_logs).pack(pady=10)

        # Manager
        if self.staff_status == "Manager":
            tk.Button(self.root, text="Manage Staff", width=20,
                      command=self.manage_staff).pack(pady=10)

        # Logout
        tk.Button(self.root, text="Logout", width=20,
                  command=self.logout).pack(pady=20)


    # Member dashboard
    def build_member_dashboard(self):
        self.root.title("Member Dashboard")

        tk.Label(self.root, text=f"Welcome, {self.member_name}!", font=("Arial", 20)).pack(pady=30)
        tk.Label(self.root, text="You are checked in. Enjoy your workout!",
                 font=("Arial", 14)).pack(pady=10)

        # Button to view member’s dashboard information
        tk.Button(self.root, text="View My Membership Info",
                  command=self.open_member_info).pack(pady=20)

        # Auto timeout after 5 seconds of inactivity
        self.root.after(5000, self.member_timeout)


    def open_member_info(self):
        messagebox.showinfo(
            "Membership Info",
            "Membership Status: ACTIVE\nRenewal Date: 12/31/2025\nPlan: Premium"
        )



    # Timeout behavior after member check-in
    def member_timeout(self):
        """
        After a few seconds, return to the member login screen automatically.
        """
        try:
            self.root.destroy()
        except:
            pass

        new = tk.Tk()
        from login import Login
        Login(new, mode="member")
        new.mainloop()



    # Staff button functions
    def edit_member(self):
        import members
        new_window = tk.Toplevel(self.root)
        members.Members(new_window)

    def class_schedule(self):
        import schedules
        new_window = tk.Toplevel(self.root)
        schedules.Schedules(new_window)

    def maintenance_logs(self):
        pass

    def manage_staff(self):
        import staff
        new_window = tk.Toplevel(self.root)
        staff.Staff(new_window)

    def logout(self):
        messagebox.showinfo("Logout Successful", "Logout Successful")
        self.root.destroy()

        root = tk.Tk()
        landing.Landing(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    # Default to staff mode for testing
    GymInterface(root, staff_status="Employee")
    root.mainloop()
