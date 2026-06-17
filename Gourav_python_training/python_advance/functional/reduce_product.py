# Q4 - Use reduce() to find the product of all elements in a list.

from functools import reduce

# Constants
NUMBERS_FOR_REDUCE = [1, 2, 3, 4, 5]


def use_reduce_to_find_product(numbers) -> int:
    """Use reduce() to find the product of all elements in a list."""
    # reduce() applies the lambda cumulatively: ((((1*2)*3)*4)*5)
    product = reduce(lambda a, b: a * b, numbers)
    print(f"Numbers: {numbers}")
    print(f"Product: {product}")
    return product


if __name__ == "__main__":
    use_reduce_to_find_product(NUMBERS_FOR_REDUCE)