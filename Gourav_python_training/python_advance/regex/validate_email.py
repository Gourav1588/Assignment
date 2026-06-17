# Q2 - Write a regular expression to validate an email address.

import re

# Constants
SAMPLE_VALID_EMAIL = "gourav.yadav@example.com"
SAMPLE_INVALID_EMAIL = "gourav.yadav@.com"


def validate_email(email) -> bool:
    """Validate an email address using a regular expression."""
    # username@domain.extension pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    is_valid = bool(re.match(pattern, email))
    print(f"Email: '{email}' -> Valid: {is_valid}")
    return is_valid


if __name__ == "__main__":
    validate_email(SAMPLE_VALID_EMAIL)
    validate_email(SAMPLE_INVALID_EMAIL)