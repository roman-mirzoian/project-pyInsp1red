# робота з JSON файлом (читання/запис)
import json
from pathlib import Path
import os

DATA_DIR = Path(__file__).parent.parent / 'data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_to_json(data, filename): 

    if not isinstance(data, (dict, list)):
        raise TypeError("Дані для JSON мають бути словником або списком.")

    file_path = DATA_DIR / filename
    # try:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    # except


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
        print(f"Попередження: Файл {file_path} пошкоджено. Завантажено порожні дані.")
        return {}