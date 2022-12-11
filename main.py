from domain import Grammar, Parser


if __name__ == "__main__":
    grammar = Grammar("./inputs/g3.txt")
    word = "aacbc"
    parser = Parser(grammar, word)

    parser.parse()
