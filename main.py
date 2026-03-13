from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from models.notes import NoteBook
from storage import save_data, load_data
from handlers import (
    add_note,
    all_notes,
    find_note,
    edit_note,
    delete_note,
    add_tag,
    find_by_tag,
    sort_by_tags,
)

NOTEBOOK_FILE = "notebook.pkl"

COMMANDS = {
    "add-note": add_note,
    "all-notes": all_notes,
    "find-note": find_note,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "add-tag": add_tag,
    "find-tag": find_by_tag,
    "sort-notes-by-tags": sort_by_tags,
}

MENU = """
========================================
       Personal Assistant
========================================
Available commands:
  add-note             — Add a new note
  all-notes            — Show all notes
  find-note <query>    — Search notes by text
  edit-note <id>       — Edit a note
  delete-note <id>     — Delete a note
  add-tag <id> <tag>   — Add a tag to a note
  find-tag <tag>       — Search notes by tag
  sort-notes-by-tags   — Sort notes by tags
  help                 — Show this menu
  exit / close         — Exit the program
========================================
"""


def main():
    notebook = load_data(NOTEBOOK_FILE, NoteBook)
    completer = WordCompleter(
        list(COMMANDS.keys()) + ["help", "exit", "close"],
        sentence=True,
    )

    print(MENU)

    while True:
        user_input = prompt(">>> ", completer=completer).strip()
        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in ("exit", "close"):
            save_data(notebook, NOTEBOOK_FILE)
            print("Good bye!")
            break

        if command == "help":
            print(MENU)
            continue

        handler = COMMANDS.get(command)
        if handler:
            result = handler(args, notebook)
            print(result)
            save_data(notebook, NOTEBOOK_FILE)
        else:
            print(f"Unknown command: '{command}'. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
