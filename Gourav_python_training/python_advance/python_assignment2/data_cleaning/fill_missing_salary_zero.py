"""
Replace missing salary values with zero.
"""

import pandas as pd


EMPLOYEE_DATA: dict[str, list] = {
    "Name": ["Rahul", "Priya", "Anuj"],
    "Age": [25, None, 29],
    "Salary": [30000, 40000, None],
}

DEFAULT_SALARY: int = 0


def create_dataframe() -> pd.DataFrame:
    """
    Create employee DataFrame.

    Returns:
        pd.DataFrame: Employee data.
    """
    return pd.DataFrame(EMPLOYEE_DATA)


def fill_missing_salary() -> pd.DataFrame:
    """
    Replace missing salary with zero.

    Returns:
        pd.DataFrame: Updated DataFrame.
    """
    employee_dataframe = create_dataframe()

    employee_dataframe["Salary"] = employee_dataframe[
        "Salary"
    ].fillna(DEFAULT_SALARY)

    return employee_dataframe


def main() -> None:
    """Display DataFrame after salary replacement."""
    print(fill_missing_salary())


if __name__ == "__main__":
    main()