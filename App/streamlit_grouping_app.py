import streamlit as st
import subprocess
import pandas as pd
import time
import json

# Estils CSS personalitzats per adaptar l'estil de la pàgina
def add_custom_styles():
    st.markdown(
        """
        <style>
        /* Fons general */
        .stApp {
            background-color: #ffffff;
            font-family: 'Arial', sans-serif;
        }

        /* Contenidor dels logos */
        .logos-container {
            position: fixed;
            top: 50px; /* Ajustem la distància des de la part superior */
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 30px;
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
        }
        .logos-container img {
            height: 80px;
        }
        .logos-container.hidden {
            opacity: 0;
            visibility: hidden;
        }

        /* Títol principal */
        .main-title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #2e2e2e;
            margin-top: 70px; /* Afegim espai respecte als logos */
            margin-bottom: 10px;
        }

        /* Subtítol */
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #8c8c8c;
            margin-bottom: 30px;
        }

        /* Botó personalitzat */
        div.stButton > button {
            display: block;
            margin: 20px auto; /* Centra el botó */
            background-color: #3c948c; /* Verd elegant */
            color: white; /* Text blanc */
            font-size: 18px; /* Mida del text */
            font-weight: bold; /* Text en negreta */
            border-radius: 12px; /* Vores arrodonides */
            padding: 10px 20px; /* Espai intern */
            border: none; /* Sense vora */
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Ombra */
            cursor: pointer; /* Cursor de mà */
            transition: background-color 0.3s ease, transform 0.2s ease, color 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: #2f7a6e; /* Verd més fosc */
            transform: scale(1.05); /* Augment de mida */
            color: white; /* Manté el text blanc */
        }

        /* Spinner verd i centrat */
        .custom-spinner-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 20px;
        }

        .custom-spinner-text {
            color: #3c948c; /* Text verd */
            font-weight: bold;
            font-size: 18px;
            margin-top: 10px;
            text-align: center;
        }

        /* Blocs de grups */
        .group-header {
            color: #ffffff;
            background-color: #3c948c;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 15px;
        }

        .participant-box {
            border: 2px solid #7ca5a8;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .participant-box h4 {
            color: #22222a;
            margin-bottom: 5px;
        }

        .participant-box p {
            margin: 0;
            font-size: 14px;
            color: #666;
        }

        .footer-text {
            text-align: center;
            font-size: 1em;
            color: #8c8c8c;
            margin-top: 30px;
        }

        </style>

        <script>
        document.addEventListener("scroll", function() {
            const logosContainer = document.querySelector(".logos-container");
            if (window.scrollY > 50) {
                logosContainer.classList.add("hidden");
            } else {
                logosContainer.classList.remove("hidden");
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

# Afegir estils personalitzats
add_custom_styles()

# Mostrar logos a la part superior
st.markdown(
    """
    <div class="logos-container">
        <img src="https://www.datathon.cat/_app/immutable/assets/accentLogo.ICfS56oN.png" alt="Logo esquerra">
        <img src="https://github.com/data-students/AEDChallenge/raw/main/public/aed_logo.png" alt="Logo dreta">
    </div>
    """,
    unsafe_allow_html=True,
)

# Cercador a la part superior amb marge superior
st.markdown('<div style="margin-top:50px;"></div>', unsafe_allow_html=True)
query_input = st.text_input("Cerca per UID o Nom del Participant:", 
                            placeholder="Exemple: John Doe o 123e4567-e89b-12d3-a456-426614174000",
                            key="participant_search_input")

# Títol centrat
st.markdown("<h1 class='main-title'>Agrupem els participants</h1>", unsafe_allow_html=True)

# Subtítol centrat
st.markdown("<p class='subtitle'>Generem els grups de manera automàtica</p>", unsafe_allow_html=True)

# Funció per mostrar els grups amb estils
def mostra_grups(data):
    st.write("### Grups Generats")
    grouped = data.groupby("group_id")

    for group_id, group in grouped:
        st.markdown(f"<div class='group-header'>Grup {group_id}</div>", unsafe_allow_html=True)

        cols = st.columns(len(group))
        for i, (_, row) in enumerate(group.iterrows()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="participant-box">
                        <h4>{row['name']}</h4>
                        <p><strong>ID:</strong> {row['id']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        common_features = group["group_common_features"].iloc[0]
        st.markdown(f"<p><strong>Característiques comunes:</strong> {common_features}</p>", unsafe_allow_html=True)

# Botó per executar l'script extern
if st.button("Generar grups"):
    with st.spinner("Recol·lectant les dades..."):
        script_path = 'jsonDownloader.py'
        try:
            result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        except FileNotFoundError:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)

    with st.spinner("Generant els grups..."):
        script_path = 'grouping.py'
        try:
            result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        except FileNotFoundError:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.returncode == 0:
        try:
            output_csv_path = "output_groups.csv"
            data = pd.read_csv(output_csv_path)
            mostra_grups(data)
        except FileNotFoundError:
            st.error("El fitxer CSV no s'ha trobat. Assegura't que 'grouping.py' crea 'output_groups.csv'.")
    else:
        st.error("Error en executar l'script.")
        st.text(result.stderr)
else:
    st.markdown("<p class='footer-text'>Prem el botó superior per generar els grups automàticament.</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("output_groups.csv")
        with open("datathon_participants.json", "r") as f:
            json_data = json.load(f)
        return df, json_data
    except FileNotFoundError:
        return None, None

df, json_data = load_data()

if query_input and df is not None and json_data is not None:
    matching_participants = []
    for participant in json_data:
        if (participant.get("id") == query_input or 
            query_input.lower() in participant.get("name", "").lower()):
            matching_participants.append(participant)

    if matching_participants:
        st.subheader(f"S'han trobat {len(matching_participants)} participants:")
        all_data_df = pd.DataFrame(matching_participants)
        column_order = [
            'name', 'id', 'age', 'preferred_team_size', 'experience_level',
            'preferred_role', 'hackathons_done', 'year_of_study', 'objective',
            'languages', 'dietary_restrictions', 'friend_registration',
            'availability_saturday_morning', 'availability_saturday_afternoon',
            'availability_saturday_night', 'availability_sunday_morning',
            'availability_sunday_afternoon'
        ]
        existing_columns = [col for col in column_order if col in all_data_df.columns]
        all_data_df = all_data_df[existing_columns]
        st.dataframe(all_data_df)

        for participant in matching_participants:
            participant_id = participant.get("id")
            curr_participant_data = df[df['id'] == participant_id]
            
            if not curr_participant_data.empty:
                group_id = curr_participant_data['group_id'].iloc[0]
                group_members = df[df['group_id'] == group_id]
                
                st.write(f"#### Membres del grup del participant {participant.get('name')} (Grup ID: {group_id})")
                st.table(group_members[['name', 'id']])
                st.markdown("---")
    else:
        st.error("No s'ha trobat cap participant amb aquesta informació.")