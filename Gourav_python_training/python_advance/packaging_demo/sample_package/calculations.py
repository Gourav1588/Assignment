# Q3 - Second module inside sample_package


def add_two_numbers(a, b) -> float:
    """Return the sum of two numbers."""
    return a + b


def multiply_two_numbers(a, b) -> float:
    """Return the product of two numbers."""
    return a * b


if __name__ == "__main__":
    print(f"3 + 4 = {add_two_numbers(3, 4)}")
    print(f"3 * 4 = {multiply_two_numbers(3, 4)}")