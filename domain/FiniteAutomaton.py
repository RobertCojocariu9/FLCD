class FiniteAutomaton:
    def __init__(self, path):
        self.__transitions = dict()
        self.__accessible = dict(list())
        file = open(path, "r")
        lines = file.readlines()
        self.__states = lines[0].strip().split()
        self.__alphabet = lines[1].strip().split()
        self.__initial = lines[2].strip()
        self.__final = lines[3].strip().split()
        for state in self.__states:
            self.__accessible[state] = []
        for i in range(4, len(lines)):
            transition = lines[i].strip().split()
            self.__transitions[(transition[0], transition[1])] = transition[2:]
            self.__accessible[transition[0]].append(transition[1])
        file.close()

    def check_sequence(self, sequence, current):
        if not len(sequence):
            return current in self.__final
        for state in self.__accessible[current]:
            if sequence[0] in self.__transitions[(current, state)]:
                return self.check_sequence(sequence[1:], state)
        return False

    def menu(self):
        # while True:
        #     print("1. States\n"
        #           "2. Alphabet\n"
        #           "3. Transitions\n"
        #           "4. Initial state\n"
        #           "5. Final states\n"
        #           "6. Check sequence\n"
        #           "0. Exit\n")
        #     option = input(">")
        #     match option:
        #         case "1":
        #             print("States: " + str(self.__states))
        #         case "2":
        #             print("Alphabet: " + str(self.__alphabet))
        #         case "3":
        #             print("Transitions: " + str(self.__transitions))
        #         case "4":
        #             print("Initial state: " + str(self.__initial))
        #         case "5":
        #             print("Final states: " + str(self.__final))
        #         case "6":
        #             sequence = input("Give sequence: ")
        #             print("The sequence " +
        #                   ("is " if self.check_sequence(sequence, self.__initial) else "is not ")
        #                   + "accepted by the current FA")
        #         case "0":
        #             exit(0)
        #         case _:
        #             print("Invalid command")
        pass


if __name__ == '__main__':
    fa = FiniteAutomaton('integers.in')
    fa.menu()
