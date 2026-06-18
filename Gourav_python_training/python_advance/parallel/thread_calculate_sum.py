# Q2 - Create a thread that calculates the sum of numbers from 1 to 100.

import threading

# Constants
SUM_RANGE_END = 100


def calculate_sum_in_thread() -> None:
    """Create a thread that calculates the sum of numbers from 1 to 100."""
    result = {}

    def sum_numbers() -> None:
        result["total"] = sum(range(1, SUM_RANGE_END + 1))

    sum_thread = threading.Thread(target=sum_numbers)
    sum_thread.start()
    sum_thread.join()

    print(f"Sum of 1 to {SUM_RANGE_END} (calculated in a thread): {result['total']}")


if __name__ == "__main__":
    calculate_sum_in_thread()