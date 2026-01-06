
from collections import deque
from exceptions import ParenthesesError, UnknownOperatorError, OperandNotFoundException

LEFT_FACING = "left"
RIGHT_FACING = "right"

LEFT_PLACED = "left_of_value"
BINARY = "between_values"
RIGHT_PLACED = "right_of_value"


def _should_pop_op(current_op, top_op) -> bool:
    """
    separated logic to check if operator should pe popped out of the stack or no depending on
    direction of operator and precedence (used in handle_operator)
    :param current_op: current operator being handled
    :param top_op: top operator on the stack
    :return: boolean of whether it should be popped (True) or it shouldn't (False)
    """
    if current_op.intensity < top_op.intensity:
        return True

    if current_op.direction == LEFT_FACING and current_op.intensity == top_op.intensity:
        return True

    if current_op.intensity > top_op.intensity:
        return False

    if current_op.placement_rules == RIGHT_PLACED and current_op.placement_rules == RIGHT_PLACED:
        return True

    if current_op.placement_rules == LEFT_PLACED and current_op.placement_rules == LEFT_PLACED:
        return False

    if current_op.direction == RIGHT_PLACED and top_op.direction == LEFT_PLACED:
        return True

    return False


def _finalize(operator_stack: list, output_queue: deque):
    """
    helper that does the final clearing of the operator stack, also checks if we have too many left parentheses
    :param operator_stack: current operator stack
    :param output_queue: current output queue
    """
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ParenthesesError(f"[ERROR] mismatched parentheses: too many left parentheses")
        output_queue.append(operator_stack.pop())


def _handle_right_parentheses(operator_stack: list, output_queue: deque):
    """
    helper to handle case where right parentheses is generated
    :param operator_stack: current operator stack
    :param output_queue: current output queue
    """
    try:
        while operator_stack[-1] != '(':
            output_queue.append(operator_stack.pop())
        operator_stack.pop()
    except IndexError:
        raise ParenthesesError(f"[ERROR] mismatched parentheses: too many right parentheses")


class Parser:
    def __init__(self, operator_registry):
        self.operator_registry = operator_registry

    def parse(self, token_generator) -> deque:
        """
        parses generated infix order tokens into postfix order tokens, based on shunting-yard algorithm
        :param token_generator: tokenizer from lexer, yields either float for numbers or string for operands/parentheses
        :return: queue containing postfix order tokens
        """
        output_queue = deque()
        operator_stack = []

        for token in token_generator:
            if isinstance(token, float):
                output_queue.append(token)

            elif token == '(':
                operator_stack.append(token)

            elif token == ')':
                _handle_right_parentheses(operator_stack, output_queue)

            else:
                self._handle_operator(token, operator_stack, output_queue)

        _finalize(operator_stack, output_queue)

        return output_queue

    def _handle_operator(self, token: str, operator_stack: list, output_queue: deque):
        """
        helper to handle case where operator is generated depending on direction of operator and precedence
        :param token: the operator token to be handled
        :param operator_stack: current operator stack
        :param output_queue: current output queue
        :return:
        """
        try:
            current_operator = self.operator_registry.get_operator(token)
        except OperandNotFoundException:
            raise UnknownOperatorError(f"[ERROR] unknown operator token: {token}")

        while operator_stack:
            top_token = operator_stack[-1]

            if top_token == '(':
                break

            top_operator = self.operator_registry.get_operator(top_token)

            if _should_pop_op(current_operator, top_operator):
                output_queue.append(operator_stack.pop())
            else:
                break

        operator_stack.append(token)
