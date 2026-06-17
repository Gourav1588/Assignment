# Q7 - Write a pattern to check if a string contains only alphabets.

import re

# Constants
ALPHA_ONLY_TEXT = "HelloWorld"
ALPHA_WITH_NUMBERS_TEXT = "Hello123"


def check_only_alphabets(text) -> bool:
    """Check if a string contains only alphabets using a regex pattern."""
    # ^[A-Za-z]+$ matches start to end with only letters, nothing else
    is_alpha_only = bool(re.match(r"^[A-Za-z]+$", text))
    print(f"Text: '{text}' -> Only alphabets: {is_alpha_only}")
    return is_alpha_only


if __name__ == "__main__":
    check_only_alphabets(ALPHA_ONLY_TEXT)
    check_only_alphabets(ALPHA_WITH_NUMBERS_TEXT)