"""
Calculate basic statistics using NumPy.
"""

import numpy as np

ARRAY_VALUES: list[int] = [10, 20, 30, 40, 50]


def calculate_statistics() -> dict[str, float]:
    """
    Calculate mean, max, min and sum.

    Returns:
        dict[str, float]: Statistics result.
    """
    numbers_array = np.array(ARRAY_VALUES)

    return {
        "mean": float(np.mean(numbers_array)),
        "max": float(np.max(numbers_array)),
        "min": float(np.min(numbers_array)),
        "sum": float(np.sum(numbers_array)),
    }


def main() -> None:
    """Display statistics."""
    statistics = calculate_statistics()

    print(f"Mean: {statistics['mean']}")
    print(f"Max: {statistics['max']}")
    print(f"Min: {statistics['min']}")
    print(f"Sum: {statistics['sum']}")


if __name__ == "__main__":
    main()