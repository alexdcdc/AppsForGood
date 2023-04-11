import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import json

creds = credentials.Certificate('C:\\Users\\alexd\\OneDrive\\Documents\\AppsForGood\\buzzwordsapp-38fcc-firebase-adminsdk-v6je1-0fbe782350.json')
app = firebase_admin.initialize_app(creds, {'databaseURL' : 'https://buzzwordsapp-38fcc-default-rtdb.firebaseio.com/'})

ref = db.reference("/")

'''
Name: 
DBWrite

Purpose:
Sets the contents of Buzzwords realtime database to inputted dictionary/json.

Input:
content -- the dictionary to write to the database
'''
def DBWrite(content: dict): 
	ref.set(content)