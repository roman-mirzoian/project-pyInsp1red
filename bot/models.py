from datetime import datetime, date, timedelta
from collections import UserDict, defaultdict
import re
from bot.constants import (
    ERROR_INVALID_PHONE,
    ERROR_INVALID_EMAIL,
    ERROR_INVALID_DATE,
    ERROR_EMPTY_NAME,
    ERROR_INVALID_NAME_LETTERS,
    ERROR_EMPTY_ADDRESS,
    ERROR_NAME_TOO_SHORT,
    ERROR_PHONE_EXISTS,
    DATE_FORMAT,
    UKRAINE_CODE
)

class Field:
    """
    Base field class that stores a single value for a contact.
    Provides a common interface for all specific field types.
    """
    def __init__(self, value):
        """
        Initialize a field with the given raw value.
        Subclasses may add validation before calling this.
        """
        self.value = value

    def __str__(self):
        """
        Returns the value as a string
        """
        return str(self.value)


class Name(Field):
    """
    Represents a contact's name with basic validation.
    Ensures name is non-empty and contains only letters.
    """
    def __init__(self, value):
        """
        Validate and normalize the name value before storing it.
        Strips whitespace and checks that the name is a single word of letters.
        """
        if not value.strip():
            raise ValueError(ERROR_EMPTY_NAME)
        
        if len(value) < 2:
            raise ValueError(ERROR_NAME_TOO_SHORT)
        
        # Check that name is a single word containing only letters
        if not re.match(r'^[a-zA-Z]+$', value.strip()):
            raise ValueError(ERROR_INVALID_NAME_LETTERS)
        
        super().__init__(value.strip())


class Phone(Field):
    """
    Represents a phone number field for a contact.
    Validates that the phone consists of exactly 10 digits.
    """
    def __init__(self, value: str):
        """
        Validate the phone number format and store it.
        Raises ValueError if the number is not 10 digits.
        """
        if len(value) != 10 or not value.isdigit() or not value.startswith(UKRAINE_CODE):
            raise ValueError(ERROR_INVALID_PHONE)
        super().__init__(value)


class Birthday(Field):
    """
    Represents a birthday date for a contact.
    Stores the date as a datetime object in a fixed format.
    """
    def __init__(self, value):
        """
        Parse and validate the date string according to DATE_FORMAT.
        Raises ValueError if the format or date value is invalid.
        """
        try:
            parsed_date = datetime.strptime(value, DATE_FORMAT)
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError(ERROR_INVALID_DATE)


class Email(Field):
    """
    Represents an email address field with basic validation.
    Ensures the email matches a simple, common pattern.
    """
    def __init__(self, value):
        """
        Validate the email string against a regex pattern.
        Raises ValueError if the email does not match the expected format.
        """
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9]'
        pattern += r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValueError(ERROR_INVALID_EMAIL)
        super().__init__(value)


class Address(Field):
    """
    Represents a text address for a contact.
    Stores a non-empty, stripped string value.
    """
    def __init__(self, value):
        """
        Validate that the address is not empty and store it.
        Strips surrounding whitespace before saving.
        """
        if not value.strip():
            raise ValueError(ERROR_EMPTY_ADDRESS)
        super().__init__(value.strip())


class Record:
    """
    Represents a full contact record with multiple fields.
    Holds name, phones, birthday, email and address for one person.
    """
    def __init__(self, name):
        """
        Initialize a contact record with the given name.
        Creates empty containers for optional fields like phones and email.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        """
        Add a new phone number to the record if it doesn't already exist.
        Validates the phone value and raises an error on duplicates.
        """
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                raise ValueError(ERROR_PHONE_EXISTS)

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Remove a phone number from the record by its string value.
        Returns True if removed successfully, otherwise False.
        """
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                self.phones.remove(existing_phone)
                return True
        return False

    def add_birthday(self, birthday):
        """
        Set or replace the birthday field for this contact.
        Accepts a date string and converts it into a Birthday object.
        """
        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        """
        Clear the birthday field if it exists.
        Returns True if birthday was removed, otherwise False.
        """
        if self.birthday:
            self.birthday = None
            return True
        return False

    def add_email(self, email):
        """
        Set or replace the email field for this contact.
        Validates the email string before storing it.
        """
        self.email = Email(email)

    def remove_email(self):
        """
        Clear the email field if it exists.
        Returns True if email was removed, otherwise False.
        """
        if self.email:
            self.email = None
            return True
        return False

    def add_address(self, address):
        """
        Set or replace the address field for this contact.
        Stores the address as an Address object.
        """
        self.address = Address(address)

    def remove_address(self):
        """
        Clear the address field if it exists.
        Returns True if address was removed, otherwise False.
        """
        if self.address:
            self.address = None
            return True
        return False

    def __str__(self):
        """
        Return a human-readable string with all available contact details.
        Includes phones, birthday, email and address when present.
        """
        result = f"Contact name: {self.name.value}"
        if self.phones:
            phones_str = "; ".join(p.value for p in self.phones)
            result += f", phones: {phones_str}"
        if self.birthday:
            birthday_str = self.birthday.value.strftime(DATE_FORMAT)
            result += f", birthday: {birthday_str}"
        if self.email:
            result += f", email: {self.email.value}"
        if self.address:
            result += f", address: {self.address.value}"
        return result
    
    def to_dict(self):
        """
        Serialize this record to a plain dictionary.
        Suitable for JSON storage and later reconstruction.
        """
        return {
            "name": self.name.value,
            "phones": [p.value for p in self.phones],
            "birthday": self.birthday.value.strftime(DATE_FORMAT) if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Record instance from a serialized dictionary.
        Restores all phones and optional fields if present.
        """
        record = cls(data["name"])

        for phone in data.get("phones", []):
            record.add_phone(phone)
        if data.get("birthday"):
            record.add_birthday(data["birthday"])
        if data.get("email"):
            record.add_email(data["email"])
        if data.get("address"):
            record.add_address(data["address"])

        return record


class AddressBook(UserDict):
    """
    Container for multiple contact records, keyed by name.
    Extends UserDict to provide find, delete and birthday utilities.
    """
    def add_record(self, record: Record):
        """
        Add a new Record to the address book.
        Uses the capitalized name as the dictionary key.
        """
        key = record.name.value.capitalize()
        self.data[key] = record

    def find(self, name) -> Record:
        """
        Find a contact record by name in a case-insensitive way.
        Returns a Record instance or None if not found.
        """
        # Search case-insensitively
        key = name.capitalize()
        return self.data.get(key)
    
    def to_dict(self):
        """
        Serialize the entire address book to a dictionary.
        Each contact is stored using its own to_dict() result.
        """
        return {name: record.to_dict() for name, record in self.data.items()}
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Rebuild an AddressBook instance from a dictionary.
        Creates Record objects for all stored contact entries.
        """
        obj = cls()
        from bot.models import Record
        for name, record_data in data.items():
            obj.data[name] = Record.from_dict(record_data)
        return obj

    def delete(self, name):
        """
        Delete a contact by name (case-insensitive).
        Returns True if deletion succeeded, otherwise False.
        """
        key = name.capitalize()
        if key in self.data:
            del self.data[key]
            return True
        return False

    def get_upcoming_birthdays(self, days_limit: int = 7):
        """
        Return a list of upcoming birthdays within the given number of days.
        Adjusts February 29 birthdays and shifts congratulations from weekends to weekdays.
        """
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_date = record.birthday.value.date()
            if birthday_date.month == 2 and birthday_date.day == 29:
                try:
                    birthday_this_year = birthday_date.replace(year=today.year)
                except ValueError:
                    birthday_this_year = date(today.year, 2, 28)
            else:
                birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if not (0 <= days_until_birthday <= days_limit):
                continue

            congratulation_date = birthday_this_year
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": record.name.value,
                "birthday": birthday_date.strftime(DATE_FORMAT),
                "congratulation_date": congratulation_date.strftime(DATE_FORMAT),
            })

        return upcoming_birthdays


class Notes(UserDict):
    """
    Container for text notes grouped by user name.
    Stores note IDs, text content and optional tags per user.
    """
    def add_note(self, user_name: str, note_text: str, tag: str = None):
        """
        Add a new note for the given user with optional tag.
        Generates a sequential string ID and returns it.
        """
        user_notes = self.data.setdefault(user_name, {})
        if user_notes:
            max_id = max(int(k) for k in user_notes.keys())
            note_id = str(max_id + 1)
        else:
            note_id = "1"

        user_notes[note_id] = {"text": note_text, "tag": tag}
        return note_id

    def edit_note(self, user_name: str, note_id: str, new_text: str):
        """
        Update the text of an existing note for a user.
        Returns the note ID on success or False if not found.
        """
        if user_name in self.data and note_id in self.data[user_name]:
            self.data[user_name][note_id]["text"] = new_text
            return note_id
        return False

    def get_all_user_notes(self, user_name: str) -> dict:
        """
        Get all notes for the specified user.
        Returns a dict of note_id to note data, or empty dict if none.
        """
        return self.data.get(user_name, {})

    def find_notes(self, note_text: str) -> dict:
        """
        Search all users' notes for a substring in the text.
        Returns a dict mapping usernames to lists of matching note info.
        """
        result = defaultdict(list)

        for user_name, notes in self.data.items():
            for note_id, note_data in notes.items():
                text = note_data.get("text", "") 
                if note_text in text:
                    result[user_name].append({
                        "id": note_id, 
                        "text": text,
                        "tag": note_data.get("tag")
                    })

        return dict(result)

    def delete_note(self, user_name: str, note_id: str):
        """
        Delete a specific note for a user by its ID.
        Returns True on success or False if user/note not found.
        """
        if user_name in self.data and note_id in self.data[user_name]:
            del self.data[user_name][note_id]
            return True

        return False
    
    def group_notes_by_tag(self) -> dict:
        """
        Group all notes from all users by their tag value.
        Notes without a tag are grouped under 'No tag'.
        """
        notes_by_tag = defaultdict(list)

        for user_name, notes in self.data.items():
            for note_id, note_data in notes.items():
                tag = note_data.get("tag")
                if tag is None or tag == "":
                    tag = "No tag"
                
                notes_by_tag[tag].append({
                    "user": user_name,
                    "id": note_id,
                    "text": note_data.get("text", "")
                })

        return dict(notes_by_tag)
    
    def to_dict(self):
        """
        Serialize all notes data to a plain dictionary.
        Useful for saving notes to JSON or other storage.
        """
        return dict(self.data)

    @classmethod
    def from_dict(cls, data):
        """
        Rebuild a Notes instance from a stored dictionary.
        Directly assigns the inner data structure and returns the object.
        """
        obj = cls()
        obj.data = data
        return obj
