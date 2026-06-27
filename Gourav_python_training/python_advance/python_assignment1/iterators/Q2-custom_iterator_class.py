# Q2 - Write a custom iterator class that returns numbers from 1 to N.

# Constants
ITERATOR_LIMIT = 5


class NumberRangeIterator:
    """Custom iterator class that returns numbers from 1 to N."""

    def __init__(self, limit) -> None:
        """Store the upper limit and starting point for iteration."""
        self.limit = limit
        self.current = 1

    def __iter__(self) -> "NumberRangeIterator":
        """Return the iterator object itself, required by the iterator protocol."""
        return self

    def __next__(self) -> int:
        """Return the next number, or raise StopIteration when limit is reached."""
        if self.current > self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


if __name__ == "__main__":
    number_iterator = NumberRangeIterator(ITERATOR_LIMIT)
    for number in number_iterator:
        print(number)