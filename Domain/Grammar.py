def print_menu():
    print('1. Non-terminals\n'
          '2. Terminals\n'
          '3. Starting symbol\n'
          '4. Productions\n'
          '5. Productions for a given non-terminal\n'
          '6. CFG check\n'
          '0. Quit\n')


class Grammar:
    def __init__(self, file_name):
        self.__non_terminals = list()
        self.__terminals = list()
        self.__productions = dict()
        self.__start_symbol = None
        self.read_from_file(file_name)

    def read_from_file(self, file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
            self.__non_terminals = lines[0].strip().split(',')
            self.__terminals = lines[1].strip().split(',')
            self.__start_symbol = lines[2]
            for index in range(3, len(lines)):
                elements = lines[index].strip().split('->')
                assert len(elements) == 2, elements
                lhs, rhs = elements
                self.__productions[lhs] = [production.split('.') for production in rhs.split(",")]

    def check_cfg(self):
        for symbol in self.__productions:
            if "," in symbol or symbol not in self.__non_terminals:
                print(symbol)
                return False
        return True

    def menu(self):
        while True:
            print_menu()
            option = input(">")
            if option == '1':
                print(str(self.__non_terminals))
            elif option == '2':
                print(str(self.__terminals))
            elif option == '3':
                print(str(self.__start_symbol))
            elif option == '4':
                to_print = ""
                for symbol in self.__productions:
                    productions_for_symbol = self.__productions[symbol]
                    to_print += symbol.replace(",", " ") + " -> "
                    for production in productions_for_symbol:
                        to_print += ''.join(production) + " | "
                    to_print = to_print[:-2]
                    to_print += "\n"
                print(to_print)
            elif option == '5':
                symbol = input('Give non-terminal: ')
                to_print = ""
                try:
                    productions_for_symbol = self.__productions[symbol]
                    for production in productions_for_symbol:
                        to_print += symbol + " -> " + ' '.join(production) + "\n"
                    print(to_print)
                except KeyError:
                    print("Invalid non-terminal")
            elif option == '6':
                result = self.check_cfg()
                print('The given grammar ' + ("is" if result else "is not") + ' a cfg')

            elif option == '0':
                exit(0)
            else:
                print("Invalid option")


if __name__ == "__main__":
    grammar = Grammar("g2.txt")
    grammar.menu()
