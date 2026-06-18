"""
Generate summary statistics for employee data.
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

def generate_summary_statistics() -> pd.DataFrame:
    """
    Generate summary statistics.

    Returns:
        pd.DataFrame: Statistics table.
    """
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    return employee_dataframe.describe()


def main() -> None:
    """Display summary statistics."""
    print(generate_summary_statistics())


if __name__ == "__main__":
    main()