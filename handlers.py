from tabulate import tabulate

from models.notes import Note
from models.address_book import Record
from ui import success, error, warning, info, confirm


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return error(str(e))
    return wrapper


@input_error
def add_contact(args, book):
    if not args:
        return warning("Please provide a name. Usage: add-contact <name>")
    name = args[0]
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = f"Contact '{name}' added."
    else:
        msg = f"Contact '{name}' updated."
    if len(args) > 1:
        record.add_phone(args[1])
        msg += f" Phone {args[1]} added."
    return success(msg)


@input_error
def all_contacts(args, book):
    if not book.data:
        return info("No contacts found.")
    rows = []
    for r in book.data.values():
        phones = '; '.join(p.value for p in r.phones) or '-'
        birthday = r.birthday.value.strftime('%d.%m.%Y') if r.birthday else '-'
        email = r.email.value if r.email else '-'
        address = r.address.value if r.address else '-'
        rows.append([r.name.value, phones, birthday, email, address])
    headers = ["Name", "Phones", "Birthday", "Email", "Address"]
    return tabulate(rows, headers=headers, tablefmt="rounded_grid")


@input_error
def find_contact(args, book):
    if not args:
        return warning("Please provide a search query. Usage: find-contact <query>")
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return info("No contacts found matching your query.")
    rows = []
    for r in results:
        phones = '; '.join(p.value for p in r.phones) or '-'
        birthday = r.birthday.value.strftime('%d.%m.%Y') if r.birthday else '-'
        email = r.email.value if r.email else '-'
        address = r.address.value if r.address else '-'
        rows.append([r.name.value, phones, birthday, email, address])
    headers = ["Name", "Phones", "Birthday", "Email", "Address"]
    return tabulate(rows, headers=headers, tablefmt="rounded_grid")


@input_error
def show_phone(args, book):
    if not args:
        return warning("Please provide a name. Usage: show-phone <name>")
    record = book.find(args[0])
    if record is None:
        return error(f"Contact '{args[0]}' not found.")
    if not record.phones:
        return info(f"No phones for '{args[0]}'.")
    return info(f"{args[0]}: {'; '.join(p.value for p in record.phones)}")


@input_error
def change_phone(args, book):
    if len(args) < 3:
        return warning("Usage: change-phone <name> <old_phone> <new_phone>")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        return error(f"Contact '{name}' not found.")
    record.edit_phone(old_phone, new_phone)
    return success(f"Phone updated for '{name}'.")


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return warning("Usage: add-birthday <name> <DD.MM.YYYY>")
    record = book.find(args[0])
    if record is None:
        return error(f"Contact '{args[0]}' not found.")
    record.add_birthday(args[1])
    return success(f"Birthday added for '{args[0]}'.")


@input_error
def show_birthday(args, book):
    if not args:
        return warning("Usage: show-birthday <name>")
    record = book.find(args[0])
    if record is None:
        return error(f"Contact '{args[0]}' not found.")
    if not record.birthday:
        return info(f"No birthday set for '{args[0]}'.")
    return info(f"{args[0]}: {record.birthday.value.strftime('%d.%m.%Y')}")


@input_error
def birthdays(args, book):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return info(f"No birthdays in the next {days} days.")
    rows = [[b['name'], b['congratulation_date']] for b in upcoming]
    headers = ["Name", "Congratulation date"]
    return tabulate(rows, headers=headers, tablefmt="rounded_grid")


@input_error
def add_email_cmd(args, book):
    if len(args) < 2:
        return warning("Usage: add-email <name> <email>")
    record = book.find(args[0])
    if record is None:
        return error(f"Contact '{args[0]}' not found.")
    record.add_email(args[1])
    return success(f"Email added for '{args[0]}'.")


@input_error
def add_address_cmd(args, book):
    if not args:
        return warning("Usage: add-address <name>")
    record = book.find(args[0])
    if record is None:
        return error(f"Contact '{args[0]}' not found.")
    address = " ".join(args[1:]) if len(args) > 1 else input("Enter address: ").strip()
    if not address:
        return warning("Address cannot be empty.")
    record.add_address(address)
    return success(f"Address added for '{args[0]}'.")


@input_error
def delete_contact(args, book):
    if not args:
        return warning("Usage: delete-contact <name>")
    name = args[0]
    if book.find(name) is None:
        return error(f"Contact '{name}' not found.")
    if not confirm(f"Delete contact '{name}'?"):
        return info("Cancelled.")
    book.delete(name)
    return success(f"Contact '{name}' deleted.")


@input_error
def add_note(args, notebook):
    text = input("Enter note text: ").strip()
    if not text:
        return warning("Note text cannot be empty.")
    note = Note(text)
    notebook.add(note)
    return success(f"Note added with ID {note.id}.")


@input_error
def all_notes(args, notebook):
    notes = notebook.get_all()
    if not notes:
        return info("No notes found.")
    return "\n".join(str(n) for n in notes)


@input_error
def find_note(args, notebook):
    if not args:
        return warning("Please provide a search query. Usage: find-note <query>")
    query = " ".join(args)
    results = notebook.search_by_text(query)
    if not results:
        return info("No notes found matching your query.")
    return "\n".join(str(n) for n in results)


@input_error
def edit_note(args, notebook):
    if not args:
        return warning("Please provide a note ID. Usage: edit-note <id>")
    note_id = int(args[0])
    note = notebook.find(note_id)
    print(f"Current text: {note.text}")
    new_text = input("Enter new text: ").strip()
    if not new_text:
        return warning("Note text cannot be empty.")
    note.edit_text(new_text)
    return success(f"Note {note_id} updated.")


@input_error
def delete_note(args, notebook):
    if not args:
        return warning("Please provide a note ID. Usage: delete-note <id>")
    note_id = int(args[0])
    notebook.find(note_id)
    if not confirm(f"Delete note {note_id}?"):
        return info("Cancelled.")
    notebook.delete(note_id)
    return success(f"Note {note_id} deleted.")


@input_error
def add_tag(args, notebook):
    if len(args) < 2:
        return warning("Please provide a note ID and tag. Usage: add-tag <id> <tag>")
    note_id = int(args[0])
    tag = args[1]
    note = notebook.find(note_id)
    note.add_tag(tag)
    return success(f"Tag '{tag.strip().lower()}' added to note {note_id}.")


@input_error
def remove_tag(args, notebook):
    if len(args) < 2:
        return warning("Please provide a note ID and tag. Usage: remove-tag <id> <tag>")
    note_id = int(args[0])
    tag = args[1]
    note = notebook.find(note_id)
    note.remove_tag(tag)
    return success(f"Tag '{tag.strip().lower()}' removed from note {note_id}.")


@input_error
def find_by_tag(args, notebook):
    if not args:
        return warning("Please provide a tag. Usage: find-tag <tag>")
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return info(f"No notes found with tag '{tag}'.")
    return "\n".join(str(n) for n in results)


@input_error
def sort_by_tags(args, notebook):
    notes = notebook.sort_by_tags()
    if not notes:
        return info("No notes found.")
    return "\n".join(str(n) for n in notes)


@input_error
def clear_contacts(args, book):
    if not book.data:
        return info("No contacts to clear.")
    if not confirm(f"Delete all {len(book.data)} contacts?"):
        return info("Cancelled.")
    book.data.clear()
    return success("All contacts have been deleted.")


@input_error
def clear_notes(args, notebook):
    if not notebook.notes:
        return info("No notes to clear.")
    if not confirm(f"Delete all {len(notebook)} notes?"):
        return info("Cancelled.")
    notebook.clear()
    return success("All notes have been deleted.")
