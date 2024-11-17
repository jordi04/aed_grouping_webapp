import streamlit as st
import subprocess
import pandas as pd
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Configuració de la pàgina
st.set_page_config(page_title="Dynamic Grouping", layout="wide")

# Estils CSS personalitzats per adaptar l'estil de la pàgina
def add_custom_styles():
    st.markdown(
        """
        <style>
        /* Fons general */
        .stApp {
            background-color: #ffffff;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Container for all content */
        .block-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Contenidor dels logos */
        .logos-container {
            position: fixed;
            top: 50px;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 1200px;
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
            margin-top: 50px; /* Reduït l'espai respecte al botó del menú de cerca */
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
            margin: 20px auto;
            background-color: #3c948c;
            color: white !important; /* Added !important */
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 20px;
            border: none;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: #2f7a6e;
            transform: scale(1.05);
            color: white !important;
        }

        .custom-spinner-container {
            display: flex;
            justify-content: center;
            align-items: center !important;
            flex-direction: column;
            margin-top: 20px;
        }

        .custom-spinner-text {
            color: #3c948c;
            font-weight: bold;
            font-size: 18px;
            margin-top: 10px;
            text-align: center;
        }

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
            margin: 10px auto;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 300px;
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

        /* Center all Streamlit elements */
        .stMarkdown, .stButton, .stSpinner {
            display: flex;
            justify-content: center;
            margin: 0 auto;
        }

        /* Amaga la roda de càrrega per defecte */
        .stSpinner > div > div {
            display: none;
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

# Ajustar el marge superior per assegurar que la barra de cerca sigui visible
st.markdown("""
<style>
.block-container {
    margin-top: 100px; /* Ajusta aquest valor segons sigui necessari */
}
</style>
""", unsafe_allow_html=True)

# Inicialitzar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebaseCred.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Títol centrat
st.markdown("<h1 class='main-title'>Agrupem els participants</h1>", unsafe_allow_html=True)

# Subtítol centrat
st.markdown("<p class='subtitle'>Generem els grups de manera automàtica</p>", unsafe_allow_html=True)

# Funció per mostrar la informació del participant
def mostra_participant(uid):
    participant_ref = db.collection('participants').document(uid)
    participant = participant_ref.get()
    if participant.exists:
        data = participant.to_dict()
        st.write(f"### Informació del participant {data['name']}")
        st.write(f"**ID:** {data['id']}")
        st.write(f"**Email:** {data['email']}")
        st.write(f"**Languages:** {', '.join(data['languages'])}")
        st.write(f"**Objective:** {data['objective']}")
    else:
        st.error("Participant no trobat.")

# Funció per mostrar els grups amb estils
def mostra_grups(data):
    st.write("### Grups Generats")
    grouped = data.groupby("group_id")

    # Mostrar els grups
    for group_id, group in grouped:
        st.markdown(f"<div class='group-header'>Grup {group_id}</div>", unsafe_allow_html=True)

        # Crear una fila amb columnes adaptatives per als participants
        cols = st.columns(len(group))
        for i, (_, row) in enumerate(group.iterrows()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="participant-box">
                        <h4>{row['name']}</h4>
                        <p><strong>ID:</strong> {row['id']}</p>
                        <button onclick="window.location.href='#{row['id']}'">Més info</button>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Més info", key=f"info-{row['id']}"):
                    mostra_participant(row['id'])

# Botó per executar l'script extern
if st.button("Generar grups"):
    # Mostrem un spinner verd centrat
    with st.spinner("Recol·lectant les dades..."):
        # Executar l'script Python extern
        script_path = 'jsonDownloader.py'  # Ruta al fitxer grouping.py
        try:
            result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        except FileNotFoundError:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)

    with st.spinner("Generant els grups..."):
        # Executar l'script Python extern
        script_path = 'grouping.py'  # Ruta al fitxer grouping.py
        try:
            result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        except FileNotFoundError:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)

    # Comprovar si l'execució ha estat exitosa
    if result.returncode == 0:
        # Eliminat el missatge de confirmació
        try:
            output_csv_path = "output_groups.csv"  # Fitxer generat pel teu script
            data = pd.read_csv(output_csv_path)

            # Mostrar els grups de forma visual
            mostra_grups(data)
        except FileNotFoundError:
            st.error("El fitxer CSV no s'ha trobat. Assegura't que 'grouping.py' crea 'output_groups.csv'.")
    else:
        st.error("Error en executar l'script.")
        st.text(result.stderr)
else:
    # Text explicatiu centrat a la part inferior
    st.markdown("<p class='footer-text'>Prem el botó superior per generar els grups automàticament.</p>", unsafe_allow_html=True)

# Peu de pàgina amb text centrat
st.markdown(
    """
    <p class='footer-text'>Desenvolupat per en Sergi Adrover, en Pol Mir, en Jaume Mora i en Jordi Roca - Datathon 2024</p>
    """,
    unsafe_allow_html=True,
)