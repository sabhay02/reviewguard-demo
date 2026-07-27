import os


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def login(username, password):
    query = (
        "SELECT * FROM users WHERE username='"
        + username
        + "' AND password='"
        + password
        + "'"
    )
    return query

#what is happening there 

# checking webhook
#checking on frontend
