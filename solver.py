from collections import deque
from operands import OperatorBinary, OperatorUnary
from exceptions import SolverException, OperationExecutionError


class Solver:
    def __init__(self, operator_registry):
        self.operator_registry = operator_registry

    def solve(self, postfix_queue: deque) -> float:
        """
        goes through all the operators and values in a postfix queue solving them until one final answer remains
        :param postfix_queue: postfix ordered queue filled with operator symbols (str) and values (float)
        :return: float result of expression
        """

        if not postfix_queue:
            raise SolverException("[ERROR] nothing in operation queue")

        stack = []

        for token in postfix_queue:
            if isinstance(token, float):
                stack.append(token)

            elif isinstance(token, str):
                self._handle_operation(token, stack)

            else:
                raise SolverException(f"[ERROR] unexpected token type in solver queue: {type(token)}")

        if len(stack) != 1:
            raise SolverException("[ERROR] incorrect amount of values in stack")

        return stack.pop()

    def _handle_operation(self, symbol: str, stack: list):
        """
        does the appropriate calculation on the values in the stack according to given operator
        :param symbol: symbol of operator to be used
        :param stack: stack with values (float) to be used by the operator
        :return: puts the result back in the stack
        """

        try:
            operator = self.operator_registry.get_operator(symbol)
        except ValueError:
            raise OperationExecutionError(f"[ERROR] unknown operator symbol: {symbol}")

        if isinstance(operator, OperatorBinary):
            if len(stack) < 2:
                raise OperationExecutionError(f"[ERROR] not enough values for binary operator {symbol}")

            right_value = stack.pop()
            left_value = stack.pop()
            stack.append(operator.calculate(left_value, right_value))

        elif isinstance(operator, OperatorUnary):
            if len(stack) < 1:
                raise OperationExecutionError(f"[ERROR] not enough values for binary operator {symbol}")

            stack.append(operator.calculate(stack.pop()))

        else:
            raise OperationExecutionError(f"[ERROR] unknown operator type: {type(operator)}")
