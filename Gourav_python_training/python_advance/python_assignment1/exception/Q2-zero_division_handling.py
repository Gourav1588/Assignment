# Q2 - Divide two numbers entered by the user and handle ZeroDivisionError.

def divide_two_numbers() -> None:
    """Divide two numbers entered by the user and handle ZeroDivisionError."""

    numerator: float = float(input("Enter numerator: "))
    denominator: float = float(input("Enter denominator: "))

    try:
        result: float = numerator / denominator
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")


if __name__ == "__main__":
    divide_two_numbers()