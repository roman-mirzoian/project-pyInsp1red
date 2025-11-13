# хелпери (валідація, логування і так далі)

def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help():
    help_text = """
    \033[1m=== Available Commands ===\033[0m
    
    \033[94m[Contact Management]\033[0m
    - hello                          Display a greeting
    - add <name> <phone>             Add a new contact
    - add-email <name> <email>       Add email to contact
    - add-address <name> <address>   Add address to contact
    - all                            Show all contacts
    
    \033[92m[Birthday Management]\033[0m
    - add-birthday <name> <birthday> Add birthday to contact
    - show-birthday <name>           Show contact's birthday
    - birthdays <days>               Show upcoming birthdays
    
    \033[93m[Note Management]\033[0m
    - add-note <title> <text>        Add a new note
    - edit-note <id> <text>          Edit existing note
    - find-notes <keyword>           Search notes by keyword
    - all-notes                      Show all notes
    - delete-note <id>               Delete a note
    
    \033[91m[Exit]\033[0m
    - close / exit                   Exit the application
    """
    print(help_text)