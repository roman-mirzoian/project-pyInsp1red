from bot.commands import handle_command
from bot.models import Notes
from bot.utils import print_help
from bot.completer import session

def run_bot():

    notes = Notes()

    print_help()
    
    try:
        while True:
            user_input = session.prompt(">>> ")
            if not user_input:
                continue

            result = handle_command(user_input, {}, notes=notes)
            if result == "exit":
                # place to save all data
                print("Good bye!")
                break
            elif result is not None:
                print(result)
    except KeyboardInterrupt:
        # place to save all data
        print("\nGood bye!")