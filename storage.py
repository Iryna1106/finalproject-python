import pickle
from models.address_book import AddressBook
from models.notes import NoteBook

# Зберігаємо стан адресної книги та нотатника у файл на диску


def save_data(book, notebook, filename="data.pkl"):
    with open(filename, "wb") as file:
        pickle.dump((book, notebook), file)

# Завантажуємо дані з файлу. Якщо програма запускається вперше і файлу ще не має,
# повертає нові порожні об'єкти AddressBook та NoteBook.


def load_data(filename="data.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    # Спрацює при першому запуску програми
    except FileNotFoundError:
        return AddressBook(), NoteBook()
    # На випадок якщо файл пошкоджено
    except Exception as e:
        print(f"Warning: Could not load data from {filename}. Error{e}")
        return AddressBook(), NoteBook
