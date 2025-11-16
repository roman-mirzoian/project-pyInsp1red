from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings


# Define the completer with possible commands.
completer = WordCompleter(
    [
        "hello",
        "add",
        "all",
        "show",
        "find",
        "delete",
        "update",
        "remove",
        "birthdays",
        "add-note",
        "edit-note",
        "find-notes",
        "all-notes",
        "delete-note",
        "help",
        "find-tag",
        "sort-notes",
        "close",
        "exit"
    ],
)

# Key bindings
bindings = KeyBindings()

@bindings.add('enter')
def _(event):
    """Make Enter accept text instead of just selecting completion."""
    buffer = event.current_buffer
    if buffer.complete_state:
        buffer.complete_state = None
    else:
        buffer.validate_and_handle()

session = PromptSession(
    history=InMemoryHistory(),
    auto_suggest=AutoSuggestFromHistory(),
    enable_history_search=True,
    completer=completer,
    key_bindings=bindings
)