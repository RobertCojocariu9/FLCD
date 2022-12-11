from .Grammar import Grammar


EPSILON = "epsilon"
PARSING_STATES = {
    "normal": "q",
    "back": "b",
    "final": "f",  # word is part of grammar
    "error": "e"  # word is not part of grammar
}


class RecursiveDescendent:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.state = PARSING_STATES["normal"]
        self.position = 1
        self.working_stack = [EPSILON]
        self.input_stack = [self.grammar.start_symbol]

    def expand(self):
        # WHEN: head of input stack is a nonterminal
        input_head = self.input_stack[0]

        if input_head in self.grammar.non_terminals:
            productions = self.grammar.productions[input_head]

            if not productions:
                # TODO: do something
                pass

            production = productions[0]

            if self.working_stack == [EPSILON]:
                self.working_stack = [production]
            else:
                self.working_stack.append(production)

            # Remove input_head from input stack
            self.input_stack = self.input_stack[1:]

            # Add production to the head of input stack
            self.input_stack = [*production, *self.input_stack]
        else:
            raise NotImplementedError

    def advance(self):
        pass

    def momentary_insuccess(self):
        pass

    def back(self):
        pass

    def another_try(self):
        pass

    def success(self):
        pass
