import os
import pickle
from collections import UserDict
from datetime import datetime
from pathlib import Path


class Name:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Tag:
    def __init__(self, tags):
        self.tags = tags

    def __repr__(self):
        return str(self.tags)


class Notes:
    def __init__(self, name: Name, data: str, tags: Tag = None, time: datetime = datetime.now()):
        self.name = name
        self.data = data
        self.tag = []
        if tags:
            self.tag.append(tags)
        self.time = time

    def add_tags(self, tags, edit_time=datetime.now()):
        self.tag.append(tags)
        self.time = edit_time

    def change_notes(self, data):
        self.data = data

    def change_tag(self, old_tag, new_tag, edit_time=datetime.now()):
        for i in self.tag:
            if i.tags == old_tag.tags:
                self.tag[self.tag.index(i)] = new_tag
        self.time = edit_time

    def delete_tags(self, tags, edit_time=datetime.now()):
        for i in self.tag:
            if i.tags == tags.tags:
                self.tag.remove(i)
        self.time = edit_time

    def __repr__(self):
        if len(self.tag) == 0:
            return f'{self.name}: {self.data}, there is no Tags and no time'
        else:
            return f'{self.name}: {self.data}, Tags {self.tag}, edited ' \
                   f'time {self.time.strftime("%H:%M:%S | edit date %d-%m-%Y")}'


class NoteBook(UserDict):
    counter = 0

    def add_to_notebook(self, note: Notes):
        self.data[note.name.value] = note

    def iterator_notebook(self, *args):
        self.counter = int(args[0])
        number_of_iterations = int(args[1])
        b = list(self.data)
        while int(self.counter) < number_of_iterations:
            yield self[b[self.counter]]
            self.counter += 1
            if self.counter == number_of_iterations:
                input("press Enter to continue...")
                number_of_iterations += int(args[1])
                if number_of_iterations > len(b):
                    number_of_iterations = len(b)


def input_error(in_func):
    def wrapper(*args):
        try:
            check = in_func(*args)
            return check
        except KeyError:
            return "Please check your input"
        except IndexError:
            return "Need more arguments"
        except AttributeError:
            return "No such attribute"
        except EOFError:
            return "DB file got corrupted"

    return wrapper


def ex(note_book, *args):
    save_db(note_book)
    return 'Bye!'


def cmd_error(*args):
    return 'I can`t help you'


@input_error
def add_to_notebook(notebook: NoteBook, *args):
    temp_name = Name(args[0])
    temp_note_txt = ' '.join(list(args[1:]))
    tmp_user_input = input('Do you need to add some Tag to your note? if so - type Y/y -> ')
    if tmp_user_input in ('Y', 'y'):
        tmp_tags_input = input('add Tag: ')
        temp_note = Notes(temp_name, temp_note_txt, Tag(tmp_tags_input), datetime.now())
    else:
        temp_note = Notes(temp_name, temp_note_txt, None, datetime.now())

    notebook.add_to_notebook(temp_note)
    save_db(notebook)
    return f'Note with name {temp_name} was added'


@input_error
def show_all(notebook: NoteBook, *args):
    if len(notebook) == 0:
        return "The notes is empty"
    if args[0] == '':
        print('Now you will get a whole book\n')
        for k, v in notebook.data.items():
            print(f'Note name: {k}')
            print(f'Note content: {v.data}')
            if v.tag:
                print(f'Tags: {v.tag}')
            else:
                print('No tags')
            print(f'edited {v.time.strftime("time %H:%M:%S | date %d-%m-%Y")}')
            print('============')
        return 'End of the NoteBook'
    if args[0].isdigit():
        if int(args[0]) > len(notebook.data.values()):
            print('Now you will get a whole book\n')
            for k, v in notebook.data.items():
                print(f'Note name {k}:')
                print(f'Note content: {v.data}')
                if v.tag:
                    print(f'Tags: {v.tag}')
                else:
                    print('No tags')
                print(f'edited {v.time.strftime("time %H:%M:%S | date %d-%m-%Y")}')
                print('============')
            return 'End of the NoteBook'
    if int(args[0]) <= len(notebook.data.values()):
        by_steps = notebook.iterator_notebook(notebook.counter, args[0])
        for n_ote in by_steps:
            print('============')
            print(f'Note name {n_ote.name}:')
            print(f'{n_ote.data}')
            if n_ote.tag:
                print(f'{n_ote.tag}')
            else:
                print('No tags')
            print(f'edited {n_ote.time.strftime("time %H:%M:%S | date %d-%m-%Y")}')
            print('============')
        notebook.counter = 0
    return "End of the NoteBook"


@input_error
def delete_note(notebook: NoteBook, *args):
    tmp_note = ' '.join(args)
    notebook.pop(tmp_note)
    return f'Note with name {tmp_note} was deleted'


@input_error
def add_tag(notebook: NoteBook, *args):
    tmp_note = ' '.join(args)
    if tmp_note not in notebook.keys():
        return 'There is no such note'
    for k_notes, v_notes in notebook.data.items():
        if tmp_note == k_notes:
            print(f'the note with name {tmp_note} exist and looks like --> {notebook.get(tmp_note)}')
            Notes.add_tags(v_notes, Tag(input('input tag: ')))
    return f'Tag for Note {tmp_note} was added'


@input_error
def change_tag(notebook: NoteBook, *args):
    global new_tag, old_tag
    tmp_note = ' '.join(args)
    if tmp_note not in notebook.keys():
        return 'There is no such note'
    for k_notes, v_notes in notebook.data.items():
        if tmp_note == k_notes:
            print(f'the note with name {tmp_note} exist and looks like --> {notebook.get(tmp_note)}')
            old_tag = Tag(input('give me Tag to change: '))
            new_tag = Tag(input('input new Tag name: '))
            Notes.change_tag(v_notes, old_tag, new_tag)
    return f'The Tag {old_tag} was changed for {new_tag} n Note:{tmp_note}'


@input_error
def delete_tag(notebook: NoteBook, *args):
    global tmp_del_tag
    tmp_note = ' '.join(args)
    if tmp_note not in notebook.keys():
        return 'There is no such note'
    for k_notes, v_notes in notebook.data.items():
        if tmp_note == k_notes:
            print(f'the note with name {tmp_note} exist and looks like --> {notebook.get(tmp_note)}')
            tmp_del_tag = input('Please give me a tag name: ')
            Notes.delete_tags(v_notes, Tag(tmp_del_tag))
    return f' The Tag {tmp_del_tag} in Note:{tmp_note} was deleted'


@input_error
def change_note(notebook: NoteBook, *args):
    tmp_note = ' '.join(args)
    if tmp_note not in notebook.keys():
        return 'There is no such note'
    for k_notes, v_notes in notebook.data.items():
        if tmp_note == k_notes:
            print(f'the note with name {tmp_note} exist and looks like --> {notebook.get(tmp_note)}')
            Notes.change_notes(v_notes, input('change the note: '))
    return f'Note {tmp_note} was changed'


@input_error
def finder(*args):
    tmp_input = input('what do you want to search? by tags - type "tags" for notes content type "notes"  ')
    if tmp_input == 'tags':
        find_tag = input('type name for needed tag -> ')
        for k_notes, v_notes in args[0].items():
            for i in v_notes.tag:
                if find_tag == i.tags:
                    print(f'Note name {k_notes}, : {v_notes.data}')
                    continue
    elif tmp_input == 'notes':
        find_note = input('type info to find -> ')
        for k_notes, v_notes in args[0].items():
            if find_note in v_notes.data:
                print(f'Note name {k_notes}, : {v_notes.data}')
    else:
        return 'Oops'
    return '-------------------'


def info(*args):
    print('The commands are:')
    print('"add note" -> to add note, example: add note __Name__ __Note TXT__')
    print('"delete note" -> to delete note , example: delete note __Name__')
    print('"change note" -> to change note , example: change note __Name__')
    print('"add tag" -> to add tag , example: add tag __Name__')
    print('"change tag" -> to add tag , example: change tag __Name__')
    print('"delete tag" -> to add tag , example: delete tag __Name__')
    print('"show all" -> to show all notes')
    print('"finder" -> to start searching in tags or text')
    print('"exit" or "." -> to exit')
    return 'Make your choice'


COMMANDS = {ex: ['exit', '.'], add_to_notebook: ['add note'], show_all: ["show all"], delete_note: ['delete note'],
            change_note: ['change note'], add_tag: ['add tag'], finder: ['finder'], change_tag: ['change tag'],
            delete_tag: ['delete tag'], info: ['info', 'help']}


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")
    return cmd_error, ['']


def db_checker():
    if os.path.isfile(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_notes.bin')):
        with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_notes.bin'), 'rb') as f:
            our_notes = NoteBook()
            our_notes.data = pickle.load(f)
        return our_notes
    else:
        filepath = Path(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_notes.bin'))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        our_notes = NoteBook()
    return our_notes


def save_db(our_notes):
    filepath = Path(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_notes.bin'))
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as f:
        pickle.dump(our_notes, f)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Welcome to Notes!\n')
    try:
        our_notes = db_checker()
    except Exception:
        our_notes = NoteBook()
    print('for help with commands type info or help')
    while True:
        our_command = input("And your command is...> ")
        result, data = parse_command(our_command)
        print(result(our_notes, *data))
        if result is ex:
            break


if '__main__' == __name__:
    main()

