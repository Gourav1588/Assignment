"""
Replace missing age values with mean age.
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


def fill_missing_age_with_mean() -> pd.DataFrame:
    """
    Replace missing age with average age.

    Returns:
        pd.DataFrame: Updated DataFrame.
    """
    employee_dataframe = create_dataframe()

    average_age = employee_dataframe["Age"].mean()

    employee_dataframe["Age"] = employee_dataframe["Age"].fillna(
        average_age
    )

    return employee_dataframe


def main() -> None:
    """Display DataFrame after replacing age."""
    print(fill_missing_age_with_mean())


if __name__ == "__main__":
    main()