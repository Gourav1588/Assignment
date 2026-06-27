"""
Create a bar chart showing employee count by department.
"""

import pandas as pd
import matplotlib.pyplot as plt

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


def create_bar_chart() -> None:
    """Create department employee count bar chart."""
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    department_counts = employee_dataframe["Department"].value_counts()

    plt.figure(figsize=(8, 5))
    plt.bar(department_counts.index, department_counts.values)

    plt.title("Employee Count by Department")
    plt.xlabel("Department")
    plt.ylabel("Employee Count")

    plt.show()


if __name__ == "__main__":
    create_bar_chart()