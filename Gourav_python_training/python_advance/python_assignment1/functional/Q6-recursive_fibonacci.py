# Q6 - Write a recursive function to calculate Fibonacci.

# Constants
FIBONACCI_POSITION = 7


def fibonacci_recursive(position) -> int:
    """Calculate the Fibonacci number at a given position using recursion."""
    # Base cases: first two Fibonacci numbers are 0 and 1
    if position <= 0:
        return 0
    if position == 1:
        return 1
    # Recursive case: each number is the sum of the two before it
    return fibonacci_recursive(position - 1) + fibonacci_recursive(position - 2)


if __name__ == "__main__":
    print(f"Fibonacci at position {FIBONACCI_POSITION} = {fibonacci_recursive(FIBONACCI_POSITION)}")