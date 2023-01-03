from typing import List, NamedTuple

from .parser import Parser, ProductionIndex


class TableRow(NamedTuple):
    index: int
    info: str
    parent: int
    left_sibling: int

    def __str__(self):
        return f"{self.index}|{self.info}|{self.parent}|{self.left_sibling}\n"


class StackItem(NamedTuple):
    production_index: ProductionIndex
    index: int


class ParserOutput:
    def __init__(self, parser: Parser, output_file: str):
        self.parser = parser
        self.working_stack = parser.working_stack
        self.table: List[TableRow] = []
        self.index = 1
        self.stack: List[StackItem] = []
        self.carryover = 0
        self.output_file = output_file

        self.create_tree()
        self.save_tree()

    def __str__(self):
        s = 'Index | Info | Parent | Left sibling\n'

        rows = sorted(self.table, key=lambda a: a.index)

        for row in rows:
            s += str(row)

        return s

    def _get_and_increment(self):
        index = self.index

        self.index += 1
        return index

    def save_tree(self):
        file = open(self.output_file, "w")
        file.write(str(self))
        file.close()

    def _create_tree(self, production_index: ProductionIndex, parent_index: int, next_index: int):
        working_stack = self.working_stack

        production = self.parser.grammar.productions[production_index.nonterminal][
            production_index.index - 1
        ]

        left_sibling = 0
        index = next_index
        first_nonterminal = True
        for i, symbol in enumerate(production):
            if symbol in self.parser.grammar.terminals:
                self.table.append(
                    TableRow(index=index, info=symbol, parent=parent_index, left_sibling=left_sibling)
                )
                assert symbol == working_stack[0]
                working_stack.pop(0)
                left_sibling = index
                index += 1
            else:
                production_index: ProductionIndex = working_stack[0]
                self.table.append(
                    TableRow(
                        index=index, info=production_index.nonterminal, left_sibling=left_sibling, parent=parent_index
                    )
                )
                left_sibling = index
                index += 1
                working_stack.pop(0)

                next_index = index + len(production) - i - 1
                if first_nonterminal:
                    self.carryover += len(
                        self.parser.grammar.productions[production_index.nonterminal][production_index.index - 1]
                    )
                    first_nonterminal = False
                else:
                    next_index += self.carryover
                    self.carryover = 0

                self._create_tree(
                    production_index=production_index,
                    parent_index=index - 1,
                    next_index=next_index
                )

    def create_tree(self):
        working_stack = self.working_stack
        root = working_stack.pop(0)

        self.table.append(TableRow(index=self._get_and_increment(), info=root.nonterminal, parent=0, left_sibling=0))
        self._create_tree(
            production_index=root,
            parent_index=1,
            next_index=2
        )
