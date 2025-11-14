from bot.commands import handle_command
from bot.models import Notes, AddressBook


def run_bot():
    # TODO: add saving notes to disk
    book = AddressBook()
    notes = Notes()

    # TODO: add greeting text and main menu

    try:
        while True:
            user_input = input("Enter a command: ")
            if not user_input:
                continue

            result = handle_command(user_input, book, notes=notes)
            if result == "exit":
                # place to save all data
                print("Good bye!")
                break
            elif result is not None:
                print(result)
    except KeyboardInterrupt:
        # place to save all data
        print("\nGood bye!")