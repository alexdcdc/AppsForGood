'''
Name: 
buzzwords-database.py

Purpose:
Contains a variety of different functions for performing 
CRUD operations on the Buzzwords database.

Used by:
main.py
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import os

cwd = os.getcwd()

creds = credentials.Certificate(os.path.join(cwd, "buzzwordsapp-38fcc-firebase-adminsdk-v6je1-0fbe782350.json"))
app = firebase_admin.initialize_app(creds, {'databaseURL' : 'https://buzzwordsapp-38fcc-default-rtdb.firebaseio.com/'})

ref = db.reference("/")

# Writes json/dictionary content to the database.
def DBWrite(path: str, content: dict): 
	ref = db.reference(path)
	ref.set(content)

def DBPush(path: str, content: dict):
	ref = db.reference(path)
	for k in content:
		if not (ref.child(k).get()):
			ref.child(k).set(content[k])

if __name__ == "__main__":
	DBPush("/bababooie/", {"baba" : "booie", "jonathan": "seena"})
	