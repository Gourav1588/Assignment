# Constants
RISKY_VALUE: str = "config.txt"


def catch_all_exceptions(risky_value) -> None:
    """Catch all exceptions using a generic Exception handler and print the message."""
    try:
        # Attempting to open and read a file provided by a user or external source
        with open(risky_value, "r") as file:
            content = file.read()
            print(f"File content successfully loaded:\n{content}")
    except Exception as error:
        # Exception catches almost everything (FileNotFoundError, PermissionError, IsADirectoryError, etc.)
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    catch_all_exceptions(RISKY_VALUE)