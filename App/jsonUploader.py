import json
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase
cred = credentials.Certificate("firebaseCred.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Reference to the collection where participants will be stored
participants_ref = db.collection("participants")

# Read the local JSON file
with open("datathon_participants.json", "r") as file:
    participants_data = json.load(file) 

# Assuming the JSON data is an array of participant objects
for participant in participants_data:
    # Add each participant to Firestore
    participants_ref.add(participant)

print("JSON data uploaded to Firestore successfully!")
