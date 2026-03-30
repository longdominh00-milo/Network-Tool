# create_user.py
<<<<<<< HEAD
import argparse
=======
>>>>>>> 549a02a1534b55cc59f4bbab78f8ab50b6e9a0ff
import json
import getpass
from werkzeug.security import generate_password_hash

USER_FILE = 'users.json'

def add_user():
<<<<<<< HEAD
    parser = argparse.ArgumentParser(description="Create a new user.")
    parser.add_argument("--username", help="The username for the new user")
    parser.add_argument("--password", help="The password for the new user")
    args = parser.parse_args()

=======
>>>>>>> 549a02a1534b55cc59f4bbab78f8ab50b6e9a0ff
    try:
        with open(USER_FILE, 'r') as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError):
        data = {'users': {}}

<<<<<<< HEAD
    if args.username:
        username = args.username
    else:
        username = input("Enter username: ")

=======
    username = input("Enter username: ")
>>>>>>> 549a02a1534b55cc59f4bbab78f8ab50b6e9a0ff
    if username in data['users']:
        print("User already exists.")
        return

<<<<<<< HEAD
    if args.password:
        password = args.password
    else:
        password = getpass.getpass("Enter password: ")
        password2 = getpass.getpass("Confirm password: ")
        if password != password2:
            print("Passwords do not match.")
            return
=======
    password = getpass.getpass("Enter password: ")
    password2 = getpass.getpass("Confirm password: ")
    if password != password2:
        print("Passwords do not match.")
        return
>>>>>>> 549a02a1534b55cc59f4bbab78f8ab50b6e9a0ff
    
    # Băm mật khẩu trước khi lưu
    password_hash = generate_password_hash(password)
    data['users'][username] = password_hash

    with open(USER_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"User '{username}' created successfully!")

if __name__ == '__main__':
    add_user()