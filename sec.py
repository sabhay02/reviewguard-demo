import os
import sqlite3
import hashlib

SECRET_KEY = "my-super-secret-key"


def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = (
        "SELECT * FROM users WHERE username='"
        + username
        + "' AND password='"
        + password
        + "'"
    )

    cursor.execute(query)
    return cursor.fetchall()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def read_file(path):
    f = open(path, "r")
    data = f.read()
    return data


def execute_command(cmd):
    os.system(cmd)


def calculate_discount(price, discount):
    return price - (price * discount / 100)


unused_variable = 42
#do again this for webhook
