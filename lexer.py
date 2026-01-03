from typing import Tuple


class Lexer:

    def __init__(self, operator_registry):
        self.operator_registry = operator_registry

    def normalize(self, expression: str) -> str:
        return expression.replace(" ", "").replace("\t", "")

    def read_number(self, expression: str, index: int) -> tuple[None, int] | tuple[float, int]:
        i = index
        length = len(expression)
        minus_sum = 0

        while i < length and expression[i] == '-':
            minus_sum += 1
            i += 1

        digit_start = i
        decimal = False

        while i < length:
            char = expression[i]

            if char.isdigit():
                i += 1
            elif char == '.':
                if decimal:
                    raise ValueError(f"[ERROR] failed to read number, number at index {digit_start} has multiple dots")
                decimal = True
                i += 1
            else:
                break

        if i == digit_start:  # if not number then return None, index, most likely unary - to be handled as an operator.
            return None, index

        number_str = expression[digit_start:i]

        try:
            value = float(number_str) * (-1 if minus_sum % 2 == 1 else 1)
            return value, i
        except:
            raise ValueError(f"[ERROR] failed to read number, invalid number format at index {index}")

    def tokenize(self, expression: str):
        pass
