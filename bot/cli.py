from bot.commands import handle_command
from bot.models import Notes
from bot.utils import print_help
from bot.completer import session
from bot.constants import NOTES_DATA, USERS_DATA
from bot.storage import load_from_json, save_to_json

def run_bot():
    """
    Run the interactive Personal Assistant bot loop:
    loads data, processes user commands, and saves before exit.
    """

    book = load_from_json('users.json', USERS_DATA)
    notes = load_from_json('notes.json', NOTES_DATA)

    print("\n\033[32;1m=== Welcome to your Personal Assistant Bot! ===\033[0m\n")
    print_help(args=[])
    
    try:
        while True:
            user_input = session.prompt(">>> ")
            if not user_input:
                continue

            result = handle_command(user_input, book=book, notes=notes)
            if result == "exit":
                break
            elif result is not None:
                print(result)
    except KeyboardInterrupt:
        print("\nOops! Looks like you want to quit. Saving your data...")
    finally:
        save_to_json(book, 'users.json')
        save_to_json(notes, 'notes.json')
        print("See you next time!")