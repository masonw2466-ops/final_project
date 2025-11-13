import tkinter as tk

class GymInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff Dashboard")
        self.root.geometry("500x500")

        self.button_add_member = tk.Button(root, text="Add Member", command=self.add_member)
        self.button_add_member.pack(pady=10)

        self.button_edit_member = tk.Button(root, text="Edit Member", command=self.edit_member)
        self.button_edit_member.pack(pady=10)

        self.button_class_schedule = tk.Button(root, text="Class Schedule", command=self.class_schedule)
        self.button_class_schedule.pack(pady=10)

        self.button_maintenance_logs = tk.Button(root, text="Maintenance Logs", command=self.maintenance_logs)
        self.button_maintenance_logs.pack(pady=10)

    def add_member(self):
        pass

    def edit_member(self):
        pass
    
    def class_schedule(self):
        pass
    
    def maintenance_logs(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = GymInterface(root)
    root.mainloop()