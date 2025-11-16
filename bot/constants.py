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
ERROR_INVALID_PHONE = "Sorry, invalid phone number, must be 10 digits and start with '380'"
ERROR_INVALID_EMAIL = "Sorry, invalid email address"
ERROR_INVALID_DATE = "Sorry, invalid date format, must be DD.MM.YYYY"
ERROR_EMPTY_NAME = "Sorry, name cannot be empty"
ERROR_NAME_TOO_SHORT = "Error: Name must be at least 2 characters long."
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

# Number format
UKRAINE_CODE = "380"

# Help messages
MAIN_HELP_TEXT = """
\033[36;1m** Available Commands **\033[0m

- help <command>                     Show help for a specific command
                                     If there are no <command>, show all available commands                    

\033[94m[Contact Management]\033[0m
- hello                              Display a greeting
- add <name>                         Add a new contact
  - add <name> <phone>               Add contact with phone
  - add <name> <field> <value>       Add field to contact (phone, email, address, birthday)
- all                                Show all contacts
- birthdays                          Show upcoming birthdays
- show <name>                        Show contact details
- update <name> <field> <value>      Update contact field
- delete <name>                      Delete a contact
- remove <name> <field>              Remove field from contact
- find <query>                       Search contacts (case insensitive)
  - find <query> [field]             Search in specified field (phone, email, address, birthday)

\033[93m[Note Management]\033[0m
- add-note <user_name> tag=<tag> <text>   Add a new note for a user
- edit-note <user_name> <id>              Edit existing note
- find-notes <keyword>                    Search notes by keyword
- find-tag <tag>                          Find notes by tag
- sort-notes                              Show notes sorted/grouped by tag
- all-notes <user_name>                   Show all notes for a user
- delete-note <user_name> <note_id>       Delete a note

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
  find <query> [field]   Search only in specified field (phone, email, address, birthday)

Description:
  Searches contacts by any text or specific fields.
  
Examples:
  find 0987654321
  find 0987654321 phone
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
  update <name> <field> <old_number> <new_number>

Description:
  Updates an existing field for the contact.
  If you want to update a <field> phone, you need to enter which number you will update.
        
Examples:        
  update john birthday 12.11.2000    
  update john phone 3333333333 5555555555      
        """,
    
    "remove": """
Command: remove
Usage:
  remove <name> <field>
  remove <name> <field_phone> <number>

Description:
  Removes specific field (phone/email/address/birthday) from a contact.
  If you want to delete a <field> phone, you need to enter which number you will delete.

Examples:
  remove John birthday
  remove john phone 0987654321
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
  add-note <user_name> <text>
  add-note <user_name> tag=<tag> <text>

Description:
  Creates a new note for the specified user. 
  You can optionally add a tag using the prefix tag=<value>.
  The command returns the ID of the newly created note.

Examples:
  add-note John Buy milk
  add-note Anna tag=work Finish the report
        """,
    
    "edit-note": """
Command: edit-note
Usage:
  edit-note <user_name> <note_id>

Description:
  Edits the text of an existing note for the specified user. 
  When executed, the current text of the note is shown as default, allowing you 
  to modify it interactively. After editing, the updated note is saved.

Examples:
  edit-note John 1
  edit-note Anna 3
        """,
    
    "find-notes": """
Command: find-notes
Usage:
  find-notes <keyword>

Description:
  Searches notes that contain given keyword.
  If you do not enter a <keyword>, all notes will be displayed.
        """,
    
    "all-notes": """
Command: all-notes
Usage:
  all-notes <user_name>

Description:
  Shows all notes that belong to the specified user.
        """,
    
    "delete-note": """
Command: delete-note
Usage:
  delete-note <user_name> <note_id>

Description:
  Deletes a specific note belonging to the given user by its ID.
  If the user or note ID is invalid, an error message is shown.

Examples:
  delete-note John 2
  delete-note Anna 5
        """,

    "sort-notes": """
Command: sort-notes
Usage:
  sort-notes

Description:
  Groups all notes by their tags and displays them in alphabetical (sorted) 
  order. Each tag is shown as a category, followed by the notes that contain
  this tag.
        """,

      "find-tag": """
Command: find-tag
Usage:
  find-tag <tag>

Description:
  Searches notes by a specific tag. Shows all notes that contain the given tag.
  If no notes with this tag exist, displays a message indicating that none were found.
        """
}
