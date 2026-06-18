"""
Add bonus column to employee DataFrame.
"""

import pandas as pd

EMPLOYEE_DATA: dict[str, list] = {
    "Name": ["Rahul", "Priya", "Amit", "Anuj"],
    "Age": [25, 30, 28, 35],
    "Department": ["HR", "IT", "Finance", "IT"],
    "Salary": [30000, 50000, 45000, 60000],
}

BONUS_PERCENTAGE: float = 0.10


def add_bonus_column() -> pd.DataFrame:
    """
    Add bonus column.

    Returns:
        pd.DataFrame: Updated DataFrame.
    """
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    # Bonus is calculated as 10% of salary.
    employee_dataframe["Bonus"] = (
        employee_dataframe["Salary"] * BONUS_PERCENTAGE
    )

    return employee_dataframe


def main() -> None:
    """Display DataFrame with bonus column."""
    print(add_bonus_column())


if __name__ == "__main__":
    main()