# Q17, Q18, Q19, Q20 - Functions


def square(number):
    """Return the square of a number."""
    return number ** 2


def is_palindrome(value):
    """Check if a number or string reads the same forwards and backwards."""
    text = str(value)
    if text == text[::-1]:  # [::-1] reverses the string
        print(f"'{value}' IS a palindrome")
    else:
        print(f"'{value}' is NOT a palindrome")


def find_max(numbers):
    """Return the maximum value from a list."""
    return max(numbers)


def greet(name, message="Hello"):
    """Greet a person with a message. Default message is Hello."""
    print(f"{message}, {name}!")


print(f"Square of 9 = {square(9)}")

is_palindrome(121)
is_palindrome("racecar")
is_palindrome("hello")

numbers = [3, 7, 1, 9, 4]
print(f"Max in list: {find_max(numbers)}")

greet("Gourav")
greet("Gourav", message="Namaste")