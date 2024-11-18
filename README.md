# 📘 **README - FME Datathon App** 🏆

## 🎯 **Descripció**
L'aplicació **AED GROUPING WEBAPP** és una eina interactiva creada per a competir en el challenge de la **Datathon FME 24**. Aquesta eina facilita el procés de registre, agrupació i gestió dels participants d'una manera visual i intuïtiva. 🚀

## 🚀 **Funcionalitats**
### 🧑‍💻 **Per als Participants**
- **Formulari de registre complet**: Amb seccions per a informació personal, habilitats tècniques, detalls personals i preferències.
- **Enregistrament de competències tècniques** amb nivells associats.
- **Selecció de disponibilitat i rols preferits** per als equips.
- **Validació automàtica de camps obligatoris** per garantir un registre complet.
- **Disseny atractiu i responsiu** per una millor experiència d'usuari.

### 🛠️ **Per als Administradors**
- **Vista d'agrupació**: Organitza els participants en equips segons els seus interessos, habilitats i disponibilitat.
- **Gestió visual dels grups creats**: Consulta i modifica els grups fàcilment.

## 🖥️ **Tecnologies Utilitzades**
- **[Streamlit](https://streamlit.io/)**: Per construir la interfície d'usuari de manera ràpida i funcional.
- **[Firebase](https://firebase.google.com/)**: Per a l'autenticació i la base de dades en temps real.
- **CSS personalitzat**: Per donar un toc visual modern i professional.
- **UUID**: Per generar identificadors únics per als participants.
- **Python**: Backend que gestiona el registre, la validació i la interacció amb Firebase.

## 🌟 **Característiques Especials**
- 🎨 **Disseny UI/UX personalitzat** per assegurar una experiència moderna i atractiva.
- ⚡ **Validacions automàtiques en temps real** per camps obligatoris.
- 🎯 **Agrupament intel·ligent**: Facilita la creació d'equips equilibrats segons habilitats i preferències.
- 🎈 **Funcions dinàmiques** com l'ús de sliders per seleccionar nivells d'habilitat o checkboxes per la disponibilitat.

## 📜 **Estructura del Formulari de Registre**
1. **Informació Bàsica**: Nom, email, edat, any acadèmic.
2. **Detalls Personals**: Universitat, talla de samarreta, restriccions alimentàries.
3. **Habilitats**: Selecció d'habilitats tècniques i nivell associat.
4. **Detalls Addicionals**: Interessos, objectius, experiència en hackathons.
5. **Preferències**: Reptes preferits, llenguatges, mida d'equip, amics.
6. **Disponibilitat i Introducció**: Disponibilitat per franges horàries i presentació personal.

## 🛡️ **Seguretat**
- Ús de **Firestore** per emmagatzemar dades de manera segura.
- **Validacions en el backend** per assegurar la qualitat de les dades introduïdes.

## 🌐 **Web per a Administradors**
- Accés només per als organitzadors.
- Mostra visual dels grups creats, amb la possibilitat de reassignar participants.
- Interfície senzilla per agilitzar la gestió dels equips.

## 🔧 **Com Executar**
1. Cloneu el repositori:
   ```bash
   git clone https://github.com/jordi04/fme-datathon-app.git
   cd fme-datathon-app
   ```
2. Installeu les dependències:
   ```bash
   pip install -r requirements.txt
   ```
3. Configureu les credencials de Firebase (`firebaseCred.json`).
4. Executeu l'aplicació:
   ```bash
   streamlit run app.py
   ```
