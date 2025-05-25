# 🔐 Password Manager

A simple, secure, and user-friendly password manager built with Python and Tkinter. This application allows you to store, manage, and update your credentials with ease, ensuring your data remains encrypted and protected.

---

## 📦 Features

- **Add New Entries**: Store website, username, and password combinations securely.
- **Update Existing Entries**: Modify stored credentials as needed.
- **Delete Entries**: Remove credentials that are no longer required.
- **Password Visibility Toggle**: Show or hide passwords in the interface.
- **Input Validation**: Ensures passwords meet minimum length requirements.
- **Encrypted Storage**: Passwords are encrypted before being saved to a CSV file.
- **Modern UI**: Built using Tkinter's `ttk` module for a sleek appearance.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter (ttk)**
- **CSV Module**: For data storage.
- **Custom Encryption Module**: Handles password encryption and decryption.

---

## 🚀 Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sharatchandra-ts/password-manager.git
   cd password-manager
   ```
2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```bash
   python main.py
   ```

---

## 📂 Project Structure
   ```pgsql
   password-manager/
   ├── database/
   │   └── passwords.csv          # Encrypted password storage
   ├── models/
   │   ├── model_pass.py          # Password data model
   │   └── model_update_widget.py # Update password dialog
   ├── encrypt.py                 # Encryption and decryption logic
   ├── gui.py                     # GUI components and layout
   ├── main.py                    # Application entry point
   ├── manager.py                 # Core password management logic
   ├── requirements.txt           # Python dependencies
   └── README.md                  # Project documentation
   ```

---

## 🧪 Usage

### Adding a Password

- Enter the website, username, and password fields.
- Password must be at least 8 characters long.
- Click **"Add Entry"** to save your credentials securely.

### Updating a Password

- Select a single password entry in the table.
- Click **"Update"**, enter a new password in the popup dialog.
- Confirm to save changes.

### Deleting Passwords

- Select one or multiple entries.
- Click **"Delete"** to remove the selected entries.

### Viewing Passwords

- Use **"Show Password"** to toggle visibility of the selected password.
- Use **"Show All Passwords"** to toggle visibility for all entries in the list.

---

## 🔐 Security

Passwords are encrypted before storage in the `passwords.csv` file using a custom encryption module (`encrypt.py`). This ensures sensitive information remains protected even if the storage file is accessed directly.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

This project was developed to gain hands-on experience building GUI applications and managing secure data storage with Python.

---

## 📞 Contact

Feel free to open issues or submit pull requests on GitHub for improvements or bug fixes.
