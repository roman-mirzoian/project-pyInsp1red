from bot.utils import parse_input
from bot.models import Notes

def handle_command(user_input: str, book, notes: Notes):
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
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
        print(f"Invalid command: {command}")

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