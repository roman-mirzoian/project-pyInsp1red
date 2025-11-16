# Personal Assistant Bot

A command-line interface (CLI) assistant to help you manage your personal data.

It helps you store detailed contact information and create user-specific notes. The application runs locally.

---

## Features

* **Contact Management:** Add, edit, delete, and search contacts.
* **Note Management:** Add, edit, delete, and search notes by content or tags.
* **Birthday Reminders:** Get a user list of upcoming birthdays.
* **Data Persistence:** All information is saved locally on your disk.
* **Command Autocompletion:** Suggestions for commands are provided as you type.
* **Error Handling:** The bot handles incorrect input without crashing.

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* Python 3.x

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/roman-mirzoian/project-pyInsp1red.git](https://github.com/roman-mirzoian/project-pyInsp1red.git)
    ```
2.  **Navigate to the project directory:**
    ```sh
    cd project-pyInsp1red
    ```
3.  **(Recommended) Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

---

## How to Use

1.  **Run the bot:**
    ```sh
    python main.py
    ```
2.  Once the bot is running, it will display a "Welcome..." message.
3.  Type `help` to see all available commands, or `help <command>` for details on a specific command.
4.  To exit the bot, type `close` or `exit`.

---

## Available Commands

Here is a list of the main commands you can use.

### Contact Management

* `add <name> <phone>`: Adds a new contact with a name and phone.
* `add <name> <field> <value>`: Adds a specific field (phone, email, address, birthday) to a contact.
* `all`: Shows all contacts in the address book.
* `birthdays`: Shows upcoming birthdays. The program will then ask for the number of days to look ahead.
* `show <name>`: Shows detailed information for a specific contact.
* `find <query>`: Finds contacts by name, phone, or email (case-insensitive).
* `delete <name>`: Deletes a contact from the address book.
* `update <name> <field> <value>`: Updates a specific field for a contact.
* `remove <name> <field>`: Removes a specific field (e.g., a phone) from a contact.

### Note Management

* `add-note <user_name> <tag=> <text>`: Adds a new note for a user. The `tag` is optional.
* `edit-note <note_id>`: Edits an existing note.
* `find-notes <keyword>`: Finds notes by searching the text content.
* `find-tag <tag>`: Finds all notes matching a specific tag.
* `sort-notes`: Sorts all notes by tag.
* `all-notes <user_name>`: Shows all notes for a specific user.
* `delete-note <note_id>`: Deletes a specific note.

### General

* `hello`: Displays a greeting.
* `help`: Shows the full list of available commands.
* `help <command>`: Shows detailed help for a specific command.
* `close` / `exit`: Exits the application.