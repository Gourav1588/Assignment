# Q8 - Convert a normal function into parallel execution using ProcessPoolExecutor.

from concurrent.futures import ProcessPoolExecutor
import os

# Constants
NUMBERS_TO_SQUARE = [1, 2, 3, 4, 5]


def square_number(number) -> int:
    """Return the square of a number - the normal function being parallelised."""
    result = number ** 2
    print(f"Process {os.getpid()} calculated: {number}^2 = {result}")
    return result


def convert_function_to_process_pool(numbers) -> list[int]:
    """Convert a normal function into parallel execution using ProcessPoolExecutor."""
    # ProcessPoolExecutor runs each call in a separate process - good for CPU-heavy tasks
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square_number, numbers))

    print(f"Squares (via ProcessPoolExecutor): {results}")
    return results


if __name__ == "__main__":
    convert_function_to_process_pool(NUMBERS_TO_SQUARE)