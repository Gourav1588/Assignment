"""
Create a seaborn barplot for department salary comparison.
"""

import pandas as pd
import seaborn as sns
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


def create_department_salary_barplot() -> None:
    """Visualize average salary by department."""
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=employee_dataframe,
        x="Department",
        y="Salary",
    )

    plt.title("Department vs Salary")
    plt.show()


if __name__ == "__main__":
    create_department_salary_barplot()