# Q4 - Handle multiple exceptions in a single program.

# Constants
INPUT_A_VALID = "10"
INPUT_B_ZERO = "0"
INPUT_A_INVALID = "abc"
INPUT_B_VALID = "5"


def handle_multiple_exceptions(value_a, value_b) -> None:
    """Handle multiple exception types in a single program."""
    try:
        num_a = int(value_a)
        num_b = int(value_b)
        result = num_a / num_b
        print(f"Result: {result}")
    except ValueError:
        print("Error: Both inputs must be valid integers.")
    except ZeroDivisionError:
        print("Error: Second number cannot be zero.")


if __name__ == "__main__":
    handle_multiple_exceptions(INPUT_A_VALID, INPUT_B_ZERO)
    handle_multiple_exceptions(INPUT_A_INVALID, INPUT_B_VALID)