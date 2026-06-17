# Q3 - Use filter() to extract even numbers from a list.

# Constants
NUMBERS_FOR_FILTER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def use_filter_to_extract_evens(numbers) -> list[int]:
    """Use filter() to extract even numbers from a list."""
    # filter() keeps only elements where the lambda returns True
    even_numbers = list(filter(lambda n: n % 2 == 0, numbers))
    print(f"Original: {numbers}")
    print(f"Evens:    {even_numbers}")
    return even_numbers


if __name__ == "__main__":
    use_filter_to_extract_evens(NUMBERS_FOR_FILTER)