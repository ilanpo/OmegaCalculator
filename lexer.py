from typing import Tuple
L_PARENTHESES = ['(']
R_PARENTHESES = [')']
PARENTHESES = L_PARENTHESES + R_PARENTHESES


class Lexer:
    def __init__(self, operator_registry):
        self.operator_registry = operator_registry

    def normalize(self, expression: str) -> str:
        return expression.replace(" ", "").replace("\t", "")

    def read_number(self, expression: str, index: int) -> tuple[float, int]:
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
                    raise ValueError(f"[ERROR] failed to read number, number at index {digit_start} has multiple dots")
                decimal = True
                i += 1
            else:
                break

        try:
            value = float(expression[digit_start:i])
            return value, i
        except:
            raise ValueError(f"[ERROR] failed to read number, invalid number format at index {index}")

    def tokenize(self, expression: str):
        expression = self.normalize(expression)
        operators = self.operator_registry.get_all_operands()
        i = 0
        length = len(expression)
        prev_token = None

        while i < length:
            char = expression[i]

            if char == '-':
                if prev_token in ['NUMBER', 'R_PARENTHESES']:
                    yield 'b-'  # binary minus
                else:
                    yield 'u-'  # unary minus

                prev_token = 'OPERATOR'

                i+=1
                continue

            if char.isdigit():
                number, new_i = self.read_number(expression, i)
                yield number

                prev_token = 'NUMBER'

                i = new_i
                continue

            if char in operators or char in PARENTHESES:
                yield char
                if char in L_PARENTHESES:
                    prev_token = "L_PARENTHESES"
                elif char in R_PARENTHESES:
                    prev_token = "R_PARENTHESES"
                else:
                    prev_token = "OPERATOR"

                i += 1
                continue

            raise ValueError(f"[ERROR] illegal character {char} at index {i}")




