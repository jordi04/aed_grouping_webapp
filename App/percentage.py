import csv
from collections import defaultdict

# Leer el archivo CSV
file_path = 'output_groups.csv'
groups = defaultdict(list)

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        group_id = row['group_id']
        preferred_team_size = int(row['preferred_team_size'])
        groups[group_id].append(preferred_team_size)

# Calcular el porcentaje de personas en grupos del tamaño preferido
total_people = 0
matched_people = 0

for group_id, preferred_sizes in groups.items():
    group_size = len(preferred_sizes)
    total_people += group_size
    matched_people += preferred_sizes.count(group_size)

percentage = (matched_people / total_people) * 100 if total_people > 0 else 0

print(f'El porcentaje de personas en un grupo del tamaño preferido es: {percentage:.2f}%')

# Leer el archivo CSV para obtener los idiomas
languages = defaultdict(list)

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        group_id = row['group_id']
        member_languages = row.get('languages', '').split(',')
        languages[group_id].append(set(member_languages))

# Calcular el porcentaje de grupos donde todos los miembros comparten al menos un idioma
total_groups = len(languages)
matched_groups = 0

for group_id, member_languages in languages.items():
    common_languages = set.intersection(*member_languages)
    if common_languages:
        matched_groups += 1

group_percentage = (matched_groups / total_groups) * 100 if total_groups > 0 else 0

print(f'El porcentaje de grupos donde todos los miembros comparten al menos un idioma es: {group_percentage:.2f}%')


# Leer el archivo CSV para obtener los objetivos
objectives = defaultdict(list)

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        group_id = row['group_id']
        objective = row.get('objective', '')
        objectives[group_id].append(objective)

# Calcular el porcentaje de grupos donde todos los miembros tienen el mismo objetivo
total_groups = len(objectives)
matched_groups = 0

for group_id, member_objectives in objectives.items():
    if len(set(member_objectives)) == 1:
        matched_groups += 1

same_objective_percentage = (matched_groups / total_groups) * 100 if total_groups > 0 else 0

print(f'El porcentaje de grupos donde todos los miembros tienen el mismo objetivo es: {same_objective_percentage:.2f}%')

# Calcular el porcentaje de grupos donde al menos el 50% de los miembros comparten el mismo objetivo
matched_groups = 0

for group_id, member_objectives in objectives.items():
    objective_counts = defaultdict(int)
    for objective in member_objectives:
        objective_counts[objective] += 1
    if any(count >= len(member_objectives) / 2 for count in objective_counts.values()):
        matched_groups += 1

half_shared_objective_percentage = (matched_groups / total_groups) * 100 if total_groups > 0 else 0

print(f'El porcentaje de grupos donde al menos el 50% de los miembros comparten el mismo objetivo es: {half_shared_objective_percentage:.2f}%')