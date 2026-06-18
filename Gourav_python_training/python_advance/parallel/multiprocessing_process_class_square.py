# Q6 - Write a multiprocessing program to calculate the square of numbers using Process class.

import multiprocessing
import os

# Constants
NUMBERS_TO_SQUARE = [1, 2, 3, 4, 5]


def square_number(number) -> None:
    """Calculate and print the square of a number - run inside a separate process."""
    result = number ** 2
    print(f"Process {os.getpid()} calculated: {number}^2 = {result}")


def calculate_squares_using_process_class(numbers) -> None:
    """Calculate the square of numbers using the multiprocessing Process class."""
    processes = []

    for number in numbers:
        process = multiprocessing.Process(target=square_number, args=(number,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    calculate_squares_using_process_class(NUMBERS_TO_SQUARE)