from collections import deque


class SymbolTable:
    def __init__(self, size):
        self.__size = size
        self.__next_position = 0
        self.__table = [deque() for _ in range(size)]

    def __h(self, item):
        sum_ascii = 0
        for char in str(item):
            sum_ascii += ord(char)
        return sum_ascii % self.__size

    def add(self, item):
        elem = self.search(item)
        if elem == -1:
            hashed = self.__h(item)
            elem = self.__next_position
            self.__table[hashed].append((item, self.__next_position))
            self.__next_position += 1
        return elem

    def search(self, item):
        for elem in self.__table[self.__h(item)]:
            if elem[0] == str(item):
                return elem[1]
        return -1

    def __str__(self):
        msg = "Token - Position\n"
        elems = ["" for _ in range(self.__next_position)]
        for bucket in self.__table:
            for elem in bucket:
                elems[elem[1]] = elem[0]
        for i in range(self.__next_position):
            msg += elems[i] + " | " + str(i) + "\n"
        return msg
