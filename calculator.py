"""
Calculator module providing basic arithmetic operations and user management.
"""

import os
import sqlite3
from getpass import getpass
from hashlib import pbkdf2_hmac
import secrets
import string

def add(a, b):
    """
    Returns the sum of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b

def subtract(a, b):
    """
    Returns the difference of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The difference of a and b.
    """
    return a - b

def login(username, password):
    """
    Verifies a user's credentials.

    Args:
        username (str): The user's username.
        password (str): The user's password.

    Returns:
        tuple or None: A tuple containing the user's data if the credentials are valid, otherwise None.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def create_user(username, password):
    """
    Creates a new user.

    Args:
        username (str): The user's username.
        password (str): The user's password.

    Returns:
        None
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    hashed_password = pbkdf2_hmac('sha256', password.encode(), secrets.token_bytes(16), 100000)
    cursor.execute(query, (username, hashed_password.hex()))
    conn.commit()
    conn.close()

def generate_password(length=12):
    """
    Generates a random password.

    Args:
        length (int): The length of the password. Defaults to 12.

    Returns:
        str: A random password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def main():
    """
    The main function of the calculator module.

    Returns:
        None
    """
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
            confirm_password = getpass("Confirm password: ")
            if password == confirm_password:
                create_user(username, password)
                print("User created successfully.")
            else:
                print("Passwords do not match.")
        elif choice == "3":
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()