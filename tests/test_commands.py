from unittest.mock import patch
from models.address_book import AddressBook, Record
from models.notes import NoteBook, Note
from handlers import (
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
    add_note,
    all_notes,
    find_note,
    edit_note,
    delete_note,
    add_tag,
    find_by_tag,
    sort_by_tags,
    clear_contacts,
    clear_notes,
)


# ── Helpers ──────────────────────────────────────────────


def make_book_with_contact(name="Alice", phone="1234567890"):
    book = AddressBook()
    r = Record(name)
    if phone:
        r.add_phone(phone)
    book.add_record(r)
    return book


def make_notebook_with_note(text="Test note", tag=None):
    nb = NoteBook()
    n = Note(text)
    nb.add(n)
    if tag:
        n.add_tag(tag)
    return nb


# ── Contact commands ─────────────────────────────────────


class TestAddContact:
    def test_add_new(self):
        book = AddressBook()
        result = add_contact(["Alice"], book)
        assert "added" in result
        assert book.find("Alice") is not None

    def test_add_with_phone(self):
        book = AddressBook()
        result = add_contact(["Alice", "1234567890"], book)
        assert "Phone" in result
        assert len(book.find("Alice").phones) == 1

    def test_add_no_args(self):
        book = AddressBook()
        result = add_contact([], book)
        assert "Usage" in result or "provide" in result.lower()

    def test_add_invalid_phone(self):
        book = AddressBook()
        result = add_contact(["Alice", "abc"], book)
        assert "10 digits" in result


class TestAllContacts:
    def test_empty(self):
        book = AddressBook()
        result = all_contacts([], book)
        assert "No contacts" in result

    def test_with_contacts(self):
        book = make_book_with_contact()
        result = all_contacts([], book)
        assert "Alice" in result


class TestFindContact:
    def test_no_args(self):
        book = AddressBook()
        result = find_contact([], book)
        assert "Usage" in result or "provide" in result.lower()

    def test_found(self):
        book = make_book_with_contact()
        result = find_contact(["Alice"], book)
        assert "Alice" in result

    def test_not_found(self):
        book = make_book_with_contact()
        result = find_contact(["Bob"], book)
        assert "No contacts found" in result

    def test_by_phone(self):
        book = make_book_with_contact()
        result = find_contact(["1234567890"], book)
        assert "Alice" in result


class TestShowPhone:
    def test_no_args(self):
        book = AddressBook()
        result = show_phone([], book)
        assert "Usage" in result or "provide" in result.lower()

    def test_found(self):
        book = make_book_with_contact()
        result = show_phone(["Alice"], book)
        assert "1234567890" in result

    def test_not_found(self):
        book = AddressBook()
        result = show_phone(["Bob"], book)
        assert "not found" in result

    def test_no_phones(self):
        book = make_book_with_contact(phone=None)
        result = show_phone(["Alice"], book)
        assert "No phones" in result


class TestChangePhone:
    def test_no_args(self):
        book = AddressBook()
        result = change_phone([], book)
        assert "Usage" in result

    def test_success(self):
        book = make_book_with_contact()
        result = change_phone(["Alice", "1234567890", "0987654321"], book)
        assert "updated" in result

    def test_contact_not_found(self):
        book = AddressBook()
        result = change_phone(["Bob", "111", "222"], book)
        assert "not found" in result

    def test_old_phone_not_found(self):
        book = make_book_with_contact()
        result = change_phone(["Alice", "0000000000", "9999999999"], book)
        assert "not found" in result


class TestAddBirthday:
    def test_no_args(self):
        book = AddressBook()
        result = add_birthday([], book)
        assert "Usage" in result

    def test_success(self):
        book = make_book_with_contact()
        result = add_birthday(["Alice", "15.06.1990"], book)
        assert "Birthday added" in result

    def test_invalid_date(self):
        book = make_book_with_contact()
        result = add_birthday(["Alice", "not-a-date"], book)
        assert "Invalid" in result or "format" in result.lower()

    def test_contact_not_found(self):
        book = AddressBook()
        result = add_birthday(["Bob", "15.06.1990"], book)
        assert "not found" in result


class TestShowBirthday:
    def test_no_args(self):
        book = AddressBook()
        result = show_birthday([], book)
        assert "Usage" in result

    def test_success(self):
        book = make_book_with_contact()
        add_birthday(["Alice", "15.06.1990"], book)
        result = show_birthday(["Alice"], book)
        assert "15.06.1990" in result

    def test_no_birthday(self):
        book = make_book_with_contact()
        result = show_birthday(["Alice"], book)
        assert "No birthday" in result

    def test_not_found(self):
        book = AddressBook()
        result = show_birthday(["Bob"], book)
        assert "not found" in result


class TestBirthdays:
    def test_no_upcoming(self):
        book = AddressBook()
        result = birthdays([], book)
        assert "No birthdays" in result

    def test_custom_days(self):
        book = AddressBook()
        result = birthdays(["30"], book)
        assert "No birthdays" in result


class TestAddEmail:
    def test_no_args(self):
        book = AddressBook()
        result = add_email_cmd([], book)
        assert "Usage" in result

    def test_success(self):
        book = make_book_with_contact()
        result = add_email_cmd(["Alice", "alice@example.com"], book)
        assert "Email added" in result

    def test_invalid_email(self):
        book = make_book_with_contact()
        result = add_email_cmd(["Alice", "not-an-email"], book)
        assert "Invalid" in result

    def test_contact_not_found(self):
        book = AddressBook()
        result = add_email_cmd(["Bob", "bob@example.com"], book)
        assert "not found" in result


class TestAddAddress:
    def test_no_args(self):
        book = AddressBook()
        result = add_address_cmd([], book)
        assert "Usage" in result

    def test_success_inline(self):
        book = make_book_with_contact()
        result = add_address_cmd(["Alice", "123", "Main", "St"], book)
        assert "Address added" in result

    def test_contact_not_found(self):
        book = AddressBook()
        result = add_address_cmd(["Bob", "some", "address"], book)
        assert "not found" in result


class TestDeleteContact:
    def test_no_args(self):
        book = AddressBook()
        result = delete_contact([], book)
        assert "Usage" in result

    def test_success(self):
        book = make_book_with_contact()
        result = delete_contact(["Alice"], book)
        assert "deleted" in result
        assert book.find("Alice") is None

    def test_not_found(self):
        book = AddressBook()
        result = delete_contact(["Bob"], book)
        assert "not found" in result


# ── Note commands ────────────────────────────────────────


class TestAddNote:
    @patch("builtins.input", return_value="My note")
    def test_success(self, mock_input):
        nb = NoteBook()
        result = add_note([], nb)
        assert "Note added" in result
        assert len(nb) == 1

    @patch("builtins.input", return_value="")
    def test_empty_text(self, mock_input):
        nb = NoteBook()
        result = add_note([], nb)
        assert "empty" in result.lower()


class TestAllNotes:
    def test_empty(self):
        nb = NoteBook()
        result = all_notes([], nb)
        assert "No notes" in result

    def test_with_notes(self):
        nb = make_notebook_with_note()
        result = all_notes([], nb)
        assert "Test note" in result


class TestFindNote:
    def test_no_args(self):
        nb = NoteBook()
        result = find_note([], nb)
        assert "Usage" in result or "provide" in result.lower()

    def test_found(self):
        nb = make_notebook_with_note()
        result = find_note(["Test"], nb)
        assert "Test note" in result

    def test_not_found(self):
        nb = make_notebook_with_note()
        result = find_note(["nonexistent"], nb)
        assert "No notes found" in result


class TestEditNote:
    @patch("builtins.input", return_value="Updated text")
    def test_success(self, mock_input):
        nb = make_notebook_with_note()
        result = edit_note(["1"], nb)
        assert "updated" in result
        assert nb.find(1).text == "Updated text"

    def test_no_args(self):
        nb = NoteBook()
        result = edit_note([], nb)
        assert "Usage" in result or "provide" in result.lower()

    def test_not_found(self):
        nb = NoteBook()
        result = edit_note(["999"], nb)
        assert "not found" in result


class TestDeleteNote:
    def test_no_args(self):
        nb = NoteBook()
        result = delete_note([], nb)
        assert "Usage" in result or "provide" in result.lower()

    def test_success(self):
        nb = make_notebook_with_note()
        result = delete_note(["1"], nb)
        assert "deleted" in result
        assert len(nb) == 0

    def test_not_found(self):
        nb = NoteBook()
        result = delete_note(["999"], nb)
        assert "not found" in result


class TestAddTag:
    def test_no_args(self):
        nb = NoteBook()
        result = add_tag([], nb)
        assert "Usage" in result or "provide" in result.lower()

    def test_success(self):
        nb = make_notebook_with_note()
        result = add_tag(["1", "important"], nb)
        assert "important" in result
        assert "important" in nb.find(1).tags

    def test_duplicate_tag(self):
        nb = make_notebook_with_note(tag="work")
        result = add_tag(["1", "work"], nb)
        assert "already exists" in result


class TestFindByTag:
    def test_no_args(self):
        nb = NoteBook()
        result = find_by_tag([], nb)
        assert "Usage" in result or "provide" in result.lower()

    def test_found(self):
        nb = make_notebook_with_note(tag="work")
        result = find_by_tag(["work"], nb)
        assert "Test note" in result

    def test_not_found(self):
        nb = make_notebook_with_note()
        result = find_by_tag(["nonexistent"], nb)
        assert "No notes found" in result


class TestSortByTags:
    def test_empty(self):
        nb = NoteBook()
        result = sort_by_tags([], nb)
        assert "No notes" in result

    def test_with_notes(self):
        nb = NoteBook()
        n1 = Note("B note")
        n2 = Note("A note")
        nb.add(n1)
        nb.add(n2)
        n1.add_tag("zebra")
        n2.add_tag("alpha")
        result = sort_by_tags([], nb)
        lines = result.split("\n")
        a_idx = next(i for i, l in enumerate(lines) if "A note" in l)
        b_idx = next(i for i, l in enumerate(lines) if "B note" in l)
        assert a_idx < b_idx


# ── Clear commands ───────────────────────────────────────


class TestClearContacts:
    def test_empty(self):
        book = AddressBook()
        result = clear_contacts([], book)
        assert "No contacts to clear" in result

    def test_success(self):
        book = make_book_with_contact()
        result = clear_contacts([], book)
        assert "All contacts have been deleted" in result
        assert len(book.data) == 0


class TestClearNotes:
    def test_empty(self):
        nb = NoteBook()
        result = clear_notes([], nb)
        assert "No notes to clear" in result

    def test_success(self):
        nb = make_notebook_with_note()
        result = clear_notes([], nb)
        assert "All notes have been deleted" in result
        assert len(nb) == 0

    def test_id_resets(self):
        nb = make_notebook_with_note()
        clear_notes([], nb)
        n = Note("New note")
        nb.add(n)
        assert n.id == 1
