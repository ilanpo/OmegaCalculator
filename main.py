from operands import *
from exceptions import *
from lexer import Lexer
from parser import Parser
from solver import Solver

LEFT_ASSOCIATIVE = "left"
RIGHT_ASSOCIATIVE = "right"

BINARY_MINUS = 'b-'
UNARY_MINUS = 'u-'
SIGN_MINUS = 's-'


def setup_registry():
    registry = OperatorRegistry()

    registry.register(Add('+', 1))
    registry.register(Subtract(BINARY_MINUS, 1))

    registry.register(Multiply('*', 2))
    registry.register(Divide('/', 2))

    registry.register(UnaryMinus(UNARY_MINUS, 3, RIGHT_ASSOCIATIVE))

    registry.register(Power('^', 4))

    registry.register(Modulo('%', 5))

    registry.register(Maximum('$', 6))
    registry.register(Minimum('&', 6))
    registry.register(Average('@', 6))

    registry.register(Factorial('!', 7, LEFT_ASSOCIATIVE))
    registry.register(Negate('~', 7, RIGHT_ASSOCIATIVE))
    registry.register(DigitSum('#', 7, LEFT_ASSOCIATIVE))

    registry.register(UnaryMinus(SIGN_MINUS, 8, RIGHT_ASSOCIATIVE))

    return registry


def main():
    registry = setup_registry()
    lexer = Lexer(registry, BINARY_MINUS, UNARY_MINUS)
    parser = Parser(registry)
    solver = Solver(registry)

    print("""                                                
  ____                        _____     __         __     __          
 ╱ __ ╲__ _  ___ ___ ____ _  ╱ ___╱__ _╱ ╱_____ __╱ ╱__ _╱ ╱____  ____
╱ ╱_╱ ╱  ' ╲╱ ─_) _ `╱ _ `╱ ╱ ╱__╱ _ `╱ ╱ __╱ ╱╱ ╱ ╱ _ `╱ __╱ _ ╲╱ __╱
╲____╱_╱_╱_╱╲__╱╲_, ╱╲_,_╱  ╲___╱╲_,_╱_╱╲__╱╲_,_╱_╱╲_,_╱╲__╱╲___╱_╱   
               ╱___╱                                                                                                                   
    """)
    print("Powerful calculator that can calculate using all sorts of operators ")
    print("""Operators: + Addition, - Subtraction and Negation, * Multiplication, / Division,
           ^ Power, % Modulo, $ Maximum, & Minimum, @ Average, ~ Negate,
           ! Factorial (has to be whole and positive), # Sum of digits.
Extras: ( left parenthesis, ) right parenthesis""")
    print("Usage instructions: type exit to end, otherwise input any mathematical equation and get the answer")

    while True:
        try:
            user_input = input("Input expression: ")

            if user_input == "exit":
                break

            if not user_input.strip():
                continue

            tokens = lexer.tokenize(user_input)

            postfix_q = parser.parse(tokens)
            print(postfix_q)

            result = solver.solve(postfix_q)

            if result.is_integer():
                print(int(result))
            else:
                print("result: " + str(result))

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
