# Q3 - Write a regular expression to validate a 10-digit mobile number.

import re

# Constants
SAMPLE_VALID_MOBILE = "9876543210"
SAMPLE_INVALID_MOBILE = "98765432"


def validate_mobile_number(mobile) -> bool:
    """Validate a 10-digit mobile number using a regular expression."""
    # exactly 10 digits, nothing more or less
    pattern = r"^\d{10}$"
    is_valid = bool(re.match(pattern, mobile))
    print(f"Mobile: '{mobile}' -> Valid: {is_valid}")
    return is_valid


if __name__ == "__main__":
    validate_mobile_number(SAMPLE_VALID_MOBILE)
    validate_mobile_number(SAMPLE_INVALID_MOBILE)