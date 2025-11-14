from bot.utils import parse_input
from bot.models import Notes, Record, AddressBook
from bot.constants import (
    ERROR_NO_COMMAND,
    ERROR_GIVE_NAME_PHONE,
    ERROR_GIVE_NAME_BIRTHDAY,
    ERROR_GIVE_NAME_EMAIL,
    ERROR_GIVE_NAME_ADDRESS,
    ERROR_CONTACT_NOT_FOUND,
    SUCCESS_CONTACT_ADDED,
    SUCCESS_CONTACT_UPDATED,
    SUCCESS_BIRTHDAY_ADDED,
    SUCCESS_EMAIL_ADDED,
    SUCCESS_ADDRESS_ADDED,
    INFO_NO_CONTACTS,
)


# Decorator to handle input errors
def input_error(func):
    def inner(args, book_or_notes):
        # No command entered
        if args is None:
            return ERROR_NO_COMMAND

        # Check for specific command errors
        if func.__name__ == "add_contact":
            if len(args) == 0:
                return ERROR_GIVE_NAME_PHONE
            elif len(args) == 1:
                return ERROR_GIVE_NAME_PHONE
        elif func.__name__ == "add_birthday":
            if len(args) < 2:
                return ERROR_GIVE_NAME_BIRTHDAY
        elif func.__name__ == "add_email":
            if len(args) < 2:
                return ERROR_GIVE_NAME_EMAIL
        elif func.__name__ == "add_address":
            if len(args) < 2:
                return ERROR_GIVE_NAME_ADDRESS

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
def get_upcoming_birthdays(args, book):
    days_limit = int(input("How many days ahead should you search? "))
    birthdays = book.get_upcoming_birthdays(days_limit)
    if not birthdays:
        return "There are no birthdays in the selected period."

    lines = []
    for b in birthdays:
        lines.append(
            f"{b['name']}, birthday {b['birthday']} – need to wish {b['congratulation_date']}"
        )
    return "\n".join(lines)


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


def handle_command(user_input: str, book, notes: Notes):
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
        "add": lambda: add_contact(args, book),
        "add-birthday": lambda: add_birthday(args, book),
        "birthdays": lambda: get_upcoming_birthdays(args, book),
        "add-email": lambda: add_email(args, book),
        "add-address": lambda: add_address(args, book),
        "all": lambda: show_all(book),
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
    user_name, *text = args

    # TODO: add user existence check
    note_id = notes.add_note(user_name, " ".join(text))

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


def all_user_notes(args, notes: Notes) -> str:
    user_name = args[0]

    # TODO: add user existence check

    user_notes = notes.get_all_user_notes(user_name)

    notes_message = f"Here are all the notes from user '{user_name}':\n"
    for note_id, note in user_notes.items():
        notes_message += f"{'':<4}#{note_id}: {note}\n"

    return notes_message


def delete_note(args, notes: Notes) -> str:
    user_name, note_id = args

    # TODO: add user existence check
    is_note_deleted = notes.delete_note(user_name, note_id)
    if not is_note_deleted:
        return "The note was not deleted, check the username and note ID."

    return f"The note for '{user_name}' has been deleted."
