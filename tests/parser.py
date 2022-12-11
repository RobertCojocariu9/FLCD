import unittest

from domain import Parser, Grammar
from domain.parser import PARSING_STATES, ProductionIndex, MomentaryInsuccess, Error


def set_up():
    grammar = Grammar("../inputs/g3.txt")
    word = "aacbc"
    parser = Parser(grammar, word)
    return grammar, word, parser


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_init(self):
        self.assertEqual('S', self.grammar.start_symbol)

        self.assertEqual(self.parser.grammar, self.grammar)
        self.assertEqual(self.parser.state, PARSING_STATES["normal"])
        self.assertEqual(self.parser.position, 1)
        self.assertEqual(self.parser.word, self.word)
        self.assertEqual(self.parser.working_stack, [])
        self.assertEqual(self.parser.input_stack, [self.grammar.start_symbol])


class TestExpand(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_initial_expand(self):
        parser = self.parser

        parser.expand()

        nonterminal, index = parser.working_stack[-1]
        production = self.grammar.productions[nonterminal][index - 1]

        self.assertEqual(production, ['a', 'S', 'b', 'S'])

        self.assertEqual(len(parser.working_stack), 1)
        self.assertEqual(nonterminal, self.grammar.start_symbol)
        self.assertEqual(index, 1)
        self.assertEqual(parser.input_stack, production)

    def test_input_head_is_terminal(self):
        parser = self.parser
        parser.input_stack = 'a'

        with self.assertRaises(NotImplementedError):
            parser.expand()

    def test_expand(self):
        parser = self.parser

        parser.position = 2
        parser.working_stack = [ProductionIndex('S', 1), 'a']
        parser.input_stack = ['S', 'b', 'S']

        parser.expand()

        self.assertEqual(
            parser.working_stack,
            [ProductionIndex('S', 1), 'a', ProductionIndex('S', 1)]
        )
        self.assertEqual(parser.input_stack, ['a', 'S', 'b', 'S', 'b', 'S'])


class TestAdvance(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_advance(self):
        self.parser.expand()
        self.parser.advance()

        self.assertEqual(self.parser.position, 2)
        self.assertEqual(
            self.parser.working_stack, [ProductionIndex('S', 1), 'a']
        )
        self.assertEqual(self.parser.input_stack, ['S', 'b', 'S'])

    def test_input_head_is_non_terminal(self):
        with self.assertRaises(NotImplementedError):
            self.parser.advance()

    def test_input_head_is_not_in_word(self):
        self.parser.word = "cbc"

        self.parser.expand()

        with self.assertRaises(MomentaryInsuccess):
            self.parser.advance()


class TestMomentaryInsuccess(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_momentary_insuccess(self):
        self.parser.momentary_insuccess()
        self.assertEqual(self.parser.state, PARSING_STATES["back"])


class TestBack(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_back(self):
        self.parser.position = 6
        working_stack = [
            ProductionIndex('S', 1),
            'a',
            ProductionIndex('S', 1),
            'a',
            ProductionIndex('S', 3),
            'c',
            'b',
            ProductionIndex('S', 3),
            'c'
        ]
        self.parser.working_stack = [*working_stack]
        self.parser.input_stack = ['b', 'S']

        self.parser.momentary_insuccess()

        self.parser.back()

        self.assertEqual(self.parser.position, 5)
        self.assertEqual(self.parser.working_stack, working_stack[:-1])

        self.assertEqual(self.parser.input_stack, ['c', 'b', 'S'])

    def test_working_head_is_non_terminal(self):
        self.parser.expand()

        self.parser.momentary_insuccess()

        with self.assertRaises(NotImplementedError):
            self.parser.back()


class TestAnotherTry(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_next_production_method_none(self):
        self.parser.working_stack = [ProductionIndex('S', 3)]

        production = self.parser._next_production()

        self.assertIsNone(production)

    def test_next_production_method(self):
        self.parser.working_stack = [ProductionIndex('S', 2)]

        production = self.parser._next_production()

        self.assertEqual(production, ['c'])

    def test_working_head_is_non_terminal(self):
        self.parser.working_stack = ['c']
        self.parser.state = PARSING_STATES["back"]

        with self.assertRaises(NotImplementedError):
            self.parser.another_try()

    def test_error_state(self):
        self.parser.expand()
        self.parser.state = PARSING_STATES["back"]

        with self.assertRaises(Error):
            self.parser.another_try()

        self.assertEqual(self.parser.state, PARSING_STATES["error"])

    def test_next_production_none(self):
        self.parser.position = 3
        working_stack = [
            ProductionIndex('S', 1),
            'a',
            ProductionIndex('S', 1),
            'a',
            ProductionIndex('S', 3)
        ]
        self.parser.working_stack = [*working_stack]
        self.parser.input_stack = ['c', 'b', 'S', 'b', 'S']
        self.parser.state = PARSING_STATES["back"]

        self.parser.another_try()

        self.assertEqual(self.parser.working_stack, working_stack[:-1])
        self.assertEqual(self.parser.input_stack, ['S', 'b', 'S', 'b', 'S'])

    def test_with_next_production(self):
        self.parser.position = 5

        working_stack = [
            ProductionIndex('S', 1),
            'a',
            ProductionIndex('S', 1),
            'a',
            ProductionIndex('S', 3),
            'c',
            'b',
            ProductionIndex('S', 1)
        ]
        self.parser.working_stack = working_stack

        self.parser.input_stack = ['a', 'S', 'b', 'S', 'b', 'S']

        self.parser.state = PARSING_STATES["back"]

        self.parser.another_try()

        self.assertEqual(self.parser.working_stack, [
            *working_stack[:-1],
            ProductionIndex('S', 2)
        ])

        self.assertEqual(self.parser.input_stack, ['a', 'S', 'b', 'S'])


class TestSuccess(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar, self.word, self.parser = set_up()

    def test_success(self):
        self.parser.position = 6
        self.parser.input_stack = []

        self.parser.success()

        self.assertEqual(self.parser.state, PARSING_STATES["final"])
