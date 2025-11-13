from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter


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