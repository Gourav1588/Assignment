# Q7 - Create a custom exception called AgeException and raise it if age is less than 18.

# Constants
MIN_VALID_AGE = 18
UNDERAGE_TEST_VALUE = 15
VALID_AGE_TEST_VALUE = 25


class AgeException(Exception):
    """Custom exception raised when age is below the minimum allowed age."""

    def __init__(self, age) -> None:
        """Store the invalid age and build a descriptive error message."""
        self.age = age
        message = f"Age {age} is invalid. Minimum required age is {MIN_VALID_AGE}."
        super().__init__(message)


def validate_age(age) -> None:
    """Check age and raise AgeException if it is below the minimum allowed age."""
    if age < MIN_VALID_AGE:
        raise AgeException(age)
    print(f"Age {age} is valid.")


if __name__ == "__main__":
    try:
        validate_age(UNDERAGE_TEST_VALUE)
    except AgeException as error:
        print(f"Caught error: {error}")

    validate_age(VALID_AGE_TEST_VALUE)