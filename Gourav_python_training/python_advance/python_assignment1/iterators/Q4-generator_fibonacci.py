# Q4 - Write a generator to produce Fibonacci numbers.

from typing import Iterator

# Constants
FIBONACCI_COUNT = 8


def generate_fibonacci(count) -> Iterator[int]:
    """Generate Fibonacci numbers one at a time using a generator."""
    first, second = 0, 1
    for _ in range(count):
        yield first
        first, second = second, first + second


if __name__ == "__main__":
    for fib_number in generate_fibonacci(FIBONACCI_COUNT):
        print(fib_number, end=" ")
    