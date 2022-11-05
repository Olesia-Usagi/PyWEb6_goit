import time
from collections import UserDict
from datetime import datetime, timedelta
from itertools import islice
import pickle
import os
import re
from pathlib import Path
from random import choice


class NoEmailUpdateTo(Exception):
	"""
	Exception raised when there is no email update to.
	"""
	pass


class EmailAlreadyExists(Exception):
	"""
	Exception raised when trying to add an email that already exists.
	"""
	pass


class NameAlreadyExists(Exception):
	"""
		Exception raised when a name already exist in the phonebook.
	"""
	pass


class PhoneAlreadyExists(Exception):
	"""
		Exception raised when a phone number already exist in the phonebook.
	"""
	pass


class WrongName(Exception):
	"""
	Raised when the name is not valid
	"""
	pass


class BirthdayIncorrect(Exception):
	"""
	Raised when the birthday is not valid
	"""
	pass


class NotEnoughArguments(Exception):
	"""
	Raised when the number of arguments is not enough
	"""
	pass


class NotANumberForCountOFRecords(Exception):
	"""
	Raised when the number of records is not a number
	"""
	pass


class WrongPhoneNumberFormat(Exception):
	"""
	Raised when the phone number is not valid
	"""
	pass


class NotRightPhoneNumberToUpdate(Exception):
	"""
	Raised when the phone number is not exist
	"""
	pass


class WrongEmailFormat(Exception):
	"""
	Raised when the email is not valid
	"""
	pass


class ThisMailDoesNotExist(Exception):
	"""
	Raised when the email is not valid
	"""
	pass


def exception_handler(function):
	def wrapper(*args, **kwargs):
		while True:
			try:
				return function(*args, **kwargs)

			except WrongName:
				print('-\n|The name is not valid!|\n-')
				time.sleep(1)
				break
			except BirthdayIncorrect:
				print('-\n|The birthday is not valid!|\n-')
				time.sleep(1)
				break
			except NotEnoughArguments:
				print('-\n|The number of arguments is not enough.|\n-')
				time.sleep(1)
				break
			except NotANumberForCountOFRecords:
				print('-\n|The number of records is not a number.|\n-')
				time.sleep(1)
				break
			except WrongPhoneNumberFormat:
				print('-\n|The entered number contains forbidden characters.|\n-')
				time.sleep(1)
				break
			except NotRightPhoneNumberToUpdate:
				print('-\n|This contact doesn\'t have a phone number you tried to update .|\n-')
				time.sleep(1)
				break
			except WrongEmailFormat:
				print('-\n|The email is not valid.|\n-')
				time.sleep(1)
				break
			except NameAlreadyExists:
				print('-\n|The name is already exist.|\n-')
				time.sleep(1)
				break
			except PhoneAlreadyExists:
				print('-\n|The phone number is already exist in this phonebook.|\n-')
				time.sleep(1)
				break
			except EmailAlreadyExists:
				print('-\n|The email is already exist in this phonebook.|\n-')
				time.sleep(1)
				break
			except NoEmailUpdateTo:
				print('-\n|Something went wrong, I guess.|\n-')
				time.sleep(1)
				break
			except ThisMailDoesNotExist:
				print('-\n|You are trying to change a non-existent email address|\n-')
				time.sleep(1)
				break

	return wrapper


class Record:

	def __init__(self, name, phone=None, birthday=None, email=None):
		self.name = name
		self.phones = []
		self.emails = []
		self.birthday = birthday

		if phone:
			self.add_phone(phone)

		if email:
			self.add_email(email)

	def check_phone(self, phone) -> bool:
		if str(phone) in self.phones:
			return True
		return False

	def add_phone(self, phone) -> bool:
		if not self.check_phone(phone):
			self.phones.append(str(phone))
			return True
		return False

	def update_phone(self, phone, new_phone) -> bool:
		if self.check_phone(phone):
			self.delete_phone(phone)
			self.add_phone(new_phone.value)
			return True
		raise NotRightPhoneNumberToUpdate

	def delete_phone(self, phone) -> bool:
		if self.check_phone(phone):
			self.phones.remove(str(phone))
			return True
		return False

	def check_email(self, email) -> bool:
		if str(email) in self.emails:
			return True
		return False

	def add_email(self, email) -> bool:
		if not self.check_email(email):
			self.emails.append(str(email))
			return True
		return False

	def update_email(self, email, new_email) -> bool:
		if self.check_email(email):
			self.delete_email(email)
			self.add_email(new_email.value)
			return True
		raise ThisMailDoesNotExist

	def delete_email(self, email) -> bool:
		if self.check_email(email):
			self.emails.remove(str(email))
			return True
		return False

	def append_email(self, email):
		if not self.check_email(email):
			self.emails.append(str(email))
			return True

	def check_birthday(self, birthday) -> bool:
		if birthday is not None:
			self.birthday = birthday
			return True
		return False

	def add_birthday(self, birthday) -> bool:
		if not self.check_birthday(birthday):
			self.birthday = birthday
			return True
		return False

	def __repr__(self):
		return f'{self.name} -- {self.birthday} -- {self.phones} -- {self.emails}'


class Field:
	def __init__(self, value) -> None:
		self.__value = None
		self.value = value


class Name(Field):

	def __repr__(self):
		return self.value

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, value):
		if re.match(r'^[a-zA-Zа-яА-Я]+$', value):
			self.__value = value.title()
		else:
			raise WrongName


class Phone(Field):

	def __repr__(self):
		return f'{self.__value}'

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, n_value):
		n_value = n_value.strip()
		for ch in n_value:
			if ch not in "0123456789()-+":
				raise WrongPhoneNumberFormat
		self.__value = n_value


class EMail(Field):
	def __repr__(self):
		return self.value

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, n_value):
		n_value = n_value.strip()
		if not re.match(r'^[a-z\d_\-.]+@[a-z\d_\-.]+\.[a-z]+$', n_value):
			raise WrongEmailFormat
		self.__value = n_value


class Birthday(Field):
	def __repr__(self):
		return self.value

	def __str__(self):
		return self.value

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, b_value):
		if b_value:
			try:
				datetime.strptime(b_value, "%d.%m.%Y")
			except ValueError:
				raise BirthdayIncorrect
		else:
			self.__value = None
		self.__value = b_value


class AddressBook(UserDict):

	def add_record(self, record: Record):
		self.data[record.name.value] = record

	def __next__(self):
		return next(self.iterator())

	def iterator(self, n=2):
		start, page = 0, n
		while True:
			yield dict(islice(self.data.items(), start, n))
			start, n = n, n + page
			if start >= len(self.data):
				break
			gate = input('|Press ENTER to proceed...|\n')


address_book = AddressBook()

...


@exception_handler
def add_contact(*args):
	try:
		name = Name(args[0][0])
		phone = Phone(args[0][1])
	except IndexError:
		raise NotEnoughArguments
	if name.value in address_book:
		raise NameAlreadyExists
	elif phone.value in address_book:
		raise PhoneAlreadyExists
	record = Record(name, phone)
	address_book.add_record(record)
	print(f'|Contact {name.value} added to the phonebook.|')


@exception_handler
def update_number(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				phone = Phone(args[0][1])
				if phone.value in address_book:
					raise PhoneAlreadyExists
				address_book[name.value].update_phone(Phone(args[0][1]), Phone(args[0][2]))
				print(f'|This contacts phone number {name.value} updated.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def append_number(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				phone = Phone(args[0][1])
				if phone.value in address_book:
					raise PhoneAlreadyExists
				address_book[name.value].add_phone(Phone(args[0][1]))
				print(f'|Number {args[0][1]} appended to contact {name.value}.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def delete_phone_number(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				address_book[name.value].delete_phone(Phone(args[0][1]))
				print(f'|Number {args[0][1]} of contact {name.value} successfully deleted.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def delete_contact(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				del address_book[name.value]
				print(f'|Contact {name.value} successfully deleted.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def show_all(*args):
	clear_screen()
	print('--- Phonebook ---')
	if address_book:
		how_much_recs = input('|Press "ENTER" to show all the records.|'
		                      '\nOr enter the required quantity: \n>>>> ')
		if how_much_recs == '':
			how_much_recs = len(address_book)
		elif how_much_recs.isalpha():
			raise NotANumberForCountOFRecords
		elif int(how_much_recs) <= 0:
			print(f'|You entered {how_much_recs} records, but I cannot show less than 1 record.|')
			how_much_recs = 1
		for rec in address_book.iterator(int(how_much_recs)):
			while True:
				for name, value in rec.items():
					print(f'***\nContact -- {name};')
					print(f'----------------\nPhone numbers: ')
					for phone in value.phones:
						print(f'{phone};')
					print(f'----------------\nDate of birth: {value.birthday if value.birthday else "Not specified."}')
					print(f'----------------\nEmail: ')
					if value.emails:
						for email in value.emails:
							print(f'{email};\n')
					else:
						print('Not specified.\n')
				break
		print('--- End of phonebook ---')
	else:
		print('|Phonebook is empty.|')


@exception_handler
def search_command(*args) -> None:
	clear_screen()
	if address_book:
		print('---Contact Search---')
		search = input('Enter the part of name, number or email: ')
		found = False
		for name, data in address_book.items():
			if re.search(search, name):
				print(f'Found in record: "{name}".')
				print(f'Phone numbers of contact:')
				for phone in data.phones:
					print(f'{phone};')
				print(f'Emails of contact: ')
				if data.emails:
					for email in data.emails:
						print(f'{email};')
				else:
					print('Not specified.')
				found = True
			if not found:
				for number in data.phones:
					if re.search(search, number):
						print(f'Found in record: "{name}".')
						print(f'Phone numbers of contact:')
						for phone in data.phones:
							print(f'{phone};')
						print(f'Emails of contact: ')
						if data.emails:
							for email in data.emails:
								print(f'{email};')
						else:
							print('Not specified.')
						found = True
						break
				if not found:
					for email in data.emails:
						if re.search(search, email):
							print(f'Found in record: "{name}".')
							print(f'Phone numbers of contact:')
							for phone in data.phones:
								print(f'{phone};')
							print(f'Emails of contact: ')
							if data.emails:
								for em in data.emails:
									print(f'{em};')
							else:
								print('Not specified.')
							found = True
							break
				if found:
					break
				else:
					print('|Not found anything.|')
					break

		print(f'\n--- Search is Complete ---')

	else:
		print('|Phonebook is empty.|')


@exception_handler
def add_email(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				email = EMail(args[0][1])
				if email.value in address_book[name.value].emails:
					raise EmailAlreadyExists
				address_book[name.value].add_email(EMail(args[0][1]))
				print(f'|Email {args[0][1]} added to contact {name.value}.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def update_email(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				address_book[name.value].update_email(EMail(args[0][1]), EMail(args[0][2]))
				print(f'|Email {args[0][1]} updated in contact {name.value}.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
		except TypeError:
			raise NoEmailUpdateTo
	else:
		print('|Phonebook is empty.|')


@exception_handler
def append_email(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				address_book[name.value].append_email(EMail(args[0][1]))
				print(f'|Email {args[0][1]} appended to contact {name.value}.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def delete_email(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				address_book[name.value].delete_email(EMail(args[0][1]))
				print(f'|Email {args[0][1]} deleted from contact {name.value}.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def add_birthday(*args):
	if address_book:
		try:
			name = Name(args[0][0])
			if name.value in address_book:
				address_book[name.value].add_birthday(Birthday(args[0][1]))
				print(f'|Birthday {args[0][1]} added to contact {name.value}.|')
			else:
				print(f'|Contact {name.value} not found.|')
		except IndexError:
			raise NotEnoughArguments
	else:
		print('|Phonebook is empty.|')


@exception_handler
def near_bd(*args):
	try:
		days = int(args[0][0])
	except NotEnoughArguments:
		print('|No number of days to search.|')
		return False
	if address_book:
		print('--- Search for contacts with the upcoming birthday ---')
		today = datetime.now().date()
		for name, data in address_book.items():
			if data.birthday:
				get_dude_date = data.birthday.value.split('.')

				dude_date = datetime(year=today.year, month=int(get_dude_date[1]), day=int(get_dude_date[0])).date()
				date_plus = today + timedelta(days=days)
				days_to_bd = (dude_date - today).days
				if today <= dude_date <= date_plus:
					print(f'|Contact {name} was born {data.birthday}, until his birthday left {days_to_bd} days.|')

		print('--- Search completed ---')
	else:
		print('|Phonebook is empty.|')


def clear_phonebook(*args):
	ask = input('Are you sure you want to clear the phonebook? (y/n) ')
	if ask == 'y':
		address_book.clear()
		print('|Phonebook cleared.|')
	else:
		print('|Phonebook not cleared.|')


...


def top_secret(*args):
	clear_screen()
	print('Ok, you asked for it.')
	time.sleep(2)
	print('Folder System32 deleting is initiated.')
	time.sleep(1)
	print('Say goodbye to your computer.')
	time.sleep(1)
	print('Starting deletion...')
	time.sleep(3)
	print('10...')
	time.sleep(1)
	print('9...')
	time.sleep(1)
	print('8...')
	time.sleep(1)
	print('7...')
	time.sleep(1)
	print('6...')
	time.sleep(1)
	print('5...')
	time.sleep(1)
	print('You still think this is a joke?')
	time.sleep(1)
	print('3...')
	time.sleep(1)
	print('2...')
	time.sleep(1)
	print('1...')
	time.sleep(3)
	print('0...')
	time.sleep(3)
	print('Folder System32 deleted.')
	time.sleep(1)
	print('Or not?')
	time.sleep(1)
	print('Just in case, do not try to swear anymore, ok?')
	time.sleep(1.5)


def goodbye(*args) -> None:
	so_long = ('Have a nice day!', 'See you later!', 'Bye!', 'Goodbye!', 'See you soon!', 'See you later!',
	           'Take care!')
	for message in so_long:
		print(choice(so_long))
		break
	time.sleep(1)


def help_command(*args) -> None:
	print(
		'---\n'
		'Available commands:\n'
		'add contact <name> <phone> - adding the record;\n'
		'show all - view all saved records;\n'
		'show near bd <days from today to> - finding out about upcoming birthdays;\n'
		'update number <name> <old number> <new number> - updating phone number;\n'
		'append number <name> <new number> - adding additional phone number;\n'
		'delete number <name> <number> - delete phone number;\n'
		'add email <name> <email> - adding email;\n'
		'append email <name> <email> - adding additional email;\n'
		'delete email <name> <email> - delete email;\n'
		'add birthday <name> <birthday "dd.mm.yyyy"> - adding birthday;\n'
		'help - view this help;\n'
		'hello, hi - greetings;\n'
		'delete contact <name> - deleting the contact;\n'
		'find - searching for record;\n'
		'clear, cls - clears the window;\n'
		'clear phonebook - clears the phonebook;\n'
		'quit, q  - closing the program;\n---')


def greetings(*args) -> None:
	clear_screen()
	print('---\nHi, looking for some info?\nHow can I help you?\n---')
	time.sleep(2)
	help_command()


def clear_screen(*args) -> None:
	os.system('cls' if os.name == 'nt' else 'clear')


def command_unknown(*args) -> None:
	print('-\n|Entered command is unknown. Try "help" for more information.|\n-')


def hello(*args) -> None:
	clear_screen()
	now_is = datetime.now().time()
	if 0 <= now_is.hour < 6:
		print('Good night!')
	elif 6 <= now_is.hour < 12:
		print('Good morning!')
	elif 12 <= now_is.hour < 18:
		print('Good afternoon!')
	elif 18 <= now_is.hour < 24:
		print('Good evening!')
	print('And welcome to the phonebook!\n-----')


def secret(*args) -> None:
	print('|You\'re welcome! Have a wonderful day!|')


...


def upload_check():
	if not os.path.exists(Path(Path.home(), 'Documents', 'PyBakers', 'database')):
		os.makedirs(Path(Path.home(), 'Documents', 'PyBakers', 'database'))
	try:
		with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_contacts.bin'), 'rb') as f:
			address_book.data = pickle.load(f)
	except FileNotFoundError:
		pass
	except ModuleNotFoundError:
		print("Preparing some stuff for you...")
		pass
	finally:
		with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_contacts.bin'), 'wb') as f:
			pickle.dump(address_book.data, f)


def save_phonebook():
	with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_contacts.bin'), 'wb') as f:
		pickle.dump(address_book.data, f)


...


def command_parser(command: str) -> None:
	for func, call in main_commands.items():
		for word in call:
			if command.startswith(word):
				arguments = command.replace(word, '').split()
				func(arguments)
				return None
			continue
	else:
		time.sleep(0.5)
		command_unknown()


main_commands = {
	clear_phonebook: ['clear phonebook', ],
	add_contact: ['add contact'],
	update_number: ['update number'],
	append_number: ['append number'],
	delete_phone_number: ['delete number'],
	add_email: ['add email'],
	update_email: ['update email'],
	append_email: ['append email'],
	delete_email: ['delete email'],
	add_birthday: ['add birthday'],
	delete_contact: ['delete contact'],
	show_all: ['show all'],
	near_bd: ['show near bd'],
	search_command: ['find', 'search'],
	help_command: ['help', 'помощь'],
	goodbye: ['exit', 'выход', 'quit', 'q'],
	greetings: ['здравствуйте', 'привет', 'hello', 'hi'],
	clear_screen: ['clear', 'cls'],
	secret: ['thank you'],
	top_secret: ['fuck you'],
}


def main():
	hello()
	upload_check()
	while True:
		command = input('Enter "hello" or "help" for more information.\n>>>>> ')
		command_parser(command.strip())
		if command in ['exit', 'выход', 'quit', 'q']:
			save_phonebook()
			break
		save_phonebook()


if __name__ == '__main__':
	main()
