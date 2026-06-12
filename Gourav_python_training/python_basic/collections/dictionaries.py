# Q32, Q33, Q34 - Dictionaries


def student_dictionary():
    """Create a student dictionary and access its values by key."""
    student = {
        "name": "Gourav",
        "roll_no": 101,
        "subject": "Data Engineering",
        "marks": 92.5
    }

    print(f"Name:    {student['name']}")
    print(f"Roll No: {student['roll_no']}")
    print(f"Subject: {student['subject']}")
    print(f"Marks:   {student['marks']}")


def character_frequency():
    """Count how many times each character appears in a string."""
    text = "programming"
    freq = {}

    for char in text:
        freq[char] = freq.get(char, 0) + 1  # increment count or start at 1

    print(f"Character frequency in '{text}':")
    for char, count in freq.items():
        print(f"  '{char}': {count}")


def merge_dicts():
    """Merge two dictionaries into one using ** unpacking."""
    dict1 = {"name": "Gourav", "city": "Indore"}
    dict2 = {"course": "Python", "year": 2025}

    merged = {**dict1, **dict2}  # values from dict2 win on key conflict
    print(f"Dict 1:  {dict1}")
    print(f"Dict 2:  {dict2}")
    print(f"Merged:  {merged}")


student_dictionary()
print()
character_frequency()
print()
merge_dicts()