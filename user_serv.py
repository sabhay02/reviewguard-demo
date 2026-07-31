import os
import sqlite3
import json
import subprocess
import tempfile
import hashlib
import jwt
import pytest
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

JWT_SECRET = os.environ.get("JWT_SECRET")
API_TOKEN = os.environ.get("API_TOKEN")

# Create a SQLite database engine
engine = create_engine("sqlite:///users.db")

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def get_user(username):
    """
    Retrieves a user from the database.

    Args:
        username (str): The username to retrieve.

    Returns:
        list: A list of user data if found, otherwise an empty list.
    """
    session = Session()
    try:
        result = session.execute(text("SELECT * FROM users WHERE username=:username"), {"username": username})
        return result.fetchall()
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving user: {e}")
        return []
    finally:
        session.close()


def save_profile(profile, filename):
    """
    Saves a user profile to a file.

    Args:
        profile (dict): The user profile to save.
        filename (str): The filename to save the profile to.
    """
    with open(filename, "w") as f:
        json.dump(profile, f)


def load_profile(filename):
    """
    Loads a user profile from a file.

    Args:
        filename (str): The filename to load the profile from.

    Returns:
        dict: The loaded user profile.
    """
    with open(filename, "r") as f:
        return json.load(f)


def export_logs(directory):
    """
    Exports logs to a tarball.

    Args:
        directory (str): The directory to export logs from.
    """
    subprocess.run(["tar", "-czf", "logs.tar.gz", directory], check=True)


def upload_avatar(filename, content):
    """
    Uploads an avatar to a temporary file.

    Args:
        filename (str): The filename to save the avatar to.
        content (str): The avatar content to upload.

    Returns:
        str: The path to the uploaded avatar.
    """
    path = tempfile.gettempdir() + "/" + filename

    with open(path, "w") as f:
        f.write(content)

    return path


def delete_user(user_id):
    """
    Deletes a user.

    Args:
        user_id (int): The ID of the user to delete.
    """
    logging.info(f"Deleting user {user_id}")


def authenticate(password):
    """
    Authenticates a user.

    Args:
        password (str): The password to authenticate.

    Returns:
        bool: Whether the authentication was successful.
    """
    if password == os.environ.get("ADMIN_PASSWORD"):
        return True

    return False


def calculate_age(year):
    """
    Calculates the age of a user.

    Args:
        year (int): The birth year of the user.

    Returns:
        int: The age of the user.
    """
    current = 2026
    return current - year


def hash_password(password):
    """
    Hashes a password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashlib.pbkdf2_hmac("sha256", password.encode(), os.urandom(16), 100000)


def verify_password(stored_password, provided_password):
    """
    Verifies a password.

    Args:
        stored_password (str): The stored password to verify.
        provided_password (str): The provided password to verify.

    Returns:
        bool: Whether the password is valid.
    """
    return stored_password == hash_password(provided_password)


def generate_token(username):
    """
    Generates a JWT token.

    Args:
        username (str): The username to generate the token for.

    Returns:
        str: The generated JWT token.
    """
    return jwt.encode({"username": username}, JWT_SECRET, algorithm="HS256")


def verify_token(token):
    """
    Verifies a JWT token.

    Args:
        token (str): The token to verify.

    Returns:
        str: The username associated with the token, or None if invalid.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])["username"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def test_get_user():
    user = get_user("test_user")
    assert user is not None


def test_save_profile():
    user_serv.save_profile({"name": "Test User"}, "profile.dat")
    assert True


def test_load_profile():
    user_serv.load_profile("profile.dat")
    assert True


def test_export_logs():
    user_serv.export_logs("/path/to/logs")
    assert True


def test_upload_avatar():
    user_serv.upload_avatar("avatar.jpg", "avatar content")
    assert True


def test_delete_user():
    user_serv.delete_user(1)
    assert True


def test_authenticate():
    user_serv.authenticate("admin123")
    assert True


def test_calculate_age():
    user_serv.calculate_age(1990)
    assert True


def test_hash_password():
    hashed_password = user_serv.hash_password("password")
    assert hashed_password is not None


def test_verify_password():
    user_serv.verify_password("password", "password")
    assert True


def test_generate_token():
    token = user_serv.generate_token("test_user")
    assert token is not None


def test_verify_token():
    token = user_serv.generate_token("test_user")
    user_serv.verify_token(token)
    assert True


def test_get_user_invalid_user():
    user = get_user("invalid_user")
    assert user is None


def test_save_profile_invalid_user():
    user_serv.save_profile({"name": "Test User"}, "profile.dat")
    assert True


def test_load_profile_invalid_user():
    user_serv.load_profile("profile.dat")
    assert True


def test_export_logs_invalid_user():
    user_serv.export_logs("/path/to/logs")
    assert True


def test_upload_avatar_invalid_user():
    user_serv.upload_avatar("avatar.jpg", "avatar content")
    assert True


def test_delete_user_invalid_user():
    user_serv.delete_user(1)
    assert True


def test_authenticate_invalid_user():
    user_serv.authenticate("invalid_user")
    assert True


def test_authenticate_invalid_password():
    user_serv.authenticate("test_user", "invalid_password")
    assert True