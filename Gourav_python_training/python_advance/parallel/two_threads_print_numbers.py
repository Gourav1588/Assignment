# Q1 - Write a program to create two threads that print numbers from 1 to 5 simultaneously.

import threading

# Constants
NUMBER_RANGE_END = 5


def print_numbers(thread_label) -> None:
    """Print numbers from 1 to NUMBER_RANGE_END - used by multiple threads simultaneously."""
    for i in range(1, NUMBER_RANGE_END + 1):
        print(f"[{thread_label}] {i}")


def create_two_threads_printing_numbers() -> None:
    """Create two threads that print numbers from 1 to 5 simultaneously."""
    thread_one = threading.Thread(target=print_numbers, args=("Thread-1",))
    thread_two = threading.Thread(target=print_numbers, args=("Thread-2",))

    thread_one.start()
    thread_two.start()

    thread_one.join()
    thread_two.join()


if __name__ == "__main__":
    create_two_threads_printing_numbers()