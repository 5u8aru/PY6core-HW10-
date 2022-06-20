from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):
    ...


class Phone(Field):
    ...


class Record:
    def __init__(self, name: Name, phones=[]):
        self.name = name
        self.phone_l = phones

    def add_p(self, phone_num: Phone):
        self.phone_l.append(phone_num)

    def del_p(self, phone_num: Phone):
        self.phone_l.remove(phone_num)

    def change_p(self, phone_num: Phone, new_phone_num: Phone):
        self.phone_l.remove(phone_num)
        self.phone_l.append(new_phone_num)

    def __str__(self):
        return f'User {self.name} - Numbers: {", ".join([phone_num.value for phone_num in self.phone_l])}'


class AddressBook(UserDict):
    def __init__(self, record: Record):
        self.data[record.name.value] = record


def input_error(func):
    def wrapper(contacts, *args):
        try:
            result = func(contacts, *args)
        except IndexError:
            result = 'Enter a name and phone!'
        except KeyError:
            result = 'Can`t find this user in list!'
        except ValueError:
            result = 'Phone number is incorrect!'
        return result

    return wrapper


def greet(*args):
    return "How can I help you?"


@input_error
def add(contacts, *args):
    name = Name(args[0])
    m_phone = Phone(args[1])
    if name.value in contacts:
        if m_phone in contacts[name.value].phone_l:
            return f'{name}`s contact has already had this number'
        else:
            contacts[name.value].add_p(m_phone)
            return f'Add phone {m_phone} to user {name}'
    else:
        contacts[name.value] = Record(name, [m_phone])
        return f'Add user {name} with phone number {m_phone}'


@input_error
def change(contacts, *args):
    name, prev_phone, new_phone = args[0], args[1], args[2]
    contacts[name].change_p(Phone(prev_phone), Phone(new_phone))
    return f"{name}`s number changed from {Phone(prev_phone)} to {new_phone}"


@input_error
def phone(contacts, *args):
    name = args[0]
    return contacts[name]


@input_error
def delete_phone(contacts, *args):
    name, m_phone = args[0], args[1]
    contacts[name].del_p(Phone(m_phone))
    return f'{name}`s phone {m_phone} was deleted'


def show_all(contacts, *args):
    res = ''
    for key in contacts.keys():
        res += f'{contacts[key]}\n'
    return res


def goodbye(*args):
    print("Good bye!")
    return None


COMMANDS = {'hello': greet, 'add': add, 'change': change, 'phone': phone, 'show all': show_all,
            'good bye': goodbye, 'exit': goodbye, 'close': goodbye, 'delete': delete_phone}


def main():
    contacts_list = {}
    while True:
        user_command = input('>>> ')
        for k, v in COMMANDS.items():
            if k in user_command.lower():
                args = user_command[len(k):].split()
                result = COMMANDS[k](contacts_list, *args)
                if result is None:
                    exit()
                print(result)
                break
        else:
            print('Unknown command! Enter again!')


if __name__ == '__main__':
    main()
