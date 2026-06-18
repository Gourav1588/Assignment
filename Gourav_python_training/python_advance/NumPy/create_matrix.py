"""
Create a 3x3 matrix using NumPy.
"""

import numpy as np

ROW_COUNT: int = 3
COLUMN_COUNT: int = 3


def create_matrix() -> np.ndarray:
    """
    Create a 3x3 matrix.

    Returns:
        np.ndarray: Matrix.
    """
    return np.arange(1, 10).reshape(ROW_COUNT, COLUMN_COUNT)


def main() -> None:
    """Display matrix."""
    matrix = create_matrix()

    print("3x3 Matrix:")
    print(matrix)


if __name__ == "__main__":
    main()