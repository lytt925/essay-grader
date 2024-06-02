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
    # mkdir if not exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def load_from_json(filepath):
    try:
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []