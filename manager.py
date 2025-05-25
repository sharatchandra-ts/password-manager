import csv
import copy

from models.model_pass import Password
import models.model_pass as model_pass
from encrypt import Encode

class PasswordManager:
    
    def __init__(self):    
        # Name/Location of passwords stored file csv
        self.file_name = "database/passwords.csv"

        self.encode = Encode()






        # Loads all the passwords from the csv file
        self.load_data()


    # Returns the list of all passwords stored
    def load_data(self):

        # Stores the field names
        self.fields = []

        # Stores the data
        self.all_passwords = []

        # Stores all data
        self.all_data = []

        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            # Stores all data
            self.all_data = list(reader)

            # Returns the first row which in this case is the field names
            self.fields = self.all_data[0]

            # Adds all the passwords to the list
            for row in self.all_data[1:]:
                # Invokes menthod from model_pass for ease
                decrypted_row = row.copy()
                decrypted_row[3] = self.encode.decrypt(row[3])
                self.all_passwords.append(model_pass.convert_list_to_pwd(decrypted_row))

        return self.all_passwords

    # Function to add a new password to the database
    def add_password(self, pwd):
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            pwd.id = len(self.all_passwords)
            pwd.password = self.encode.encrypt(pwd.password)
            # Appends a new row in the csv with the new password
            writer.writerow(model_pass.convert_pwd_to_list(pwd))

    # Function to update password
    def update_password(self, pwd):
        # Create deep copy to avoid changing the original in memory
        data = copy.deepcopy(self.all_data)

        # Convert password to encrypted list format
        updated_pwd = copy.deepcopy(pwd)
        updated_pwd.password = self.encode.encrypt(updated_pwd.password)
        updated_row = model_pass.convert_pwd_to_list(updated_pwd)

        try:
            data[int(pwd.id) + 1] = updated_row  # +1 because data includes header at index 0
        except IndexError:
            print("IndexError: Invalid password ID")
            return

        # Write updated data to file
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # Update internal memory (optional but good for consistency)
        self.load_data()


    # Function to delete a password
    def delete_password(self, id):
        id += 1  # Adjust for header row
        with open(self.file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Trys to delete the item. If failure, throws an exception
        try:
            data.pop(id)
        except IndexError:
            print("IndexError: ID not found")
        else:
            for i in range(id, len(data)):
                data[i][0] = str(int(data[i][0]) - 1)

        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
