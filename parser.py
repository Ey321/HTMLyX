from typing import *


class Parser:
    def __init__(self, path_to_file):
        self.file = open(path_to_file)
        self.file_path = path_to_file
        self.current_line: Optional[str] = None
        self.next_line: Optional[str] = None
        self.update_next()

    def update_next(self):
        self.current_line = self.next_line
        self.next_line = self.file.readline()
        while self.next_line != "" and (self.next_line == "\n" or
                                        self.next_line[0] == "#"):
            self.next_line = self.file.readline()

    def has_next(self):
        return self.next_line == ""

    def next(self):
        return self.next_line

    def advance(self):
        n = self.next_line
        self.update_next()
        return n

    def current(self):
        return self.current_line

    def is_current_command(self):
        return self.current_line.startswith("\\")

    def current_command(self):
        return self.current_line.split()[0]

    def current_parameters(self):
        return self.current_line.split()[1:]

    def next_command(self):
        return self.next_line.split()[0]

    def next_parameters(self):
        return self.next_line.split()[1:]

    def is_next_command(self):
        return self.next_line.startswith("\\")


