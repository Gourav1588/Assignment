# Q35, Q36, Q37, Q38, Q39 - File Handling

import os

# Constants - no hardcoded values in functions
FILE_NAME = "gourav.txt"
COPY_FILE_NAME = "gourav_copy.txt"
OWNER_NAME = "Gourav"
APPEND_LINE_1 = "Python Training 2025\n"
APPEND_LINE_2 = "Data Engineering Batch\n"
SEARCH_WORD_1 = "Gourav"
SEARCH_WORD_2 = "Python"

OUTPUT_DIR = "file_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_name():
    """Create a file and write a name into it."""
    path = os.path.join(OUTPUT_DIR, FILE_NAME)
    with open(path, "w") as f:
        f.write(OWNER_NAME + "\n")
    print(f"File created: {path}")


def analyse_file():
    """Read a file and count its words, lines and characters."""
    path = os.path.join(OUTPUT_DIR, FILE_NAME)
    with open(path, "r") as f:
        content = f.read()
    print(f"Lines:      {len(content.splitlines())}")
    print(f"Words:      {len(content.split())}")
    print(f"Characters: {len(content)}")


def append_to_file():
    """Append new lines to an existing file without overwriting it."""
    path = os.path.join(OUTPUT_DIR, FILE_NAME)
    with open(path, "a") as f:
        f.write(APPEND_LINE_1)
        f.write(APPEND_LINE_2)
    print("Data appended successfully")


def copy_file():
    """Copy all content from one file into another file."""
    source = os.path.join(OUTPUT_DIR, FILE_NAME)
    destination = os.path.join(OUTPUT_DIR, COPY_FILE_NAME)
    with open(source, "r") as src:
        content = src.read()
    with open(destination, "w") as dst:
        dst.write(content)
    print(f"Copied '{source}' to '{destination}'")


def search_word(word):
    """Search for a word in a file and print the matching lines."""
    path = os.path.join(OUTPUT_DIR, FILE_NAME)
    found = False
    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            if word in line:
                print(f"Found '{word}' on line {line_num}: {line.strip()}")
                found = True
    if not found:
        print(f"'{word}' not found in file")

 
if __name__ == "__main__":
    write_name()
    append_to_file()
    print()
    analyse_file()
    print()
    copy_file()
    print()
    search_word(SEARCH_WORD_1)  
    search_word(SEARCH_WORD_2)