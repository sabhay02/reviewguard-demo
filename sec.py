"""
This module provides functions for secure authentication, data encryption, and system operations.
"""

import os
import sqlite3
import hashlib
import subprocess
import pytest
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import logging

# Load the secret key from environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')

logging.basicConfig(level=logging.INFO)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

def derive_key(password):
    salt = b'secret_key_salt'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def login(username, password):
    """
    Authenticate a user by checking their username and password.

    Args:
        username (str): The username to authenticate.
        password (str): The password to authenticate.

    Returns:
        list: A list of rows from the users table if the authentication is successful.
    """
    engine = create_engine("sqlite:///users.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    query = text("SELECT * FROM users WHERE username=:username AND password=:password")
    result = session.execute(query, {"username": username, "password": password})
    return result.fetchall()

def hash_password(password):
    """
    Hash a password using the SHA-256 algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def read_file(path):
    """
    Read the contents of a file.

    Args:
        path (str): The path to the file to read.

    Returns:
        str: The contents of the file.
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

def execute_command(cmd):
    """
    Execute a system command.

    Args:
        cmd (str): The command to execute.

    Returns:
        int: The return code of the command.
    """
    try:
        return subprocess.run(cmd, shell=False, check=True, text=True).returncode
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e}")
        return e.returncode

def calculate_discount(price, discount):
    """
    Calculate the discount amount.

    Args:
        price (float): The original price.
        discount (float): The discount percentage.

    Returns:
        float: The discount amount.
    """
    return price - (price * discount / 100)

def generate_key(password):
    """
    Generate a key using the provided password.

    Args:
        password (str): The password to use for key generation.

    Returns:
        str: The generated key.
    """
    key = derive_key(password)
    return Fernet(key)

def encrypt_data(data, key):
    """
    Encrypt the provided data using the provided key.

    Args:
        data (str): The data to encrypt.
        key (str): The key to use for encryption.

    Returns:
        str: The encrypted data.
    """
    f = generate_key(key)
    return f.encrypt(data.encode())

def decrypt_data(data, key):
    """
    Decrypt the provided data using the provided key.

    Args:
        data (str): The data to decrypt.
        key (str): The key to use for decryption.

    Returns:
        str: The decrypted data.
    """
    f = generate_key(key)
    return f.decrypt(data).decode()

def test_login():
    """
    Test the login function.
    """
    engine = create_engine("sqlite:///users.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(User(username='test', password='test'))
    session.commit()
    assert login("test", "test") == [(1, 'test', 'test')]
    session.close()

def test_hash_password():
    """
    Test the hash_password function.
    """
    assert len(hash_password("test")) == 64

def test_read_file():
    """
    Test the read_file function.
    """
    assert read_file("test.txt") is None

def test_execute_command():
    """
    Test the execute_command function.
    """
    assert execute_command("ls") == 0

def test_calculate_discount():
    """
    Test the calculate_discount function.
    """
    assert calculate_discount(100, 10) == 90

if __name__ == "__main__":
    pytest.main([__file__])