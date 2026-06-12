# Q22, Q23, Q24 - Modules

import math
import random


def use_math_module():
    """Demonstrate sqrt, power and factorial from the math module."""
    number = 25
    print(f"Square root of {number}: {math.sqrt(number)}")
    print(f"Power 2^8:               {math.pow(2, 8)}")
    print(f"Factorial of 6:          {math.factorial(6)}")


def generate_random():
    """Generate random numbers using the random module."""
    print(f"Random number (1-100): {random.randint(1, 100)}")
    print(f"Random float:          {round(random.random(), 4)}")
    print(f"Random from list:      {random.choice(['Python', 'Java', 'C++'])}")


def custom_module_demo():
    """Show how this file itself acts as a custom importable module."""
    print("This file (modules.py) is a custom module.")
    print("Import it with: from python_basic.modules import use_math_module")


use_math_module()
print()
generate_random()
print()
custom_module_demo()