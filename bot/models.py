# всі структури даних (Field, Record і так далі)

from datetime import datetime
from collections import UserDict, defaultdict
import re
from bot.constants import (
    ERROR_INVALID_PHONE,
    ERROR_INVALID_EMAIL,
    ERROR_INVALID_DATE,
    ERROR_EMPTY_NAME,
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
        # Regular expression for email validation
        # Matches: email.test@example.com, asdsad2312@gmail.com,
        # vasia.pupkin@domain.com.ua
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
        # Check if phone already exists
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                raise ValueError(ERROR_PHONE_EXISTS)

        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

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


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)


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
