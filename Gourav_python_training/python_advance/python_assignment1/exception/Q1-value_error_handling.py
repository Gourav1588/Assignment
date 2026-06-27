# Q1 - Take a number as input and handle ValueError if it is not a valid integer.

def take_integer_input() -> None:
    """Take a number as input and handle ValueError if it is not a valid integer."""
    user_input = input("Enter a number: ")
    try:
        number = int(user_input)
        print(f"You entered: {number}")
    except ValueError:
        print("Error: That is not a valid integer.")


if __name__ == "__main__":
    take_integer_input()