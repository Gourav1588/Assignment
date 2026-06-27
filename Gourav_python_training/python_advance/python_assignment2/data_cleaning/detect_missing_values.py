"""
Detect missing values in a dataset.
"""

import pandas as pd


EMPLOYEE_DATA: dict[str, list] = {
    "Name": ["Rahul", "Priya", "Anuj"],
    "Age": [25, None, 29],
    "Salary": [30000, 40000, None],
}


def create_dataframe() -> pd.DataFrame:
    """
    Create employee DataFrame.

    Returns:
        pd.DataFrame: Employee data.
    """
    return pd.DataFrame(EMPLOYEE_DATA)


def detect_missing_values() -> pd.DataFrame:
    """
    Detect missing values in each column.

    Returns:
        pd.DataFrame: Boolean DataFrame showing missing values.
    """
    employee_dataframe = create_dataframe()

    return employee_dataframe.isnull()


def main() -> None:
    """Display missing value locations."""
    print("Missing Values:")
    print(detect_missing_values())


if __name__ == "__main__":
    main()