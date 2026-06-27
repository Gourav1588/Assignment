# Q6 - Replace multiple spaces in a string with a single space using re.sub().

import re

# Constants
SAMPLE_TEXT = "This   text has    multiple     spaces"


def replace_multiple_spaces(text) -> str:
    """Replace multiple spaces in a string with a single space using re.sub()."""
    # \s+ matches one or more whitespace characters
    cleaned_text = re.sub(r"\s+", " ", text)
    print(f"Original: '{text}'")
    print(f"Cleaned:  '{cleaned_text}'")
    return cleaned_text


if __name__ == "__main__":
    replace_multiple_spaces(SAMPLE_TEXT)