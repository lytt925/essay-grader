import json
import os

def save_to_json(filepath, data):
    # read output_file to dict
    results = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = []

    # Find the dictionary with the same dirpath field
    for result in results:
        if result['dirpath'] == data['dirpath']:
            results.remove(result)
            break
    
    results.append(data)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def load_from_json(filepath):
    try:
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

# Usage
# # save_to_json('data.json', {'last_directory': '/path/to/last/directory'})
# data = load_from_json('../data.json')
# print(data)
# print(type(data))
