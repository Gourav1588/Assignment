# Q4 - Module inside math_operations_package containing add, subtract, multiply, divide

FIRST_NUMBER = 5
SECOND_NUMBER = 3


def add(a, b) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b) -> float:
    """Return the difference between two numbers."""
    return a - b


def multiply(a, b) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a, b) -> float:
    """Return the division of two numbers, raises ValueError if dividing by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


if __name__ == "__main__":
    print(f"{FIRST_NUMBER} + {SECOND_NUMBER} = {add(FIRST_NUMBER, SECOND_NUMBER)}")
    print(f"{FIRST_NUMBER} - {SECOND_NUMBER} = {subtract(FIRST_NUMBER, SECOND_NUMBER)}")
    print(f"{FIRST_NUMBER} * {SECOND_NUMBER} = {multiply(FIRST_NUMBER, SECOND_NUMBER)}")
    print(f"{FIRST_NUMBER} / {SECOND_NUMBER} = {divide(FIRST_NUMBER, SECOND_NUMBER)}")