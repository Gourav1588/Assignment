# Q7 - Process a large dataset using a generator instead of storing all values in a list.

# Constants
LARGE_DATASET_SIZE = 1_000_000


def process_large_dataset_with_generator(size) -> int:
    """Process a large dataset using a generator instead of storing all values in a list."""
    # A generator expression - does NOT create the whole list in memory
    number_generator = (i for i in range(size))

    total = sum(number_generator)  # generator is consumed lazily, one value at a time
    print(f"Sum of numbers from 0 to {size - 1} using a generator: {total}")
    return total


if __name__ == "__main__":
    process_large_dataset_with_generator(LARGE_DATASET_SIZE)