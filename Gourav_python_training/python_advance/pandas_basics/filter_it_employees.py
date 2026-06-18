"""
Filter employees from IT department.
"""

import pandas as pd

EMPLOYEE_DATA: dict[str, list] = {
    "Name": ["Rahul", "Priya", "Amit", "Anuj"],
    "Age": [25, 30, 28, 35],
    "Department": ["HR", "IT", "Finance", "IT"],
    "Salary": [30000, 50000, 45000, 60000],
}

IT_DEPARTMENT: str = "IT"


def filter_it_employees() -> pd.DataFrame:
    """
    Filter employees belonging to IT department.

    Returns:
        pd.DataFrame: IT employees.
    """
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    return employee_dataframe[
        employee_dataframe["Department"] == IT_DEPARTMENT
    ]


def main() -> None:
    """Display IT employees."""
    print(filter_it_employees())


if __name__ == "__main__":
    main()