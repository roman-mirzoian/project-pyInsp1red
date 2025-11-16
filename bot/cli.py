from bot.commands import handle_command
from bot.utils import Log, log_result, print_help
from bot.completer import session
from bot.constants import NOTES_DATA, USERS_DATA
from bot.storage import load_from_json, save_to_json
from time import sleep

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
                log_result(result)
    except KeyboardInterrupt:
        Log.warning("Oops! Looks like you want to quit. Saving your data...")
        # a little delay just for fun
        sleep(1)
    finally:
        save_to_json(book, 'users.json')
        save_to_json(notes, 'notes.json')
        Log.success("See you next time!")