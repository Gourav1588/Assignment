# Q7, Q8, Q9, Q10, Q11 - Operators and Conditionals


def check_even_odd(number):
    """Check whether a number is even or odd."""
    if number % 2 == 0:
        print(f"{number} is Even")
    else:
        print(f"{number} is Odd")


def check_sign(number):
    """Check whether a number is positive, negative or zero."""
    if number > 0:
        print(f"{number} is Positive")
    elif number < 0:
        print(f"{number} is Negative")
    else:
        print("The number is Zero")


def find_largest(a, b, c):
    """Find and print the largest among three numbers."""
    largest = max(a, b, c)
    print(f"Largest of {a}, {b}, {c} is: {largest}")


def calculate_grade(marks):
    """Calculate letter grade based on marks out of 100."""
    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    else:
        grade = "Fail"
    print(f"Marks: {marks} => Grade: {grade}")


def check_leap_year(year):
    """Check whether a year is a leap year."""
    # Divisible by 4 but not 100, OR divisible by 400
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print(f"{year} is a Leap Year")
    else:
        print(f"{year} is NOT a Leap Year")


check_even_odd(7)
check_sign(-3)
find_largest(10, 42, 27)
calculate_grade(85)
check_leap_year(2024)