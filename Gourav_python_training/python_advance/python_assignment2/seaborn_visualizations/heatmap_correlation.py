"""
Create a correlation heatmap for Age and Salary.
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


def create_correlation_heatmap() -> None:
    """Visualize correlation between Age and Salary."""
    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    correlation_matrix = employee_dataframe[
        ["Age", "Salary"]
    ].corr()

    plt.figure(figsize=(6, 4))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="Blues"
    )

    plt.title("Age and Salary Correlation")
    plt.show()


if __name__ == "__main__":
    create_correlation_heatmap()