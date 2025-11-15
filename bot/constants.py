# Data types
USERS_DATA = 'user_data'
NOTES_DATA = 'notes_data'

# Error messages Constants
ERROR_NO_COMMAND = "Please enter a command."
ERROR_INSUFFICIENT_ARGS = "Error: Insufficient arguments provided"
ERROR_CONTACT_NOT_FOUND = "Sorry, contact not found"
ERROR_PHONE_EXISTS = "Sorry, phone number already exists"
ERROR_PHONE_NOT_FOUND = "Sorry, phone number not found"
ERROR_BIRTHDAY_NOT_FOUND = "Sorry, birthday not found"
ERROR_EMAIL_NOT_FOUND = "Sorry, email not found"
ERROR_ADDRESS_NOT_FOUND = "Sorry, address not found"
ERROR_INVALID_PHONE = "Sorry, invalid phone number, must be 10 digits"
ERROR_INVALID_EMAIL = "Sorry, invalid email address"
ERROR_INVALID_DATE = "Sorry, invalid date format, must be DD.MM.YYYY"
ERROR_EMPTY_NAME = "Sorry, name cannot be empty"
ERROR_INVALID_NAME_LETTERS = "Name must be a single word containing only letters"
ERROR_EMPTY_ADDRESS = "Sorry, address cannot be empty"

# Success messages
SUCCESS_CONTACT_ADDED = "Contact added."
SUCCESS_CONTACT_UPDATED = "Contact updated."
SUCCESS_CONTACT_DELETED = "Contact deleted."
SUCCESS_PHONE_ADDED = "Phone added."
SUCCESS_PHONE_UPDATED = "Phone updated."
SUCCESS_PHONE_REMOVED = "Phone removed."
SUCCESS_BIRTHDAY_ADDED = "Birthday added."
SUCCESS_BIRTHDAY_UPDATED = "Birthday updated."
SUCCESS_BIRTHDAY_REMOVED = "Birthday removed."
SUCCESS_EMAIL_ADDED = "Email added."
SUCCESS_EMAIL_UPDATED = "Email updated."
SUCCESS_EMAIL_REMOVED = "Email removed."
SUCCESS_ADDRESS_ADDED = "Address added."
SUCCESS_ADDRESS_UPDATED = "Address updated."
SUCCESS_ADDRESS_REMOVED = "Address removed."

# Info messages
INFO_NO_CONTACTS = "No contacts"

# Date format
DATE_FORMAT = "%d.%m.%Y"

# Help messages
MAIN_HELP_TEXT = """
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
"""

HELP_MESSAGES = {
"add": """
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
""",
    
    "all": """
Command: all
Usage:
  all

Description:
  Shows a list of all contacts stored in your address book.
""",
    
    "show": """
Command: show
Usage:
  show <name>

Description:
  Displays all details of a selected contact.
        """,
    
    "find": """
Command: find
Usage:
  find <query>           Search in all fields
  find <digits> phone    Search only by phone
  find <text> email      Search only by email

Description:
  Searches contacts by any text or specific fields.
        """,
    
    "delete": """
Command: delete
Usage:
  delete <name>

Description:
  Removes the contact entirely from your address book.
        """,
    
    "update": """
Command: update
Usage:
  update <name> <field> <value>

Description:
  Updates an existing field for the contact.
        """,
    
    "remove": """
Command: remove
Usage:
  remove <name> <field>

Description:
  Removes specific field (phone/email/address/birthday) from a contact.
        """,
    
    "birthdays": """
Command: birthdays
Usage:
  birthdays
Then enter the number of days you want to see upcoming birthdays for.

Description:
  Shows contacts with upcoming birthdays within <days>.
        """,
    
    "add-note": """
Command: add-note
Usage:
  add-note <title> <text>

Description:
  Creates a new note.
        """,
    
    "edit-note": """
Command: edit-note
Usage:
  edit-note <id> <text>

Description:
  Edits an existing note.
        """,
    
    "find-notes": """
Command: find-notes
Usage:
  find-notes <keyword>

Description:
  Searches notes that contain given keyword.
        """,
    
    "all-notes": """
Command: all-notes
Usage:
  all-notes

Description:
  Shows list of all notes.
        """,
    
    "delete-note": """
Command: delete-note
Usage:
  delete-note <id>

Description:
  Deletes a note by its ID.
        """
}
