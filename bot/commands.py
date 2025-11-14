from bot.utils import parse_input
from bot.models import Notes, Record
from bot.constants import (
    ERROR_NO_COMMAND,
    ERROR_INSUFFICIENT_ARGS,
    ERROR_CONTACT_NOT_FOUND,
    ERROR_PHONE_NOT_FOUND,
    ERROR_BIRTHDAY_NOT_FOUND,
    ERROR_EMAIL_NOT_FOUND,
    ERROR_ADDRESS_NOT_FOUND,
    SUCCESS_CONTACT_ADDED,
    SUCCESS_CONTACT_UPDATED,
    SUCCESS_CONTACT_DELETED,
    SUCCESS_BIRTHDAY_ADDED,
    SUCCESS_BIRTHDAY_UPDATED,
    SUCCESS_BIRTHDAY_REMOVED,
    SUCCESS_EMAIL_ADDED,
    SUCCESS_EMAIL_UPDATED,
    SUCCESS_EMAIL_REMOVED,
    SUCCESS_ADDRESS_ADDED,
    SUCCESS_ADDRESS_UPDATED,
    SUCCESS_ADDRESS_REMOVED,
    SUCCESS_PHONE_UPDATED,
    SUCCESS_PHONE_REMOVED,
    INFO_NO_CONTACTS,
    DATE_FORMAT,
)


# Decorator to handle input errors
def input_error(func):
    def inner(args, book_or_notes):
        # No command entered
        if args is None:
            return ERROR_NO_COMMAND

        # Check for specific command errors
        if func.__name__ in ("add_contact", "add_birthday", "add_email",
                             "add_address", "update_phone", "update_birthday",
                             "update_email", "update_address", "remove_phone"):
            if len(args) < 2:
                return ERROR_INSUFFICIENT_ARGS
        elif func.__name__ in ("delete_contact", "show_contact",
                               "remove_birthday", "remove_email",
                               "remove_address","all_user_notes"):
            if len(args) < 1:
                return ERROR_INSUFFICIENT_ARGS

        # Handle exceptions from the command functions
        try:
            return func(args, book_or_notes)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError:
            return ERROR_CONTACT_NOT_FOUND
        except Exception as e:
            return f"Unexpected error: {e}"

    return inner


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = SUCCESS_CONTACT_ADDED
    else:
        message = SUCCESS_CONTACT_UPDATED

    if phone:
        record.add_phone(phone)

    return message


@input_error
def add_birthday(args, book):
    name, birthday = args[0], args[1]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    record.add_birthday(birthday)
    return SUCCESS_BIRTHDAY_ADDED


@input_error
def add_email(args, book):
    if len(args) < 2:
        return "Error: Give me name and email"

    name = args[0]
    email = args[1]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    record.add_email(email)
    return SUCCESS_EMAIL_ADDED


@input_error
def add_address(args, book):
    name = args[0]
    address = " ".join(args[1:])

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    record.add_address(address)
    return SUCCESS_ADDRESS_ADDED


def show_all(book):
    if not book.data:
        return INFO_NO_CONTACTS

    result = []
    for record in book.data.values():
        result.append(str(record))

    return "\n".join(result)


@input_error
def show_contact(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    # If only name provided, show all information
    if len(args) == 1:
        return str(record)

    # If field specified, show only that field
    field = args[1].lower()

    if field in ("phone", "phones"):
        if not record.phones:
            return f"{name}: no phone numbers"
        phones = ", ".join(p.value for p in record.phones)
        return f"{name} (phones): {phones}"

    elif field == "birthday":
        if not record.birthday:
            return f"{name}: no birthday"
        return f"{name} (birthday): {record.birthday.value.strftime(DATE_FORMAT)}"

    elif field == "email":
        if not record.email:
            return f"{name}: no email"
        return f"{name} (email): {record.email.value}"

    elif field == "address":
        if not record.address:
            return f"{name}: no address"
        return f"{name} (address): {record.address.value}"

    else:
        return f"Unknown field: {field}. Available: phone, birthday, email, address"


@input_error
def delete_contact(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    book.delete(name)
    return SUCCESS_CONTACT_DELETED


@input_error
def update_phone(args, book):
    name, new_phone = args[0], args[1]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if not record.phones:
        return ERROR_PHONE_NOT_FOUND

    # Update the first phone number
    record.phones[0] = record.phones[0].__class__(new_phone)

    return SUCCESS_PHONE_UPDATED


@input_error
def update_birthday(args, book):
    name, new_birthday = args[0], args[1]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    record.add_birthday(new_birthday)
    return SUCCESS_BIRTHDAY_UPDATED


@input_error
def update_email(args, book):
    name, new_email = args[0], args[1]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    record.add_email(new_email)
    return SUCCESS_EMAIL_UPDATED


@input_error
def update_address(args, book):
    name = args[0]
    new_address = " ".join(args[1:])

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    record.add_address(new_address)
    return SUCCESS_ADDRESS_UPDATED


@input_error
def remove_phone(args, book):
    name, phone = args[0], args[1]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if record.remove_phone(phone):
        return SUCCESS_PHONE_REMOVED
    else:
        return ERROR_PHONE_NOT_FOUND


@input_error
def remove_birthday(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if record.remove_birthday():
        return SUCCESS_BIRTHDAY_REMOVED
    else:
        return ERROR_BIRTHDAY_NOT_FOUND


@input_error
def remove_email(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if record.remove_email():
        return SUCCESS_EMAIL_REMOVED
    else:
        return ERROR_EMAIL_NOT_FOUND


@input_error
def remove_address(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if record.remove_address():
        return SUCCESS_ADDRESS_REMOVED
    else:
        return ERROR_ADDRESS_NOT_FOUND


def handle_command(user_input: str, book, notes: Notes):
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
        "add": lambda: add_contact(args, book),
        "add-birthday": lambda: add_birthday(args, book),
        "add-email": lambda: add_email(args, book),
        "add-address": lambda: add_address(args, book),
        "all": lambda: show_all(book),
        "show": lambda: show_contact(args, book),
        "delete": lambda: delete_contact(args, book),
        "update-phone": lambda: update_phone(args, book),
        "update-birthday": lambda: update_birthday(args, book),
        "update-email": lambda: update_email(args, book),
        "update-address": lambda: update_address(args, book),
        "remove-phone": lambda: remove_phone(args, book),
        "remove-birthday": lambda: remove_birthday(args, book),
        "remove-email": lambda: remove_email(args, book),
        "remove-address": lambda: remove_address(args, book),
        "add-note": lambda: add_note(args, notes),
        "edit-note": lambda: edit_note(args, notes),
        "find-notes": lambda: find_notes(args, notes),
        "all-notes": lambda: all_user_notes(args, notes),
        "delete-note": lambda: delete_note(args, notes),
    }

    if command in ("close", "exit"):
        return "exit"

    func = commands.get(command)
    if func:
        return func()
    else:
        return f"Invalid command: {command}"


def add_note(args, notes: Notes) -> str:
    user_name, *text_parts = args
    
    tag = None
    note_text_parts = []

    if text_parts and text_parts[0].startswith("tag="):
        tag = text_parts[0][4:] 
        note_text_parts = text_parts[1:] 
    else:
        note_text_parts = text_parts

    note_text = " ".join(note_text_parts)

    # TODO: add user existence check
    note_id = notes.add_note(user_name, note_text, tag) 

    return f"A new note with ID {note_id} for '{user_name}' has been added."


def edit_note(args, notes: Notes):
    pass


def find_notes(args, notes: Notes) -> str:
    note_part = " ".join(args)

    search_result = notes.find_notes(note_part)
    if not len(search_result):
        return f"'{note_part}' not found in any notes."

    search_message = "Here are the search matches:\n"
    for user_name, notes in search_result.items():
        search_message += f"{'':<4}{user_name}: \n"
        for note in notes:
            search_message += f"{'':<8}#{note['id']}: {note['text']}\n"

    return search_message


@input_error
def all_user_notes(args, notes: Notes) -> str:
    user_name = args[0]

    # TODO: add user existence check

    user_notes = notes.get_all_user_notes(user_name)

    notes_message = f"Here are all the notes from user '{user_name}':\n"
    for note_id, note_data in user_notes.items():
        text = note_data.get("text", "")
        tag = note_data.get("tag")

        note_display = f"#{note_id}: {text}"
        if tag:
            note_display += f" [Tag: {tag}]" 
        
        notes_message += f"{'':<4}{note_display}\n"

    return notes_message


def delete_note(args, notes: Notes) -> str:
    user_name, note_id = args

    # TODO: add user existence check
    is_note_deleted = notes.delete_note(user_name, note_id)
    if not is_note_deleted:
        return "The note was not deleted, check the username and note ID."

    return f"The note for '{user_name}' has been deleted."
