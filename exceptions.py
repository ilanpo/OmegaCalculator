# parsers errors
class ParserException(Exception):
    pass


class ParenthesesError(ParserException):
    pass


class UnknownOperatorError(ParserException):
    pass


# lexers errors
class LexerError(Exception):
    pass


class InvalidNumberError(LexerError):
    pass


class IllegalCharacterError(LexerError):
    pass


class UnaryMishandleError(LexerError):
    pass


class NegationError(LexerError):
    pass


# solvers errors
class SolverException(Exception):
    pass


class OperationExecutionError(SolverException):
    pass


# operands errors
class OperandException(Exception):
    pass


class DivideByZeroException(OperandException):
    pass


class OperandNotFoundException(OperandException):
    pass
