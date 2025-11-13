import tkinter as tk

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x500")

        self.label_prompt_id = tk.Label(root, text="Enter Employee ID")
        self.label_prompt_id.pack(pady=10)

        self.entry_id = tk.Entry(root)
        self.entry_id.pack(pady=10)


        self.label_prompt_passcode = tk.Label(root, text="Enter Passcode")
        self.label_prompt_passcode.pack(pady=10)
        
        self.entry_passcode = tk.Entry(root)
        self.entry_passcode.pack(pady=10)