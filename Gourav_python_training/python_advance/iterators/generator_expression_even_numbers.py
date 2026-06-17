# Q5 - Write a generator expression to generate even numbers from 1 to 50.

# Constants
RANGE_END = 50


def generate_even_numbers(limit) -> list[int]:
    """Generate even numbers from 1 to limit using a generator expression."""
    # Generator expression - similar to list comprehension but lazy (uses () not [])
    even_numbers = (num for num in range(1, limit + 1) if num % 2 == 0)
    result = list(even_numbers)
    print(result)
    return result


if __name__ == "__main__":
    generate_even_numbers(RANGE_END)