# Q17, Q18, Q19, Q20 - Functions

SQUARE_NUMBER = 9
PALINDROME_NUMBER = 121
PALINDROME_STRING_TRUE = "racecar"
PALINDROME_STRING_FALSE = "hello"
NUMBERS_LIST = [3, 7, 1, 9, 4]
GREET_NAME = "Gourav"


def square(number) -> int :
    """Return the square of a number."""
    return number ** 2


def is_palindrome(value) -> None:
    """Check if a number or string reads the same forwards and backwards."""
    text = str(value)
    if text == text[::-1]:  # [::-1] reverses the string
        print(f"'{value}' IS a palindrome")
    else:
        print(f"'{value}' is NOT a palindrome")


def find_max(numbers) -> int:
    """Return the maximum value from a list."""
    return max(numbers)


def greet(name, message="Hello") -> None:
    """Greet a person with a message. Default message is Hello."""
    print(f"{message}, {name}!")

 
if __name__ == "__main__":
    print(f"Square of {SQUARE_NUMBER} = {square(SQUARE_NUMBER)}")
    is_palindrome(PALINDROME_NUMBER)
    is_palindrome(PALINDROME_STRING_TRUE)
    is_palindrome(PALINDROME_STRING_FALSE)
    numbers: list[int] = NUMBERS_LIST
    print(f"Max in list: {find_max(numbers)}")
    greet(GREET_NAME)
    greet(GREET_NAME, message="Namaste")