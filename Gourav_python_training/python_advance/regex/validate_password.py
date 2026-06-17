# Q8 - Create a password validation program using regex (minimum length, one digit, one special character).

import re

# Constants
SAMPLE_STRONG_PASSWORD = "Pass@123"
SAMPLE_WEAK_PASSWORD = "password"
MIN_PASSWORD_LENGTH = 8


def validate_password(password) -> bool:
    """Validate a password: minimum length, at least one digit, one special character."""
    has_min_length = len(password) >= MIN_PASSWORD_LENGTH
    has_digit = bool(re.search(r"\d", password))
    has_special_char = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    is_valid = has_min_length and has_digit and has_special_char

    print(f"Password: '{password}'")
    print(f"  Min length ({MIN_PASSWORD_LENGTH}+): {has_min_length}")
    print(f"  Has digit:               {has_digit}")
    print(f"  Has special character:   {has_special_char}")
    print(f"  Overall valid:           {is_valid}")
    return is_valid


if __name__ == "__main__":
    validate_password(SAMPLE_STRONG_PASSWORD)
    validate_password(SAMPLE_WEAK_PASSWORD)