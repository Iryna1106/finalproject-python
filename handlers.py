from models.notes import Note
from models.address_book import Record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)
    return wrapper


# ---- Contact handlers ----


@input_error
def add_contact(args, book):
    if not args:
        return "Please provide a name. Usage: add-contact <name>"
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
    return msg


@input_error
def all_contacts(args, book):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(r) for r in book.data.values())


@input_error
def find_contact(args, book):
    if not args:
        return "Please provide a search query. Usage: find-contact <query>"
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return "No contacts found matching your query."
    return "\n".join(str(r) for r in results)


@input_error
def show_phone(args, book):
    if not args:
        return "Please provide a name. Usage: show-phone <name>"
    record = book.find(args[0])
    if record is None:
        return f"Contact '{args[0]}' not found."
    if not record.phones:
        return f"No phones for '{args[0]}'."
    return f"{args[0]}: {'; '.join(p.value for p in record.phones)}"


@input_error
def change_phone(args, book):
    if len(args) < 3:
        return "Usage: change-phone <name> <old_phone> <new_phone>"
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone updated for '{name}'."


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Usage: add-birthday <name> <DD.MM.YYYY>"
    record = book.find(args[0])
    if record is None:
        return f"Contact '{args[0]}' not found."
    record.add_birthday(args[1])
    return f"Birthday added for '{args[0]}'."


@input_error
def show_birthday(args, book):
    if not args:
        return "Usage: show-birthday <name>"
    record = book.find(args[0])
    if record is None:
        return f"Contact '{args[0]}' not found."
    if not record.birthday:
        return f"No birthday set for '{args[0]}'."
    return f"{args[0]}: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book):
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} days."
    lines = [f"{b['name']}: {b['congratulation_date']}" for b in upcoming]
    return "\n".join(lines)


@input_error
def add_email_cmd(args, book):
    if len(args) < 2:
        return "Usage: add-email <name> <email>"
    record = book.find(args[0])
    if record is None:
        return f"Contact '{args[0]}' not found."
    record.add_email(args[1])
    return f"Email added for '{args[0]}'."


@input_error
def add_address_cmd(args, book):
    if not args:
        return "Usage: add-address <name>"
    record = book.find(args[0])
    if record is None:
        return f"Contact '{args[0]}' not found."
    address = " ".join(args[1:]) if len(args) > 1 else input("Enter address: ").strip()
    if not address:
        return "Address cannot be empty."
    record.add_address(address)
    return f"Address added for '{args[0]}'."


@input_error
def delete_contact(args, book):
    if not args:
        return "Usage: delete-contact <name>"
    name = args[0]
    if book.find(name) is None:
        return f"Contact '{name}' not found."
    book.delete(name)
    return f"Contact '{name}' deleted."


@input_error
def add_note(args, notebook):
    text = input("Enter note text: ").strip()
    if not text:
        return "Note text cannot be empty."
    note = Note(text)
    notebook.add(note)
    return f"Note added with ID {note.id}."


@input_error
def all_notes(args, notebook):
    notes = notebook.get_all()
    if not notes:
        return "No notes found."
    return "\n".join(str(n) for n in notes)


@input_error
def find_note(args, notebook):
    if not args:
        return "Please provide a search query. Usage: find-note <query>"
    query = " ".join(args)
    results = notebook.search_by_text(query)
    if not results:
        return "No notes found matching your query."
    return "\n".join(str(n) for n in results)


@input_error
def edit_note(args, notebook):
    if not args:
        return "Please provide a note ID. Usage: edit-note <id>"
    note_id = int(args[0])
    note = notebook.find(note_id)
    print(f"Current text: {note.text}")
    new_text = input("Enter new text: ").strip()
    if not new_text:
        return "Note text cannot be empty."
    note.edit_text(new_text)
    return f"Note {note_id} updated."


@input_error
def delete_note(args, notebook):
    if not args:
        return "Please provide a note ID. Usage: delete-note <id>"
    note_id = int(args[0])
    notebook.delete(note_id)
    return f"Note {note_id} deleted."


@input_error
def add_tag(args, notebook):
    if len(args) < 2:
        return "Please provide a note ID and tag. Usage: add-tag <id> <tag>"
    note_id = int(args[0])
    tag = args[1]
    note = notebook.find(note_id)
    note.add_tag(tag)
    return f"Tag '{tag.strip().lower()}' added to note {note_id}."


@input_error
def find_by_tag(args, notebook):
    if not args:
        return "Please provide a tag. Usage: find-tag <tag>"
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return f"No notes found with tag '{tag}'."
    return "\n".join(str(n) for n in results)


@input_error
def sort_by_tags(args, notebook):
    notes = notebook.sort_by_tags()
    if not notes:
        return "No notes found."
    return "\n".join(str(n) for n in notes)
