# логіка виконання команд (add, phone, all і так далі)

from bot.utils import parse_input

def handle_command(user_input: str, book, notes):
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
    }

    if command in ("close", "exit"):
        return "exit"
    
    func = commands.get(command)
    if func:
        return func()
    else:
        print(f"Invalid command: {command}")