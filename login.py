import tkinter as tk

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
        self.button_submit = tk.Button(root, text="Submit", command="check_login")
        self.button_submit.pack(pady=10)

        # Left empty to start but will display message if done wrong
        self.label_output = tk.Label(root, text="")
        self.label_output.pack(pady=10)

    # Method for checking that the login exists
    def check_login(self):
        employee_id = self.entry_id.get()
        password = self.entry_passcode()
        if (employee_id.strip()) or (password) == "":
            self.label_output.config(text="Invalid ID or password")
        
        ''' Right here we want to add an if or 
        omehting that will check if the id and 
        password are in a dictionary or something
        and then decide whether to send a value of 
        manager or employee. Or should we add a 
        database? It would also need to send them to
        the main page'''