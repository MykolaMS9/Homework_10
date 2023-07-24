import sys
import re
from contacts_core import AddressBook, Record, ContactExist, ContactNotExist, UncorrectPhoneNumber, TypeValue

# Constants
FULL_LEN_NUMBER = 12
SHORT_LEN_NUMBER = 10

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeValue:
            return 'Uncorrect format of a contact!!! \nExample: \n         add/change contact_name phone_number'
        except ContactExist:
            return 'Contact is already existed!!! \nExample: \n         add new_contact_name new_phone_number'
        except ContactNotExist:
            return 'Contact is not exist :('
        except UncorrectPhoneNumber:
            return 'Uncorrect type of number :('
        except SystemExit:
            return func(*args, **kwargs)
        except TypeError:
            return 'Missing arguments: name or number :('
        except ValueError:
            return 'Number is not exist :('
        except:
            return raise_error()

    return inner


def format_phone_number(phone, full_len_number=FULL_LEN_NUMBER, short_len_number=SHORT_LEN_NUMBER):
    if len(phone) == full_len_number:
        result = f'+{phone}'
    elif len(phone) == short_len_number:
        result = f'+38{phone}'
    else:
        raise UncorrectPhoneNumber
    return result

def sanitize_phone_number(phone):
    result = ''.join(re.findall("[0-9]", phone))
    result = format_phone_number(result)
    return result

def raise_error(*args, **kwargs):
    return f'Error command or uncorrected format'

@input_error
def command_close():
    sys.exit(f'Good bye!')


@input_error
def command_hello():
    return 'How can I help you?'


@input_error
def command_add(name_str, phone_number):
    if not name_str or not phone_number:
        raise TypeValue
    phone_number = sanitize_phone_number(phone_number)
    if name_str in concacts_dict.data:
        # added new phone to existed record
        record_ = concacts_dict.data[name_str]
    else:
        # created new record with name
        record_ = Record(name_str)
    record_.add_phone(phone_number)
    concacts_dict.add_record(record_)
    return f'Successfully added {name_str} with number {phone_number}'


@input_error
def command_change(name_str, exist_phone, phone_number):
    if not name_str or not phone_number or not exist_phone:
        raise TypeValue
    if name_str in concacts_dict.data:
        exist_phone = sanitize_phone_number(exist_phone)
        phone_number = sanitize_phone_number(phone_number)
        record_ = concacts_dict.data[name_str]
        record_.edit_phone(exist_phone, phone_number)
        concacts_dict.add_record(record_)
    else:
        raise ContactNotExist
    return f'Successfully changed {name_str} exist number {exist_phone} to {phone_number}'


@input_error
def command_phone(name_str):
    if not name_str:
        raise IndexError
    if name_str in concacts_dict.data:
        record_ = concacts_dict.data[name_str].phonesS
        result = ' '.join([phone.value for phone in record_])
        return result
    else:
        raise ContactNotExist


@input_error
def command_show_all():
    result = ''
    for key in concacts_dict.data:
        result += '{:<10} -> {}\n'.format(key, command_phone(key))
    return result


@input_error
def command_delete(name_str, phone_number):
    if not phone_number or not name_str:
        raise TypeError
    if name_str in concacts_dict.data:
        phone_number = sanitize_phone_number(phone_number)
        record_ = concacts_dict.data[name_str]
        record_.delete_phone(phone_number)
        concacts_dict.add_record(record_)
        return f'Number {phone_number} in {name_str} has been deleted'
    else:
        raise ContactNotExist


concacts_dict = AddressBook()

comand_dict = {
    'good bye': command_close,
    'close': command_close,
    'exit': command_close,
    'hello': command_hello,
    'add': command_add,
    'change': command_change,
    'phone': command_phone,
    'show all': command_show_all,
    'delete': command_delete
}


def get_handler(operator):
    return comand_dict.get(operator, raise_error)


def find_command(string) -> tuple:
    for key in comand_dict:
        l1 = key.split(' ')
        l2 = string.split(' ')
        command = l2[:len(l1)]
        if key == (' '.join(command).lower()):
            return key, l2[len(l1):]
    return None, []


def main():
    while True:
        inp = input("Write command: ")
        s1 = None
        s2 = None
        s3 = None
        (command, arguments) = find_command(inp)
        handler = get_handler(command)
        for val in arguments:
            if 0 == arguments.index(val):
                s1 = val
            elif 1 == arguments.index(val):
                s2 = val
            elif 2 == arguments.index(val):
                s3 = val
            else:
                raise_error()
        if not s1:
            h = handler()
        elif not s2:
            h = handler(s1)
        elif not s3:
            h = handler(s1, s2)
        else:
            h = handler(s1, s2, s3)
        print(h)

if __name__ == "__main__":
    main()