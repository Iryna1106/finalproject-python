from datetime import datetime


class Note:

    def __init__(self, text, tags=None):
        self.id = None
        self.text = self._validate_text(text)
        self.tags = self._normalize_tags(tags or [])
        self.created_at = datetime.now()

    @staticmethod
    def _validate_text(text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Note text cannot be empty.")
        return text.strip()

    @staticmethod
    def _normalize_tags(tags):
        seen = set()
        result = []
        for tag in tags:
            t = tag.strip().lower()
            if not t:
                continue
            if " " in t:
                raise ValueError(f"Tag cannot contain spaces: '{tag}'.")
            if t not in seen:
                seen.add(t)
                result.append(t)
        return result

    def edit_text(self, new_text):
        self.text = self._validate_text(new_text)

    def add_tag(self, tag):
        t = tag.strip().lower()
        if not t:
            raise ValueError("Tag cannot be empty.")
        if " " in t:
            raise ValueError(f"Tag cannot contain spaces: '{tag}'.")
        if t in self.tags:
            raise ValueError(f"Tag '{t}' already exists on note {self.id}.")
        self.tags.append(t)

    def remove_tag(self, tag):
        t = tag.strip().lower()
        if t not in self.tags:
            raise ValueError(f"Tag '{t}' not found on note {self.id}.")
        self.tags.remove(t)

    def __str__(self):
        date_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        lines = [f"[ID: {self.id}] {date_str}"]
        if self.tags:
            lines.append(f"Tags: {', '.join(self.tags)}")
        lines.append(self.text)
        lines.append("---")
        return "\n".join(lines)


class NoteBook:

    def __init__(self):
        self.notes = {}
        self._next_id = 1

    def add(self, note):
        note.id = self._next_id
        self.notes[self._next_id] = note
        self._next_id += 1
        return note

    def find(self, note_id):
        if note_id not in self.notes:
            raise KeyError(f"Note with ID {note_id} not found.")
        return self.notes[note_id]

    def delete(self, note_id):
        if note_id not in self.notes:
            raise KeyError(f"Note with ID {note_id} not found.")
        del self.notes[note_id]

    def get_all(self):
        return sorted(self.notes.values(), key=lambda n: n.created_at)

    def search_by_text(self, query):
        q = query.lower()
        return [n for n in self.notes.values() if q in n.text.lower()]

    def search_by_tag(self, tag):
        t = tag.strip().lower()
        return [n for n in self.notes.values() if t in n.tags]

    def sort_by_tags(self):
        def sort_key(note):
            if note.tags:
                return (0, sorted(note.tags)[0], note.created_at)
            return (1, "", note.created_at)
        return sorted(self.notes.values(), key=sort_key)

    def __iter__(self):
        return iter(self.notes.values())

    def clear(self):
        self.notes.clear()
        self._next_id = 1

    def __len__(self):
        return len(self.notes)
