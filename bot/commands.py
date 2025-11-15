import prompt_toolkit
from bot.decorators import input_error, user_exists
from bot.utils import parse_input
from bot.models import AddressBook, Notes, Record
from bot.constants import (
    ERROR_INSUFFICIENT_ARGS,
    ERROR_CONTACT_NOT_FOUND,
    ERROR_PHONE_NOT_FOUND,
    ERROR_BIRTHDAY_NOT_FOUND,
    ERROR_EMAIL_NOT_FOUND,
    ERROR_ADDRESS_NOT_FOUND,
    SUCCESS_CONTACT_ADDED,
    SUCCESS_CONTACT_UPDATED,
    SUCCESS_CONTACT_DELETED,
    SUCCESS_PHONE_ADDED,
    SUCCESS_PHONE_UPDATED,
    SUCCESS_PHONE_REMOVED,
    SUCCESS_BIRTHDAY_ADDED,
    SUCCESS_BIRTHDAY_UPDATED,
    SUCCESS_BIRTHDAY_REMOVED,
    SUCCESS_EMAIL_ADDED,
    SUCCESS_EMAIL_UPDATED,
    SUCCESS_EMAIL_REMOVED,
    SUCCESS_ADDRESS_ADDED,
    SUCCESS_ADDRESS_UPDATED,
    SUCCESS_ADDRESS_REMOVED,
    INFO_NO_CONTACTS,
    DATE_FORMAT,
)

@input_error
def add_contact(args, book):
    if len(args) < 1:
        return ERROR_INSUFFICIENT_ARGS

    name = args[0]

    # Case 1: add John - just create contact
    if len(args) == 1:
        record = book.find(name)
        if record is None:
            # Capitalize name for consistency
            record = Record(name.capitalize())
            book.add_record(record)
            return SUCCESS_CONTACT_ADDED
        else:
            return "Contact already exists"

    # Case 2: add John 1231231231 - create contact + add phone
    # Check if second arg is a phone number (10 digits)
    if len(args) == 2 and args[1].isdigit() and len(args[1]) == 10:
        record = book.find(name)
        if record is None:
            # Capitalize name for consistency
            record = Record(name.capitalize())
            book.add_record(record)
            message = SUCCESS_CONTACT_ADDED
        else:
            message = SUCCESS_CONTACT_UPDATED

        record.add_phone(args[1])
        return message

    # Case 3: add John phone 1231231231 - add field to existing contact
    if len(args) >= 3:
        field = args[1].lower()

        record = book.find(name)
        if record is None:
            # Auto-create contact if it doesn't exist (capitalize name)
            record = Record(name.capitalize())
            book.add_record(record)

        if field in ("phone", "phones"):
            phone = args[2]
            record.add_phone(phone)
            return SUCCESS_PHONE_ADDED if hasattr(record, 'phones') and len(record.phones) > 0 else SUCCESS_CONTACT_UPDATED

        elif field == "birthday":
            birthday = args[2]
            record.add_birthday(birthday)
            return SUCCESS_BIRTHDAY_ADDED

        elif field == "email":
            email = args[2]
            record.add_email(email)
            return SUCCESS_EMAIL_ADDED

        elif field == "address":
            address = " ".join(args[2:])
            record.add_address(address)
            return SUCCESS_ADDRESS_ADDED

        else:
            return f"Unknown field: {field}. Available: phone, birthday, email, address"

    return ERROR_INSUFFICIENT_ARGS


@input_error
def get_upcoming_birthdays(args, book):
    days_limit = int(input("How many days ahead should you search? "))
    birthdays = book.get_upcoming_birthdays(days_limit)
    if not birthdays:
        return "There are no birthdays in the selected period."
    birthdays_message = []
    for b in birthdays:
        birthdays_message.append(
            f"{b['name']}, birthday {b['birthday']} – need to wish {b['congratulation_date']}"
        )
    return "\n".join(birthdays_message)


def show_all(book):
    if not book.data:
        return INFO_NO_CONTACTS

    result = []
    for record in book.data.values():
        result.append(str(record))

    return "\n".join(result)


@input_error
@user_exists
def show_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    # If only name provided, show all information
    if len(args) == 1:
        return str(record)

    # If field specified, show only that field
    stored_name = record.name.value
    field = args[1].lower()

    if field in ("phone", "phones"):
        if not record.phones:
            return f"{stored_name}: no phone numbers"
        phones = ", ".join(p.value for p in record.phones)
        return f"{stored_name} (phones): {phones}"

    elif field == "birthday":
        if not record.birthday:
            return f"{stored_name}: no birthday"
        return f"{stored_name} (birthday): {record.birthday.value.strftime(DATE_FORMAT)}"

    elif field == "email":
        if not record.email:
            return f"{stored_name}: no email"
        return f"{stored_name} (email): {record.email.value}"

    elif field == "address":
        if not record.address:
            return f"{stored_name}: no address"
        return f"{stored_name} (address): {record.address.value}"

    else:
        return f"Unknown field: {field}. Available: phone, birthday, email, address"


@input_error
def find_contacts(args, book: AddressBook):
    if len(args) < 1:
        return ERROR_INSUFFICIENT_ARGS

    search_string = args[0].lower()

    # Case 1: find search_string - search all fields
    if len(args) == 1:
        results = []
        for record in book.data.values():
            # Search in name
            if search_string in record.name.value.lower():
                results.append(record)
                continue

            # Search in phones
            if any(search_string in phone.value for phone in record.phones):
                results.append(record)
                continue

            # Search in birthday
            if record.birthday and search_string in record.birthday.value.strftime(DATE_FORMAT):
                results.append(record)
                continue

            # Search in email
            if record.email and search_string in record.email.value.lower():
                results.append(record)
                continue

            # Search in address
            if record.address and search_string in record.address.value.lower():
                results.append(record)
                continue

        if not results:
            return f"No contacts found matching '{args[0]}'"

        return "\n".join(str(record) for record in results)

    # Case 2: find search_string field - search specific field
    field = args[1].lower()
    results = []

    if field in ("phone", "phones"):
        for record in book.data.values():
            if any(search_string in phone.value for phone in record.phones):
                results.append(record)

    elif field == "birthday":
        for record in book.data.values():
            if record.birthday and search_string in record.birthday.value.strftime(DATE_FORMAT):
                results.append(record)

    elif field == "email":
        for record in book.data.values():
            if record.email and search_string in record.email.value.lower():
                results.append(record)

    elif field == "address":
        for record in book.data.values():
            if record.address and search_string in record.address.value.lower():
                results.append(record)

    elif field == "name":
        for record in book.data.values():
            if search_string in record.name.value.lower():
                results.append(record)

    else:
        return f"Unknown field: {field}. Available: name, phone, birthday, email, address"

    if not results:
        return f"No contacts found with '{args[0]}' in {field}"

    return "\n".join(str(record) for record in results)

@input_error
@user_exists
def delete_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    book.delete(name)
    return SUCCESS_CONTACT_DELETED

@input_error
@user_exists
def update_contact(args, book: AddressBook):
    if len(args) < 3:
        return ERROR_INSUFFICIENT_ARGS

    name = args[0]
    field = args[1].lower()

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if field in ("phone", "phones"):
        new_phone = args[2]
        if not record.phones:
            return ERROR_PHONE_NOT_FOUND
        # Update the first phone number
        record.phones[0] = record.phones[0].__class__(new_phone)
        return SUCCESS_PHONE_UPDATED

    elif field == "birthday":
        new_birthday = args[2]
        record.add_birthday(new_birthday)
        return SUCCESS_BIRTHDAY_UPDATED

    elif field == "email":
        new_email = args[2]
        record.add_email(new_email)
        return SUCCESS_EMAIL_UPDATED

    elif field == "address":
        new_address = " ".join(args[2:])
        record.add_address(new_address)
        return SUCCESS_ADDRESS_UPDATED

    else:
        return f"Unknown field: {field}. Available: phone, birthday, email, address"

@input_error
@user_exists
def remove_field(args, book: AddressBook):
    if len(args) < 1:
        return ERROR_INSUFFICIENT_ARGS

    name = args[0]

    # Case 1: remove John - delete entire contact
    if len(args) == 1:
        if book.delete(name):
            return SUCCESS_CONTACT_DELETED
        else:
            return ERROR_CONTACT_NOT_FOUND

    # Case 2: remove John field [value] - remove specific field
    field = args[1].lower()

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if field in ("phone", "phones"):
        if len(args) < 3:
            return ERROR_INSUFFICIENT_ARGS
        phone = args[2]
        if record.remove_phone(phone):
            return SUCCESS_PHONE_REMOVED
        else:
            return ERROR_PHONE_NOT_FOUND

    elif field == "birthday":
        if record.remove_birthday():
            return SUCCESS_BIRTHDAY_REMOVED
        else:
            return ERROR_BIRTHDAY_NOT_FOUND

    elif field == "email":
        if record.remove_email():
            return SUCCESS_EMAIL_REMOVED
        else:
            return ERROR_EMAIL_NOT_FOUND

    elif field == "address":
        if record.remove_address():
            return SUCCESS_ADDRESS_REMOVED
        else:
            return ERROR_ADDRESS_NOT_FOUND

    else:
        return f"Unknown field: {field}. Available: phone, birthday, email, address"


def handle_command(user_input: str, book: AddressBook, notes: Notes):
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
        # book commands
        "add": lambda: add_contact(args, book),
        "all": lambda: show_all(book),
        "birthdays": lambda: get_upcoming_birthdays(args, book),
        "show": lambda: show_contact(args, book),
        "find": lambda: find_contacts(args, book),
        "delete": lambda: delete_contact(args, book),
        "update": lambda: update_contact(args, book),
        "remove": lambda: remove_field(args, book),
        # note commands
        "add-note": lambda: add_note(args, book=book, notes=notes),
        "edit-note": lambda: edit_note(args, book=book, notes=notes),
        "find-notes": lambda: find_notes(args, notes=notes),
        "all-notes": lambda: all_user_notes(args, book=book, notes=notes),
        "delete-note": lambda: delete_note(args, book=book, notes=notes),
        "find-tag": lambda: find_notes_by_tag(args, notes=notes),
        "sort-notes": lambda: sort_notes_by_tag(notes),
    }

    if command in ("close", "exit"):
        return "exit"

    func = commands.get(command)
    if func:
        return func()
    else:
        return f"Invalid command: {command}"

@input_error
@user_exists
def add_note(args, book: AddressBook, notes: Notes) -> str:
    user_name, *text_parts = args
    
    tag = None
    note_text_parts = []
    
    if text_parts:
        parts = text_parts[0].split("=", 1) 
        
        if len(parts) == 2 and parts[0] == "tag":
            tag = parts[1]
            note_text_parts = text_parts[1:]
        else:
            note_text_parts = text_parts
    else:
        note_text_parts = text_parts

    note_text = " ".join(note_text_parts)
    note_id = notes.add_note(user_name, note_text, tag) 

    return f"A new note with ID {note_id} for '{user_name}' has been added."

@input_error
@user_exists
def edit_note(args, notes: Notes):
    user_name, note_id  = args
    all_user_notes = notes.get_all_user_notes(user_name)
    editing_note = all_user_notes.get(note_id, {})
    text_for_edit = editing_note.get("text", "")
    new_text = prompt_toolkit.prompt("Enter the new note text: ", default=text_for_edit)
    
    note_id = notes.edit_note(user_name, note_id, new_text)
    if not note_id:
        return "The note was not edited, check the username and note ID."
    return f"The note #{note_id} for '{user_name}' has been updated."

@input_error
def find_notes(args, notes: Notes) -> str:
    note_part = " ".join(args)

    search_result = notes.find_notes(note_part)
    if not len(search_result):
        return f"'{note_part}' not found in any notes."

    search_message = "Here are the search matches:\n"
    for user_name, notes_list in search_result.items():
        search_message += f"{'':<4}{user_name}: \n"
        
        for note in notes_list:
            text = note.get("text", "")
            tag = note.get("tag")
            
            note_display = ""
            if tag:
                note_display += f"[Tag: {tag}] "
            
            note_display += f"#{note['id']}: {text}"
            
            search_message += f"{'':<8}{note_display}\n"

    return search_message


@input_error
@user_exists
def all_user_notes(args, book: AddressBook, notes: Notes) -> str:
    user_name = args[0]
    user_notes = notes.get_all_user_notes(user_name)

    notes_message = f"Here are all the notes from user '{user_name}':\n"
    for note_id, note_data in user_notes.items():
        text = note_data.get("text", "")
        tag = note_data.get("tag")

        note_display = ""
        if tag:
            note_display += f"[Tag: {tag}] "
            
        note_display += f"#{note_id}: {text}"
        notes_message += f"{'':<4}{note_display}\n"

    return notes_message

@input_error
@user_exists
def delete_note(args, book: AddressBook, notes: Notes) -> str:
    user_name, note_id = args
    is_note_deleted = notes.delete_note(user_name, note_id)
    if not is_note_deleted:
        return "The note was not deleted, check the username and note ID."

    return f"The note for '{user_name}' has been deleted."


def _format_note_output(note_info: dict) -> str:
    user = note_info.get('user', 'Unknown')
    note_id = note_info.get('id', '?')
    text = note_info.get('text', '')
    
    return f"{'':<4}User: {user}, #{note_id}: {text}\n"


@input_error
def find_notes_by_tag(args, notes: Notes) -> str:
    tag_to_find = args[0]
    all_notes_by_tag = notes.find_and_group_by_tag()

    if tag_to_find not in all_notes_by_tag:
        return f"Notes with tag '{tag_to_find}' not found."

    search_message = f"Found notes with tag '{tag_to_find}':\n"
    
    for note_info in all_notes_by_tag[tag_to_find]:
        search_message += _format_note_output(note_info)
    
    return search_message

def sort_notes_by_tag(notes: Notes) -> str:
    all_notes_by_tag = notes.group_notes_by_tag()

    if not all_notes_by_tag:
        return "No notes found."

    sorted_tags = sorted(all_notes_by_tag.keys())

    search_message = "All notes, sorted by tag:\n"

    for tag in sorted_tags:
        search_message += f"\n  [Tag: {tag}]\n"
        
        for note_info in all_notes_by_tag[tag]:
            search_message += _format_note_output(note_info)
    
    return search_message