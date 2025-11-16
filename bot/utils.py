from bot.constants import HELP_MESSAGES, MAIN_HELP_TEXT

def parse_input(user_input: str):
    """
    Parse a raw user input string into a command and arguments.
    Splits by whitespace, lowercases the command, and returns (cmd, *args).
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help(args):
    """
    Print help text for a specific command or show full help.
    If no args are provided, prints the main help menu; otherwise prints
    command-specific help if available.
    """
    if not args:
        print(MAIN_HELP_TEXT)
        return
    cmd = args[0].lower()
    message = HELP_MESSAGES.get(cmd)
    if message:
        print(message)
    else:
        print(f"No help available for '{cmd}'.")
