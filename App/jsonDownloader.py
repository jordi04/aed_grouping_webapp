import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebaseCred.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Reference to the collection where participants are stored
participants_ref = db.collection("participants")

# Get all documents in the collection
participants = participants_ref.stream()

# Create a list to hold participant data
participants_data = []

# Iterate through the documents and add them to the list
for participant in participants:
    participants_data.append(participant.to_dict())

# Write the data to a local JSON file
with open("datathon_participants.json", "w") as file:
    json.dump(participants_data, file, indent=4)

print("Firestore data downloaded to JSON file successfully!")
