from typing import List, Tuple, Union
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


class RecursiveDescendent:
    def __init__(self, grammar: Grammar, word: str):
        self.grammar = grammar
        self.state = PARSING_STATES["normal"]
        self.position = 1
        self.working_stack: List[ProductionIndex] = []
        self.input_stack = [self.grammar.start_symbol]
        self.word = word

    def expand(self):
        # WHEN: head of input stack is a nonterminal
        print("Start expand...")
        input_head = self.input_stack[0]

        if input_head not in self.grammar.non_terminals:
            raise NotImplementedError

        productions = self.grammar.productions[input_head]

        if not productions:
            # TODO: do something
            pass

        production = productions[0]

        print(f"Add {production} in working stack {self.working_stack}.")
        production_index = ProductionIndex(input_head, 1)
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

        print("End expand...")

    def advance(self):
        # WHEN: head of input stack is a terminal = current symbol from input
        print("Start advance...")
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

        print("End advance...")

    def momentary_insuccess(self):
        print("Start momentary insuccess...")
        self.state = PARSING_STATES["back"]
        print("End momentary insuccess...")

    def _next_production(self) -> Union[List[str], None]:
        nonterminal, production_index = self.working_stack[-1]

        productions = self.grammar.productions[nonterminal]

        if production_index == len(productions) - 1:
            return None

        return productions[production_index + 1]

    def back(self):
        # WHEN: head of working stack is a terminal
        print("Start back...")
        working_head = self.working_stack[-1]

        if working_head not in self.grammar.terminals:
            raise NotImplementedError

        self.position -= 1

        self.input_stack = [working_head, *self.input_stack]

        self.working_stack = self.working_stack[1:]

        print("End back...")

    def another_try(self):
        # WHEN: head of working stack is a nonterminal
        print("Start another_try...")

        working_head = self.working_stack[-1]

        if working_head not in self.grammar.terminals:
            raise NotImplementedError

        if self.position == 1 and working_head == self.grammar.start_symbol:
            self.state = PARSING_STATES["error"]
            raise Error

        next_production = self._next_production()
        nonterminal, production_index = self.working_stack.pop()

        if next_production is None:

            self.input_stack = [nonterminal, *self.input_stack]
            return

        self.state = PARSING_STATES["normal"]
        self.working_stack[-1] = ProductionIndex(nonterminal, production_index + 1)
        self.input_stack = [*next_production, *self.input_stack]

        print("End another try...")

    def success(self):
        print("Start success...")

        if self.position != len(self.word) + 1 or not self.input_stack:
            raise NotImplementedError

        self.state = PARSING_STATES["final"]

        print("End success...")
