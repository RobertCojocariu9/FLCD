import re

from SymbolTable import SymbolTable


def check_part(char):
    return re.search("[a-zA-z0-9+-]", char)


def check_id(char):
    return re.search("^[a-zA-z]*$", char)


def check_char(char):
    return re.search("^'[a-zA-z0-9]'$", char)


def check_string(char):
    return re.search("^\"[a-zA-z0-9 ]*\"$", char)


def check_integer(char):
    return re.search("^[-+]?[0-9]+$", char)


def check_boolean(char):
    return re.search("^0|1$", char)


def check_cons(char):
    return check_char(char) or check_string(char) or check_integer(char) or check_boolean(char)


class Scanner:
    def __init__(self):
        self.__st_identifiers = SymbolTable(50)
        self.__st_constants = SymbolTable(50)
        self.__pif = []
        self.__multiple_part_tokens = {
            "<": ["-", "="],
            ">": ["="],
            "!": ["="],
            "&": ["&"],
            "|": ["|"],
            "\\": ["n", "t"]
        }
        with open("token.in", "r") as file:
            self.__tokens = []
            for line in file:
                line = line[:-1] if line[-1] == "\n" else line
                self.__tokens.append(line)

    def parse_line(self, line):
        formatted_line = []
        i = 0
        while i < len(line):  # parse for chars, digits and separators
            if check_part(line[i]):  # char or digit
                if line[i] == "+" or line[i] == "-":  # +/- can be used as an addition or as a sign
                    if i != len(line) - 1 and line[i + 1] != " ":  # if sign
                        formatted_line.append(line[i])
                    else:  # if addition
                        formatted_line.append(" ")
                        formatted_line.append(line[i])
                        formatted_line.append(" ")
                else:
                    formatted_line.append(line[i])
            else:  # separator
                if line[i] != " ":  # discard spaces
                    formatted_line.append(" ")
                    formatted_line.append(line[i])
                    formatted_line.append(" ")
                else:
                    formatted_line.append(" ")
            i += 1
        line = "".join(formatted_line).split()
        formatted_line = []
        i = 0
        while i < len(line):  # check for multiple part tokens
            if line[i] in self.__multiple_part_tokens:  # found first part
                values = self.__multiple_part_tokens[line[i]]
                if i != len(line) - 1 and line[i + 1] in values:  # found second part
                    formatted_line.append(line[i] + line[i + 1])
                    i += 1
                else:  # no second part => single part token
                    formatted_line.append(line[i])
            else:  # not a multiple part start => other token
                formatted_line.append(line[i])
            i += 1
        line = formatted_line
        formatted_line = []
        current_sep = ""
        i = 0
        while i < len(line):  # add " and ' to strings/chars
            if line[i] == "\"" or line[i] == "\'":  # found separator
                if current_sep == " ":  # starting separator
                    current_sep = line[i]
                else:  # ending separator
                    if current_sep == line[i]:  # extra check
                        formatted_line.append(current_sep + line[i - 1] + line[i])
            else:  # found constant val
                if current_sep != " ":  # no sep selected
                    formatted_line.append(line[i])
                else:
                    continue  # case covered above
            i += 1
        return formatted_line

    def scan(self, path):
        with open(path, "r") as file:
            line_nr = 0
            for line in file:
                line_nr += 1
                tokens = self.parse_line(line)
                for token in tokens:
                    if token in self.__tokens:
                        self.__pif.append((token, -1))
                    elif check_id(token):
                        pos = self.__st_identifiers.add(token)
                        self.__pif.append((token, pos))
                    elif check_cons(token):
                        pos = self.__st_constants.add(token)
                        self.__pif.append((token, pos))
                    else:
                        raise Exception("Lexical error on line " + str(line_nr) + " , unidentified token: " + token)
                line_nr += 1
            print("Lexically correct")

    def dump(self, path):
        with open("PIF_" + path + ".out", "w") as file:
            file.write("Token - Position\n")
            for elem in self.__pif:
                file.write(elem[0] + " - " + str(elem[1]) + "\n")
        with open("STConstants_" + path + ".out", "w") as file:
            file.write(str(self.__st_constants))
        with open("STIdentifiers_" + path + ".out", "w") as file:
            file.write(str(self.__st_identifiers))

