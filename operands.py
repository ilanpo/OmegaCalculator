from abc import ABC, abstractmethod
import math
from exceptions import OperandException, DivideByZeroException, OperandNotFoundException

LEFT_ASSOCIATIVE = "left"
RIGHT_ASSOCIATIVE = "right"


class Operator(ABC):
    def __init__(self, symbol: str, intensity: int, direction: str):
        self.symbol = symbol
        self.intensity = intensity
        self.direction = direction

    @abstractmethod
    def calculate(self, *args) -> float:
        pass


class OperatorBinary(Operator):
    def __init__(self, symbol: str, intensity: int, direction: str = LEFT_ASSOCIATIVE):
        super().__init__(symbol, intensity, direction)  # ALL binary operators are left associative
                                                        # (according to instructions)

    @abstractmethod
    def calculate(self, operand1: float, operand2: float) -> float:
        pass


class Add(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return operand1 + operand2


class Subtract(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return operand1 - operand2


class Divide(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        if operand2 == 0:
            raise DivideByZeroException("[ERROR] division by zero not allowed")
        return operand1 / operand2


class Multiply(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return operand1 * operand2


class Power(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return math.pow(operand1, operand2)


class Modulo(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return operand1 % operand2


class Maximum(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return operand1 if operand1 >= operand2 else operand2


class Minimum(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
        return operand1 if operand1 <= operand2 else operand2


class Average(OperatorBinary):
    def calculate(self, operand1: float, operand2: float) -> float:
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
            raise OperandException("[ERROR] factorial only defined for positive whole numbers i.e integers")
        result = 1
        for i in range(int(operand)):
            result *= i
        return float(result)


class DigitSum(OperatorUnary):
    def calculate(self, operand: float) -> float:
        num_str = str(operand)

        total = 0
        for char in num_str:
            if char.isdigit():
                total += int(char)

        return float(total)


class OperatorRegistry:
    """
    used to flexibly store and retrieve the various operands
    """
    def __init__(self):
        self.operators = {}

    def register(self, op: Operator):
        """
        stores an operand in the dict according to its symbol
        :param op: operand to store
        """
        self.operators[op.symbol] = op

    def get_operator(self, symbol: str) -> Operator:
        """
        checks if symbol is in the dict, if it is returns the operand function associated with it
        :param symbol: symbol to search by
        :return: Operator which the symbol belongs to
        """
        if symbol not in self.operators:
            raise OperandNotFoundException(f"[ERROR] unknown operator: {symbol}")
        return self.operators[symbol]

    def get_all_operands(self) -> list[str]:
        """
        returns a list of all the symbols of the operands in the registry
        """
        return list(self.operators.keys())
