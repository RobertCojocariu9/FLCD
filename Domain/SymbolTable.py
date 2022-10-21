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
            self.__table[hashed].append((str(item), self.__next_position))
            self.__next_position += 1
        return elem

    def search(self, item):
        for elem in self.__table[self.__h(item)]:
            if elem[0] == str(item):
                return elem[1]
        return -1

    def __str__(self):
        msg = ""
        for i in range(self.__size):
            msg += "Bucket {}: {}\n".format(i, self.__table[i])
        return msg


"""
if __name__ == "__main__":
    ST = SymbolTable(5)
    ST.add("test")
    print(ST)
    ST.add("testing")
    print(ST)
    ST.add(3)
    print(ST)
    ST.add(8)
    print(ST)
    ST.add("testing")
    print(ST)
"""
