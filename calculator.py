from operands import *
from lexer import Lexer
from parser import Parser
from solver import Solver

LEFT_FACING = "left"
RIGHT_FACING = "right"

LEFT_PLACED = "left_of_value"
BINARY = "between_values"
RIGHT_PLACED = "right_of_value"

BINARY_MINUS = 'b-'
UNARY_MINUS = 'u-'
SIGN_MINUS = 's-'


def setup_registry() -> OperatorRegistry:
    """
    registers all operators to the registry so calculator recognises them
    :return: OperatorRegistry object
    """
    registry = OperatorRegistry()

    registry.register(Add('+', 1))
    registry.register(Subtract(BINARY_MINUS, 1))

    registry.register(Multiply('*', 2))
    registry.register(Divide('/', 2))

    registry.register(UnaryMinus(UNARY_MINUS, 3, RIGHT_PLACED))

    registry.register(Power('^', 4, LEFT_FACING))

    registry.register(Modulo('%', 5))

    registry.register(Maximum('$', 6))
    registry.register(Minimum('&', 6))
    registry.register(Average('@', 6))

    registry.register(Factorial('!', 7, RIGHT_PLACED))
    registry.register(Negate('~', 7, LEFT_PLACED))
    registry.register(DigitSum('#', 7, RIGHT_PLACED))

    registry.register(UnaryMinus(SIGN_MINUS, 8, LEFT_PLACED))

    return registry


class Calculator:
    def __init__(self):
        self.registry = setup_registry()
        self.lexer = Lexer(self.registry, BINARY_MINUS, UNARY_MINUS, SIGN_MINUS)
        self.parser = Parser(self.registry)
        self.solver = Solver(self.registry)

    def calculate(self, user_input) -> float:
        """
        converts input into tokens then puts the into a queue in postfix order and then solves the expression
        :param user_input: mathematical expression as string
        :return: result as float
        """
        try:
            tokens = self.lexer.tokenize(user_input)

            postfix_q = self.parser.parse(tokens)

            result = self.solver.solve(postfix_q)
            return result
        except Exception as e:
            raise e
