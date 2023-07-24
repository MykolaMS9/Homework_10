from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


class Record():
    def __init__(self, name, phone=None):
        self.phones = []
        self.add_phone(phone)
        self.name = Name(name)

    def add_phone(self, phone):
        if phone:
            self.phones.append(Phone(phone))

    def __find_phone(self, phone):
        result = list(filter(lambda phon: phon.value == phone, self.phones))
        return result[0] if len(result) > 0 else None

    def delete_phone(self, phone):
        self.phones.remove(self.__find_phone(phone))

    def edit_phone(self, exist_phone, new_phone):
        self.phones[self.phones.index(self.__find_phone(exist_phone))] = Phone(new_phone)


class Field():
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):
    pass


class Phone(Field):
    pass


class ContactExist(Exception):
    pass


class ContactNotExist(Exception):
    pass


class UncorrectPhoneNumber(Exception):
    pass


class TypeValue(Exception):
    pass