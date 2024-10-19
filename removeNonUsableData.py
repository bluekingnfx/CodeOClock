import json
import re

# Load the JSON data with utf-8 encoding
with open('dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to check if a string contains only numbers
def is_numeric(s):
    return s.isdigit()

# Process the data
processed_data = []
for entry in data:
    if is_numeric(entry['uniqueId']):
        continue
    if entry['impact'].startswith('/'):
        continue
    processed_data.append(entry)

# Save the modified data to a new file with utf-8 encoding
with open('processed_dataset.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, indent=4)