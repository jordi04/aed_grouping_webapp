import streamlit as st
import firebase_admin
import json
import os
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


# Inicializar estado de la página
if "page" not in st.session_state:
    st.session_state.page = 1  # Página inicial

# Función para manejar el cambio de página
def next_page():
    st.session_state.page += 1
    page = st.session_state.page

def prev_page():
    st.session_state.page -= 1
    page = st.session_state.page

a=0
# Initialize session state for each section if not already present
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

# Streamlit form to add participants
st.title("Formulari de Participants - Datathon FME 2024")
st.logo("https://www.datathon.cat/_app/immutable/assets/accentLogo.ICfS56oN.png")

if st.session_state.page == 1:
    with st.form(key="participant_form"):
        st.header("Secció 1: Informació Bàsica")
        name = st.text_input("Nom del participant:")
        email = st.text_input("Email:")
        age = st.number_input("Edat:", min_value=10, max_value=100, step=1)
        year_of_study = st.selectbox(
            "Curs acadèmic:", 
            ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"]
        )
        submit = st.form_submit_button("Siguiente")
        if submit:
            IB = {
            "name": name,
            "email": email,
            "age": age,
            "year_of_study": year_of_study
            }
            if submit:
                next_page()


elif st.session_state.page == 2:
    with st.form(key="participant_form"):    
        st.header("Secció 2: Detalls Personals")
        shirt_size = st.selectbox(
            "Talla de samarreta:", 
            ["S", "M", "L", "XL"]
        )
        university = st.text_input("Universitat:")
        dietary_restrictions = st.selectbox(
            "Restriccions alimentàries:", 
            ["None", "Vegetarian", "Vegan", "Gluten-free", "Other"]
        )

        experience_level = st.selectbox(
            "Nivell d'experiència:",
            ["Beginner", "Intermediate", "Advanced"]
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            DP= {
            "shirt_size": shirt_size,
            "university": university,
            "dietary_restrictions": dietary_restrictions,
            "experience_level": experience_level,
            }
            next_page()

elif st.session_state.page == 3:
    st.header("Secció 3: Habilitats")
    
    # Llista predefinida d'habilitats
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
    
    st.title("Selecció d'Habilitats amb Nivells")

    # Selecció d'habilitats amb desplegable (multiselect)
    selected_skills = st.multiselect(
        label="Escriu o selecciona habilitats des de la llista:",
        options=available_skills,
        help="Fes clic per veure totes les opcions disponibles o comença a escriure per filtrar."
    )

    # Ajusta nivells per a habilitats seleccionades
    skill_levels = {}
    if selected_skills:
        for skill in selected_skills:
            skill_levels[skill] = st.slider(f"Nivell de {skill}:", 0, 10, 5, key=f"{skill}_slider")
            if skill_levels[skill] == 0:
                del skill_levels[skill]
            if selected_skills:
                a = 1
    # Formulario para navegar entre páginas (fuera de la parte de las habilitats)
    if a == 1:
        with st.form(key="participant_form"):
            col1, col2 = st.columns(2)
            with col1:
                prev = st.form_submit_button("Anterior")
            with col2:
                next_ = st.form_submit_button("Siguiente")
        
        if prev:
            prev_page()  # Función para navegar a la página anterior (definida en tu código)
        if next_:
            next_page()  # Función para navegar a la siguiente página (definida en tu código)

elif st.session_state.page == 4:
    with st.form(key="participant_form"):
        st.header("Secció 4: Detalls Addicionals")
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

        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            DA = {
            "hackathons_done": hackathons_done,
            "interests": interests,
            "preferred_role": preferred_role,
            "objective": objective
            }
            next_page()

elif st.session_state.page == 5:
    with st.form(key="participant_form"):
        st.header("Secció 5: Preferències")
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

        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            P = {
            "interest_in_challenges": interest_in_challenges,
            "preferred_languages": preferred_languages,
            "friend_registration": friend_registration,
            "preferred_team_size": preferred_team_size
            }
            next_page()

elif st.session_state.page == 6:
    with st.form(key="participant_form"):
        st.header("Secció 6: Detalls Addicionals")
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
        
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Anterior")
        with col2:
            next_ = st.form_submit_button("Siguiente")
        if prev:
            prev_page()
        if next_:
            Disp= {
            "availability": availability,
            "introduction": introduction,
            "technical_project": technical_project,
            "future_excitement": future_excitement,
            "fun_fact": fun_fact
            }
            next_page()
    
        
elif st.session_state.page == 7:
    st.header("Resum i Confirmació")
    
    # Mostrem les dades recopilades fins ara
    st.subheader("Informació recopilada:")
    participant_data = {
        "Informació Bàsica": IB,
        "Detalls Personals": DP,
        #"Habilitats": skill_levels,
        "Detalls Addicionals": DA,
        "Preferències": P,
        "Disponibilitat": Disp
    }
    
    # Mostra les dades de forma estructurada
    for section, data in participant_data.items():
        st.write(f"### {section}")
        if isinstance(data, dict):
            for key, value in data.items():
                st.write(f"- **{key}**: {value}")
        else:
            st.write(data)
    
    # Form per confirmar i enviar
    with st.form(key="confirmation_form"):
        submit_button = st.form_submit_button(label="Enviar")
        
        if submit_button:
            # Unim totes les dades en un sol diccionari
            full_participant_data = {
                "basic_info": IB,
                "personal_details": DP,
                #"skills": skill_levels,
                "additional_details": DA,
                "preferences": P,
                "availability": Disp
            }
            print(full_participant_data)
            # Guardem les dades del participant al fitxer "DatathonParticipants.json"

            json_file = "DatathonParticipants.json"

            # Comprovem si el fitxer ja existeix
            if os.path.exists(json_file):
                with open(json_file, "r") as file:
                    participants = json.load(file)
            else:
                participants = []

            # Afegim les noves dades del participant
            participants.append(full_participant_data)

            # Guardem les dades actualitzades al fitxer JSON
            with open(json_file, "w") as file:
                json.dump(participants, file, indent=4, ensure_ascii=False)
            
            try:
                # Enviem les dades a Firebase Firestore
                participants_ref.add(full_participant_data)
                st.success("Les dades s'han enviat correctament!")
                st.balloons()
            except Exception as e:
                st.error(f"Error en enviar les dades: {e}")
