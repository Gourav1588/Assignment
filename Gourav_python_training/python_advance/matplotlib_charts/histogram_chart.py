"""
Create salary histogram.
"""

import matplotlib.pyplot as plt

SALARIES: list[int] = [
    30000,
    40000,
    50000,
    60000,
    45000,
]


def create_histogram() -> None:
    """Display salary distribution."""
    plt.figure(figsize=(8, 5))

    plt.hist(SALARIES, bins=5,edgecolor="black")

    plt.title("Salary Distribution")
    plt.xlabel("Salary")
    plt.ylabel("Frequency")

    plt.show()


if __name__ == "__main__":
    create_histogram()