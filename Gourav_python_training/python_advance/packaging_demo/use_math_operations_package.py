# Q4 - This file USES the math_operations_package by importing from it.

from math_operations_package.basic_operations import add, subtract, multiply, divide

# Constants
NUM_A = 10
NUM_B = 4


def use_math_operations_package() -> None:
    """Use the math_operations_package to perform basic arithmetic."""
    print(f"{NUM_A} + {NUM_B} = {add(NUM_A, NUM_B)}")
    print(f"{NUM_A} - {NUM_B} = {subtract(NUM_A, NUM_B)}")
    print(f"{NUM_A} * {NUM_B} = {multiply(NUM_A, NUM_B)}")
    print(f"{NUM_A} / {NUM_B} = {divide(NUM_A, NUM_B)}")


if __name__ == "__main__":
    use_math_operations_package()