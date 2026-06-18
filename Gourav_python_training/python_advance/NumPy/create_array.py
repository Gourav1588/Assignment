"""
Create and display a NumPy array.
"""

import numpy as np

ARRAY_VALUES: list[int] = [10, 20, 30, 40, 50]


def create_numpy_array() -> np.ndarray:
    """
    Create a NumPy array from predefined values.

    Returns:
        np.ndarray: Created NumPy array.
    """
    return np.array(ARRAY_VALUES)


def main() -> None:
    """Run the array creation example."""
    numbers_array = create_numpy_array()
    print("NumPy Array:")
    print(numbers_array)


if __name__ == "__main__":
    main()