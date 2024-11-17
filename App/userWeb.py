import streamlit as st
import firebase_admin
import json
import os
from firebase_admin import credentials, firestore
import uuid  # Add this at the beginning of the file


# Estils CSS personalitzats
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
            top: 50px;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 30px;
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .logos-container img {
            height: 80px;
        }

        /* Títol principal */
        .main-title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #2e2e2e;
            margin-top: 150px;
            margin-bottom: 10px;
        }

        /* Estil per als botons */
        div.stButton > button {
            display: block;
            margin: 20px auto;
            background-color: transparent;
            color: #3c948c !important;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 20px;
            border: 2px solid #3c948c;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease, color 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: #e6f2ef;
            color: #3c948c !important;
            border: 2px solid #3c948c;
        }

        /* Posicionament específic per al botó "Next" */
        div.stButton.next-button {
            float: right;
            margin-right: 0;
        }

        /* Posicionament específic per al botó "Previous" */
        div.stButton.prev-button {
            float: left;
            margin-left: 0;
        }

        /* Camps d'entrada */
        input[type="text"], input[type="number"], textarea, select {
            border: 2px solid #d9d9d9;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
            width: 100%;
            background-color: #f9f9f9;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        /* Hover en camps d'entrada */
        input[type="text"]:hover, input[type="number"]:hover, textarea:hover, select:hover {
            border-color: #3c948c !important;
            box-shadow: 0 0 5px rgba(60, 148, 140, 0.5);
        }

        /* Focus (quan hi ha cursor dins del camp) */
        input[type="text"]:focus, input[type="number"]:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #3c948c;
            box-shadow: 0 0 5px rgba(60, 148, 140, 0.5);
        }

        /* Camps amb errors */
        .stAlert {
            background-color: #e6f2ef;
            color: #3c948c;
            border-color: #3c948c;
        }

        /* Placeholder en camps d'entrada */
        input::placeholder, textarea::placeholder {
            color: #8c8c8c;
        }

        /* Spinner turquesa centrat */
        .custom-spinner-container {
            display: flex;
            justify-content: center;
            align-items: center;
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

        /* Clear fix for button columns */
        .button-container::after {
            content: "";
            display: table;
            clear: both;
        }
        </style>
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

# Títol centrat
st.markdown("<h1 class='main-title'>Fill out the form to register</h1>", unsafe_allow_html=True)


# Initialize Firebase only if it hasn't been initialized already
if not firebase_admin._apps:  # Check if any Firebase app is initialized
    cred = credentials.Certificate("firebaseCred.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()
# Reference to the collection of participants
participants_ref = db.collection("participants")

# Initialize session state variables
if "ID" not in st.session_state:
    st.session_state.ID = str(uuid.uuid4())  # Generate a unique ID
    
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


requiredString = "Please fill all fields are required."
# Page 1: Basic Information
if st.session_state.page == 1:
    with st.form(key="participant_form"):
        st.header("Section 1: Basic Information")
        name = st.text_input("Participant's Name:", st.session_state.IB.get("name", ""))
        email = st.text_input("Email:", st.session_state.IB.get("email", ""))
        age = st.number_input("Age:", min_value=10, max_value=100, step=1, value=st.session_state.IB.get("age", 18))
        year_of_study = st.selectbox(
            "Academic Year:", 
            ["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"], 
            index=["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"].index(st.session_state.IB.get("year_of_study", "1st year"))
        )
        submit = st.form_submit_button("Next")

        # Validation for required fields
        if submit:
            if not name or not email or not age or not year_of_study: 
                st.error(requiredString)  # Error message if any field is missing
            else:
                st.session_state.IB = {
                    "name": name,
                    "email": email,
                    "age": age,
                    "year_of_study": year_of_study
                }
                next_page()

# Page 2: Personal Details
elif st.session_state.page == 2:
    with st.form(key="participant_form_dp"):
        st.header("Section 2: Personal Details")
        shirt_size = st.selectbox(
            "Shirt Size:", 
            ["S", "M", "L", "XL"], 
            index=["S", "M", "L", "XL"].index(st.session_state.DP.get("shirt_size", "S"))
        )
        university = st.text_input("University:", value=st.session_state.DP.get("university", ""))
        dietary_restrictions = st.selectbox(
            "Dietary Restrictions:", 
            ["None", "Vegetarian", "Vegan", "Gluten-free", "Other"],
            index=["None", "Vegetarian", "Vegan", "Gluten-free", "Other"].index(st.session_state.DP.get("dietary_restrictions", "None"))
        )
        experience_level = st.selectbox(
            "Experience Level:", 
            ["Beginner", "Intermediate", "Advanced"],
            index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.DP.get("experience_level", "Beginner"))
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Previous")
        with col2:
            next_ = st.form_submit_button("Next")

        # Validation for required fields
        if next_:
            if not shirt_size or not university or not dietary_restrictions or not experience_level:
                st.error(requiredString)  # Error message if any field is missing
            else:
                st.session_state.DP.update({
                    "shirt_size": shirt_size,
                    "university": university,
                    "dietary_restrictions": dietary_restrictions,
                    "experience_level": experience_level
                })
                next_page()

        if prev:
            prev_page()

# Page 3: Skills
elif st.session_state.page == 3:
    st.header("Section 3: Skills")
    available_skills = [
        "Python", "C++", "JavaScript", "SQL", "TensorFlow", "PyTorch", "Docker", "HTML/CSS",
        "Data Analysis", "Natural Language Processing", "Java", "Go", "Rust", "Figma", "Flask",
        "React", "React Native", "PostgreSQL", "AWS/Azure/GCP", "IoT", "Machine Learning",
        "Android Development", "iOS Development", "UI/UX Design", "Git", 
        "Blockchain", "Computer Vision", "Data Visualization"
    ]
    selected_skills = st.multiselect("Select skills:", options=available_skills, default=list(st.session_state.skills.keys()))
    skill_levels = {skill: st.slider(f"Level for {skill}:", 0, 10, value=st.session_state.skills.get(skill, 5)) for skill in selected_skills}
    col1, col2 = st.columns(2)
    with col1:
        prev = st.button("Previous")
    with col2:
        next_ = st.button("Next")

    if next_:
        if not selected_skills:
            st.error("Please select at least one skill.")  # Error message if no skill is selected
        else:
            st.session_state.skills = skill_levels
            next_page()

    if prev:
        prev_page()

# Page 4: Additional Details
elif st.session_state.page == 4:
    with st.form(key="additional_details_form"):
        st.header("Section 4: Additional Details")
        hackathons_done = st.number_input(
            "Number of hackathons completed:", 
            min_value=0, 
            step=1, 
            value=st.session_state.DA.get("hackathons_done", 0)
        )
        interests = st.multiselect(
            "Select your interests:",
            ["Machine Learning/AI", "Gaming", "E-commerce/Retail", "Productivity", "Web", 
             "Music/Art", "Quantum", "Databases", "DevOps"],
            default=st.session_state.DA.get("interests", [])
        )
        preferred_role = st.selectbox(
            "Preferred role:", 
            ["Analysis", "Visualization", "Development", "Design"],
            index=["Analysis", "Visualization", "Development", "Design"].index(
                st.session_state.DA.get("preferred_role", "Analysis")
            )
        )
        objective = st.text_area("Main objective:", value=st.session_state.DA.get("objective", ""))
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Previous")
        with col2:
            next_ = st.form_submit_button("Next")

        if next_:
            if not interests or not preferred_role or not objective:
                st.error(requiredString)  # Error message if any field is missing
            else:
                st.session_state.DA = {
                    "hackathons_done": hackathons_done,
                    "interests": interests,
                    "preferred_role": preferred_role,
                    "objective": objective
                }
                next_page()

        if prev:
            prev_page()
# Page 5: Preferences
elif st.session_state.page == 5:
    with st.form(key="preferences_form"):
        st.header("Section 5: Preferences")
        interest_in_challenges = st.multiselect(
            "Challenges of interest:",
            ["Mango Challenge", "Restb.ai Challenge", "AED Challenge"],
            default=st.session_state.P.get("interest_in_challenges", [])
        )
        preferred_languages = st.multiselect(
            "Preferred languages:",
            ["English", "Catalan", "Spanish", "French", "German", "Italian"],
            default=st.session_state.P.get("preferred_languages", [])
        )
        friend_registration = st.text_area(
            "Identifiers (UUID) of registered friends (separated by commas):",
            value=", ".join(st.session_state.P.get("friend_registration", []))
        )
        friend_registration_list = [
            friend.strip() for friend in friend_registration.split(",") if friend.strip()
        ]
        preferred_team_size = st.slider(
            "Preferred team size:", 
            min_value=1, 
            max_value=4, 
            value=st.session_state.P.get("preferred_team_size", 4)
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Previous")
        with col2:
            next_ = st.form_submit_button("Next")

        # Validation for required fields
        if next_:
            if not interest_in_challenges or not preferred_languages or not preferred_team_size:
                st.error(requiredString)  # Error message if any field is missing
            else:
                st.session_state.P = {
                    "interest_in_challenges": interest_in_challenges,
                    "preferred_languages": preferred_languages,
                    "friend_registration": friend_registration_list,
                    "preferred_team_size": preferred_team_size
                }
                next_page()

        if prev:
            prev_page()

# Page 6: Availability
elif st.session_state.page == 6:
    with st.form(key="availability_form"):
        st.header("Section 6: Availability")
        availability = {
            "Saturday morning": st.checkbox(
                "Saturday morning", value=st.session_state.Disp.get("availability", {}).get("Saturday morning", False)
            ),
            "Saturday afternoon": st.checkbox(
                "Saturday afternoon", value=st.session_state.Disp.get("availability", {}).get("Saturday afternoon", False)
            ),
            "Saturday night": st.checkbox(
                "Saturday night", value=st.session_state.Disp.get("availability", {}).get("Saturday night", False)
            ),
            "Sunday morning": st.checkbox(
                "Sunday morning", value=st.session_state.Disp.get("availability", {}).get("Sunday morning", False)
            ),
            "Sunday afternoon": st.checkbox(
                "Sunday afternoon", value=st.session_state.Disp.get("availability", {}).get("Sunday afternoon", False)
            ),
        }
        introduction = st.text_area(
            "Briefly introduce yourself:", value=st.session_state.Disp.get("introduction", "")
        )
        technical_project = st.text_area(
            "Describe a technical project you have done:", 
            value=st.session_state.Disp.get("technical_project", "")
        )
        future_excitement = st.text_area(
            "What are your expectations for the future?", 
            value=st.session_state.Disp.get("future_excitement", "")
        )
        fun_fact = st.text_input(
            "Tell us a fun fact about yourself:", 
            value=st.session_state.Disp.get("fun_fact", "")
        )
        col1, col2 = st.columns(2)
        with col1:
            prev = st.form_submit_button("Previous")
        with col2:
            next_ = st.form_submit_button("Next")

        # Validation for required fields
        if next_:
            if not introduction or not technical_project or not future_excitement or not fun_fact:
                st.error(requiredString)  # Error message if any field is missing
            else:
                st.session_state.Disp = {
                    "availability": availability,
                    "introduction": introduction,
                    "technical_project": technical_project,
                    "future_excitement": future_excitement,
                    "fun_fact": fun_fact
                }
                next_page()

        if prev:
            prev_page()


# Page 7: Summary and Confirmation
elif st.session_state.page >= 7:
    st.header("Section 7: Submit")
    
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
        "introduction": st.session_state.Disp.get("introduction", ""),
        "technical_project": st.session_state.Disp.get("technical_project", ""),
        "future_excitement": st.session_state.Disp.get("future_excitement", ""),
        "fun_fact": st.session_state.Disp.get("fun_fact", ""),
        "preferred_languages": st.session_state.P.get("preferred_languages", []),
        "friend_registration": st.session_state.P.get("friend_registration", []),
        "preferred_team_size": st.session_state.P.get("preferred_team_size", 0),
        "availability": st.session_state.Disp.get("availability", {}),
        "programming_skills": st.session_state.skills,  # Assuming skills are pre-collected in correct format
        "interest_in_challenges": st.session_state.P.get("interest_in_challenges", [])
    }

    # Submit button
    submit = st.button("Submit")
    if submit:
        try:
            # Save the data to Firestore
            print("outside")
            if (st.session_state.page == 7):
                participants_ref.document().set(participant_data)
                print("inside")

            st.success("Data has been successfully submitted!")
            st.header("Thank you for registering!")
            st.write("Your registration has been successfully completed. See you at the event!")
            st.write("Your user ID is:", st.session_state.ID, " Save this ID for future reference, very important.")
            st.balloons()
            st.session_state.page = 8  # Final page, no more navigation
        except Exception as e:
            st.error(f"Error submitting data: {e}")
