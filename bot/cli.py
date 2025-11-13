from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from bot.commands import handle_command
from bot.models import Notes
from bot.utils import print_help

def run_bot():

    # Define the completer with possible commands.
    completer = WordCompleter(
        [
            "hello", 
            "add", 
            "add-birthday", 
            "add-email", 
            "add-address",
            "all", 
            "add-note", 
            "edit-note",
            "find-notes",
            "all-notes",
            "delete-note", 
            "close",
            "exit"
        ],
    )

    session = PromptSession(
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
        completer=completer,
    )

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