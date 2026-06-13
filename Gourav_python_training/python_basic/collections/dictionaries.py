# Q32, Q33, Q34 - Dictionaries

STUDENT_NAME = "Gourav"
STUDENT_ROLL = 101
STUDENT_SUBJECT = "Data Engineering"
STUDENT_MARKS = 92.5
FREQUENCY_TEXT = "programming"

def student_dictionary() -> None:
    """Create a student dictionary and access its values by key."""
    student = {
        "name": STUDENT_NAME,
        "roll_no": STUDENT_ROLL,
        "subject": STUDENT_SUBJECT,
        "marks": STUDENT_MARKS
    }

    print(f"Name:    {student['name']}")
    print(f"Roll No: {student['roll_no']}")
    print(f"Subject: {student['subject']}")
    print(f"Marks:   {student['marks']}")


def character_frequency() -> None:
    """Count how many times each character appears in a string."""
    text = FREQUENCY_TEXT
    freq = {}

    for char in text:
        freq[char] = freq.get(char, 0) + 1  # increment count or start at 1

    print(f"Character frequency in '{text}':")
    for char, count in freq.items():
        print(f"  '{char}': {count}")


def merge_dicts() -> None:
    """Merge two dictionaries into one using ** unpacking."""
    dict1 = {"name": "Gourav", "city": "Indore"}
    dict2 = {"course": "Python", "year": 2025}

    merged = {**dict1, **dict2}  # values from dict2 win on key conflict
    print(f"Dict 1:  {dict1}")
    print(f"Dict 2:  {dict2}")
    print(f"Merged:  {merged}")

 
if __name__ == "__main__":
    student_dictionary()
    print()
    character_frequency()
    print()
    merge_dicts()