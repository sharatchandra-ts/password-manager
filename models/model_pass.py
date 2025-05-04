class password:
    def __init__(self, org, username, password):
        self.org = org
        self.username = username
        self.password = password

def convert_list_to_pwd(list):
    return password(org=list[0], username=list[1], password=list[2])

def convert_pwd_to_list(pwd):
    return [pwd.org, pwd.username, pwd.password]