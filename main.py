from calculator import Calculator


def main():
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

    calculator = Calculator()
    while True:
        try:
            user_input = input("Input expression: ")

            if user_input == "exit":
                break

            if not user_input.strip():
                continue

            result = calculator.calculate(user_input)

            if result.is_integer():
                print(int(result))
            else:
                print("result: " + str(result))

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
