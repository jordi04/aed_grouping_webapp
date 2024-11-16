
import streamlit as st
import subprocess
import pandas as pd
import time

# Configuració de la pàgina
st.set_page_config(page_title="Dynamic Grouping", layout="wide")

# Títol
st.title("Execute Grouping Script and Display Results")

# Botó per executar l'script extern
if st.button("Generate Groups"):
    # Mostrem una barra de progrés
    with st.spinner("Executing grouping script..."):
        # Executar l'script Python extern
        script_path = 'grouping.py'  # Ruta al fitxer grouping.py
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        time.sleep(2)  # Simulem un temps d'espera per mostrar la càrrega
    
    # Comprovar si l'execució ha estat exitosa
    if result.returncode == 0:
        st.success("Script executed successfully! Reading the generated CSV...")
        
        # Carregar el CSV generat
        try:
            output_csv_path = "output_groups.csv"  # Assegura't que grouping.py genera aquest fitxer
            data = pd.read_csv(output_csv_path)
            
            # Agrupar les dades (si cal)
            grouped = data.groupby("group_id")

            # Mostrar els grups
            for group_id, group in grouped:
                st.header(f"Group ID: {group_id}")
                st.table(group)
        except FileNotFoundError:
            st.error("The generated CSV file was not found. Ensure 'grouping.py' creates 'output_groups.csv'.")
    else:
        st.error("Error executing the grouping script.")
        st.text(result.stderr)
else:
    st.write("Press the button above to generate groups using the external script.")
