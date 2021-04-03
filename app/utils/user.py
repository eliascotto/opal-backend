import re

USER_R = r'^@?(\w){1,15}$'

def check_username(username: str):
    return re.match(USER_R, username)
