import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class UpdatePasswordDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Update Password")

        self.password_var = tk.StringVar()
        self.show_password_var = tk.IntVar()


        ttk.Label(master, text="New Password:").grid(row=0, column=0, sticky="w")

        self.entry_password = ttk.Entry(master, textvariable=self.password_var, show="•")
        self.entry_password.grid(row=0, column=1, padx=5, pady=5)

        
        self.password_var.trace_add('write', self.validate_password)

        self.check_show_password = ttk.Checkbutton(master, text="Show Password",
                                                   variable=self.show_password_var,
                                                   command=self.toggle_password_visibility)
        self.check_show_password.grid(row=1, column=1, sticky="w")

        return self.entry_password  # focus here

    def buttonbox(self):
        box = ttk.Frame(self)

        self.ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.ok_button.state(['disabled'])  # disable OK initially

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="•")

    def validate_password(self, *_):
        pwd = self.password_var.get()
        if len(pwd) >= 8:
            self.ok_button.state(['!disabled'])
        else:
            self.ok_button.state(['disabled'])

    def apply(self):
        # This runs when OK pressed and dialog closes
        self.result = self.password_var.get()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    dialog = UpdatePasswordDialog(root)
    if dialog.result:
        print("New password:", dialog.result)
    else:
        print("No password set")
