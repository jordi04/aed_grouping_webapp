import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import json
import pathlib
import uuid
from dataclasses import dataclass
from typing import Dict, List, Literal

@dataclass
class Participant:
    id: uuid.UUID
    name: str
    email: str
    age: int
    year_of_study: Literal["1st year", "2nd year", "3rd year", "4th year", "Masters", "PhD"]
    shirt_size: Literal["S", "M", "L", "XL"]
    university: str
    dietary_restrictions: Literal["None", "Vegetarian", "Vegan", "Gluten-free", "Other"]
    programming_skills: Dict[str, int]
    experience_level: Literal["Beginner", "Intermediate", "Advanced"]
    hackathons_done: int
    interests: List[str]
    preferred_role: Literal[
        "Analysis", "Visualization", "Development", "Design", "Don't know", "Don't care"
    ]
    objective: str
    interest_in_challenges: List[str]
    preferred_languages: List[str]
    friend_registration: List[uuid.UUID]
    preferred_team_size: int
    availability: Dict[str, bool]
    introduction: str
    technical_project: str
    future_excitement: str
    fun_fact: str


def load_participants(path: str) -> List[Participant]:
    if not pathlib.Path(path).exists():
        raise FileNotFoundError(f"The file {path} does not exist.")
    if not pathlib.Path(path).suffix == ".json":
        raise ValueError(f"The file {path} is not a JSON file.")

    return [Participant(**participant) for participant in json.load(open(path))]


# Load data
# Cridem que s'executi jsonDownloader.py per obtenir el fitxer datathon_participants.json



data_path = "datathon_participants.json"
participants = load_participants(data_path)

df = pd.DataFrame(participants)
df = df.drop(
    columns=[
        "email", "age", "interest_in_challenges", "shirt_size", "university", 
        "dietary_restrictions", "introduction", "technical_project", "future_excitement", 
        "fun_fact"
    ]
)

# Classify objectives
def classify_objective_numeric(text):
    text = text.lower()
    competitive_keywords = ["win", "competition", "prize", "victorious", "trophy", "on top", "crush", "edge"]
    learning_keywords = ["learn", "skills", "knowledge", "improve", "grow", "hands-on", "challenge myself"]
    social_keywords = ["friends", "connections", "fun", "enjoy", "networking", "community", "blast", "vibes"]
    if any(keyword in text for keyword in competitive_keywords):
        return 1  # Competitive
    elif any(keyword in text for keyword in learning_keywords):
        return 2  # Learning
    elif any(keyword in text for keyword in social_keywords):
        return 3  # Social
    return 2  # Default to Learning

df['objective'] = df['objective'].apply(classify_objective_numeric)

# Preprocess columns
df['year_of_study'] = df['year_of_study'].replace({'1st year': 1, '2nd year': 2, '3rd year': 3, '4th year': 4, 'Masters': 5, 'PhD': 6})
df['experience_level'] = df['experience_level'].replace({'Beginner': 1, 'Intermediate': 2, 'Advanced': 3})
df['preferred_role'] = df['preferred_role'].replace({'Design': 1, 'Analysis': 2, 'Development': 3, 'Visualization': 4, "Don't know": 5, "Don't care": 5})

availability_df = pd.json_normalize(df['availability']).applymap(lambda x: 1 if x else 0)
df = pd.concat([df.drop(columns=['availability']), availability_df], axis=1)

# Encode preferred languages
mlb = MultiLabelBinarizer()
languages_encoded = pd.DataFrame(
    mlb.fit_transform(df['preferred_languages']),
    columns=mlb.classes_,
    index=df.index
)

# Normalize programming skills and interests
skill_normalization = {
    "python": "Python", "Python": "Python",
    "c++": "C++", "C++": "C++",
    "java script": "JavaScript", "javascript": "JavaScript", "JavaScript": "JavaScript",
    "SQL ": "SQL", "sql": "SQL", "SQL": "SQL",
    "tensorflow": "TensorFlow", "TensorFlow": "TensorFlow",
    "pytorch": "PyTorch", "PyTorch": "PyTorch",
    "docker": "Docker", "Docker": "Docker",
    "html": "HTML/CSS", "css": "HTML/CSS", "HTML/CSS": "HTML/CSS",
    "data analyss": "Data Analysis",
    "nlp": "Natural Language Processing", "Natural Language Processing": "Natural Language Processing",
    "Natural Language Processing ": "Natural Language Processing",
    "java": "Java", "Java": "Java",
    "go": "Go", "Go": "Go",
    "Rust ": "Rust", "rust": "Rust", "Rust": "Rust",
    "figma": "Figma", "Figma": "Figma",
    "flask": "Flask", "Flask": "Flask",
    "flutter": "Flutter", "Flutter": "Flutter",
    "react": "React", "React": "React",
    "react native": "React Native", "React Native": "React Native",
    "postgreSQL": "PostgreSQL", "PostgreSQL": "PostgreSQL", "postgres": "PostgreSQL",
    "Aws": "AWS/Azure/GCP", "AWS": "AWS/Azure/GCP", "AWS/Azure/GCP": "AWS/Azure/GCP",
    "IoT": "IoT", "iot": "IoT",
    "Machine Learning": "Machine Learning", "ML": "Machine Learning",
    "DevOps": "DevOps",
    "android": "Android Development", "Android Development": "Android Development",
    "iOS Development ": "iOS Development", "ios": "iOS Development", "iOS Development": "iOS Development",
    "UI/UX Design": "UI/UX", "UI/UX": "UI/UX", "UI/UX Design ": "UI/UX",
    "GitHub": "Git", "git": "Git", "Git": "Git",
    "Design": "Design",
    "Agile": "Agile", "Agile Methodology": "Agile",
    "Lifehacks": "Life Hacks",
    "Blockchain": "Blockchain",
    "Computer Vision ": "Computer Vision", "Computer Vision": "Computer Vision",
    "Data Analysis": "Data Analysis", "Data Visualization": "Data Visualization",
    "android development": "Android Development"
}

df['interests'] = df['interests'].apply(lambda x: [skill_normalization.get(i.strip(), i.strip()) for i in x] if isinstance(x, list) else [])
df['programming_skills'] = df['programming_skills'].apply(
    lambda skills: {skill_normalization.get(k.strip(), k.strip()): v for k, v in skills.items()} if isinstance(skills, dict) else {}
)

# Create columns for programming skills
skill_columns = set()
for skills in df['programming_skills']:
    skill_columns.update(skills.keys())

for skill in skill_columns:
    df[skill] = 0

for idx, skills in enumerate(df['programming_skills']):
    for skill, value in skills.items():
        df.at[idx, skill] = value

# Encode interests
interests_encoded = pd.DataFrame(
    mlb.fit_transform(df['interests']),
    columns=mlb.classes_,
    index=df.index
)

df = pd.concat([df.drop(columns=['preferred_languages', 'interests', 'programming_skills']), languages_encoded, interests_encoded], axis=1)
df = df.fillna(0)

# Group participants
df['group_id'] = None
groups = {}
group_id = 1

visited = set()

def find_all_friends(participant, visited, group):
    if participant in visited:
        return
    visited.add(participant)
    group.append(participant)

    if participant not in df['id'].values:
        return
    
    friends = df.loc[df['id'] == participant, 'friend_registration'].values[0]
    if not isinstance(friends, list):
        friends = []
    
    for friend in friends:
        find_all_friends(friend, visited, group)

for participant in df[df['friend_registration'].apply(lambda x: isinstance(x, list) and len(x) > 0)]['id']:
    if participant not in visited:
        group = []
        find_all_friends(participant, visited, group)
        for member in group:
            df.loc[df['id'] == member, 'group_id'] = group_id
        groups[group_id] = group
        group_id += 1

df = df.sort_values(by='group_id')

# Llenguatges de programació i altres columnes classificades per nivells
strict_columns = [col for col in [
    'objective', 'Catalan', 'English', 'French', 'German', 'Italian', 'Portuguese', 'Spanish',
    'Saturday morning', 'Saturday afternoon', 'Saturday night', 'Sunday morning', 'Sunday afternoon'
] if col in df.columns]

medium_columns = [
    'hackathons_done', 'experience_level', 'preferred_role', 'Python', 'React', 'JavaScript',
    'TypeScript', 'Docker', 'SQL', 'TensorFlow', 'PyTorch', 'Machine Learning', 'React Native', 'C++', 'year_of_study'
]

relaxed_columns = [
    'Gaming', 'Health', 'E-commerce/Retail', 'Education', 'Enterprise', 'Social Good',
    'Machine Learning/AI', 'Communication', 'Cybersecurity', 'Music/Art', 'Quantum',
    'Robotic Process Automation', 'Voice skills', 'Web', 'age'
]

programming_languages = [
    'Python', 'React', 'JavaScript', 'TypeScript', 'C++', 'SQL', 
    'TensorFlow', 'PyTorch', 'Docker', 'AWS/Azure/GCP', 'Java', 'Go', 'Rust', 'Figma', 'Flask', 'React Native', 'PostgreSQL', 'Android Development', 'iOS Development', 'UI/UX', 'Git'
]

all_columns = [
    'Catalan', 'English', 'French', 'German', 'Italian', 'Portuguese', 'Spanish', 'Saturday morning', 'Saturday afternoon', 'Saturday night', 'Sunday morning', 'Sunday afternoon',
    'hackathons_done', 'experience_level', 'preferred_role', 'Python', 'React', 'JavaScript', 'TypeScript', 'Docker', 'SQL', 'TensorFlow', 'PyTorch', 'Machine Learning', 'React Native', 'C++', 'year_of_study',
    'Gaming', 'Health', 'E-commerce/Retail', 'Education', 'Enterprise', 'Social Good', 'Machine Learning/AI', 'Communication', 'Cybersecurity', 'DevOps', 'Music/Art', 'Quantum', 'Robotic Process Automation', 'Voice skills', 'Web'
]



# Funció per calcular característiques comunes d'un grup (només positives)
def calculate_common_features(group_members, df):
    common_features = []
    for column in all_columns:
        if column in df.columns:
            values = df.loc[group_members, column]
            if all(values > 0):  # Comprovar si tots els valors són > 0
                common_features.append(column)
    return "; ".join(common_features)

def calculate_common_languages(group_members, df):
    for language in languages:
        if all(df.loc[group_members, language] > 0):
            return language
    return "None"

# Funció per calcular la puntuació parell a parell
def calculate_pair_score(participant, member, columns):
    """
    Calcula la compatibilitat entre un participant i un membre del grup
    segons les columnes especificades.

    Args:
        participant (pd.Series): Dades del participant a avaluar.
        member (pd.Series): Dades d'un membre del grup.
        columns (list): Llista de columnes a comparar.

    Returns:
        float: Puntuació de compatibilitat entre el participant i el membre.
    """
    score = 0
    for col in columns:
        if col in participant.index and col in member.index:
            if participant[col] == member[col]:  # Coincidència exacta
                score += 1
            elif isinstance(participant[col], (int, float)) and isinstance(member[col], (int, float)):
                # Similitud relativa per a valors numèrics
                diff = abs(participant[col] - member[col])
                max_value = max(participant[col], member[col], 1)
                score += 1 - (diff / max_value)
    return score

# Funció per assignar a grups amb mida estrictament compatible
def assign_to_group_with_compatible_size(participant_idx, groups, df):
    participant = df.loc[participant_idx]
    preferred_size = participant['preferred_team_size']
    best_group = None
    best_score = -1

    for group_id, group_members in groups.items():
        # Comprovar si el grup actual pot complir la preferència de mida
        if len(group_members) + 1 > preferred_size:
            continue  # Saltar si la mida resultant és massa gran

        # Comprovar si els membres existents també són compatibles
        group_preferred_sizes = df.loc[group_members, 'preferred_team_size']
        if any((len(group_members) + 1) > group_preferred_sizes):
            continue  # Saltar si algun membre existent no estaria còmode

        # Comprovar compatibilitat d'objectiu
        group_objective = df.loc[group_members[0], 'objective']
        if group_objective != participant['objective']:
            continue

        # Comprovar llenguatge en comú (només valors > 0)
        group_languages = df.loc[group_members, programming_languages].sum(axis=0)
        participant_languages = df.loc[participant_idx, programming_languages]
        if not any(participant_languages & (group_languages > 0)):
            continue  # Saltar si no hi ha cap llenguatge en comú

        # Calcular puntuació segons nivells
        group_score = 0
        for level, columns in enumerate([strict_columns, medium_columns, relaxed_columns], start=1):
            for member in group_members:
                group_score += calculate_pair_score(participant, df.loc[member], columns)

        group_score = group_score / len(group_members)  # Puntuació mitjana
        if group_score > best_score:
            best_group = group_id
            best_score = group_score

    return best_group, best_score

# Inicialitzar grups
groups = {group_id: list(group.index) for group_id, group in df.groupby('group_id') if not pd.isna(group_id)}
new_group_id = int(df['group_id'].max()) + 1

# Assignar iterativament
for idx in df[df['group_id'].isna()].index:
    best_group, best_score = assign_to_group_with_compatible_size(idx, groups, df)
    if best_group is not None:
        groups[best_group].append(idx)
        df.at[idx, 'group_id'] = best_group
    else:
        # Crear un grup nou si no s'ha trobat cap compatible
        groups[new_group_id] = [idx]
        df.at[idx, 'group_id'] = new_group_id
        new_group_id += 1

# Calcular característiques comunes per grup
common_features_per_group = {}
for group_id, members in groups.items():
    common_features_per_group[group_id] = calculate_common_features(members, df)

# Afegir columna de característiques comunes al DataFrame
df['group_common_features'] = df['group_id'].map(common_features_per_group)



# Regroup solo participants
def regroup_solo_participants(df, max_size=4):
    solo_groups = df['group_id'].value_counts()
    solo_group_ids = solo_groups[solo_groups == 1].index
    solo_participants = df[(df['group_id'].isin(solo_group_ids)) & (df['preferred_team_size'] > 1)]

    if solo_participants.empty:
        return df

    solo_list = list(solo_participants.index)
    new_group_id = int(df['group_id'].max()) + 1 if not df['group_id'].isna().all() else 1

    while solo_list:
        group = []
        while solo_list and len(group) < max_size:
            group.append(solo_list.pop(0))
        for member in group:
            df.at[member, 'group_id'] = new_group_id
        new_group_id += 1

    return df

df = regroup_solo_participants(df)

df = df.sort_values(by='group_id')
columns_order = ['group_id'] + [col for col in df.columns if col != 'group_id']
df = df[columns_order]
df.to_csv('output_groups.csv', index=False)
print("Participants grouped and results saved to 'output_groups.csv'.")