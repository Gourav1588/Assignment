# Q35, Q36, Q37, Q38, Q39 - File Handling

import os

OUTPUT_DIR = "file_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # create folder if it doesn't exist


def write_name():
    """Create a file and write a name into it."""
    path = f"{OUTPUT_DIR}/gourav.txt"
    with open(path, "w") as f:
        f.write("Gourav\n")
    print(f"File created: {path}")


def analyse_file():
    """Read a file and count its words, lines and characters."""
    path = f"{OUTPUT_DIR}/gourav.txt"
    with open(path, "r") as f:
        content = f.read()
    print(f"Lines:      {len(content.splitlines())}")
    print(f"Words:      {len(content.split())}")
    print(f"Characters: {len(content)}")


def append_to_file():
    """Append new lines to an existing file without overwriting it."""
    path = f"{OUTPUT_DIR}/gourav.txt"
    with open(path, "a") as f:  # 'a' mode keeps existing content
        f.write("Python Training 2026\n")
        f.write("Data Engineering Batch\n")
    print("Data appended successfully")


def copy_file():
    """Copy all content from one file into another file."""
    source = f"{OUTPUT_DIR}/gourav.txt"
    destination = f"{OUTPUT_DIR}/gourav_copy.txt"
    with open(source, "r") as src:
        content = src.read()
    with open(destination, "w") as dst:
        dst.write(content)
    print(f"Copied '{source}' to '{destination}'")


def search_word(word):
    """Search for a word in a file and print the matching lines."""
    path = f"{OUTPUT_DIR}/gourav.txt"
    found = False
    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            if word in line:
                print(f"Found '{word}' on line {line_num}: {line.strip()}")
                found = True
    if not found:
        print(f"'{word}' not found in file")


write_name()
append_to_file()
print()
analyse_file()
print()
copy_file()
print()
search_word("Gourav")
search_word("Python")