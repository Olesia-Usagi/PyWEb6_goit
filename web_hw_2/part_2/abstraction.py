
from abc import ABC, abstractmethod


class IOConsole(ABC):

    @abstractmethod
    def show_msg(self):
        ...


class IOWeb(ABC):

    @abstractmethod
    def show_msg(self):
        ...


class Console(IOConsole):

    def __init__(self, message):
        self.message = message

    def show_msg(self):
        return f'Got a message for you in this console: "{self.message}"'


class Web(IOWeb):

    def __init__(self, message):
        self.message = message

    def show_msg(self):
        return f'Got a message for you on this site: "{self.message}"'


def main():
    c = Console('Is this a console?')
    print(c.show_msg())

    w = Web('Is this a site?')
    print(w.show_msg())


if __name__ == '__main__':
    main()
