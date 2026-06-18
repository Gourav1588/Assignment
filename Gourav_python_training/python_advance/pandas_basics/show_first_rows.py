"""
Display first two rows from employee DataFrame.
"""

import pandas as pd

EMPLOYEE_DATA: dict[str, list] = {
    "Name": [
        "Rahul",
        "Priya",
        "Amit",
        "Anuj",
        "Neha",
        "Vikas",
        "Rohit",
        "Sneha",
        "Pooja",
        "Karan",
        ],
    "Age": [25, 30, 28, 35, 27, 32, 29, 31, 26, 34],
    "Department": [
        "HR",
        "IT",
        "Finance",
        "IT",
        "HR",
        "Finance",
        "IT",
        "HR",
        "Finance",
        "IT",
    ],
    "Salary": [
        30000,
        50000,
        45000,
        60000,
        35000,
        55000,
        52000,
        38000,
        48000,
        65000,
    ],
}

ROW_COUNT: int = 2


def get_first_rows() -> pd.DataFrame:
    """
    Return first rows of DataFrame.

    Returns:
        pd.DataFrame: First rows.
    """
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    return employee_dataframe.head(ROW_COUNT)


def main() -> None:
    """Display first rows."""
    print(get_first_rows())


if __name__ == "__main__":
    main()