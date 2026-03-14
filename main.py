from colorama import Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from storage import save_data, load_data
from ui import success, warning, info, confirm
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
    "add-contact":  (add_contact,   "<name> [phone] — Add a contact"),
    "all-contacts": (all_contacts,  "               — Show all contacts"),
    "find-contact": (find_contact,  "<query>       — Search contacts"),
    "show-phone":   (show_phone,    "<name>          — Show phones"),
    "change-phone": (change_phone,  "<name> <old> <new> — Change phone"),
    "add-birthday": (add_birthday,  "<name> <DD.MM.YYYY> — Set birthday"),
    "show-birthday": (show_birthday, "<name>       — Show birthday"),
    "birthdays":    (birthdays,     "[days]           — Upcoming birthdays"),
    "add-email":    (add_email_cmd, "<name> <email>   — Set email"),
    "add-address":  (add_address_cmd, "<name>         — Set address"),
    "delete-contact": (delete_contact, "<name>      — Delete contact"),
    "clear-contacts": (clear_contacts, "             — Delete all contacts"),
}

NOTE_COMMANDS = {
    "add-note":          (add_note,     "                   — Add a note"),
    "all-notes":         (all_notes,    "                   — Show all notes"),
    "find-note":         (find_note,    "<query>          — Search notes by text"),
    "edit-note":         (edit_note,    "<id>             — Edit a note"),
    "delete-note":       (delete_note,  "<id>           — Delete a note"),
    "add-tag":           (add_tag,      "<id> <tag>         — Add a tag to a note"),
    "find-tag":          (find_by_tag,  "<tag>             — Search notes by tag"),
    "sort-notes-by-tags": (sort_by_tags, "         — Sort notes by tags"),
    "clear-notes":       (clear_notes,  "                — Delete all notes"),
}

GENERAL_COMMANDS = {
    "clear-all":   "                  — Delete all contacts and notes",
    "help":        "                       — Show this menu",
    "exit / close": "               — Exit the program",
}


def build_menu():
    lines = [
        "",
        f"{Fore.CYAN}========================================",
        "       Personal Assistant",
        f"========================================{Style.RESET_ALL}",
        f"{Fore.GREEN}Contacts:{Style.RESET_ALL}",
    ]
    for cmd, (_, desc) in CONTACT_COMMANDS.items():
        lines.append(f"  {cmd} {desc}")
    lines.append("")
    lines.append(f"{Fore.GREEN}Notes:{Style.RESET_ALL}")
    for cmd, (_, desc) in NOTE_COMMANDS.items():
        lines.append(f"  {cmd} {desc}")
    lines.append("")
    lines.append(f"{Fore.GREEN}General:{Style.RESET_ALL}")
    for cmd, desc in GENERAL_COMMANDS.items():
        lines.append(f"  {cmd} {desc}")
    lines.append(f"{Fore.CYAN}========================================{Style.RESET_ALL}")
    lines.append("")
    return "\n".join(lines)


def get_prompt(book, notebook):
    c = len(book.data)
    n = len(notebook)
    return f"{Fore.CYAN}[{c} contacts, {n} notes]{Style.RESET_ALL} >>> "


def main():
    book, notebook = load_data()

    all_commands = {**CONTACT_COMMANDS, **NOTE_COMMANDS}
    completer = WordCompleter(
        list(all_commands.keys()) + ["clear-all", "help", "exit", "close"],
        sentence=True,
    )

    menu = build_menu()
    print(menu)

    while True:
        user_input = prompt(get_prompt(book, notebook), completer=completer).strip()
        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in ("exit", "close"):
            save_data(book, notebook)
            print(success("Good bye!"))
            break

        if command == "clear-all":
            if not book.data and not notebook.notes:
                print(info("Nothing to clear."))
            elif confirm("Delete ALL contacts and notes?"):
                book.data.clear()
                notebook.clear()
                save_data(book, notebook)
                print(success("All contacts and notes have been deleted."))
            else:
                print(info("Cancelled."))
            continue

        if command == "help":
            print(menu)
            continue

        if command in CONTACT_COMMANDS:
            handler = CONTACT_COMMANDS[command][0]
            result = handler(args, book)
            print(result)
            save_data(book, notebook)
        elif command in NOTE_COMMANDS:
            handler = NOTE_COMMANDS[command][0]
            result = handler(args, notebook)
            print(result)
            save_data(book, notebook)
        else:
            print(warning(f"Unknown command: '{command}'. Type 'help' to see available commands."))


if __name__ == "__main__":
    main()
