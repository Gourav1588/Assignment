# Q1, Q2, Q3 - Introduction to Python

import sys


def print_welcome():
    """Print the training welcome message."""
    print("Welcome to Python Training")


def check_python_version():
    """Display the current Python version."""
    print(f"Python version: {sys.version}")


def greet_user():
    """Take name and age as input and print a formatted greeting."""
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    print(f"Hello {name}! You are {age} years old.")


print_welcome()
check_python_version()
greet_user()