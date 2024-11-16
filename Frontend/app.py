import streamlit as st
import json
import os
import uuid
import streamlit as st


# Mostra una imatge des d'una URL
st.image("datathon.png")
# Ruta al itxer JSON
JSON_FILE_PATH = "datathon_participants.json"

# Carregar dades existents o crear una llista buida
if os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, "r") as file:
        participants = json.load(file)
else:
    participants = []

# Títol de l'aplicació
st.title("Formulari de Participants - Datathon FME 2024")

# Descripció
st.write("Emplena aquest formulari per registrar un participant al Datathon. Les dades s'afegiran automàticament al fitxer JSON.")

# Formulari per recollir les dades
with st.form(key="participant_form"):
    # Camps bàsics
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

    # Interessos
    interests = st.multiselect(
        "Selecciona els teus interessos:",
        ["Machine Learning/AI", "Gaming", "E-commerce/Retail", "Productivity", "Web", 
         "Music/Art", "Quantum", "Databases", "DevOps"]
    )

    # Rol preferit
    preferred_role = st.selectbox(
        "Rol preferit:", 
        ["Analysis", "Visualization", "Development", "Design", "Don't know"]
    )

    # Experiència
    experience_level = st.selectbox(
        "Nivell d'experiència:",
        ["Beginner", "Intermediate", "Advanced"]
    )
    hackathons_done = st.number_input(
        "Nombre de hackathons completats:", min_value=0, step=1
    )

    # Objectius i introducció
    objective = st.text_area("Objectiu principal:")
    introduction = st.text_area("Introdueix-te breument:")

    # Projectes tècnics
    technical_project = st.text_area("Descriu un projecte tècnic que hagis realitzat:")

    # Expectatives de futur
    future_excitement = st.text_area("Quines són les teves expectatives pel futur?")

    # Dada curiosa
    fun_fact = st.text_input("Fes-nos saber una curiositat sobre tu:")

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

    # Habilitats tècniques
    st.write("### Habilitats de programació:")
    programming_skills = {
        "Data Visualization": st.slider("Data Visualization", 1, 10, 5),
        "Flask": st.slider("Flask", 1, 10, 5),
        "React": st.slider("React", 1, 10, 5),
        "MongoDB": st.slider("MongoDB", 1, 10, 5)
    }

    # Reptes d'interès
    interest_in_challenges = st.multiselect(
        "Reptes d'interès:",
        ["Mango Challenge", "Restb.ai Challenge", "AED Challenge"]
    )


    

    # Botó d'enviament
    submit_button = st.form_submit_button(label="Enviar")

    if submit_button:
        # Crear una ID única per al participant
        participant_id = str(uuid.uuid4())

        # Crear l'objecte del participant
        new_participant = {
            "id": participant_id,
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
            "preferred_team_size": preferred_team_size,
            "availability": availability,
            "programming_skills": programming_skills,
            "interest_in_challenges": interest_in_challenges
        }

        # Afegir el nou participant al fitxer
        participants.append(new_participant)

        # Escriure al fitxer JSON
        with open(JSON_FILE_PATH, "w") as file:
            json.dump(participants, file, indent=4)

        st.success("Participant afegit i dades desades correctament!")
        st.json(new_participant)  # Mostrar dades afegides
