"""
Generate summary statistics for employee data.
"""

import pandas as pd

EMPLOYEE_DATA: dict[str, list] = {
    "Name": ["Rahul", "Priya", "Amit", "Anuj"],
    "Age": [25, 30, 28, 35],
    "Department": ["HR", "IT", "Finance", "IT"],
    "Salary": [30000, 50000, 45000, 60000],
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