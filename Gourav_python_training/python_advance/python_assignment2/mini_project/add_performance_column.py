"""
Add performance column based on marks.
"""

import pandas as pd

PASSING_MARKS: int = 65

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


def add_performance_column() -> pd.DataFrame:
    """
    Add Pass/Fail classification.

    Returns:
        pd.DataFrame: Updated DataFrame.
    """
    student_dataframe = pd.DataFrame(STUDENT_DATA)

    student_dataframe["Performance"] = student_dataframe[
        "Marks"
    ].apply(
        lambda marks: "Pass"
        if marks > PASSING_MARKS
        else "Fail"
    )

    return student_dataframe


def main() -> None:
    """Display performance results."""
    print(add_performance_column())


if __name__ == "__main__":
    main()