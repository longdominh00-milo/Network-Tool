# create_user.py
import json
import getpass
from werkzeug.security import generate_password_hash

USER_FILE = 'users.json'

def add_user():
    try:
        with open(USER_FILE, 'r') as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError):
        data = {'users': {}}

    username = input("Enter username: ")
    if username in data['users']:
        print("User already exists.")
        return

    password = getpass.getpass("Enter password: ")
    password2 = getpass.getpass("Confirm password: ")
    if password != password2:
        print("Passwords do not match.")
        return
    
    # Băm mật khẩu trước khi lưu
    password_hash = generate_password_hash(password)
    data['users'][username] = password_hash

    with open(USER_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"User '{username}' created successfully!")

if __name__ == '__main__':
    add_user()