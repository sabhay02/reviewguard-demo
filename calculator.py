import os
import sqlite3
from getpass import getpass
from hashlib import sha256

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, sha256(password.encode()).hexdigest()))
    result = cursor.fetchone()
    conn.close()
    return result

def create_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, sha256(password.encode()).hexdigest()))
    conn.commit()
    conn.close()

def main():
    while True:
        print("1. Login")
        print("2. Create User")
        print("3. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            result = login(username, password)
            if result:
                print("Login successful!")
            else:
                print("Invalid username or password.")
        elif choice == "2":
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            create_user(username, password)
            print("User created successfully.")
        elif choice == "3":
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()