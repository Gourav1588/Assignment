# Q1 - Write pytest test cases for a function that adds two numbers.


def add_numbers(a, b) -> float:
    """Return the sum of two numbers. (Function under test)"""
    return a + b


def test_add_two_positive_numbers() -> None:
    """Adding two positive numbers should return the correct sum."""
    assert add_numbers(2, 3) == 5


def test_add_negative_numbers() -> None:
    """Adding two negative numbers should return a negative sum."""
    assert add_numbers(-2, -3) == -5


def test_add_positive_and_negative() -> None:
    """Adding a positive and a negative number should return the correct result."""
    assert add_numbers(5, -3) == 2


def test_add_with_zero() -> None:
    """Adding zero to a number should return the same number."""
    assert add_numbers(10, 0) == 10


def test_add_floats() -> None:
    """Adding two floating point numbers should return the correct sum."""
    assert add_numbers(2.5, 3.5) == 6.0