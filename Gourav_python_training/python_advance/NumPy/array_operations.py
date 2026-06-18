"""
Perform arithmetic operations on NumPy arrays.
"""

import numpy as np

FIRST_ARRAY_VALUES: list[int] = [1, 2, 3]
SECOND_ARRAY_VALUES: list[int] = [4, 5, 6]


def perform_array_operations() -> tuple[np.ndarray, np.ndarray]:
    """
    Perform addition and multiplication.

    Returns:
        tuple[np.ndarray, np.ndarray]: Addition and multiplication results.
    """
    first_array = np.array(FIRST_ARRAY_VALUES)
    second_array = np.array(SECOND_ARRAY_VALUES)

    addition_result = first_array + second_array

    # Element-wise multiplication
    multiplication_result = first_array * second_array

    return addition_result, multiplication_result


def main() -> None:
    """Display arithmetic operation results."""
    addition_result, multiplication_result = perform_array_operations()

    print("Addition:")
    print(addition_result)

    print("\nMultiplication:")
    print(multiplication_result)


if __name__ == "__main__":
    main()