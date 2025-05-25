import tkinter
from tkinter import ttk
import tkinter.simpledialog
from manager import PasswordManager
from models.model_pass import Password
from models.model_update_widget import UpdatePasswordDialog

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.password_manager = PasswordManager()

        # Variables
        self.website_var = tkinter.StringVar()
        self.username_var = tkinter.StringVar()
        self.password_var = tkinter.StringVar()
        self.checkbox_var = tkinter.IntVar()

        self.show_all_passwords = False
        self.show_selected_password = False
        self.last_selected_item = None

        # Build UI
        self.build_add_frame()
        self.build_table_frame()
        self.build_options_frame()

        # Load data
        self.all_passwords = self.password_manager.load_data()
        self.original_passwords = [pwd.password for pwd in self.all_passwords]

        self.refresh_tree()

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        updated_passwords = self.password_manager.load_data()
        self.original_passwords = [pwd.password for pwd in updated_passwords]

        for password in updated_passwords:
            masked = '•' * len(password.password)
            pwd_to_show = password.password if self.show_all_passwords else masked
            self.tree.insert("", "end", values=(password.id, password.org, password.username, pwd_to_show))

        self.all_passwords = updated_passwords

    def toggle_password_entry_visibility(self):
        if self.checkbox_var.get():
            self.pwd_entry.config(show='')
        else:
            self.pwd_entry.config(show='•')

    def add_entry(self):
        pwd = Password(id=None, org=self.website_var.get(), username=self.username_var.get(), password=self.password_var.get())
        self.password_manager.add_password(pwd=pwd)
        self.refresh_tree()

    def delete_selected_entries(self):
        selected_items = self.tree.selection()
        ids_to_delete = []

        for item in selected_items:
            item_values = self.tree.item(item, "values")
            ids_to_delete.append(int(item_values[0]))

        for id in sorted(ids_to_delete, reverse=True):
            self.password_manager.delete_password(id)

        self.refresh_tree()

    def update_selected_entry(self):
        
        current_item = self.selected_items[0]
        index = self.tree.index(current_item)
        current_pwd = self.all_passwords[index]
        
        dialog = UpdatePasswordDialog(self.root)
        if dialog.result:
            print(dialog.result)
            current_pwd.password = dialog.result
            self.password_manager.update_password(current_pwd)
            self.refresh_tree() 


    def toggle_selected_password(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        self.show_selected_password = not self.show_selected_password
        value = list(self.tree.item(selected_item, 'values'))
        i = list(self.tree.get_children()).index(selected_item)

        if self.show_selected_password:
            self.btn_show_password.config(text='Hide Password')
            value[3] = self.original_passwords[i]
        else:
            self.btn_show_password.config(text='Show Password')
            value[3] = '•' * len(self.original_passwords[i])

        self.tree.item(selected_item, values=value)


    def toggle_all_passwords(self):
        self.show_all_passwords = not self.show_all_passwords
        for i, item_id in enumerate(self.tree.get_children()):
            values = list(self.tree.item(item_id, 'values'))

            if self.show_all_passwords:
                self.btn_toggle_all_passwords.config(text='Hide All Passwords')
                values[3] = self.original_passwords[i]
            else:
                self.btn_toggle_all_passwords.config(text='Show All Passwords')
                values[3] = '•' * len(self.original_passwords[i])

            self.tree.item(item_id, values=values)

    # TODO Fix the selection issue
    def handle_selection(self, event):
        self.selected_items = event.widget.selection()

        if self.selected_items:
            current_item = self.selected_items[0]

            # If same item clicked again — deselect
            if self.last_selected_item == current_item:
                self.tree.selection_remove(current_item)
                self.last_selected_item = None
                self.btn_delete.state(['disabled'])
                self.btn_update.state(['disabled'])
                self.btn_show_password.state(['disabled'])

            # One new item selected
            elif len(self.selected_items) == 1:
                self.last_selected_item = current_item
                self.btn_delete.state(['!disabled'])
                self.btn_update.state(['!disabled'])
                self.btn_show_password.state(['!disabled'])

            # Multiple items selected
            else:
                self.last_selected_item = current_item
                self.btn_delete.state(['!disabled'])
                self.btn_update.state(['disabled'])
                self.btn_show_password.state(['disabled'])

        else:
            self.last_selected_item = None
            self.btn_delete.state(['disabled'])
            self.btn_update.state(['disabled'])
            self.btn_show_password.state(['disabled'])


    def check_inputs(self, *_):
        if self.website_var.get().strip() != "" and self.username_var.get().strip() != "" and len(self.password_var.get().strip()) >= 8:
            self.btn_add.state(["!disabled"])
        else:
            self.btn_add.state(["disabled"])

    def build_add_frame(self):
        frame_add = ttk.Frame(self.root)
        frame_add.grid(pady=(100, 50), padx=25, column=0, row=0)

        ttk.Label(frame_add, text="Website:").grid(row=1, column=0)
        ttk.Entry(frame_add, textvariable=self.website_var).grid(row=1, column=1)

        ttk.Label(frame_add, text="Username:").grid(row=2, column=0)
        ttk.Entry(frame_add, textvariable=self.username_var).grid(row=2, column=1)

        ttk.Label(frame_add, text="Password:").grid(row=3, column=0)
        self.pwd_entry = ttk.Entry(frame_add, show='•', textvariable=self.password_var)
        self.pwd_entry.grid(row=3, column=1)

        ttk.Checkbutton(frame_add, text="Show password", variable=self.checkbox_var, command=self.toggle_password_entry_visibility).grid(row=4, column=1)

        self.btn_add = ttk.Button(frame_add, text='Add Entry', command=self.add_entry)
        self.btn_add.grid(row=5, column=1)
        self.btn_add.state(['disabled'])

        self.website_var.trace_add('write', self.check_inputs)
        self.username_var.trace_add('write', self.check_inputs)
        self.password_var.trace_add('write', self.check_inputs)

    def build_table_frame(self):
        frame_display = ttk.Frame(self.root)
        frame_display.grid(pady=15, padx=25, column=1, row=0)

        self.tree = ttk.Treeview(frame_display, columns=('ID', 'Website', 'Username', 'Password'), show="headings")

        for name in ('ID', 'Website', 'Username', 'Password'):
            self.tree.heading(name, text=name)
            self.tree.column(name, width=100)

        self.tree.bind("<<TreeviewSelect>>", self.handle_selection)
        self.tree.grid(row=0, column=0)

    def build_options_frame(self):
        frame_edit = ttk.Frame(self.root)
        frame_edit.grid(pady=(0,20), padx=0, column=1, row=1)

        self.btn_delete = ttk.Button(frame_edit, text='Delete', command=self.delete_selected_entries)
        self.btn_delete.grid(row=0, column=0)
        self.btn_delete.state(['disabled'])

        self.btn_update = ttk.Button(frame_edit, text='Update', command=self.update_selected_entry)
        self.btn_update.grid(row=0, column=1)
        self.btn_update.state(['disabled'])

        self.btn_show_password = ttk.Button(frame_edit, text='Show Password', command=self.toggle_selected_password)
        self.btn_show_password.grid(row=0, column=3)
        self.btn_show_password.state(['disabled'])

        self.btn_toggle_all_passwords = ttk.Button(frame_edit, text='Show All Passwords', command=self.toggle_all_passwords)
        self.btn_toggle_all_passwords.grid(row=0, column=4)

if __name__ == "__main__":
    root = tkinter.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()