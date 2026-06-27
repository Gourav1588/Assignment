"""
Load student dataset into a DataFrame.
"""

import pandas as pd

STUDENT_DATA: dict[str, list] = {
    "Name": [
        "Rahul",
        "Priya",
        "Siri",
        "Anuj",
        "Neha",
        "Vikas",
        "Rohit",
        "Sneha",
    ],
    "Marks": [70, 80, 90, 60, 85, 75, 55, 95],
    "Hours_Studied": [2, 3, 5, 1, 4, 3, 1, 6],
}


def load_student_data() -> pd.DataFrame:
    """
    Create student DataFrame.

    Returns:
        pd.DataFrame: Student dataset.
    """
    return pd.DataFrame(STUDENT_DATA)


def main() -> None:
    """Display student dataset."""
    print(load_student_data())


if __name__ == "__main__":
    main()