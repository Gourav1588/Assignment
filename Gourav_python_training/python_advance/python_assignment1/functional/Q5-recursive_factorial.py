# Q5 - Write a recursive function to calculate factorial.

# Constants
FACTORIAL_NUMBER = 6


def factorial_recursive(n) -> int:
    """Calculate factorial of n using recursion."""
    # Base case stops the recursion from running forever
    if n <= 1:
        return 1
    # Recursive case: n! = n * (n-1)!
    return n * factorial_recursive(n - 1)


if __name__ == "__main__":
    print(f"Factorial of {FACTORIAL_NUMBER} = {factorial_recursive(FACTORIAL_NUMBER)}")