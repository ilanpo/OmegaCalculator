from typing import Generator, Union
from abc import ABC, abstractmethod
from exceptions import InvalidNumberError, IllegalCharacterError, UnaryMishandleError, PlacementError


class TokenTypes:
    # token types
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    L_PAREN = 'L_PAREN'
    R_PAREN = 'R_PAREN'
    UNARY_MINUS = 'U_MINUS'


LEFT_PLACED = "left_of_value"
BINARY = "between_values"
RIGHT_PLACED = "right_of_value"

L_PARENTHESES = ['(']
R_PARENTHESES = [')']
PARENTHESES = L_PARENTHESES + R_PARENTHESES


def _normalize(expression: str) -> str:
    """
    replaces spaces and tabs with nothing
    :param expression: string to normalize
    :return: normalized expression as string
    """
    return expression.replace(" ", "").replace("\t", "")


class ExpressionInfo:
    def __init__(self, expression: str):
        self.expression = _normalize(expression)
        self.length = len(self.expression)
        self.index = 0
        self.prev_token = None

    def current_char(self) -> Union[str, None]:
        """
        if were not outside the bounds of the expression returns the current char were on
        :return: char were on
        """
        if self.index < self.length:
            return self.expression[self.index]
        return None

    def next(self, jump: int = 1):
        """
        advances the index in the expression by jump, defaults to 1
        :param jump: steps to move forward
        """
        self.index += jump


class TokenHandler(ABC):
    @abstractmethod
    def can_handle(self, info: ExpressionInfo) -> bool:
        pass

    @abstractmethod
    def handle(self, info: ExpressionInfo) -> Generator[Union[str, float], None, None]:
        pass


class MinusHandler(TokenHandler):

    def __init__(self, binary_minus: str, unary_minus: str, sign_minus: str):
        self.binary_minus = binary_minus
        self.unary_minus = unary_minus
        self.sign_minus = sign_minus

    def can_handle(self, info: ExpressionInfo) -> bool:
        """
        :param info: info object of expression
        :return: whether current char were on can be handled by this handler
        """
        return info.current_char() == '-'

    def handle(self, info: ExpressionInfo) -> Generator[Union[str, float], None, None]:
        """
        yields appropriate value depending on the current char were on in the expression
        :param info: info object of expression
        :return: type of minus it is, can be binary, unary, or sign
        """
        if info.prev_token is None:
            try:
                if info.expression[info.index + 1] == "-":
                    yield self.sign_minus
                else:
                    yield self.unary_minus
            except IndexError:
                raise UnaryMishandleError(f"[ERROR] incorrect unary minus at index {info.index}")
            info.prev_token = TokenTypes.UNARY_MINUS
            info.next()
        else:
            if info.prev_token in [TokenTypes.NUMBER, TokenTypes.R_PAREN]:
                info.prev_token = TokenTypes.OPERATOR
                yield self.binary_minus
            elif info.prev_token in [TokenTypes.OPERATOR, TokenTypes.UNARY_MINUS, TokenTypes.L_PAREN]:
                info.prev_token = TokenTypes.UNARY_MINUS
                yield self.sign_minus
            else:
                info.prev_token = TokenTypes.UNARY_MINUS
                yield self.unary_minus
            info.next()


class ValueHandler(TokenHandler):
    def can_handle(self, info: ExpressionInfo) -> bool:
        """
        :param info: info object of expression
        :return: whether current char were on can be handled by this handler
        """
        char = info.current_char()
        if char is not None and char.isdigit():
            return True
        return False

    def handle(self, info: ExpressionInfo) -> Generator[Union[str, float], None, None]:
        """
        yields appropriate value depending on the current char were on in the expression,
        this advances multiple chars because it reads the whole number
        :param info: info object of expression
        :return: the value of the number were on
        """
        digit_start = info.index
        decimal = False

        while info.index < info.length:
            char = info.expression[info.index]

            if char.isdigit():
                info.next()
            elif char == '.':
                if decimal:
                    raise InvalidNumberError(f"[ERROR] number at index {digit_start} has multiple dots")
                decimal = True
                info.next()
            else:
                break

        try:
            value = float(info.expression[digit_start:info.index])
            info.prev_token = TokenTypes.NUMBER
            yield value
        except ValueError:
            raise InvalidNumberError(f"[ERROR] failed to read number, invalid number format at index {info.index}")


class OperatorHandler(TokenHandler):
    def __init__(self, operator_registry):
        self.operator_registry = operator_registry
        self.operators = operator_registry.get_all_operands()

    def can_handle(self, info: ExpressionInfo) -> bool:
        """
        :param info: info object of expression
        :return: whether current char were on can be handled by this handler
        """
        return info.current_char() in self.operators or info.current_char() in PARENTHESES

    def handle(self, info: ExpressionInfo) -> Generator[Union[str, float], None, None]:
        """
        yields appropriate value depending on the current char were on in the expression
        :param info: info object of expression
        :return: type of operator currently handled, can be anything in the registry
        """
        char = info.current_char()

        if char in L_PARENTHESES:
            yield '('
            info.prev_token = TokenTypes.L_PAREN
            info.next()
            return
        elif char in R_PARENTHESES:
            yield ')'
            info.prev_token = TokenTypes.R_PAREN
            info.next()
            return

        self._handle_operator_token(info, char)

        if char == "~":
            info.prev_token = TokenTypes.UNARY_MINUS
        elif self.operator_registry.get_operator(char).placement_rules == RIGHT_PLACED:
            info.prev_token = TokenTypes.NUMBER
        else:
            info.prev_token = TokenTypes.OPERATOR

        yield char
        info.next()

    def _handle_operator_token(self, info: ExpressionInfo, char: str):
        """
        checks for whether the rules describing an operators placement are followed
        :param info: lexer info object
        :param char: symbol of operator
        :return: nothing, only raises errors if something's wrong
        """
        if info.prev_token == TokenTypes.UNARY_MINUS:
            raise UnaryMishandleError(f"[ERROR] incorrect negation at index {info.index - 1}")

        op_placement = self.operator_registry.get_operator(char).placement_rules

        prev_is_value = info.prev_token in [TokenTypes.NUMBER, TokenTypes.R_PAREN]

        if op_placement in ["right_of_value", "between_values"] and not prev_is_value:
            raise PlacementError(f"[ERROR] operand {char} placed in incorrect location {info.index}")
        if op_placement == "left_of_value" and prev_is_value:
            raise PlacementError(f"[ERROR] operand {char} placed in incorrect location {info.index}")


class Lexer:
    def __init__(self, operator_registry, binary_minus: str, unary_minus: str, sign_minus: str):
        self.handlers = [
            MinusHandler(binary_minus, unary_minus, sign_minus),
            ValueHandler(),
            OperatorHandler(operator_registry)
        ]

    def tokenize(self, expression: str) -> Generator[Union[str, float], None, None]:
        """
        translates the expression to tokens of either a string if it's an operator/parentheses or float if it's a number
        :param expression: string containing expression to tokenize
        :return: yields string if it's an operator/parentheses or float if it's a number
        """
        info = ExpressionInfo(expression)

        while info.index < info.length:
            handled = False

            for handler in self.handlers:
                if handler.can_handle(info):
                    yield from handler.handle(info)
                    handled = True
                    break

            if not handled:
                raise IllegalCharacterError(f"[ERROR] illegal character {info.current_char()} at index {info.index}")
