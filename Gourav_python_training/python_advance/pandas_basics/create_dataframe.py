"""
Create an employee DataFrame using Pandas.
"""

import pandas as pd

EMPLOYEE_DATA: dict[str, list] = {
    "Name": ["Rahul", "Priya", "Amit", "Anuj"],
    "Age": [25, 30, 28, 35],
    "Department": ["HR", "IT", "Finance", "IT"],
    "Salary": [30000, 50000, 45000, 60000],
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