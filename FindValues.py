import re
import json

def process_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    pattern = re.compile(r'(\w+\d+)\s+([^\n]+)\n([^\n]+)')
    matches = pattern.findall(data)

    dataset = []
    current_tactic = "Unknown"
    current_mitigation = "Unknown"
    
    url_pattern = re.compile(r'(https://attack\.mitre\.org/techniques/T\d+)')
    tactic_pattern = re.compile(r'Tactic:\s*([^\n]+)')
    mitigation_pattern = re.compile(r'Mitigations:\s*\n([^\n]+)')

    for match in matches:
        unique_id, name, description = match
        entry = {
            "uniqueId": unique_id,
            "procedure": name.strip(),
            "impact": description.strip(),
            "tactic": current_tactic,
            
        }

        # Check for URL and update tactic if found
        url_match = url_pattern.search(data)
        if url_match:
            url = url_match.group(1)
            tactic_match = tactic_pattern.search(data[url_match.end():])
            if tactic_match:
                current_tactic = tactic_match.group(1).strip()
            data = data[url_match.end():]  # Remove processed part

        # Check for mitigation
        mitigation_match = mitigation_pattern.search(data)
        if mitigation_match:
            current_mitigation = mitigation_match.group(1).strip()
            data = data[mitigation_match.end():]  # Remove processed part

        entry["tactic"] = current_tactic
        
        dataset.append(entry)

    return dataset

# Process the data
result = process_data('extract_text_data.txt')

# Write the result to a JSON file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=2, ensure_ascii=False)

print("Data has been processed and saved to output.json")