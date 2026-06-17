# Q6 - Explain the difference between iterator and generator with a small example.

from typing import Iterator


def generate_squares(n) -> Iterator[int]:
    """Yield square numbers from 1 up to n. Used as the example generator."""
    for i in range(1, n + 1):
        yield i ** 2


class NumberRangeIterator:
    """Custom iterator class used as the example iterator."""

    def __init__(self, limit) -> None:
        """Store the upper limit and starting point for iteration."""
        self.limit = limit
        self.current = 1

    def __iter__(self) -> "NumberRangeIterator":
        """Return the iterator object itself."""
        return self

    def __next__(self) -> int:
        """Return the next number, or raise StopIteration when limit is reached."""
        if self.current > self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def explain_iterator_vs_generator() -> None:
    """Explain the difference between an iterator and a generator with an example."""
    print("Iterator: an object with __iter__ and __next__ methods, built manually.")
    print("          Example: NumberRangeIterator class above.")
    print("Generator: a simpler way to create an iterator using yield - Python")
    print("           handles __iter__ and __next__ for you automatically.")
    print("           Example: generate_squares() function above.\n")

    iterator_example = NumberRangeIterator(3)
    print(f"Iterator output:  {list(iterator_example)}")

    generator_example = generate_squares(3)
    print(f"Generator output: {list(generator_example)}")


if __name__ == "__main__":
    explain_iterator_vs_generator()