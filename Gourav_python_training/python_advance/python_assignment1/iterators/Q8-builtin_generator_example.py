# Q8 - Show an example of a built-in generator (like range) and iterate over it.

# Constants
RANGE_START = 1
RANGE_END = 6


def demonstrate_builtin_generator() -> None:
    """Show an example of a built-in generator (range) and iterate over it."""
    # range() does not store all numbers in memory - it generates them on demand
    number_range = range(RANGE_START, RANGE_END)
    print(f"Iterating over range({RANGE_START}, {RANGE_END}):")
    for number in number_range:
        print(number, end=" ")
    print()


if __name__ == "__main__":
    demonstrate_builtin_generator()