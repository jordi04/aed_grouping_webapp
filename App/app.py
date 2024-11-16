import streamlit as st
import firebase_admin
from streamlit_tags import st_tags
from firebase_admin import credentials, firestore

# Initialize Firebase only if it hasn't been initialized already
if not firebase_admin._apps:  # Check if any Firebase app is initialized
    cred = credentials.Certificate("firebaseCred.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Reference to the collection of participants
participants_ref = db.collection("participants")

# Predefined list of programming skills
available_skills = [
    "Python", "C++", "JavaScript", "SQL", "TensorFlow", 
    "PyTorch", "Docker", "HTML/CSS", "Data Analysis", 
    "Natural Language Processing", "Java", "Go", 
    "Rust", "Figma", "Flask", "React", "React Native", 
    "PostgreSQL", "AWS/Azure/GCP", "IoT", "Machine Learning", 
    "DevOps", "Android Development", "iOS Development", 
    "UI/UX Design", "Git", "Blockchain", "Computer Vision", 
    "Data Visualization"
]

# Streamlit form to add participants
st.title("Formulari de Participants - Datathon FME 2024")
st.logo("https://www.datathon.cat/_app/immutable/assets/accentLogo.ICfS56oN.png")
with st.form(key="participant_form"):
    # Fields for participant data
    name = st.text_input("Nom del participant:")
    email = st.text_input("Email:")
    age = st.number_input("Edat:", min_value=10, max_value=100, step=1)
    year_of_study = st.selectbox(
        "Curs acadèmic:", 
        ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"]
    )
    shirt_size = st.selectbox(
        "Talla de samarreta:", 
        ["S", "M", "L", "XL"]
    )
    university = st.text_input("Universitat:")
    dietary_restrictions = st.selectbox(
        "Restriccions alimentàries:", 
        ["None", "Vegetarian", "Vegan", "Gluten-free", "Other"]
    )
    
    selected_skills = st.multiselect(
        "Escriu o selecciona habilitats des de la llista:",
        options=available_skills
    )
    #afegir slider per a cada skill
    experience_level = st.selectbox(
        "Nivell d'experiència:",
        ["Beginner", "Intermediate", "Advanced"]
    )
    hackathons_done = st.number_input(
        "Nombre de hackathons completats:", min_value=0, step=1
    )
    interests = st.multiselect( #uhgsuygizgcs
        "Selecciona els teus interessos:",
        ["Machine Learning/AI", "Gaming", "E-commerce/Retail", "Productivity", "Web", 
         "Music/Art", "Quantum", "Databases", "DevOps"] #afegir més interessos
    )
    preferred_role = st.selectbox(
        "Rol preferit:", 
        ["Analysis", "Visualization", "Development", "Design"]
    )
    
    objective = st.text_area("Objectiu principal:")
    
    #INTERESTS in challenges
    interest_in_challenges = st.multiselect(
        "Reptes d'interès:",
        ["Mango Challenge", "Restb.ai Challenge", "AED Challenge"]
    )

    # Idiomes preferits
    preferred_languages = st.multiselect(
        "Idiomes preferits:",
        ["English", "Catalan", "Spanish", "French", "German", "Italian"]
    )

    # Amics registrats
    friend_registration = st.text_area(
        "Identificadors (UUID) d'amics registrats (separats per comes):"
    )
    friend_registration = [
        friend.strip() for friend in friend_registration.split(",") if friend.strip()
    ]

    # Mida preferida de l'equip
    preferred_team_size = st.slider("Mida preferida de l'equip:", 1, 5, 4)

    # Disponibilitat
    st.write("### Disponibilitat:")
    availability = {
        "Saturday morning": st.checkbox("Dissabte matí"),
        "Saturday afternoon": st.checkbox("Dissabte tarda"),
        "Saturday night": st.checkbox("Dissabte nit"),
        "Sunday morning": st.checkbox("Diumenge matí"),
        "Sunday afternoon": st.checkbox("Diumenge tarda"),
    }

    introduction = st.text_area("Introdueix-te breument:")

    # Projectes tècnics
    technical_project = st.text_area("Descriu un projecte tècnic que hagis realitzat:")

    # Expectatives de futur
    future_excitement = st.text_area("Quines són les teves expectatives pel futur?")

    # Dada curiosa
    fun_fact = st.text_input("Fes-nos saber una curiositat sobre tu:")


    
    
    # Submit button
    submit_button = st.form_submit_button(label="Enviar")

    if submit_button:
        # Create the new participant entry
        new_participant = {
            "name": name,
            "email": email,
            "age": age,
            "year_of_study": year_of_study,
            "shirt_size": shirt_size,
            "university": university,
            "dietary_restrictions": dietary_restrictions,
            "interests": interests,
            "preferred_role": preferred_role,
            "experience_level": experience_level,
            "hackathons_done": hackathons_done,
            "objective": objective,
            "introduction": introduction,
            "technical_project": technical_project,
            "future_excitement": future_excitement,
            "fun_fact": fun_fact,
            "preferred_languages": preferred_languages,
            "friend_registration": friend_registration,
            "preferred_team_size": preferred_team_size
        }

        # Add new participant to Firestore
        participants_ref.add(new_participant)

        st.success("Participant afegit correctament!")
