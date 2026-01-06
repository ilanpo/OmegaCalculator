from typing import Generator, Union

from exceptions import InvalidNumberError, IllegalCharacterError


class LexerTypes:
    # token types
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    L_PAREN = 'L_PAREN'
    R_PAREN = 'R_PAREN'

    # binary and unary minus for special logic
    BINARY_MINUS = 'b-'
    UNARY_MINUS = 'u-'


def _read_number(expression: str, index: int) -> tuple[float, int]:
    """
    scans expression starting from given index for a number (can be a float with a '.')
    :param expression: string from which number is scanned
    :param index: index from which to start the scan
    :return: tuple with the number found and the index at which it ends, so we can continue from there
    """
    i = index
    length = len(expression)
    digit_start = i
    decimal = False

    while i < length:
        char = expression[i]

        if char.isdigit():
            i += 1
        elif char == '.':
            if decimal:
                raise InvalidNumberError(f"[ERROR] number at index {digit_start} has multiple dots")
            decimal = True
            i += 1
        else:
            break

    try:
        value = float(expression[digit_start:i])
        return value, i
    except ValueError:
        raise InvalidNumberError(f"[ERROR] failed to read number, invalid number format at index {index}")


def _normalize(expression: str) -> str:
    """
    replaces spaces and tabs with nothing
    :param expression: string to normalize
    :return: normalized expression as string
    """
    return expression.replace(" ", "").replace("\t", "")


def _decide_minus_type(prev_token: str) -> str:
    """
    decides if this token is a binary or unary minus based on previous token
    :param prev_token: previous item in expression, whether number operator or parentheses
    :return: either the symbol for a binary minus or the symbol for a unary minus
    """
    if prev_token in [LexerTypes.NUMBER, LexerTypes.R_PAREN]:
        return LexerTypes.BINARY_MINUS
    return LexerTypes.UNARY_MINUS


class Lexer:
    L_PARENTHESES = ['(']
    R_PARENTHESES = [')']
    PARENTHESES = L_PARENTHESES + R_PARENTHESES

    def __init__(self, operator_registry):
        self.operator_registry = operator_registry

    def tokenize(self, expression: str) -> Generator[Union[str, float]]:
        """
        translates the expression to tokens of either a string if it's an operator/parentheses or float if it's a number
        :param expression: string containing expression to tokenize
        :return: string if it's an operator/parentheses or float if it's a number
        """
        expression = _normalize(expression)
        operators = self.operator_registry.get_all_operands()
        i = 0
        length = len(expression)
        prev_token = None

        while i < length:
            char = expression[i]

            if char == '-':
                if prev_token is None:
                    yield LexerTypes.UNARY_MINUS
                else:
                    yield _decide_minus_type(prev_token)

                prev_token = 'OPERATOR'

                i += 1
                continue

            if char.isdigit():
                number, new_i = _read_number(expression, i)
                yield number

                prev_token = 'NUMBER'

                i = new_i
                continue

            if char in operators or char in self.PARENTHESES:
                if char in self.L_PARENTHESES:
                    yield '('
                    prev_token = LexerTypes.L_PAREN
                elif char in self.R_PARENTHESES:
                    yield ')'
                    prev_token = LexerTypes.R_PAREN
                else:
                    yield char
                    prev_token = LexerTypes.OPERATOR

                i += 1
                continue

            raise IllegalCharacterError(f"[ERROR] illegal character {char} at index {i}")
