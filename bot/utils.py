# хелпери (валідація, логування і так далі)

def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def print_help(args):
    if not args:
        print("""
    \033[1m=== Available Commands ===\033[0m
    
    - help <command>                     Show help for a specific command
                                         If there are no <command>, show all available commands                    

    \033[94m[Contact Management]\033[0m
    - hello                              Display a greeting
    - add <name>                         Add a new contact
    - add <name> <phone>                 Add contact with phone
    - add <name> <field> <value>         Add field to contact (phone, email, address, birthday)
    - all                                Show all contacts
    - birthdays                          Show upcoming birthdays
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
    """)
        return

    cmd = args[0].lower()

    if cmd == "add":
        print("""
Command: add
Usage:
  add <name>
  add <name> <phone>
  add <name> <field> <value>

Description:
  Adds a new contact or adds a new field to an existing contact.
              
Examples:
  add John
  add John 0987654321
  add John email john@gmail.com
        """)
        return

    if cmd == "all":
        print("""
Command: all
Usage:
  all

Description:
  Shows a list of all contacts stored in your address book.
        """)
        return

    if cmd == "show":
        print("""
Command: show
Usage:
  show <name>

Description:
  Displays all details of a selected contact.
        """)
        return

    if cmd == "find":
        print("""
Command: find
Usage:
  find <query>           Search in all fields
  find <digits> phone    Search only by phone
  find <text> email      Search only by email

Description:
  Searches contacts by any text or specific fields.
        """)
        return

    if cmd == "delete":
        print("""
Command: delete
Usage:
  delete <name>

Description:
  Removes the contact entirely from your address book.
        """)
        return

    if cmd == "update":
        print("""
Command: update
Usage:
  update <name> <field> <value>

Description:
  Updates an existing field for the contact.
        """)
        return

    if cmd == "remove":
        print("""
Command: remove
Usage:
  remove <name> <field>

Description:
  Removes specific field (phone/email/address/birthday) from a contact.
        """)
        return

    if cmd == "birthdays":
        print("""
Command: birthdays
Usage:
  birthdays
Then enter the number of days you want to see upcoming birthdays for.

Description:
  Shows contacts with upcoming birthdays within <days>.
        """)
        return

    if cmd == "add-note":
        print("""
Command: add-note
Usage:
  add-note <title> <text>

Description:
  Creates a new note.
        """)
        return

    if cmd == "edit-note":
        print("""
Command: edit-note
Usage:
  edit-note <id> <text>

Description:
  Edits an existing note.
        """)
        return

    if cmd == "find-notes":
        print("""
Command: find-notes
Usage:
  find-notes <keyword>

Description:
  Searches notes that contain given keyword.
        """)
        return

    if cmd == "all-notes":
        print("""
Command: all-notes
Usage:
  all-notes

Description:
  Shows list of all notes.
        """)
        return

    if cmd == "delete-note":
        print("""
Command: delete-note
Usage:
  delete-note <id>

Description:
  Deletes a note by its ID.
        """)
        return

    print(f"No help available for '{cmd}'.")
