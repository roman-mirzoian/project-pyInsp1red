from bot.utils import parse_input
from bot.models import Notes
from bot.models import Record


def add_contact(args, book):
    if len(args) < 2:
        return "Error: Give me name and phone"
    
    name = args[0]
    phone = args[1]
    
    try:
        record = book.find(name)
        
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        
        record.add_phone(phone)
        return message
    
    except ValueError as e:
        return f"Error: {e}"


def add_birthday(args, book):
    if len(args) < 2:
        return "Error: Give me name and birthday"
    
    name = args[0]
    birthday = args[1]
    
    record = book.find(name)
    
    if record is None:
        return "Error: Contact not found"
    
    try:
        record.add_birthday(birthday)
        return "Birthday added."
    except ValueError as e:
        return f"Error: {e}"


def add_email(args, book):
    if len(args) < 2:
        return "Error: Give me name and email"
    
    name = args[0]
    email = args[1]
    
    record = book.find(name)
    
    if record is None:
        return "Error: Contact not found"
    
    try:
        record.add_email(email)
        return "Email added."
    except ValueError as e:
        return f"Error: {e}"


def add_address(args, book):
    if len(args) < 2:
        return "Error: Please provide name and address"
    
    name = args[0]
    address = " ".join(args[1:])
    
    record = book.find(name)
    
    if record is None:
        return "Error: Contact not found"
    
    record.add_address(address)
    return "Address added."


def show_all(book):
    if not book.data:
        return "No contacts"
    
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
    for id, note in user_notes.items():
        notes_message += f"{'':<4}#{id}: {note}\n"

    return notes_message

def delete_note(args, notes: Notes) -> str:
    user_name, note_id = args

    # TODO: add user existence check
    isNoteDeleted = notes.delete_note(user_name, note_id)
    if not isNoteDeleted:
        return "The note was not deleted, check the username and note ID."

    return f"The note for '{user_name}' has been deleted."