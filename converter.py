# import csv
# import json

# csv_file_path = 'movie_metadata.csv'
# json_file_path = 'movie_metadata.json'

# data = []

# with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
    
#     for row in csv_reader:
#         data.append(row)
        
# with open(json_file_path, mode='w', encoding='utf-8') as json_file:
#     json_file.write(json.dumps(data, indent=4))

import csv
import json
from collections import defaultdict

# Step 1: Read the CSV File
filename = 'movie_metadata.csv'
directors_actors = defaultdict(set)  # A dictionary to hold directors and their actors

with open(filename, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        directors_actors[row['director_name']].update([row['actor_1_name'], row['actor_2_name'], row['actor_3_name']])

# Step 2: Process Collaborations
collaborations = defaultdict(lambda: defaultdict(int))  # Nested dictionary to count collaborations

for director, actors in directors_actors.items():
    for other_director, other_actors in directors_actors.items():
        if director != other_director:
            shared_actors = actors.intersection(other_actors)
            if shared_actors:
                collaborations[director][other_director] += len(shared_actors)

# Preparing the data for JSON
nodes = [{"id": director, "group": 1} for director in directors_actors.keys()]
links = [{"source": source, "target": target, "value": value} 
         for source, targets in collaborations.items() 
         for target, value in targets.items()]

output = {"nodes": nodes, "links": links}

# Step 3: Write to JSON
with open('movie_director_node.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(output, jsonfile, ensure_ascii=False, indent=4)
