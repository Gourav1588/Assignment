"""
Create seaborn barplot for performance comparison.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

PASSING_MARKS: int = 65

STUDENT_DATA: dict[str, list] = {
    "Name": [
        "Rahul",
        "Priya",
        "Siri",
        "Anuj",
        "Neha",
        "Vikas",
        "Rohit",
        "Sneha",
    ],
    "Marks": [70, 80, 90, 60, 85, 75, 55, 95],
    "Hours_Studied": [2, 3, 5, 1, 4, 3, 1, 6],
}


def create_performance_barplot() -> None:
    """Visualize performance against marks."""
    student_dataframe = pd.DataFrame(STUDENT_DATA)

    student_dataframe["Performance"] = student_dataframe[
        "Marks"
    ].apply(
        lambda marks: "Pass"
        if marks > PASSING_MARKS
        else "Fail"
    )

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=student_dataframe,
        x="Performance",
        y="Marks",
    )

    plt.title("Performance vs Marks")

    plt.show()


if __name__ == "__main__":
    create_performance_barplot()