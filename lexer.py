from typing import Generator, Union

from exceptions import InvalidNumberError, IllegalCharacterError, UnaryMishandleError, NegationError


class TokenTypes:
    # token types
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    L_PAREN = 'L_PAREN'
    R_PAREN = 'R_PAREN'
    UNARY_MINUS = 'U_MINUS'


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


class Lexer:
    L_PARENTHESES = ['(']
    R_PARENTHESES = [')']
    PARENTHESES = L_PARENTHESES + R_PARENTHESES

    def __init__(self, operator_registry, binary_minus: str, unary_minus: str, sign_minus: str):
        self.operator_registry = operator_registry
        self.binary_minus = binary_minus
        self.unary_minus = unary_minus
        self.sign_minus = sign_minus

    def tokenize(self, expression: str) -> Generator[Union[str, float], None, None]:
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
                    yield self.unary_minus
                    prev_token = TokenTypes.OPERATOR
                else:
                    minus_type, token_type = self._decide_minus_type(prev_token)
                    yield minus_type
                    prev_token = TokenTypes.UNARY_MINUS

                i += 1
                continue

            if char.isdigit():
                number, new_i = _read_number(expression, i)
                yield number

                prev_token = TokenTypes.NUMBER

                i = new_i
                continue

            if char in operators or char in self.PARENTHESES:
                if char in self.L_PARENTHESES:
                    yield '('
                    prev_token = TokenTypes.L_PAREN
                elif char in self.R_PARENTHESES:
                    yield ')'
                    prev_token = TokenTypes.R_PAREN
                else:
                    if prev_token == TokenTypes.UNARY_MINUS:
                        raise UnaryMishandleError(f"[ERROR] incorrect unary minus at index {i - 1}")
                    yield char
                    if char == '~':
                        prev_token = TokenTypes.UNARY_MINUS
                    else:
                        prev_token = TokenTypes.OPERATOR

                i += 1
                continue

            raise IllegalCharacterError(f"[ERROR] illegal character {char} at index {i}")

    def _decide_minus_type(self, prev_token: str) -> tuple[str, str]:
        """
        decides if this token is a binary, unary or sign minus based on previous token
        :param prev_token: previous item in expression, whether number operator or parentheses
        :return: either the symbol for a binary minus or the symbol for a unary minus
        """
        if prev_token in [TokenTypes.NUMBER, TokenTypes.R_PAREN]:
            return self.binary_minus, TokenTypes.OPERATOR
        if prev_token in [TokenTypes.OPERATOR, TokenTypes.UNARY_MINUS]:
            return self.sign_minus, TokenTypes.UNARY_MINUS
        return self.unary_minus, TokenTypes.UNARY_MINUS

