"""
Create line chart for hours studied and marks.
"""

import pandas as pd
import matplotlib.pyplot as plt

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


def create_line_chart() -> None:
    """Visualize hours studied versus marks."""
    student_dataframe = pd.DataFrame(STUDENT_DATA)

    plt.figure(figsize=(8, 5))

    plt.plot(
        student_dataframe["Hours_Studied"],
        student_dataframe["Marks"],
        marker="o",
    )

    plt.title("Hours Studied vs Marks")
    plt.xlabel("Hours Studied")
    plt.ylabel("Marks")

    plt.show()


if __name__ == "__main__":
    create_line_chart()