# Q7 - Convert a normal function into parallel execution using ThreadPoolExecutor.

from concurrent.futures import ThreadPoolExecutor

# Constants
NUMBERS_TO_SQUARE = [1, 2, 3, 4, 5]


def square_number(number) -> int:
    """Return the square of a number - the normal function being parallelised."""
    return number ** 2


def convert_function_to_thread_pool(numbers) -> list[int]:
    """Convert a normal function into parallel execution using ThreadPoolExecutor."""
    # ThreadPoolExecutor manages a pool of threads automatically - no manual start/join
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(square_number, numbers))

    print(f"Numbers: {numbers}")
    print(f"Squares (via ThreadPoolExecutor): {results}")
    return results


if __name__ == "__main__":
    convert_function_to_thread_pool(NUMBERS_TO_SQUARE)