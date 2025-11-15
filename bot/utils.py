# хелпери (валідація, логування і так далі)

def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help():
    help_text = """
    \033[1m=== Available Commands ===\033[0m

    \033[94m[Contact Management]\033[0m
    - hello                              Display a greeting
    - add <name>                         Add a new contact
    - add <name> <phone>                 Add contact with phone
    - add <name> <field> <value>         Add field to contact (phone, email, address, birthday)
    - all                                Show all contacts
    - show <name>                        Show contact details
    - update <name> <field> <value>      Update contact field
    - delete <name>                      Delete a contact
    - remove <name> <field>              Remove field from contact
    - find [field] <query>               Search contacts (case insensitive)
                                         - find <query> (search all fields)
                                         - find phone <query> (search phone only)
                                         - find email <query> (search email only)
    - birthdays <days>                   Show upcoming birthdays within <days>

    \033[93m[Note Management]\033[0m
    - add-note <user_name> <text>        Add a new note for a user
    - edit-note <user_name> <id>         Edit existing note
    - find-notes <keyword>               Search notes by keyword
    - find-tag <tag>                     Find notes by tag
    - sort-notes                         Show notes sorted/grouped by tag
    - all-notes <user_name>              Show all notes for a user
    - delete-note <user_name> <id>       Delete a note

    \033[91m[Exit]\033[0m
    - close / exit                       Exit the application
    """
    print(help_text)