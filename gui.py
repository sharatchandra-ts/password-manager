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
all_passwords = passwordManager.get_all_passwords()

# Handels the show password function
def checkboxCommand():
    if checkbox_var.get():
        pwd_entry.config(show='')
    else:
        pwd_entry.config(show='*')

# Handels the action to be taken when the button is clicked
def btnCommand():
    print(username_var.get(), website_var.get(), password_var.get())
    pwd = Password(id=None, org=website_var.get(), username=username_var.get(), password=password_var.get())
    passwordManager.add_password(pwd=pwd)


frame_entry = ttk.Frame(root)
frame_entry.grid(pady=50, padx=25, column=0, row=0)

frame_display = ttk.Frame(root)
frame_display.grid(pady=50, padx=25, column=1, row=0)

root.title("My App")

ttk.Label(frame_entry, text="ADD NEW PASSWORD\n").grid()

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

ttk.Button(frame_entry, text="Submit", command=btnCommand).grid(row=5,column=1)

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

# Adds evey password into the table
for password in all_passwords:
    tree.insert("", "end", values=(password.id, password.org, password.username, password.password))
tree.grid(row=1, column=10)

root.mainloop()