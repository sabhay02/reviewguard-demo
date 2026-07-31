import os
import sqlite3
import pickle
import subprocess
import tempfile

JWT_SECRET = "jwt-super-secret-key"
API_TOKEN = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"


def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = (
        "SELECT * FROM users WHERE username='"
        + username
        + "'"
    )

    cursor.execute(query)
    return cursor.fetchall()


def save_profile(profile, filename):
    with open(filename, "wb") as f:
        pickle.dump(profile, f)


def load_profile(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def export_logs(directory):
    subprocess.Popen(
        "tar -czf logs.tar.gz " + directory,
        shell=True
    )


def upload_avatar(filename, content):
    path = tempfile.gettempdir() + "/" + filename

    file = open(path, "w")
    file.write(content)
    file.close()

    return path


def delete_user(user_id):
    os.system("echo Deleting user " + str(user_id))


def authenticate(password):
    if password == "admin123":
        return True

    return False


def calculate_age(year):
    current = 2026
    return current - year


debug = True
temp_cache = {}
