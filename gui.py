import tkinter
from tkinter import ttk
from manager import PasswordManager
from models.model_pass import Password

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My App")
        self.passwordManager = PasswordManager()

        # Variables
        self.website_var = tkinter.StringVar()
        self.username_var = tkinter.StringVar()
        self.password_var = tkinter.StringVar()
        self.checkbox_var = tkinter.IntVar()

        # Build UI
        self.build_add_frame()
        self.build_table_frame()
        self.build_options_frame()

        # Load data
        self.all_passwords = self.passwordManager.load_data()
        self.refresh_tree()

    def refresh_tree(self):
        # Clear current table rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reload passwords
        updated_passwords = self.passwordManager.load_data()

        # Reinsert rows
        for password in updated_passwords:
            self.tree.insert("", "end", values=(password.id, password.org, password.username, password.password))

    # Handles the show password function
    def checkboxCommand(self):
        if self.checkbox_var.get():
            self.pwd_entry.config(show='')
        else:
            self.pwd_entry.config(show='*')

    # Handles the action to be taken when the button is clicked
    def funBtnAdd(self):
        pwd = Password(id=None, org=self.website_var.get(), username=self.username_var.get(), password=self.password_var.get())
        self.passwordManager.add_password(pwd=pwd)
        self.refresh_tree()

    def funBtnDelete(self):
        selected_items = self.tree.selection()
        ids_to_delete = []

        for item in selected_items:
            item_values = self.tree.item(item, "values")
            ids_to_delete.append(int(item_values[0]))

        for id in sorted(ids_to_delete, reverse=True):
            self.passwordManager.delete_password(id)

        self.refresh_tree()

    def funBtnUpdate(self):
        pass

    def onSelect(self, event):
        selected_items = event.widget.selection()
        if len(selected_items) == 1:
            self.btn_delete.state(['!disabled'])
            self.btn_update.state(['!disabled'])
        elif len(selected_items) >= 1:
            self.btn_update.state(['disabled'])
            self.btn_delete.state(['!disabled'])
        else:
            self.btn_delete.state(['disabled'])
            self.btn_update.state(['disabled'])

    def check_inputs(self, *_):
        if self.website_var.get().strip() != "" and self.username_var.get().strip() != "" and len(self.password_var.get().strip()) >= 8:
            self.btn_add.state(["!disabled"])
        else:
            self.btn_add.state(["disabled"])

    def build_add_frame(self):
        frame_add = ttk.Frame(self.root)
        frame_add.grid(pady=50, padx=25, column=0, row=0)

        # Text field for website name entry
        ttk.Label(frame_add, text="Enter website name: ").grid(row=1, column=0)
        ttk.Entry(frame_add, textvariable=self.website_var).grid(row=1, column=1)

        # Text field for username entry
        ttk.Label(frame_add, text="Enter username: ").grid(row=2, column=0)
        ttk.Entry(frame_add, textvariable=self.username_var).grid(row=2, column=1)

        # Text field for password entry
        ttk.Label(frame_add, text="Enter website password: ").grid(row=3, column=0)
        self.pwd_entry = ttk.Entry(frame_add, show='*', textvariable=self.password_var)
        self.pwd_entry.grid(row=3, column=1)

        ttk.Checkbutton(frame_add, text="Show password", variable=self.checkbox_var, command=self.checkboxCommand).grid(row=4, column=1)

        self.btn_add = ttk.Button(frame_add, text='Add Entry', command=self.funBtnAdd)
        self.btn_add.grid(row=5, column=1)
        self.btn_add.state(['disabled'])

        self.website_var.trace_add('write', self.check_inputs)
        self.username_var.trace_add('write', self.check_inputs)
        self.password_var.trace_add('write', self.check_inputs)

    def build_table_frame(self):
        frame_display = ttk.Frame(self.root)
        frame_display.grid(pady=15, padx=25, column=1, row=0)

        # This is the table to show the list of passwords
        self.tree = ttk.Treeview(frame_display, columns=('i', 'o', 'u', 'p'), show="headings")

        self.tree.heading("i", text="ID")
        self.tree.heading("o", text="Organization")
        self.tree.heading("u", text="Username")
        self.tree.heading("p", text="Password")
        self.tree.column("i", width=50)
        self.tree.column("o", width=100)
        self.tree.column("u", width=100)
        self.tree.column("p", width=100)

        self.tree.bind("<<TreeviewSelect>>", self.onSelect)  # Bind select event

        self.tree.grid(row=0, column=0)

    def build_options_frame(self):
        frame_edit = ttk.Frame(self.root)
        frame_edit.grid(pady=15, padx=0, column=1, row=1)

        self.btn_delete = ttk.Button(frame_edit, text='Delete', command=self.funBtnDelete)
        self.btn_delete.grid(row=0, column=0)
        self.btn_delete.state(['disabled'])

        self.btn_update = ttk.Button(frame_edit, text='Update', command=self.funBtnUpdate)
        self.btn_update.grid(row=0, column=1)
        self.btn_update.state(['disabled'])

if __name__ == "__main__":
    root = tkinter.Tk()
    passwordManagerApp = PasswordManagerApp(root)
    root.mainloop()
