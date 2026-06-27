"""
Create an employee DataFrame using Pandas.
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


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create employee DataFrame.

    Returns:
        pd.DataFrame: Employee data.
    """
    return pd.DataFrame(EMPLOYEE_DATA)


def main() -> None:
    """Display employee DataFrame."""
    employee_dataframe = create_employee_dataframe()

    print("Employee DataFrame:")
    print(employee_dataframe)


if __name__ == "__main__":
    main()