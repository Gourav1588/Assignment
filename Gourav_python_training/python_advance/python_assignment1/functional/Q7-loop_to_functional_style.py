# Q7 - Convert a simple loop-based program into a functional style using map or filter.

# Constants
LOOP_BASED_NUMBERS = [2, 4, 6, 8, 10]


def loop_based_approach(numbers) -> list[int]:
    """Original loop-based approach: double numbers greater than 5."""
    doubled = []
    for n in numbers:
        if n > 5:
            doubled.append(n * 2)
    return doubled


def convert_loop_to_functional_style(numbers) -> list[int]:
    """Convert the loop-based approach into a functional style using map and filter."""
    # filter() keeps numbers > 5, then map() doubles each remaining number
    result = list(map(lambda n: n * 2, filter(lambda n: n > 5, numbers)))
    print(f"Original:           {numbers}")
    print(f"Functional result:  {result}")
    return result


if __name__ == "__main__":
    convert_loop_to_functional_style(LOOP_BASED_NUMBERS)