# Q12, Q13, Q14, Q15, Q16 - Loops


def print_one_to_hundred():
    """Print all numbers from 1 to 100 in a single line."""
    for i in range(1, 101):
        print(i, end=" ")
    print()


def multiplication_table(number):
    """Print the multiplication table of a given number up to 10."""
    print(f"\nMultiplication table of {number}:")
    for i in range(1, 11):
        print(f"{number} x {i} = {number * i}")


def factorial(n):
    """Calculate factorial of n using a loop."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    print(f"Factorial of {n} = {result}")


def reverse_number(number):
    """Reverse the digits of a number using a loop."""
    reversed_num = 0
    temp = abs(number)  # handle negatives
    while temp > 0:
        last_digit = temp % 10
        reversed_num = reversed_num * 10 + last_digit
        temp //= 10
    print(f"Reverse of {number} = {reversed_num}")


def check_prime(number):
    """Check if a number is prime by testing divisors up to its square root."""
    if number < 2:
        print(f"{number} is NOT prime")
        return
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            print(f"{number} is NOT prime")
            return
    print(f"{number} IS prime")


print_one_to_hundred()
multiplication_table(5)
factorial(6)
reverse_number(12345)
check_prime(29)