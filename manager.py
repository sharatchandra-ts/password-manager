import csv
from models.model_pass import password
import models.model_pass as model_pass

# Name/Location of passwords stored file csv
file_name = "database/passwords.csv"

# Stores the field names
fields = []

# Stores the data
all_passwords = []

# Loads all the passwords from the csv file
with open(file_name, 'r') as file:
        reader = csv.reader(file)

        # Returns the first row which in this case is the field names
        fields = next(reader)
 
        # Adds all the passwords to the list
        for row in reader:
            # Invokes menthod from model_pass for ease
            all_passwords.append(model_pass.convert_list_to_pwd(row))


# Returns the list of all passwords stored
def get_all_passwords():
    return all_passwords

def add_password(pwd):
     with open(file_name, 'a', newline='') as file:
          writer = csv.writer(file)
          
          # Appends a new row in the csv with the new password
          writer.writerow(model_pass.convert_pwd_to_list(pwd))
          

