# Q5 - Use re.findall() to extract all words starting with a capital letter.

import re

# Constants
SAMPLE_TEXT = "Gourav went to Indore with Priya and Rahul"


def find_all_capitalized_words(text) -> list[str]:
    """Use re.findall() to extract all words starting with a capital letter."""
    # \b[A-Z][a-z]* matches a word boundary, one capital letter, then lowercase letters
    capitalized_words = re.findall(r"\b[A-Z][a-z]*", text)
    print(f"Text:  {text}")
    print(f"Words: {capitalized_words}")
    return capitalized_words


if __name__ == "__main__":
    find_all_capitalized_words(SAMPLE_TEXT)