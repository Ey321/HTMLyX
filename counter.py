def split_first_command(line):
    separating_characters = "\\.<>"
    first_space = first_sep_char = len(line)
    if " " in line:
        first_space = line.index(" ")
    for character in separating_characters:
        if character in line[1:]:
            first_sep_char = min(first_sep_char, line[1:].index(character) + 1)
    split_index = min((first_space, first_sep_char))

    # if the command was ended with a space, skip the space
    if split_index == first_space:
        return line[:split_index], line[split_index + 1:]
    # else, save the separating char
    else:  # split_index == first_sep_char
        return line[:split_index], line[split_index:]


class Counter:
    HIERARCHY = ("part", "section", "subsection", "subsubsection",
                 "paragraph", "subparagraph")
    PART_FORMAT = r"\Roman\c@part"
    SECTION_FORMAT = r"\arabic\c@section"
    SUBSECTION_FORMAT = r"\thesection.\arabic\c@subsection"
    SUBSUBSECTION_FORMAT = r"\thesubsection.\arabic\c@subsubsection"
    PARAGRAPH_FORMAT = r""
    SUBPARAGRAPH_FORMAT = r""

    def __init__(self):
        self.COUNTER_VALUES = {
            "\\c@part": 0,
            "\\c@section": 0,
            "\\c@subsection": 0,
            "\\c@subsubsection": 0,
            "\\c@paragraph": 0,
            "\\c@subparagraph": 0
        }
        self.COMMANDS = {
            "\\arabic\\c": self.evaluate_arabic,
            "\\roman\\c": self.evaluate_lowercase_roman,
            "\\Roman\\c": self.evaluate_uppercase_roman,

            "\\thepart": self.the_part,
            "\\thesection": self.the_section,
            "\\thesubsection": self.the_subsection,
            "\\thesubsubsection": self.the_subsubsection,
            "\\theparagraph": self.the_paragraph,
            "\\thesubparagraph": self.the_subparagraph
        }

        self.CONSTANTS = {
            "\\partname": "חלק"
        }

        for key in self.CONSTANTS.keys():
            self.COMMANDS[key] = self.evaluate_constant

    def increase_counter(self, counter_name):
        # support input as both '\c@part' and 'part'
        if not counter_name.startswith("\\c@"):
            counter_name = "\\c@" + counter_name
        self.COUNTER_VALUES[counter_name] += 1
        index = self.HIERARCHY.index(counter_name[3:])
        if index != 0:  # increasing part does not reset other values
            for i in range(index+1, len(self.HIERARCHY)):
                self.COUNTER_VALUES["\\c@" + self.HIERARCHY[i]] = 0

    def evaluate(self, number_format):
        if "\\" not in number_format:
            return number_format
        if number_format.startswith("\\"):
            out, remains = self.evaluate_command(number_format)
            return out + self.evaluate(remains)
        else:
            text, command = number_format.split("\\", 1)
            out, remains = self.evaluate_command("\\" + command)
            return text + out + self.evaluate(remains)

    def evaluate_command(self, number_format):
        for command, function in self.COMMANDS.items():
            if number_format.startswith(command):
                return function(number_format)
        return "error", ""

    def evaluate_constant(self, number_format):
        command, remains = split_first_command(number_format)
        return self.CONSTANTS[command], remains

    def evaluate_counter(self, display_type, number_format):
        command, after_command = split_first_command(number_format)
        counter, remains = split_first_command(after_command)
        return display_type(self.COUNTER_VALUES[counter]), remains

    def evaluate_the_commands(self, the_command, number_format):
        command, remains = split_first_command(number_format)
        return self.evaluate(the_command), remains

    # repetitive implementations of functions based on evaluate_the_commands
    # and evaluate_constant commands

    def evaluate_arabic(self, number_format):
        return self.evaluate_counter(arabic, number_format)

    def evaluate_lowercase_roman(self, number_format):
        return self.evaluate_counter(lowercase_roman, number_format)

    def evaluate_uppercase_roman(self, number_format):
        return self.evaluate_counter(uppercase_roman, number_format)

    def the_part(self, number_format):
        return self.evaluate_the_commands(self.PART_FORMAT, number_format)

    def the_section(self, number_format):
        return self.evaluate_the_commands(self.SECTION_FORMAT, number_format)

    def the_subsection(self, number_format):
        return self.evaluate_the_commands(self.SUBSECTION_FORMAT,
                                          number_format)

    def the_subsubsection(self, number_format):
        return self.evaluate_the_commands(self.SUBSUBSECTION_FORMAT,
                                          number_format)

    def the_paragraph(self, number_format):
        return self.evaluate_the_commands(self.PARAGRAPH_FORMAT, number_format)

    def the_subparagraph(self, number_format):
        return self.evaluate_the_commands(self.SUBPARAGRAPH_FORMAT,
                                          number_format)


def arabic(number):
    return str(number)


_LOWERCASE_ROMAN_NUMBERS = {
    1: "i",
    2: "ii",
    3: "iii",
    4: "iv",
    5: "v",
    6: "vi",
    7: "vii",
    8: "viii",
    9: "ix",
    10: "x",
    20: "xx",
    30: "xxx",
    40: "xl",
    50: "l",
    60: "lx",
    70: "lxx",
    80: "lxxx",
    90: "xc",
    100: "c",
    200: "cc",
    300: "ccc",
    400: "cd",
    500: "d",
    600: "dc",
    700: "dcc",
    800: "dccc",
    900: "cm",
    1000: "m",
    2000: "mm",
    3000: "mmm"
}


def lowercase_roman(number):
    out = ""
    current_factor = 10
    while number != 0:
        remainder = number % current_factor
        out = _LOWERCASE_ROMAN_NUMBERS[remainder] + out
        number -= remainder
        current_factor *= 10
    return out


def uppercase_roman(number):
    return lowercase_roman(number).upper()


if __name__ == "__main__":
    print(split_first_command("<span>\\partname</span>"))
    c = Counter()
    print(c.evaluate("<span>\\partname  \\thesection</span>"))

    c.increase_counter("subsection")
    print(c.evaluate('\\thesubsection'))
    c.increase_counter("section")
    print(c.evaluate('\\thesection'))
    c.increase_counter("subsection")
    print(c.evaluate('\\thesubsection'))
    c.increase_counter("part")
    print(c.evaluate("\\thepart"))
    c.increase_counter("section")
    print(c.evaluate('\\thesection'))
    c.increase_counter("subsection")
    print(c.evaluate('\\thesubsection'))
    c.increase_counter("subsection")
    print(c.evaluate('\\thesubsection'))
    c.increase_counter("part")
    print(c.evaluate("\\thepart"))
    c.increase_counter("section")
    print(c.evaluate('\\thesection'))
    c.increase_counter("subsection")
    print(c.evaluate('\\thesubsection'))
    c.increase_counter("subsection")
    print(c.evaluate('\\thesubsection'))

