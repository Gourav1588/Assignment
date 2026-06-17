# Q4 - Use re.search() to check whether a word exists in a sentence.

import re

# Constants
SAMPLE_SENTENCE = "Python is a powerful programming language"
SEARCH_WORD = "powerful"


def search_word_in_sentence(sentence, word) -> bool:
    """Use re.search() to check whether a word exists in a sentence."""
    match = re.search(word, sentence)
    found = match is not None
    print(f"Sentence: '{sentence}'")
    print(f"'{word}' found: {found}")
    return found


if __name__ == "__main__":
    search_word_in_sentence(SAMPLE_SENTENCE, SEARCH_WORD)