# Q3 - Use try-except-else-finally to read a number from a file and print its square.

import os

# Constants
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "file_outputs")
SAMPLE_NUMBER_FILE = "number.txt"
SAMPLE_NUMBER_VALUE = "45"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_sample_number_file(file_path, value) -> None:
    """Create a sample file containing a number, used to test the read logic below."""
    with open(file_path, "w") as file:
        file.write(value)


def read_number_and_square_from_file(file_path) -> None:
    """Read a number from a file and print its square using try-except-else-finally."""
    try:
        with open(file_path, "r") as file:
            content = file.read().strip()
            number = int(content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' was not found.")
    except ValueError:
        print("Error: File content is not a valid number.")
    else:
        # else runs only if no exception occurred in the try block
        square = number ** 2
        print(f"Square of {number} is {square}")
    finally:
        # finally always runs, whether an exception occurred or not
        print("File read attempt finished.")


if __name__ == "__main__":
    file_path = os.path.join(OUTPUT_DIR, SAMPLE_NUMBER_FILE)
    create_sample_number_file(file_path, SAMPLE_NUMBER_VALUE)
    read_number_and_square_from_file(file_path)