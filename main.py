from domain import Grammar, Parser, ParserOutput
from domain.parser import Error


if __name__ == "__main__":
    grammar = Grammar("./inputs/g1.txt")
    word = "xaaacbc"
    output_file = "./outputs/error.out"
    try:
        parser = Parser(grammar, word)

        parser.parse()
        parser_output = ParserOutput(parser=parser, output_file=output_file)
    except Error:
        file = open(output_file, "w")
        file.write(f"Sequence {word} not accepted!")
        file.close()

