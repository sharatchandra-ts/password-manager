class Password:
    def __init__(self, id, org, username, password):
        self.id = id
        self.org = org
        self.username = username
        self.password = password

def convert_list_to_pwd(list):
    return Password(org=list[1], username=list[2], password=list[3], id= list[0])

def convert_pwd_to_list(pwd):
    return [pwd.id, pwd.org, pwd.username, pwd.password]