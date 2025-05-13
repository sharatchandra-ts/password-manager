import tkinter
from tkinter import ttk
from manager import PasswordManager
from models.model_pass import Password


root = tkinter.Tk()
checkbox_var = tkinter.IntVar()
username_var = tkinter.StringVar()
website_var = tkinter.StringVar()
password_var = tkinter.StringVar()

passwordManager = PasswordManager()
all_passwords = passwordManager.load_data()

def refresh_tree():
    # Clear current table rows
    for item in tree.get_children():
        tree.delete(item)

    # Reload passwords
    updated_passwords = passwordManager.load_data()

    # Reinsert rows
    for password in updated_passwords:
        tree.insert("", "end", values=(password.id, password.org, password.username, password.password))

# Handels the show password function
def checkboxCommand():
    if checkbox_var.get():
        pwd_entry.config(show='')
    else:
        pwd_entry.config(show='*')

# Handels the action to be taken when the button is clicked
def funBtnAdd():
    pwd = Password(id=None, org=website_var.get(), username=username_var.get(), password=password_var.get())
    passwordManager.add_password(pwd=pwd)
    refresh_tree()

def funBtnDelete():
    selected_items = tree.selection()
    ids_to_delete = []

    for item in selected_items:
        item_values = tree.item(item, "values")
        ids_to_delete.append(int(item_values[0]))

    for id in sorted(ids_to_delete, reverse=True):
        passwordManager.delete_password(id)

    refresh_tree()

def funBtnUpdate():
    pass

def onSelect(event):
    selected_items = event.widget.selection()
    if len(selected_items) == 1:
        btn_delete.state(['!disabled'])
        btn_update.state(['!disabled'])
    elif len(selected_items) >= 1:
        btn_update.state(['disabled'])
        btn_delete.state(['!disabled'])
    else:
        btn_delete.state(['disabled'])
        btn_update.state(['disabled'])

def check_inputs(*_):
    if website_var.get().strip() != "" and username_var.get().strip() != "" and len(password_var.get().strip()) >= 8:
        btn_add.state(["!disabled"])
    else:
        btn_add.state(["disabled"])


frame_entry = ttk.Frame(root)
frame_entry.grid(pady=50, padx=25, column=0, row=0)

frame_display = ttk.Frame(root)
frame_display.grid(pady=15, padx=25, column=1, row=0)

frame_edit = ttk.Frame(root)
frame_edit.grid(pady=15, padx=0, column=1, row=1)

root.title("My App")

# ttk.Label(frame_entry, text="ADD NEW PASSWORD\n").grid()

# Text field for website name entry
ttk.Label(frame_entry, text="Enter website name: ").grid(row=1, column=0)
ttk.Entry(frame_entry, textvariable= website_var).grid(row=1,column=1)

# Text field for username entry
ttk.Label(frame_entry, text="Enter username: ").grid(row=2, column=0)
ttk.Entry(frame_entry, textvariable= username_var).grid(row=2,column=1)


# Text field for password entry
ttk.Label(frame_entry, text="Enter website password: ").grid(row=3, column=0)
pwd_entry = ttk.Entry(frame_entry, show='*' ,  textvariable= password_var)
pwd_entry.grid(row=3,column=1)

ttk.Checkbutton(frame_entry, text="Show password", variable=checkbox_var, command= checkboxCommand).grid(row=4,column=1)

btn_add = ttk.Button(frame_entry, text='Add Entry', command=funBtnAdd)
btn_add.grid(row=5,column=1)
btn_add.state(['disabled'])

website_var.trace_add('write', check_inputs)
username_var.trace_add('write', check_inputs)
password_var.trace_add('write', check_inputs)

# This is the table to show the list of passwords
tree = ttk.Treeview(frame_display, columns=('i','o','u','p'), show="headings")

tree.heading("i", text="ID")
tree.heading("o", text="Organization")
tree.heading("u", text="Username")
tree.heading("p", text="Password")
tree.column("i", width=50)
tree.column("o",  width=100)
tree.column("u", width=100)
tree.column("p", width=100)

tree.bind("<<TreeviewSelect>>", onSelect)  # Bind select event

# Adds evey password into the table
for password in all_passwords:
    tree.insert("", "end", values=(password.id, password.org, password.username, password.password))
tree.grid(row=0, column=0)

btn_delete = ttk.Button(frame_edit, text='Delete', command=funBtnDelete)
btn_delete.grid(row=0, column=0)
btn_delete.state(['disabled'])

btn_update = ttk.Button(frame_edit, text='Update', command=funBtnUpdate)
btn_update.grid(row=0, column=1)
btn_update.state(['disabled'])

root.mainloop()