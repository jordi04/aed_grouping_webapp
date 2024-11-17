import streamlit as st
import firebase_admin
import json
import os
from firebase_admin import credentials, firestore
import uuid  # Afegeix això a l'inici del fitxer


# Initialize Firebase only if it hasn't been initialized already
if not firebase_admin._apps:  # Check if any Firebase app is initialized
    cred = credentials.Certificate("firebaseCred.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()
st.logo("https://www.datathon.cat/_app/immutable/assets/accentLogo.ICfS56oN.png")
# Reference to the collection of participants
participants_ref = db.collection("participants")

# Inicialitza les variables del session_state
if "ID" not in st.session_state:
    st.session_state.ID = str(uuid.uuid4())  # Genera un ID únic
    
# Initialize session state for persistent storage
if "page" not in st.session_state:
    st.session_state.page = 1

if "IB" not in st.session_state:
    st.session_state.IB = {}

if "DP" not in st.session_state:
    st.session_state.DP = {}

if "DA" not in st.session_state:
    st.session_state.DA = {}

if "P" not in st.session_state:
    st.session_state.P = {}

if "Disp" not in st.session_state:
    st.session_state.Disp = {}

if "skills" not in st.session_state:
    st.session_state.skills = {}

# Page navigation functions
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# Page 1: Informació Bàsica
if st.session_state.page == 1:
    with st.form(key="participant_form"):
        st.header("Secció 1: Informació Bàsica")
        name = st.text_input("Nom del participant:", st.session_state.IB.get("name", ""))
        email = st.text_input("Email:", st.session_state.IB.get("email", ""))
        age = st.number_input("Edat:", min_value=10, max_value=100, step=1, value=st.session_state.IB.get("age", 18))
        year_of_study = st.selectbox(
            "Curs acadèmic:", 
            ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"], 
            index=["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"].index(st.session_state.IB.get("year_of_study", "1st year"))
        )
        submit = st.form_submit_button("Siguiente")
        if submit:
            st.session_state.IB = {
                "name": name,
                "email": email,
                "age": age,
                "year_of_study": year_of_study
            }
            next_page()

# Page 2: Detalls Personals
elif st.session_state.page == 2:
    with st.form(key="participant_form_dp"):
        st.header("Secció 2: Detalls Personals")
        shirt_size = st.selectbox(
            "Talla de samarreta:", 
            ["S", "M", "L", "XL"], 
            index=["S", "M", "L", "XL"].index(st.session_state.DP.get("shirt_size", "S"))
        )
        university = st.text_input(
            "Universitat:", 
            value=st.session_state.DP.get("university", "")
        )
        dietary_restrictions = st.selectbox(
            "Restriccions alimentàries:", 
            ["None", "Vegetarian", "Vegan", "Gluten-free", "Other"],
            index=["None", "Vegetarian", "Vegan", "Gluten-free", "Other"].index(st.session_state.DP.get("dietary_restrictions", "None"))
        )
        experience_level = st.selectbox(
            "Nivell d'experiència:", 
            ["Beginner", "Intermediate", "Advanced"],
            index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.DP.get("experience_level", "Beginner"))
        )

        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")

        if prev:
            prev_page()
        if next_:
            # Store the updated inputs in the session state
            st.session_state.DP.update({
                "shirt_size": shirt_size,
                "university": university,
                "dietary_restrictions": dietary_restrictions,
                "experience_level": experience_level
            })
            next_page()

# Page 3: Habilitats
elif st.session_state.page == 3:
    st.header("Secció 3: Habilitats")
    available_skills = [
        "Python", "C++", "JavaScript", "SQL", "TensorFlow", "PyTorch", "Docker", "HTML/CSS",
        "Data Analysis", "Natural Language Processing", "Java", "Go", "Rust", "Figma", "Flask",
        "React", "React Native", "PostgreSQL", "AWS/Azure/GCP", "IoT", "Machine Learning",
        "Android Development", "iOS Development", "UI/UX Design", "Git", 
        "Blockchain", "Computer Vision", "Data Visualization"
    ]
    selected_skills = st.multiselect(
        "Selecciona habilitats:",
        options=available_skills,
        default=list(st.session_state.skills.keys())
    )
    skill_levels = {skill: st.slider(f"Nivell per {skill}:", 0, 10, value=st.session_state.skills.get(skill, 5)) for skill in selected_skills}
    col1, col2 = st.columns(2)
    with col1:
        prev = st.button("Anterior")
    with col2:
        next_ = st.button("Siguiente")
    if prev:
        prev_page()
    if next_:
        st.session_state.skills = skill_levels
        next_page()

# Page 4: Detalls Addicionals
elif st.session_state.page == 4:
    with st.form(key="additional_details_form"):
        st.header("Secció 4: Detalls Addicionals")
        hackathons_done = st.number_input(
            "Nombre de hackathons completats:", 
            min_value=0, 
            step=1, 
            value=st.session_state.DA.get("hackathons_done", 0)
        )
        interests = st.multiselect(
            "Selecciona els teus interessos:",
            ["Machine Learning/AI", "Gaming", "E-commerce/Retail", "Productivity", "Web", 
             "Music/Art", "Quantum", "Databases", "DevOps"],
            default=st.session_state.DA.get("interests", [])
        )
        preferred_role = st.selectbox(
            "Rol preferit:", 
            ["Analysis", "Visualization", "Development", "Design"],
            index=["Analysis", "Visualization", "Development", "Design"].index(
                st.session_state.DA.get("preferred_role", "Analysis")
            )
        )
        objective = st.text_area(
            "Objectiu principal:", 
            value=st.session_state.DA.get("objective", "")
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            st.session_state.DA = {
                "hackathons_done": hackathons_done,
                "interests": interests,
                "preferred_role": preferred_role,
                "objective": objective
            }
            next_page()

# Page 5: Preferències
elif st.session_state.page == 5:
    with st.form(key="preferences_form"):
        st.header("Secció 5: Preferències")
        interest_in_challenges = st.multiselect(
            "Reptes d'interès:",
            ["Mango Challenge", "Restb.ai Challenge", "AED Challenge"],
            default=st.session_state.P.get("interest_in_challenges", [])
        )
        preferred_languages = st.multiselect(
            "Idiomes preferits:",
            ["English", "Catalan", "Spanish", "French", "German", "Italian"],
            default=st.session_state.P.get("preferred_languages", [])
        )
        friend_registration = st.text_area(
            "Identificadors (UUID) d'amics registrats (separats per comes):",
            value=", ".join(st.session_state.P.get("friend_registration", []))
        )
        friend_registration_list = [
            friend.strip() for friend in friend_registration.split(",") if friend.strip()
        ]
        preferred_team_size = st.slider(
            "Mida preferida de l'equip:", 
            min_value=1, 
            max_value=4, 
            value=st.session_state.P.get("preferred_team_size", 4)
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            st.session_state.P = {
                "interest_in_challenges": interest_in_challenges,
                "preferred_languages": preferred_languages,
                "friend_registration": friend_registration_list,
                "preferred_team_size": preferred_team_size
            }
            next_page()

# Page 6: Disponibilitat
elif st.session_state.page == 6:
    with st.form(key="availability_form"):
        st.header("Secció 6: Disponibilitat")
        availability = {
            "Saturday morning": st.checkbox(
                "Dissabte matí", value=st.session_state.Disp.get("availability", {}).get("Saturday morning", False)
            ),
            "Saturday afternoon": st.checkbox(
                "Dissabte tarda", value=st.session_state.Disp.get("availability", {}).get("Saturday afternoon", False)
            ),
            "Saturday night": st.checkbox(
                "Dissabte nit", value=st.session_state.Disp.get("availability", {}).get("Saturday night", False)
            ),
            "Sunday morning": st.checkbox(
                "Diumenge matí", value=st.session_state.Disp.get("availability", {}).get("Sunday morning", False)
            ),
            "Sunday afternoon": st.checkbox(
                "Diumenge tarda", value=st.session_state.Disp.get("availability", {}).get("Sunday afternoon", False)
            ),
        }
        introduction = st.text_area(
            "Introdueix-te breument:", value=st.session_state.Disp.get("introduction", "")
        )
        technical_project = st.text_area(
            "Descriu un projecte tècnic que hagis realitzat:", 
            value=st.session_state.Disp.get("technical_project", "")
        )
        future_excitement = st.text_area(
            "Quines són les teves expectatives pel futur?", 
            value=st.session_state.Disp.get("future_excitement", "")
        )
        fun_fact = st.text_input(
            "Fes-nos saber una curiositat sobre tu:", 
            value=st.session_state.Disp.get("fun_fact", "")
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            st.session_state.Disp = {
                "availability": availability,
                "introduction": introduction,
                "technical_project": technical_project,
                "future_excitement": future_excitement,
                "fun_fact": fun_fact
            }
            next_page()

# Page 7: Resum i Confirmació
elif st.session_state.page >= 7:
    st.header("Secció 7: Enviar")
    

    # Prepare the final data format
    participant_data = {
        "id": st.session_state.ID,  # Example for ID - ensure you set this earlier in the flow
        "name": st.session_state.IB.get("name", ""),
        "email": st.session_state.IB.get("email", ""),
        "age": st.session_state.IB.get("age", 0),
        "year_of_study": st.session_state.IB.get("year_of_study", ""),
        "shirt_size": st.session_state.DP.get("shirt_size", ""),
        "university": st.session_state.DP.get("university", ""),
        "dietary_restrictions": st.session_state.DP.get("dietary_restrictions", ""),
        "interests": st.session_state.DA.get("interests", []),
        "preferred_role": st.session_state.DA.get("preferred_role", ""),
        "experience_level": st.session_state.DP.get("experience_level", ""),
        "hackathons_done": st.session_state.DA.get("hackathons_done", 0),
        "objective": st.session_state.DA.get("objective", ""),
        "introduction": st.session_state.DA.get("introduction", ""),
        "technical_project": st.session_state.DA.get("technical_project", ""),
        "future_excitement": st.session_state.DA.get("future_excitement", ""),
        "fun_fact": st.session_state.DA.get("fun_fact", ""),
        "preferred_languages": st.session_state.P.get("preferred_languages", []),
        "friend_registration": st.session_state.P.get("friend_registration", []),
        "preferred_team_size": st.session_state.P.get("preferred_team_size", 0),
        "availability": st.session_state.Disp.get("availability", {}),
        "programming_skills": st.session_state.skills,  # Assuming skills are pre-collected in correct format
        "interest_in_challenges": st.session_state.P.get("interest_in_challenges", [])
    }


    # Submit button
    submit = st.button("Enviar")
    if submit:
        try:
            st.session_state.page += 1;
            # Save the data to Firestore
            if st.session_state.page == 8:
                participants_ref.document().set(participant_data)

            st.success("Les dades s'han enviat correctament!")
            st.header("Gràcies per registrar-te!")
            st.write("La teva inscripció s'ha completat amb èxit. Ens veiem a l'esdeveniment!")
            st.write("El teu ID d'usuari és:", st.session_state.ID, " Guarda aquest ID per a futura referència, molt important.")
            st.balloons()
        except Exception as e:
            st.error(f"Error en enviar les dades: {e}")

