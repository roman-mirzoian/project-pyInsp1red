from collections import UserDict
import json
from pathlib import Path
from typing import Union

from bot.constants import NOTES_DATA, USERS_DATA
from bot.models import AddressBook, Notes

DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_DIR.mkdir(exist_ok=True, parents=True)

def save_to_json(data: Union[AddressBook, Notes], filename: str):
    """Save pure JSON-serializable dict/list or objects supporting to_dict()"""
    if hasattr(data, "to_dict"):
        data = data.to_dict()

    if not isinstance(data, (dict, list, UserDict)):
        raise TypeError("Data persistence error: Data for JSON must be a dictionary or a list.")

    file_path = DATA_DIR / filename
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except TypeError as e:
        raise TypeError(f"Data serialization error in JSON: {e}")
    except IOError as e:
        raise IOError(f"Error writing to file {file_path}: {e}")
    
def create_empty_data(data_type: str):
    """Return an empty model instance based on data type constant"""
    if data_type == USERS_DATA:
        return AddressBook()
    if data_type == NOTES_DATA:
        return Notes()
    raise ValueError(f"Unknown data type: {data_type}")


def load_from_json(filename: str, data_type: str):
    """
    Load data from a JSON file and convert it into the proper model.
    Returns an AddressBook or Notes instance depending on data_type, or
    a fresh empty object if the file is missing or corrupted.
    """
    file_path = DATA_DIR / filename

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return create_empty_data(data_type)
    except json.JSONDecodeError:
        print(f"Warning: '{filename}' is corrupted. Loading empty data.")
        return create_empty_data(data_type)

    if data_type == USERS_DATA:
        return AddressBook.from_dict(raw)
    if data_type == NOTES_DATA:
        return Notes.from_dict(raw)

    return raw