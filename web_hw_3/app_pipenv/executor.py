from project_of_the_5_th.Notes import main as notes
from project_of_the_5_th.average_phonebook import main as phonebook
from project_of_the_5_th.sort_starter import start as sorting
from project_of_the_5_th.info import main as info
import time
import os

options = {
	'1': [phonebook, 'phonebook'],
	'2': [notes, 'notes'],
	'3': [sorting, 'sorting utility'],
	'4': [info, 'info']
}


def main(*args, **kwargs):
	os.system('cls' if os.name == 'nt' else 'clear')
	print('Welcome to our program!\nHere you can choose what you want to do:\n')
	while True:
		print("""
		1. Open phonebook;
		2. Open notes;
		3. Initialize file sorter;
		4. Project info
		5. Exit
		""")
		choice = input('Please choose an option: ')
		if choice in options:
			print('So you want to open {}?'.format(options[choice][1]))
			print('Loading...')
			time.sleep(3)
			options[choice][0](*args, **kwargs)
		elif choice == '5':
			print('Thank you for using our program! Have a nice day!')
			break
		else:
			print("Invalid choice. Try again.")
			continue


if __name__ == '__main__':
	main()
