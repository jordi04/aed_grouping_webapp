import csv
from collections import defaultdict

def calculate_percentages(file_path):
    # Read the CSV file
    groups = defaultdict(list)

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            group_id = row['group_id']
            preferred_team_size = int(row['preferred_team_size'])
            groups[group_id].append(preferred_team_size)

    # Calculate the percentage of people in groups of the preferred size
    total_people = 0
    matched_people = 0

    for group_id, preferred_sizes in groups.items():
        group_size = len(preferred_sizes)
        total_people += group_size
        matched_people += preferred_sizes.count(group_size)

    percentage = (matched_people / total_people) * 100 if total_people > 0 else 0

    # Read the CSV file to get the languages
    languages = defaultdict(list)

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            group_id = row['group_id']
            member_languages = row.get('languages', '').split(',')
            languages[group_id].append(set(member_languages))

    # Calculate the percentage of groups where all members share at least one language
    total_groups = len(languages)
    matched_groups = 0

    for group_id, member_languages in languages.items():
        common_languages = set.intersection(*member_languages)
        if common_languages:
            matched_groups += 1

    group_percentage = (matched_groups / total_groups) * 100 if total_groups > 0 else 0

    # Read the CSV file to get the objectives
    objectives = defaultdict(list)

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            group_id = row['group_id']
            objective = row.get('objective', '')
            objectives[group_id].append(objective)

    # Calculate the percentage of groups where all members have the same objective
    total_groups = len(objectives)
    matched_groups = 0

    for group_id, member_objectives in objectives.items():
        if len(set(member_objectives)) == 1:
            matched_groups += 1

    same_objective_percentage = (matched_groups / total_groups) * 100 if total_groups > 0 else 0

    # Calculate the percentage of groups where at least 50% of the members share the same objective
    matched_groups = 0

    for group_id, member_objectives in objectives.items():
        objective_counts = defaultdict(int)
        for objective in member_objectives:
            objective_counts[objective] += 1
        if any(count >= len(member_objectives) / 2 for count in objective_counts.values()):
            matched_groups += 1

    half_shared_objective_percentage = (matched_groups / total_groups) * 100 if total_groups > 0 else 0

    # Return a string with the calculated percentages
    result = (
        f'The percentage of people in a group of the preferred size is: {percentage:.2f}%\n'
        f'The percentage of groups where all members share at least one language is: {group_percentage:.2f}%\n'
        f'The percentage of groups where all members have the same objective is: {same_objective_percentage:.2f}%\n'
        f'The percentage of groups where at least 50% of the members share the same objective is: {half_shared_objective_percentage:.2f}%'
    )

    return result

# Example usage
file_path = 'output_groups.csv'
result = calculate_percentages(file_path)
print(result)