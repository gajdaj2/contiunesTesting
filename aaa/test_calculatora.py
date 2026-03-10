import pytest


class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Nie można dzielić przez 0")
        return a / b


# TEST
def test_calculator_add():
    # Arrange
    calc = Calculator()
    # Act
    result = calc.add(5, 3)
    # Assert
    assert result == 8


def test_calculator_divide_by_zero():
    # Arrange
    calc = Calculator()
    # Act & Assert
    with pytest.raises(ValueError):
        calc.divide(10, 0)
        