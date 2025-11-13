from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from bot.commands import handle_command

def run_bot():

    # Create some history first.
    history = InMemoryHistory()
    history.append_string("add")
    history.append_string("change")
    history.append_string("phone")
    history.append_string("all")
    history.append_string("add-birthday")
    history.append_string("show-birthday")
    history.append_string("birthdays")

    # Define the completer with possible commands.
    compleater = WordCompleter(
        ["hello", "add", "change", "phone", "all", "add-birthday", "show-birthday", "birthdays", "exit", "close"],
    )
    # Define key bindings.
    bindings = KeyBindings()

    # Handle the Enter key.
    @bindings.add('enter')
    def _(event):
        buffer = event.current_buffer
        if buffer.complete_state:
            buffer.complete_state = None  # Exit completion mode
        else:
            buffer.validate_and_handle()  # Accept the input

    session = PromptSession(
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
        completer=compleater,
        key_bindings=bindings,
    )
    # Print help.
    print("This CLI has fish-style auto-suggestion enabled.")
    print('Type for instance "add", then you\'ll see a suggestion.')
    print("Press the right arrow to insert the suggestion.")
    print("Press Control-C to retry. Control-D to exit.")
    print()
    try:
        while True:
            user_input = session.prompt(">>> ")
            if not user_input:
                continue

            result = handle_command(user_input, {}, {})
            if result == "exit":
                # place to save all data
                print("Good bye!")
                break
            elif result is not None:
                print(result)
    except KeyboardInterrupt:
        # place to save all data
        print("\nGood bye!")