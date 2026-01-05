from abc import ABC, abstractmethod
import math


class Operator(ABC):
    def __init__(self, symbol: str, intensity: int):
        self.symbol = symbol
        self.intensity = intensity

    @abstractmethod
    def calculate(self, *args) -> float:
        pass


class OperatorBinary(Operator):
    @abstractmethod
    def calculate(self, operand1: float, operand2: float) -> float:
        pass


class Add(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return operand1 + operand2


class Subtract(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return operand1 - operand2


class Divide(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        if operand2 == 0:
            raise ValueError("[ERROR] division by zero not allowed")
        return operand1 / operand2


class Multiply(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return operand1 * operand2


class Power(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return math.pow(operand1, operand2)


class Modulo(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return operand1 % operand2


class Maximum(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return max(operand1, operand2)


class Minimum(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return min(operand1, operand2)


class Average(OperatorBinary):
    def calculate(self, operand1: float, operand2: float):
        return (operand1 + operand2) / 2


class OperatorUnary(Operator):
    @abstractmethod
    def calculate(self, operand: float) -> float:
        pass


class UnaryMinus(OperatorUnary):
    def calculate(self, operand: float) -> float:
        return -operand


class Negate(OperatorUnary):
    def calculate(self, operand: float) -> float:
        return -operand


class Factorial(OperatorUnary):
    def calculate(self, operand: float) -> float:
        if operand < 0 or not operand.is_integer():
            raise ValueError("[ERROR] factorial only defined for positive whole numbers i.e integers")
        return math.factorial(int(operand))


class DigitSum(OperatorUnary):
    def calculate(self, operand: float) -> float:
        num_str = str(operand)

        total = 0
        for char in num_str:
            if char.isdigit():
                total += int(char)

        return float(total)


class OperatorRegistry:
    def __init__(self):
        self.operators = {}

    def register(self, op: Operator):
        self.operators[op.symbol] = op

    def get_operator(self, symbol: str) -> Operator:
        if symbol not in self.operators:
            raise ValueError(f"[ERROR] unknown operator: {symbol}")
        return self.operators[symbol]

    def get_all_operands(self):
        return list(self.operators.keys())


registry = OperatorRegistry()


registry.register(Add('+', 1))
registry.register(Subtract('b-', 1))

registry.register(Multiply('*', 2))
registry.register(Divide('/', 2))

registry.register(UnaryMinus('u-', 3))

registry.register(Power('^', 4))

registry.register(Modulo('%', 5))

registry.register(Maximum('$', 6))
registry.register(Minimum('&', 6))
registry.register(Average('@', 6))

registry.register(Factorial('!', 7))
registry.register(Negate('~', 7))
registry.register(DigitSum('#', 7))