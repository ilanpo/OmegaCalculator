import queue
from collections import deque

LEFT_ASSOCIATIVE = "left"
RIGHT_ASSOCIATIVE = "right"


class ParserException(Exception):
    pass


class ParenthesesError(ParserException):
    pass


class UnknownOperatorError(ParserException):
    pass


class Parser:
    def __init__(self, operator_registry):
        self.operator_registry = operator_registry

    def parse(self, token_generator):
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
                self.handle_right_parentheses(operator_stack, output_queue)

            else:
                self.handle_operator(token, operator_stack, output_queue)

        self.finalize(operator_stack, output_queue)

        return output_queue

    def handle_right_parentheses(self, operator_stack: list, output_queue: deque):
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

    def handle_operator(self, token: str, operator_stack: list, output_queue: deque):
        """
        helper to handle case where operator is generated depending on direction of operator and precedence
        :param token: the operator token to be handled
        :param operator_stack: current operator stack
        :param output_queue: current output queue
        :return:
        """
        try:
            current_operator = self.operator_registry.get_operator(token)
        except ValueError:
            raise UnknownOperatorError(f"[ERROR] unknown operator token: {token}")

        while operator_stack:
            top_token = operator_stack[-1]

            if top_token == '(':
                break

            top_operator = self.operator_registry.get_operator(top_token)

            if self.should_pop_op(current_operator, top_operator):
                output_queue.append(operator_stack.pop())
            else:
                break

        operator_stack.append(token)

    def should_pop_op(self, current_op, top_op) -> bool:
        """
        separated logic to check if operator should pe popped out of the stack or no depending on
        direction of operator and precedence (used in handle_operator)
        :param current_op: current operator being handled
        :param top_op: top operator on the stack
        :return: boolean of whether it should be popped (True) or it shouldn't (False)
        """
        if (current_op.direction == LEFT_ASSOCIATIVE and current_op.precedence <= top_op.precedence or
                current_op.direction == RIGHT_ASSOCIATIVE and current_op.precedence < top_op.precedence):
            return True
        return False

    def finalize(self, operator_stack: list, output_queue: deque):
        """
        helper that does the final clearing of the operator stack, also checks if we have too many left parentheses
        :param operator_stack: current operator stack
        :param output_queue: current output queue
        """
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ParenthesesError(f"[ERROR] mismatched parentheses: too many left parentheses")
            output_queue.append(operator_stack.pop())
