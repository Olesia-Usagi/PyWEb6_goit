import os
import time


def phonebook_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""   

    Module name: PhoneBook
                About module:
                            it saves, check, edit, delete records \\ from the contact book and also calculates the days before the birthday\n
                
                List of the commands:
                                add contact - adding the record;
                                update number - updating phone number;
                                append number - adding additional phone number;
                                delete number - delete phone number;
                                show all - view all saved records;
                                show near bd - finding out about upcoming birthdays;
                                add email - adding email;
                                append email - adding additional email;
                                delete email - delete email;
                                add birthday <birthday "dd.mm.yyyy"> - adding birthday;
                                help - view this help;
                                hello, hi - greetings;
                                delete contact - deleting the contact;
                                find - searching the record;
                                clear, cls - clears the window;
                                clear phonebook - clears the phonebook;
                                quit, q - closing the program;
    """)
    input('Press Enter to proceed')

def notes_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""   
    Module name: Notes\n
                About module: 
                            it saves, add, edit, delete, search for notes by tags or notes,\n
                
                List of the commands:
                                "add note" -> to add note, example: add note __Name__ __Note TXT__
                                "delete note" -> to delete note , example: delete note __Name__
                                "change note" -> to change note , example: change note __Name__
                                "add tag" -> to add tag , example: add tag __Name__
                                "change tag" -> to add tag , example: change tag __Name__
                                "delete tag" -> to add tag , example: delete tag __Name__
                                "show all" -> to show all notes
                                "show all #" -> to show all notes by # steps
                                "finder" -> to start searching in tags or text
                                "exit" or "." -> to exit

    """)
    input('Press Enter to proceed')

def sorting_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('it sorts the files in the specified folder by categories')
    print("""
    Module name: File-sorting-utility \n
                About module: 
                            it sorts files by extentians in choosen directory,\n
                List of the commands:
                                !!!IMPORTANT INFO!!! Folder to sort should be inside the folder where the utility was launched from.
                                <.> -- enter dot to exit;
    """)
    input('Press Enter to proceed')

def team_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""Team Name: PyBakers \n
                Our goal: to create a personal helper with command line interface \n
                version: 0.1.0\n
                Authors of the program: \n
                    Serhii Sytnik as Team lead
                    Olesia Popilovska as Scrum Master
                    Andrii Vasylchenko as developer
    """)
    input('Press Enter to proceed')


options = {
	'1': [phonebook_info, 'phonebook'],
	'2': [notes_info, 'notes'],
	'3': [sorting_info, 'sorting utility'],
    '4': [team_info, 'Team info'],
}

def main(*args, **kwargs):
	os.system('cls' if os.name == 'nt' else 'clear')
	print('We are PyBakers and this is info page!\nPlease choose information what you need:\n')
	while True:
		print("""
		1. Info about phonebook;
		2. Info about notes;
		3. Info about file sorter;
		4. Team info;
		5. Quit info;
		""")
		choice = input('Please choose an option: ')
		if choice in options:
			print('So you want receive info about {} module?'.format(options[choice][1]))
			print('Loading...')
			time.sleep(3)
			options[choice][0](*args, **kwargs)
		elif choice == '5':
			print('Have a lovely day!')
			break
		else:
			print("Invalid choice. Try again.")
			continue

if __name__ == '__main__':
	main()