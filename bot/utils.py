from colorama import Fore, init
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


init(autoreset=True)
class Log:
    """
    Utility logger for printing colored messages to the console.
    Provides simple methods for info, success, and error outputs
    using colorama formatting.
    """
    COLORS = {
        "info": Fore.BLUE,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
    }

    PREFIXES = {
        "info": "",
        "success": "",
        "warning": "[WARN] ",
        "error": "[ERROR] ",
    }

    @classmethod
    def _print(cls, message, level):
        color = cls.COLORS.get(level, Fore.WHITE)
        prefix = cls.PREFIXES.get(level, "")
        print(f"{color}{prefix}{message}")

    @classmethod
    def info(cls, message):
        cls._print(message, "info")

    @classmethod
    def success(cls, message):
        cls._print(message, "success")

    @classmethod
    def warning(cls, message):
        cls._print(message, "warning")

    @classmethod
    def error(cls, message):
        cls._print(message, "error")

def log_result(result: str):
    text = result.lower()

    error_keywords = ["error"]
    warning_keywords = ["not found", "unknown", "please", "invalid", "not exist"]
    info_keywords = ["sorry"]

    if any(word in text for word in error_keywords):
        Log.error(result)
    elif any(word in text for word in warning_keywords):
        Log.warning(result)
    elif any(word in text for word in info_keywords):
        Log.info(result)
    else:
        Log.success(result)