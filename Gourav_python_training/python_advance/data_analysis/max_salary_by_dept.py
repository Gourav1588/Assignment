"""
Find maximum salary for each department.
"""

import pandas as pd

EMPLOYEE_DATA: dict[str, list] = {
    "Name": [
        "Rahul", "Priya", "Amit", "Anuj", "Neha",
        "Vikas", "Rohit", "Sneha", "Pooja", "Karan"
    ],
    "Age": [25, 30, 28, 35, 27, 32, 29, 31, 26, 34],
    "Department": [
        "HR", "IT", "Finance", "IT", "HR",
        "Finance", "IT", "HR", "Finance", "IT"
    ],
    "Salary": [
        30000, 50000, 45000, 60000, 35000,
        55000, 52000, 38000, 48000, 65000
    ],
}


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create employee DataFrame.

    Returns:
        pd.DataFrame: Employee dataset.
    """
    return pd.DataFrame(EMPLOYEE_DATA)


def calculate_max_salary_by_department() -> pd.Series:
    """
    Find maximum salary for each department.

    Returns:
        pd.Series: Maximum salary by department.
    """
    employee_dataframe = create_employee_dataframe()

    return employee_dataframe.groupby("Department")["Salary"].max()


def main() -> None:
    """Display maximum salary by department."""
    print("Maximum Salary By Department")
    print(calculate_max_salary_by_department())


if __name__ == "__main__":
    main()