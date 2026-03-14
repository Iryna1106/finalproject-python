from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
    add_contact,
    all_contacts,
    find_contact,
    show_phone,
    change_phone,
    add_birthday,
    show_birthday,
    birthdays,
    add_email_cmd,
    add_address_cmd,
    delete_contact,
    clear_contacts,
    clear_notes,
)

CONTACT_COMMANDS = {
    "add-contact": add_contact,
    "all-contacts": all_contacts,
    "find-contact": find_contact,
    "show-phone": show_phone,
    "change-phone": change_phone,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "add-email": add_email_cmd,
    "add-address": add_address_cmd,
    "delete-contact": delete_contact,
    "clear-contacts": clear_contacts,
}

NOTE_COMMANDS = {
    "add-note": add_note,
    "all-notes": all_notes,
    "find-note": find_note,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "add-tag": add_tag,
    "find-tag": find_by_tag,
    "sort-notes-by-tags": sort_by_tags,
    "clear-notes": clear_notes,
}

MENU = """
========================================
       Personal Assistant
========================================
Contacts:
  add-contact <name> [phone] — Add a contact
  all-contacts               — Show all contacts
  find-contact <query>       — Search contacts
  show-phone <name>          — Show phones
  change-phone <name> <old> <new> — Change phone
  add-birthday <name> <DD.MM.YYYY> — Set birthday
  show-birthday <name>       — Show birthday
  birthdays [days]           — Upcoming birthdays
  add-email <name> <email>   — Set email
  add-address <name>         — Set address
  delete-contact <name>      — Delete contact
  clear-contacts             — Delete all contacts

Notes:
  add-note                   — Add a note
  all-notes                  — Show all notes
  find-note <query>          — Search notes by text
  edit-note <id>             — Edit a note
  delete-note <id>           — Delete a note
  add-tag <id> <tag>         — Add a tag to a note
  find-tag <tag>             — Search notes by tag
  sort-notes-by-tags         — Sort notes by tags
  clear-notes                — Delete all notes

General:
  clear-all                  — Delete all contacts and notes
  help                       — Show this menu
  exit / close               — Exit the program
========================================
"""


def main():
    book, notebook = load_data()

    all_commands = {**CONTACT_COMMANDS, **NOTE_COMMANDS}
    completer = WordCompleter(
        list(all_commands.keys()) + ["clear-all", "help", "exit", "close"],
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
            save_data(book, notebook)
            print("Good bye!")
            break

        if command == "clear-all":
            if not book.data and not notebook.notes:
                print("Nothing to clear.")
            else:
                book.data.clear()
                notebook.clear()
                save_data(book, notebook)
                print("All contacts and notes have been deleted.")
            continue

        if command == "help":
            print(MENU)
            continue

        if command in CONTACT_COMMANDS:
            result = CONTACT_COMMANDS[command](args, book)
            print(result)
            save_data(book, notebook)
        elif command in NOTE_COMMANDS:
            result = NOTE_COMMANDS[command](args, notebook)
            print(result)
            save_data(book, notebook)
        else:
            print(f"Unknown command: '{command}'. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
