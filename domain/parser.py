from typing import List, Union
from collections import namedtuple

from .Grammar import Grammar


EPSILON = "epsilon"
PARSING_STATES = {
    "normal": "q",
    "back": "b",
    "final": "f",  # word is part of grammar
    "error": "e"  # word is not part of grammar
}


ProductionIndex = namedtuple("ProductionIndex", ["nonterminal", "index"])


class MomentaryInsuccess(Exception):
    pass


class Error(Exception):
    pass


class Parser:
    def __init__(self, grammar: Grammar, word: str):
        self.grammar = grammar
        self.state = PARSING_STATES["normal"]
        self.position = 1
        self.working_stack: List[Union[ProductionIndex, str]] = []
        self.input_stack = [self.grammar.start_symbol]
        self.word = word

    def parse(self):
        while self.state not in [PARSING_STATES["final"], PARSING_STATES["error"]]:
            if self.state == PARSING_STATES["normal"]:
                is_position_final = self.position == len(self.word) + 1
                # Check success
                if is_position_final and not self.input_stack:
                    self.success()
                    continue

                input_head = self.input_stack[0]
                if input_head in self.grammar.non_terminals:
                    self.expand()
                elif not is_position_final and input_head == self.word[self.position - 1]:
                    self.advance()
                else:
                    self.momentary_insuccess()

            elif self.state == PARSING_STATES["back"]:
                working_head = self.working_stack[-1]

                if isinstance(working_head, ProductionIndex):
                    symbol = working_head.nonterminal
                else:
                    symbol = working_head

                if symbol in self.grammar.terminals:
                    self.back()
                else:
                    self.another_try()
            else:
                raise NotImplementedError

        if self.state == PARSING_STATES["error"]:
            print("ERROR")
        else:
            print("Sequence accepted")

    def expand(self):
        # WHEN: head of input stack is a nonterminal
        print(f"Start expand...\n")
        input_head = self.input_stack[0]

        if input_head not in self.grammar.non_terminals:
            raise NotImplementedError

        productions = self.grammar.productions[input_head]

        if not productions:
            raise NotImplementedError

        production = productions[0]

        production_index = ProductionIndex(input_head, 1)
        print(f"Add {production_index} in working stack {self.working_stack}.")
        if not self.working_stack:
            self.working_stack = [production_index]
        else:
            self.working_stack.append(production_index)

        # Remove input_head from input stack
        print(f"Remove {input_head} from input stack {self.input_stack}.")
        self.input_stack = self.input_stack[1:]

        # Add production to the head of input stack
        print(f"Add production {production} to the head of {self.input_stack}.")
        self.input_stack = [*production, *self.input_stack]

        print("End expand...\n")

    def advance(self):
        # WHEN: head of input stack is a terminal = current symbol from input
        print(f"Start advance...\n")
        input_head = self.input_stack[0]

        if input_head not in self.grammar.terminals:
            raise NotImplementedError

        if input_head != self.word[self.position - 1]:
            print(f"Input head {input_head} not equal to current symbol from word {self.word}.")
            raise MomentaryInsuccess

        print(f"Adding input {input_head} to working stack {self.working_stack}.")
        self.working_stack.append(input_head)

        print(f"Deleting input head {input_head} from input stack {self.input_stack}.")
        self.input_stack = self.input_stack[1:]

        print(f"Increasing position to {self.position + 1}.")
        self.position += 1

        print("End advance...\n")

    def momentary_insuccess(self):
        print("Start momentary insuccess...\n")
        self.state = PARSING_STATES["back"]
        print("End momentary insuccess...\n")

    def _next_production(self) -> Union[List[str], None]:
        assert isinstance(self.working_stack[-1], ProductionIndex)

        nonterminal, production_index = self.working_stack[-1]

        productions = self.grammar.productions[nonterminal]

        if production_index == len(productions):
            return None

        return productions[production_index]

    def back(self):
        # WHEN: head of working stack is a terminal
        print("Start back...\n")
        assert self.state == PARSING_STATES["back"]
        working_head = self.working_stack[-1]

        if isinstance(working_head, ProductionIndex):
            symbol = working_head.nonterminal
        else:
            symbol = working_head

        if symbol not in self.grammar.terminals:
            raise NotImplementedError

        self.position -= 1

        self.input_stack = [working_head, *self.input_stack]

        self.working_stack.pop()

        print("End back...\n")

    def another_try(self):
        # WHEN: head of working stack is a nonterminal
        print(f"Start another_try...\n")
        assert self.state == PARSING_STATES["back"]

        working_head = self.working_stack[-1]

        if isinstance(working_head, ProductionIndex):
            symbol = working_head.nonterminal
        else:
            symbol = working_head

        if symbol not in self.grammar.non_terminals:
            raise NotImplementedError

        if self.position == 1 and symbol == self.grammar.start_symbol:
            self.state = PARSING_STATES["error"]
            raise Error

        next_production = self._next_production()
        nonterminal, production_index = self.working_stack[-1]
        production = self.grammar.productions[nonterminal][production_index - 1]

        if next_production is None:
            self.working_stack.pop()
            self.input_stack = [nonterminal, *self.input_stack[len(production):]]
            print(f"{nonterminal} has no next production.")
            print("End another try...\n")
            return

        self.state = PARSING_STATES["normal"]
        self.working_stack[-1] = ProductionIndex(nonterminal, production_index + 1)
        self.input_stack = [*next_production, *self.input_stack[len(production):]]

        print("End another try...\n")

    def success(self):
        print(f"Start success...\n")
        assert self.state == PARSING_STATES["normal"]

        if self.position != len(self.word) + 1 or self.input_stack:
            raise NotImplementedError

        self.state = PARSING_STATES["final"]

        print("End success...\n")
