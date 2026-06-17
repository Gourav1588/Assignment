# Q1 - Write a program to extract all numbers from a given string using regular expressions.

import re

# Constants
SAMPLE_TEXT = "I have 2 apples, 15 oranges and 100 mangoes."


def extract_all_numbers(text) -> list[str]:
    """Extract all numbers from a given string using regular expressions."""
    # \d+ matches one or more digits in a row
    numbers = re.findall(r"\d+", text)
    print(f"Text:    {text}")
    print(f"Numbers: {numbers}")
    return numbers


if __name__ == "__main__":
    extract_all_numbers(SAMPLE_TEXT)