# Q8 - Handle FileNotFoundError when trying to open a file.

# Constants
MISSING_FILE_NAME = "does_not_exist.txt"


def open_missing_file(file_path) -> None:
    """Try to open a file and handle FileNotFoundError if it does not exist."""
    try:
        with open(file_path, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error: '{file_path}' does not exist.")


if __name__ == "__main__":
    open_missing_file(MISSING_FILE_NAME)