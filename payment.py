"""
Payment module for handling payment-related operations.

This module provides functions for processing payments, hashing card numbers,
backing up the database, reading receipts, generating one-time passwords (OTPs),
and checking user roles.
"""

import os
import subprocess
import hashlib
import sqlite3
import secrets
import pytest
from sqlite3 import Error
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text

SECRET_TOKEN = os.environ.get('SECRET_TOKEN')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')

def process_payment(user_id, amount, card_number):
    """
    Process a payment by inserting the payment details into the database.

    Args:
        user_id (int): The ID of the user making the payment.
        amount (float): The amount of the payment.
        card_number (str): The card number used for the payment.

    Returns:
        str: A success message indicating that the payment was processed successfully.
    """
    try:
        engine = create_engine("sqlite:///payments.db")
        with engine.connect() as conn:
            query = text("INSERT INTO payments(user_id, amount, card_number) VALUES (:user_id, :amount, :card_number)")
            conn.execute(query, {"user_id": user_id, "amount": amount, "card_number": card_number})
        return "Payment Successful"
    except Error as e:
        return f"Error processing payment: {e}"

def hash_card(card_number):
    """
    Hash a card number using the SHA-256 algorithm.

    Args:
        card_number (str): The card number to be hashed.

    Returns:
        str: The hashed card number.
    """
    return hashlib.sha256(card_number.encode()).hexdigest()

def backup_database(folder):
    """
    Backup the database by creating a zip file of the specified folder.

    Args:
        folder (str): The folder to be backed up.
    """
    try:
        subprocess.run(["zip", "-r", "backup.zip", folder], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error backing up database: {e}")

def read_receipt(filename):
    """
    Read the contents of a receipt file.

    Args:
        filename (str): The name of the receipt file.

    Returns:
        str: The contents of the receipt file.
    """
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Receipt file not found"

def generate_otp():
    """
    Generate a random one-time password (OTP).

    Returns:
        str: The generated OTP.
    """
    return str(secrets.randbelow(900000) + 100000)

def check_admin(role):
    """
    Check if a user has the admin role.

    Args:
        role (str): The role of the user.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    return role == "admin"

def encrypt_data(data):
    """
    Encrypt data using Fernet.

    Args:
        data (str): The data to be encrypted.

    Returns:
        str: The encrypted data.
    """
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text.decode()

def decrypt_data(data):
    """
    Decrypt data using Fernet.

    Args:
        data (str): The data to be decrypted.

    Returns:
        str: The decrypted data.
    """
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(data.encode())
    return plain_text.decode()

def test_process_payment():
    """
    Test the process_payment function.
    """
    assert process_payment(1, 10.99, "1234567890123456") == "Payment Successful"

def test_hash_card():
    """
    Test the hash_card function.
    """
    assert len(hash_card("1234567890123456")) == 64

def test_backup_database():
    """
    Test the backup_database function.
    """
    backup_database("test_folder")

def test_read_receipt():
    """
    Test the read_receipt function.
    """
    assert read_receipt("receipt.txt") == "Receipt contents"

def test_generate_otp():
    """
    Test the generate_otp function.
    """
    assert len(generate_otp()) == 6

def test_check_admin():
    """
    Test the check_admin function.
    """
    assert check_admin("admin") == True

if __name__ == "__main__":
    pytest.main([__file__])