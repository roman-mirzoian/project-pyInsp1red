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
    ERROR_PHONE_EXISTS,
    DATE_FORMAT
)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError(ERROR_EMPTY_NAME)
        
        # Check that name is a single word containing only letters
        if not re.match(r'^[a-zA-Z]+$', value.strip()):
            raise ValueError(ERROR_INVALID_NAME_LETTERS)
        
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError(ERROR_INVALID_PHONE)
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, DATE_FORMAT)
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError(ERROR_INVALID_DATE)


class Email(Field):
    def __init__(self, value):
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9]'
        pattern += r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValueError(ERROR_INVALID_EMAIL)
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError(ERROR_EMPTY_ADDRESS)
        super().__init__(value.strip())


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                raise ValueError(ERROR_PHONE_EXISTS)

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                self.phones.remove(existing_phone)
                return True
        return False

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        if self.birthday:
            self.birthday = None
            return True
        return False

    def add_email(self, email):
        self.email = Email(email)

    def remove_email(self):
        if self.email:
            self.email = None
            return True
        return False

    def add_address(self, address):
        self.address = Address(address)

    def remove_address(self):
        if self.address:
            self.address = None
            return True
        return False

    def __str__(self):
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
        return {
            "name": self.name.value,
            "phones": [p.value for p in self.phones],
            "birthday": self.birthday.value.strftime(DATE_FORMAT) if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
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
    def add_record(self, record: Record):
        key = record.name.value.capitalize()
        self.data[key] = record

    def find(self, name):
        # Search case-insensitively
        key = name.capitalize()
        return self.data.get(key)
    
    def to_dict(self):
        return {name: record.to_dict() for name, record in self.data.items()}
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        from bot.models import Record
        for name, record_data in data.items():
            obj.data[name] = Record.from_dict(record_data)
        return obj

    def delete(self, name):
        # Delete case-insensitively
        key = name.capitalize()
        if key in self.data:
            del self.data[key]
            return True
        return False

    def get_upcoming_birthdays(self, days_limit: int = 7):
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
    def add_note(self, user_name: str, note: str):
        user_notes = self.data.setdefault(user_name, {})
        if user_notes:
            max_id = max(int(k) for k in user_notes.keys())
            note_id = str(max_id + 1)
        else:
            note_id = "1"

        user_notes[note_id] = note
        return note_id

    def edit_note(self):
        pass

    def get_all_user_notes(self, user_name: str) -> dict:
        return self.data.get(user_name, {})

    def find_notes(self, note_text: str) -> dict:
        result = defaultdict(list)

        for user_name, notes in self.data.items():
            for note_id, text in notes.items():
                if note_text in text:
                    result[user_name].append({"id": note_id, "text": text})

        return dict(result)

    def delete_note(self, user_name: str, note_id: str):
        if user_name in self.data and note_id in self.data[user_name]:
            del self.data[user_name][note_id]
            return True

        return False
    
    def to_dict(self):
        return dict(self.data)

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.data = data
        return obj
