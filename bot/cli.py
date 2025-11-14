from bot.commands import handle_command
from bot.constants import NOTES_DATA, USERS_DATA
from bot.storage import load_from_json, save_to_json

def run_bot():
    book = load_from_json('users.json', USERS_DATA)
    notes = load_from_json('notes.json', NOTES_DATA)

    # TODO: add greeting text and main menu

    try:
        while True:
            user_input = input("Enter a command: ").strip()
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