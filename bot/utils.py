# хелпери (валідація, логування і так далі)
from bot.constants import HELP_MESSAGES, MAIN_HELP_TEXT

def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help(args):
    if not args:
        print(MAIN_HELP_TEXT)
        return
    cmd = args[0].lower()
    message = HELP_MESSAGES.get(cmd)
    if message:
        print(message)
    else:
        print(f"No help available for '{cmd}'.")
