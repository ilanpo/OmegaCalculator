from abc import ABC, abstractmethod
import math
from exceptions import OperandException, DivideByZeroException, OperandNotFoundException

LEFT_FACING = "left"
RIGHT_FACING = "right"

LEFT_PLACED = "left_of_value"
BINARY = "between_values"
RIGHT_PLACED = "right_of_value"


class Operator(ABC):
    def __init__(self, symbol: str, intensity: int, direction: str, placement_rules: str):
        self.symbol = symbol
        self.intensity = intensity
        self.direction = direction
        self.placement_rules = placement_rules

    @abstractmethod
    def calculate(self, *args) -> float:
        pass


class OperatorBinary(Operator):
    def __init__(self, symbol: str, intensity: int, direction: str = LEFT_FACING):
        super().__init__(symbol, intensity, direction, BINARY)  # all go left-to-right according to instructions


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
        """
        flips the sign of the number
        :param operand1: float to work with
        :param operand1: second float to work with
        :return: result as float
        """
        return (operand1 + operand2) / 2


class OperatorUnary(Operator):
    def __init__(self, symbol: str, intensity: int, placement: str, direction: str = RIGHT_FACING):
        super().__init__(symbol, intensity, direction, placement)  # all go left-to-right according to instructions

    @abstractmethod
    def calculate(self, operand: float) -> float:
        pass


class UnaryMinus(OperatorUnary):
    def calculate(self, operand: float) -> float:
        """
        flips the sign of the number
        :param operand: float to work with
        :return: result as float
        """
        return -operand


class Negate(OperatorUnary):
    def calculate(self, operand: float) -> float:
        """
        flips the sign of the number
        :param operand: float to work with
        :return: result as float
        """
        return -operand


class Factorial(OperatorUnary):
    def calculate(self, operand: float) -> float:
        """
        calculates the factorial of operand
        :param operand: float to work with
        :return: result as float
        """
        if operand < 0 or not operand.is_integer():
            raise OperandException("[ERROR] factorial only defined for positive whole numbers i.e integers")
        result = 1
        for i in range(1, int(operand) + 1):
            result *= i
        return float(result)


class DigitSum(OperatorUnary):
    def calculate(self, operand: float) -> float:
        """
        sums all the digits in the operand
        :param operand: float to work with
        :return: result as float
        """
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
