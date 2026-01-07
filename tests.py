
import pytest
from exceptions import *
from calculator import Calculator

calculator = Calculator()


def test_5_syntax_errors():
    with pytest.raises(PlacementError):
        assert calculator.calculate("3^*2")

    with pytest.raises(PlacementError):
        assert calculator.calculate("5-*/2")

    with pytest.raises(PlacementError):
        assert calculator.calculate("/2-3#")

    with pytest.raises(PlacementError):
        assert calculator.calculate("/23+")

    with pytest.raises(PlacementError):
        assert calculator.calculate("$332*")


def test_gibberish():
    with pytest.raises(IllegalCharacterError):
        assert calculator.calculate("bfhfguyg636g8f8h91&^#&@#*&8")


def test_empty():
    with pytest.raises(Exception):
        assert calculator.calculate("")


def test_whitespace():
    with pytest.raises(Exception):
        assert calculator.calculate("                  ")
    with pytest.raises(Exception):
        assert calculator.calculate(" \t   ")


def test_minus_clarification():
    assert calculator.calculate("-1 + 7") == 6.0

    assert calculator.calculate("-2 ^ 4") == -16.0

    assert calculator.calculate("3+~-3") == 6.0

    assert calculator.calculate("~-3!") == 6.0

    with pytest.raises(Exception):
        assert calculator.calculate("~--3!")

    with pytest.raises(Exception):
        assert calculator.calculate("--~--3")

    with pytest.raises(Exception):
        assert calculator.calculate("~--~-3")

    with pytest.raises(Exception):
        assert calculator.calculate("~~3")

    with pytest.raises(Exception):
        assert calculator.calculate("2 - - 3!")

    assert calculator.calculate("-3!") == -6.0

    assert calculator.calculate("--3!") == 6.0

    assert calculator.calculate("2---3!") == -4.0

    assert calculator.calculate("2 +--3!") == 8.0


def test_simple_equations():
    assert calculator.calculate("1 + 1") == 2.0

    assert calculator.calculate("10 - 4") == 6.0

    assert calculator.calculate("6 * 7") == 42.0

    assert calculator.calculate("8 / 2") == 4.0

    assert calculator.calculate("2 ^ 3") == 8.0

    assert calculator.calculate("-5 + 3") == -2.0

    assert calculator.calculate("~3 + 5") == 2.0

    assert calculator.calculate("10 % 3") == 1.0

    assert calculator.calculate("10 $ 5") == 10.0

    assert calculator.calculate("10 & 20") == 10.0

    assert calculator.calculate("10 @ 20") == 15.0

    assert calculator.calculate("3!") == 6.0

    assert calculator.calculate("123.123#") == 12.0

    assert calculator.calculate("2 ^ 3 ^ 4") == 4096.0

    assert calculator.calculate("1.2 + 2.3") == 3.5


def test_complex_equations():
    assert calculator.calculate("(3+5)*2-4/2^  2+((10-10)*5)") == 15.0

    assert calculator.calculate("10%3+2*5 -3+(100/100)  -1") == 8.0

    assert calculator.calculate("2+3 ! +4-10+(5*0) +(   10-10)") == 2.0

    assert calculator.calculate("56#+9-1 0+ 2+(10@1 0)-10") == 12.0

    assert calculator.calculate("(10@30)*2+(5$2)-(10 & 100)") == 35.0

    assert calculator.calculate("(10$20)& 5+(3!-6)*  10 0") == 5.0

    assert calculator.calculate("10+~5+(2 ^ 3)-8+( 100@50 )") == 80.0

    assert calculator.calculate("2@6+10+(123#)-6+          (5$1)") == 19.0

    assert calculator.calculate("2^3!+1 +(10 /2)-5+(1&100)") == 66.0

    assert calculator.calculate("123#+4!+(10-10 )+(2*0)") == 30.0

    assert calculator.calculate("10$ (10 0&5)+(20@20)-20") == 10.0

    assert calculator.calculate("(~5 )^2+(100/10)-10  +(1$0)") == 26.0

    assert calculator.calculate("2*(3+(4*  11#))+(0*500)") == 22.0

    assert calculator.calculate("1.5 @ 4.5+(3!-6)+(10-10)") == 3.0

    assert calculator.calculate("5!/10$5+ (99#)-18+(0$0)") == 12.0

    assert calculator.calculate("55 #@ 30 + (100-101) + (2&10)") == 21.0

    assert calculator.calculate("100- (10$100)  +(5!-120)") == 0.0

    assert calculator.calculate("16^0.5+9^  0.5+(10@30)-20") == 7.0

    assert calculator.calculate("10+20 -5*2+99#+(1$0)-1") == 38.0

    assert calculator.calculate("(2+1)!+(100/10  )-10+(0@0)") == 6.0
