from models.notes import Note


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)
    return wrapper


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
