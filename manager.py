import csv
import copy

from models.model_pass import Password
import models.model_pass as model_pass

class PasswordManager:

    def __init__(self):    
        # Name/Location of passwords stored file csv
        self.file_name = "database/passwords.csv"

        # Stores the field names
        self.fields = []

        # Stores the data
        self.all_passwords = []

        # Stores all data
        self.all_data = []

        self.length = 0

        # Loads all the passwords from the csv file
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)

            # Stores all data
            all_data = list(reader)

            # Returns the first row which in this case is the field names
            fields = all_data[0]

            # Adds all the passwords to the list
            for row in all_data[1:]:
                # Invokes menthod from model_pass for ease
                self.all_passwords.append(model_pass.convert_list_to_pwd(row))

            self.length = len(self.all_passwords)


    # Returns the list of all passwords stored
    def get_all_passwords(self):
        return self.all_passwords

    # Function to add a new password to the database
    def add_password(self, pwd):
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            pwd.id = self.length
            # Appends a new row in the csv with the new password
            writer.writerow(model_pass.convert_pwd_to_list(pwd))
            self.length += 1

    # Function to update password
    def update_password(self, pwd):
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)

            # Ensures a deep copu of all data list so, when data is modified, all data dosent change
            data = copy.deepcopy(self.all_data)
            
            # Trys to delete the item. If failure, throws an exception
            try:
                data[pwd.id] = model_pass.convert_pwd_to_list(pwd)
            except IndexError:
                print(IndexError)
            
            writer.writerows(data)

    # Function to delete a password
    def delete_password(self, id):
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)

            # Ensures a deep copu of all data list so, when data is modified, all data dosent change
            data = copy.deepcopy(self.all_data)
            
            # Trys to delete the item. If failure, throws an exception
            try:
                data.pop(id)
            except IndexError:
                print(IndexError)
            else:
                for i in range(id, len(data)):
                    data[i][0] = str(int(data[i][0]) - 1)
            
            writer.writerows(data)
