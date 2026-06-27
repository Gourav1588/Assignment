# Q2 - Use map() to convert a list of numbers into their squares.

# Constants
NUMBERS_FOR_MAP = [1, 2, 3, 4, 5]


def use_map_to_square_numbers(numbers) -> list[int]:
    """Use map() to convert a list of numbers into their squares."""
    # map() applies the lambda to every element, returns a map object so we wrap in list()
    squared_numbers = list(map(lambda n: n ** 2, numbers))
    print(f"Original: {numbers}")
    print(f"Squared:  {squared_numbers}")
    return squared_numbers


if __name__ == "__main__":
    use_map_to_square_numbers(NUMBERS_FOR_MAP)