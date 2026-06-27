# Q1 - Create an iterator for a list and print elements using next().

# Constants
SAMPLE_LIST = [10, 20, 30, 40, 50]


def iterate_list_with_next() -> None:
    """Create an iterator for a list and print elements using next()."""
    list_iterator = iter(SAMPLE_LIST)  # iter() converts list into an iterator

    # next() pulls one item at a time until StopIteration is raised
    while True:
        try:
            item = next(list_iterator)
            print(item)
        except StopIteration:
            break


if __name__ == "__main__":
    iterate_list_with_next()