'''
Name:
buzzwords-database.py

Purpose:
Contains a variety of different functions for performing
CRUD operations on the Buzzwords database.

Used by:
main.py
'''

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cwd = os.getcwd()

creds = credentials.Certificate(os.path.join(
    cwd, "buzzwordsapp-38fcc-firebase-adminsdk-v6je1-0fbe782350.json"))
app = firebase_admin.initialize_app(
    creds, {'databaseURL': 'https://buzzwordsapp-38fcc-default-rtdb.firebaseio.com/'})


# Writes json/dictionary content to the database.
def DBWrite(path: str, content: dict):
    ref = db.reference(path)
    ref.set(content)


# Appends json/dictionary content to the database if existent, else writes to the database.
def DBPush(path: str, content: dict):
    ref = db.reference(path)
    for k in content:
        ref.child(k).set(content[k])


# Tests pushing function to database using user input
def PushTest():
    print("------RUNNING TEST: UPDATING------")
    push = input("Enter string to be updated to database: ")
    DBPush("test", {"TestPush": push + "a", "ttt": push + "a"})


# Tests writing function to database using user input
def WriteTest():
    print("------RUNNING TESTS: SETTING------")
    push = input("Enter string to be written to database: ")
    DBWrite("test", {"TestWrite": push})


if __name__ == "__main__":
    pass