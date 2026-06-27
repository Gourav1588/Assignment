# Q3 - Write a generator function that yields square numbers up to N.

from typing import Iterator

# Constants
SQUARE_LIMIT = 5


def generate_squares(n) :
    """Yield square numbers from 1 up to n."""
    for i in range(1, n + 1):
        yield i ** 2  # yield pauses the function and returns one value at a time


if __name__ == "__main__":
    for square in generate_squares(SQUARE_LIMIT):
        print(square)