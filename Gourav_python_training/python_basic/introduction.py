# Q1, Q2, Q3 - Introduction to Python

import sys


def print_welcome() -> None:
    """Print the training welcome message."""
    print("Welcome to Python Training")


def check_python_version() -> None:
    """Display the current Python version."""
    print(f"Python version: {sys.version}")


def greet_user() -> None:
    """Take name and age as input and print a formatted greeting."""
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    print(f"Hello {name}! You are {age} years old.")

 
if __name__ == "__main__":
  print_welcome()
  check_python_version()
  greet_user()