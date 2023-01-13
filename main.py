from domain import Grammar, Parser, ParserOutput
from domain.parser import Error


def get_sequence(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    sequence = []

    for line in lines:
        elements = line.split("|")
        if elements[0] != 'TOKEN':
            sequence.append(elements[0])

    return "".join(sequence)


if __name__ == "__main__":
    grammar = Grammar("./inputs/g2.txt")
    word = get_sequence("./inputs/pif.txt")
    output_file = "./outputs/error.out"
    try:
        parser = Parser(grammar, word)

        parser.parse()
        parser_output = ParserOutput(parser=parser, output_file=output_file)
    except Error:
        file = open(output_file, "w")
        file.write(f"Sequence {word} not accepted!")
        file.close()
