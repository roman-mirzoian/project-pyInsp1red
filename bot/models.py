# всі структури даних (Field, Record і так далі)

from datetime import datetime
from collections import UserDict, defaultdict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Email(Field):
    def __init__(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        super().__init__(value)


class Address(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
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
            result += f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
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
            for id, text in notes.items():
                if note_text in text:
                    result[user_name].append({"id": id, "text": text})

        return dict(result)

    def delete_note(self, user_name: str, note_id: str):
        if user_name in self.data and note_id in self.data[user_name]:
            del self.data[user_name][note_id]
            return True
        
        return False