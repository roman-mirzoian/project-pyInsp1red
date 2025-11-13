import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_DIR.mkdir(exist_ok=True, parents=True)

def save_to_json(data, filename):
    if not isinstance(data, (dict, list)):
        raise TypeError("Data persistence error: Data for JSON must be a dictionary or a list.")

    file_path = DATA_DIR / filename
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    except TypeError as e:
        raise TypeError(f"Data serialization error in JSON: {e}")
    except IOError as e:
        raise IOError(f"Error writing to file {file_path}: {e}")


def load_from_json(filename):
    file_path = DATA_DIR / filename  

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)        
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Warning: File {file_path} is corrupted. Loading empty data.")
        return {}