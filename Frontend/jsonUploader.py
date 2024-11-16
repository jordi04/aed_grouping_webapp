import json
import firebase_admin
from firebase_admin import credentials, firestore

st.write("### Habilitats de programació:")
    programming_skills = {
        skill: st.slider(skill, 0, 10, 0) for skill in [
            "Python", "C++", "JavaScript", "SQL", "TensorFlow", 
            "PyTorch", "Docker", "HTML/CSS", "Data Analysis", 
            "Natural Language Processing", "Java", "Go", 
            "Rust", "Figma", "Flask", "React", "React Native", 
            "PostgreSQL", "AWS/Azure/GCP", "IoT", "Machine Learning", 
            "DevOps", "Android Development", "iOS Development", 
            "UI/UX Design", "Git", "Blockchain", "Computer Vision", 
            "Data Visualization"
        ]
    }
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
