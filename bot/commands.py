from bot.utils import Log, parse_input, print_help
import prompt_toolkit
from bot.decorators import input_error, user_exists
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
def add_contact(args, book: AddressBook):
    """
    Add a contact to the address book using the given args and book.
    Supports: just name, name + phone, or name + field (phone, birthday, email, address) + value.
    """
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
def get_upcoming_birthdays(args, book: AddressBook):
    """
    Ask user for a days range and fetch upcoming birthdays from the book.
    Returns a formatted multiline string with names and congratulation dates or a fallback message.
    """
    while True:
        user_input = input("How many days ahead should you search? ")

        try:
            days_limit = int(user_input)
            break
        except ValueError:
            Log.warning("Please enter a valid integer.")
    
    birthdays = book.get_upcoming_birthdays(days_limit)
    if not birthdays:
        return "There are no birthdays in the selected period."
    birthdays_message = []
    for b in birthdays:
        birthdays_message.append(
            f"{b['name']}, birthday {b['birthday']} – need to wish {b['congratulation_date']}"
        )
    return "\n".join(birthdays_message)


def show_all(book: AddressBook):
    """
    Return a formatted list of all contacts stored in the address book.
    If the book is empty, returns an informational message instead.
    """
    if not book.data:
        return INFO_NO_CONTACTS

    result = []
    for record in book.data.values():
        result.append(str(record))

    return "\n".join(result)


@input_error
@user_exists
def show_contact(args, book: AddressBook, notes: Notes):
    """
    Show full info about a contact or a specific field for a given name.
    Supports fields: phone, birthday, email, address; returns formatted text.
    """
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
    """
    Search contacts in the address book by substring in all fields or a specific field.
    Returns formatted matches or a message if nothing is found.
    """
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
def delete_contact(args, book: AddressBook, notes: Notes):
    """
    Delete a contact from the address book by name.
    Returns a success message or an error if the contact is not found.
    """
    name = args[0]
    record = book.find(name)
    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    book.delete(name)
    return SUCCESS_CONTACT_DELETED

@input_error
@user_exists
def update_contact(args, book: AddressBook, notes=Notes):
    """
    Update one field of an existing contact (phone, birthday, email, address).
    Expects: name, field name, and new value; returns a status message.
    """
    if len(args) < 3:
        return ERROR_INSUFFICIENT_ARGS

    name = args[0]
    field = args[1].lower()

    record = book.find(name)

    if record is None:
        return ERROR_CONTACT_NOT_FOUND

    if field in ("phone", "phones"):
        try:
            old_phone = args[2]
            new_phone = args[3]
        except IndexError:
            return "Please enter command arguments"
        
        for i, phone_obj in enumerate(record.phones):
            if phone_obj.value == old_phone:
                record.phones[i] = phone_obj.__class__(new_phone)
                return SUCCESS_PHONE_UPDATED
        return ERROR_PHONE_NOT_FOUND

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
def remove_field(args, book: AddressBook, notes: Notes):
    """
    Remove a whole contact or a specific field value from it.
    Supports removing phone, birthday, email, or address, based on args.
    """
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

@input_error
@user_exists
def add_note(args, book: AddressBook, notes: Notes) -> str:
    """
    Create a new note for a user, optionally with a 'tag=...' prefix.
    Returns a message with the newly created note ID.
    """
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
def edit_note(args, book: AddressBook, notes: Notes):
    """
    Edit text of an existing note for a given user and note ID.
    Prompts user with the current text as default and saves the updated version.
    """
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
    """
    Search notes by a text fragment across all users.
    Returns a grouped, formatted list of matches or a not-found message.
    """
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
    """
    Return all notes for a specific user in a readable list.
    Each note line includes optional tag, ID and text.
    """
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
    """
    Delete a specific note for a user by note ID.
    Returns a success message or an error if the note/user is invalid.
    """
    user_name, note_id = args
    is_note_deleted = notes.delete_note(user_name, note_id)
    if not is_note_deleted:
        return "The note was not deleted, check the username and note ID."

    return f"The note for '{user_name}' has been deleted."


def _format_note_output(note_info: dict) -> str:
    """
    Format a single note entry into a human-readable string.
    Includes user name, note ID and note text aligned with basic indentation.
    """
    user = note_info.get('user', 'Unknown')
    note_id = note_info.get('id', '?')
    text = note_info.get('text', '')
    
    return f"{'':<4}User: {user}, #{note_id}: {text}\n"


@input_error
def find_notes_by_tag(args, notes: Notes) -> str:
    """
    Find notes grouped by tag and return those matching the given tag.
    Shows all notes under that tag or a message if none exist.
    """
    tag_to_find = args[0]
    
    all_notes_by_tag = notes.group_notes_by_tag()

    if tag_to_find not in all_notes_by_tag:
        return f"Notes with tag '{tag_to_find}' not found."

    search_message = f"Found notes with tag '{tag_to_find}':\n"
    
    for note_info in all_notes_by_tag[tag_to_find]:
        search_message += _format_note_output(note_info)
    
    return search_message

def sort_notes_by_tag(notes: Notes) -> str:
    """
    Group all notes by their tags and show them in sorted tag order.
    Returns a multiline string with sections per tag and formatted notes.
    """
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

def handle_command(user_input: str, book: AddressBook, notes: Notes):
    """
    Parse raw user input into a command and its args, then dispatch it.
    Uses a mapping of command names to handler functions for contacts and notes.
    """
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
        "help": lambda: print_help(args),
        # book commands
        "add": lambda: add_contact(args, book),
        "all": lambda: show_all(book),
        "birthdays": lambda: get_upcoming_birthdays(args, book),
        "show": lambda: show_contact(args, book=book, notes=notes),
        "find": lambda: find_contacts(args, book),
        "delete": lambda: delete_contact(args, book, notes=notes),
        "update": lambda: update_contact(args, book=book, notes=notes),
        "remove": lambda: remove_field(args, book=book, notes=notes),
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