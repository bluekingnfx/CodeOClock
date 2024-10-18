import json
import re

def extract_and_structure_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    # Regular expression to match the pattern ID Name followed by Description
    pattern = re.compile(r'(\w+\d+)\s+([^\n]+)\n([^\n]+)')
    matches = pattern.findall(data)

    dataset = []
    for match in matches:
        unique_id, name, description = match
        entry = {
            "uniqueId": unique_id,
            "target": f"{unique_id} {name}",
            "description": description
        }
        dataset.append(entry)

    return dataset

# Extract and structure the data
input_file = 'extract_text_data.txt'
dataset = extract_and_structure_data(input_file)

# Save the dataset to a JSON file
with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=4)

print("Dataset created and saved to dataset.json")