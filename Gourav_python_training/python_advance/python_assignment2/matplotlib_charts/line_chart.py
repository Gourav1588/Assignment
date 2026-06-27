
"""
Create a line chart showing salaries.
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


def create_line_chart() -> None:
    """Create line chart of employee salaries."""
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    plt.figure(figsize=(10, 5))

    plt.plot(
        employee_dataframe["Name"],
        employee_dataframe["Salary"],
        marker="o"
    )

    plt.title("Employee Salary Trend")
    plt.xlabel("Employee")
    plt.ylabel("Salary")

    plt.show()


if __name__ == "__main__":
    create_line_chart()