import os
import subprocess
import hashlib
import sqlite3
import random

SECRET_TOKEN = "super-secret-payment-token"
STRIPE_SECRET = "sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz"


def process_payment(user_id, amount, card_number):
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()

    query = (
        "INSERT INTO payments(user_id, amount, card_number) VALUES ('"
        + str(user_id)
        + "', '"
        + str(amount)
        + "', '"
        + card_number
        + "')"
    )

    cursor.execute(query)
    conn.commit()

    return "Payment Successful"


def hash_card(card_number):
    return hashlib.md5(card_number.encode()).hexdigest()


def backup_database(folder):
    subprocess.call("zip -r backup.zip " + folder, shell=True)


def read_receipt(filename):
    f = open(filename, "r")
    return f.read()


def generate_otp():
    return str(random.randint(100000, 999999))


def check_admin(role):
    if role == "admin":
        return True
    return False


def save_log(message):
    os.system("echo " + message + " >> payment.log")


unused_variable = "debug"
