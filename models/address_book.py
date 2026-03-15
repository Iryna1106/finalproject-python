from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""

    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    """Клас для зберігання дня народження. Має валідацію формату (DD.MM.YYYY)."""

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Email(Field):
    """Клас для зберігання електронної пошти. Має валідацію формату. Перевіряє валідність email за допомогою регулярного виразу."""

    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, value) is not None


class Address(Field):
    """Клас для зберігання фізичної адреси контакту."""
    pass


class Record:
    """Клас для зберігання інформації про контакт."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number):
        """Додає новий номер телефону до контакту."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        """Видаляє номер телефону з контакту."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone_number} not found.")

    def edit_phone(self, old_number, new_number):
        """Змінює існуючий номер телефону на новий."""
        phone_to_edit = self.find_phone(old_number)
        if phone_to_edit:
            self.add_phone(new_number)
            self.remove_phone(old_number)
        else:
            raise ValueError(f"Phone {old_number} not found.")

    def find_phone(self, phone_number):
        """Шукає номер телефону серед списку телефонів контакту."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday):
        """Додає або змінює день народження контакту."""
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        """Додає або змінює email контакту."""
        self.email = Email(email)

    def add_address(self, address):
        """Додає або змінює адресу контакту."""
        self.address = Address(address)

    def __str__(self):
        """Повертає відформатований рядок з усіма даними контакту."""
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        email_str = f", email: {self.email.value}" if self.email else ""
        address_str = f", address: {self.address.value}" if hasattr(
            self, 'address') and self.address else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}{email_str}{address_str}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами контактів."""

    def add_record(self, record):
        """Додає новий запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name):
        """Шукає контакт за іменем."""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє контакт за іменем."""
        if name in self.data:
            del self.data[name]

    def search(self, query):
        """Шукає контакти за збігом у імені, номерах телефонів, email або адресі."""
        results = []
        query = query.lower()

        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
                continue

            match_found = False
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    match_found = True
                    break

            if match_found:
                continue

            if hasattr(record, 'email') and record.email and query in record.email.value.lower():
                results.append(record)
                continue

            if hasattr(record, 'address') and record.address and query in str(record.address.value).lower():
                results.append(record)

        return results

    def get_upcoming_birthdays(self, days=7):
        """
        Повертає список контактів, у яких день народження відбудеться 
        протягом вказаної кількості днів (за замовчуванням 7).
        """
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday:
                user_birthday = record.birthday.value
                birthday_this_year = user_birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= days:
                    if birthday_this_year.weekday() == 5:
                        congratulation_date = (
                            birthday_this_year + timedelta(days=2))
                    elif birthday_this_year.weekday() == 6:
                        congratulation_date = (
                            birthday_this_year + timedelta(days=1))
                    else:
                        congratulation_date = birthday_this_year

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays
