from bot.constants import ERROR_CONTACT_NOT_FOUND, ERROR_INSUFFICIENT_ARGS, ERROR_NO_COMMAND
from bot.models import AddressBook, Notes

# Decorator to handle input errors
def input_error(func):
    """
    Decorator for command handlers that normalizes common input errors.
    Wraps a function, checks arguments count and catches typical exceptions,
    returning user-friendly error messages instead of tracebacks.
    """
    def inner(*args, **kwargs):
        """
        Wrapper that validates arguments for the wrapped command
        and handles ValueError/KeyError/other exceptions, mapping them
        to readable error strings for the CLI user.
        """
        # No command entered
        if args is None:
            return ERROR_NO_COMMAND

        # Check for specific command errors
        if func.__name__ in ("add_birthday", "add_email",
                             "add_address", "update_phone", "update_birthday",
                             "update_email", "update_address", "remove_phone"):
            if len(args) < 2:
                return ERROR_INSUFFICIENT_ARGS

        elif func.__name__ in ("delete_contact", "show_contact", "all_user_notes",                  "find_notes_by_tag"):
            if len(args) < 1:
                return ERROR_INSUFFICIENT_ARGS

        # Handle exceptions from the command functions
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError:
            return ERROR_CONTACT_NOT_FOUND
        except Exception as e:
            return f"Unexpected error: {e}"

    return inner

# Decorator to check user exists
def user_exists(func):
    """
    Decorator for note- and contact-related commands that require an existing user.
    It looks up the first argument as a username in the AddressBook and aborts
    the call with a message if the user is not found.
    """
    def inner(args, book: AddressBook, notes: Notes):
        """
        Wrapper that verifies the user from args[0] exists in the AddressBook.
        If the user is missing, returns an error string; otherwise calls the
        wrapped function with the same arguments.
        """
        try:
            user_name = args[0]
            user = book.find(user_name)
            if not user:
                return f"User '{user_name}' does not exist."
            return func(args, book=book, notes=notes)
        except Exception as e:
            return f"Unexpected error: {e}"
    
    return inner