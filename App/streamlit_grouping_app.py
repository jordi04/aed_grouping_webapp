import streamlit as st
import subprocess
import pandas as pd
import time

# Configuració de la pàgina
st.set_page_config(page_title="Dynamic Grouping", layout="wide")

st.title("Agrupem els participants")

# Estils CSS per a personalitzar els blocs
def add_custom_styles():
    st.markdown(
        """
        <style>
        .participant-box {
            border: 2px solid #7ca5a8;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
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
        .group-header {
            color: #ffffff;
            background-color: #3c948c;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Funció per mostrar els grups amb estils
def mostra_grups(data):
    st.write("### Groups Overview")

    # Agrupar les dades pel group_id
    grouped = data.groupby("group_id")

    # Mostrar els grups
    for group_id, group in grouped:
        st.markdown(f"<div class='group-header'>Group {group_id}</div>", unsafe_allow_html=True)
        
        # Mostrar característiques comunes
        common_features = group["group_common_features"].iloc[0]
        st.write(f"**Common Features:** {common_features}")
        
        # Crear una fila amb columnes adaptatives per als participants
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

# Botó per executar l'script extern
if st.button("Generate Groups"):
    # Mostrem una barra de progrés
    with st.spinner("Executing grouping script..."):
        # Executar l'script Python extern
        script_path = 'grouping.py'  # Ruta al fitxer grouping.py

        # Ajust segons el sistema operatiu (python o python3)
        try:
            result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        except FileNotFoundError:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)

        time.sleep(2)  # Simulem un temps d'espera per mostrar la càrrega
    
    # Comprovar si l'execució ha estat exitosa
    if result.returncode == 0:
        st.success("Script executed successfully! Reading the generated CSV...")
        
        # Carregar el CSV generat
        try:
            output_csv_path = "output_groups.csv"  # Fitxer generat pel teu script
            data = pd.read_csv(output_csv_path)
            
            # Afegir estils personalitzats
            add_custom_styles()

            # Mostrar els grups de forma visual
            mostra_grups(data)
        except FileNotFoundError:
            st.error("The generated CSV file was not found. Ensure 'grouping.py' creates 'participants_final.csv'.")
    else:
        st.error("Error executing the grouping script.")
        st.text(result.stderr)
else:
    st.write("Press the button above to generate groups using the external script.")