import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import landing
import sqlite3


class GymInterface:
    def __init__(self, root, staff_status=None, member_name=None, member_username=None):
        self.root = root
        self.staff_status = staff_status
        self.member_name = member_name
        self.member_username = member_username
        self.timeout_id = None

        self.root.geometry("500x500")

        if self.staff_status is not None:
            self.build_staff_dashboard()
        elif self.member_name is not None:
            self.build_member_dashboard()

    # Staff dashboard
    def build_staff_dashboard(self):
        self.root.title("Staff Dashboard")

        tk.Label(self.root, text=f"Welcome, {self.staff_status}", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Manage Members", width=20,
                  command=self.edit_member).pack(pady=10)

        tk.Button(self.root, text="Manage Class Schedules", width=20,
                  command=self.class_schedule).pack(pady=10)

        tk.Button(self.root, text="Maintenance Logs", width=20,
                  command=self.maintenance_logs).pack(pady=10)
        
        # Manager dashboard gets "Manage Staff Button"
        if self.staff_status == "Manager":
            tk.Button(self.root, text="Manage Staff", width=20,
                      command=self.manage_staff).pack(pady=10)

        tk.Button(self.root, text="Logout", width=20,
                  command=self.logout).pack(pady=20)

    # Member dashboard
    def build_member_dashboard(self):
        self.root.title("Member Dashboard")

        tk.Label(self.root, text=f"Welcome, {self.member_name}!", font=("Arial", 24)).pack(pady=25)
        tk.Label(self.root, text="You are checked in. Enjoy your workout!",
                font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="View My Membership Info",
                command=self.open_membership_info).pack(pady=15)
        
        tk.Button(self.root, text="Change Membership", 
                command=self.change_membership).pack(pady=15)

        tk.Button(self.root, text="View Class Schedule",
                command=self.open_class_schedule_view).pack(pady=15)

        # Inactivity timer (after member check-in, goes back to default check-in screen)
        self.start_timeout()


    # Timeout cancel (member navigates through the software)
    def cancel_timeout(self):
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)
            self.timeout_id = None

    # Restart a new timeout timer
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

        # Timeout timer restarts (Member goes back to welcome screen after check-in)
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

        # Restart timeout timer when this window closes
        win.protocol("WM_DELETE_WINDOW", lambda: (win.destroy(), self.start_timeout()))

    def change_membership(self):
        self.cancel_timeout()
        EditMembershipWindow(self)

    # Auto reset after member checks-in
    def member_timeout(self):
        try:
            self.root.destroy()
        except:
            pass
        from login import Login
        new = tk.Tk()
        Login(new, mode="member")
        new.mainloop()

    # Staff functions
    def edit_member(self):
        import members
        new = tk.Toplevel(self.root)
        members.Members(new)

    def class_schedule(self):
        import schedules
        new = tk.Toplevel(self.root)
        schedules.Schedules(new)

    def maintenance_logs(self):
        messagebox.showinfo("Maintenance Logs", "Not implemented yet.")

    def manage_staff(self):
        import staff
        new = tk.Toplevel(self.root)
        staff.Staff(new)

    def logout(self):
        messagebox.showinfo("Logout Successful", "Logout Successful")
        self.root.destroy()
        root = tk.Tk()
        landing.Landing(root)
        root.mainloop()

class EditMembershipWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Edit Membership")
        self.win.geometry("500x500")

        tk.Label(self.win, text="Membership options").pack(pady=10)

        #Choose the type of membership
        tk.Label(self.win, text="Membership Type").pack(pady=5)
        self.membership_type = ttk.Combobox(
            self.win,
            values=["Basic", "Premium", "VIP", "Student", "Family"]
        )
        self.membership_type.pack()

        tk.Button(self.win, text="Save Changes",
                  command=self.save_changes).pack(pady=15)
        
    def save_changes(self):
        new_membership = self.membership_type.get()

        if not new_membership:
            messagebox.showerror("Error", "Please select a membership type.")
            return

        # Update ONLY the membership column for this user
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




if __name__ == "__main__":
    root = tk.Tk()
    GymInterface(root, staff_status="Employee")
    root.mainloop()
