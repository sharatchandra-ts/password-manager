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
                row[3] = self.encode.decrypt(row[3])
                self.all_passwords.append(model_pass.convert_list_to_pwd(row))

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
