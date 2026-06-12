# Q4, Q5, Q6 - Variables and Data Types


def show_data_types():
    """Create variables of each type and print their types."""
    num = 10
    price = 3.14
    name = "Gourav"
    is_active = True

    print(type(num))        # int
    print(type(price))      # float
    print(type(name))       # str
    print(type(is_active))  # bool


def swap_numbers():
    """Swap two numbers using Python one-line swap."""
    a = 5
    b = 10
    print(f"Before swap: a={a}, b={b}")
    a, b = b, a
    print(f"After swap:  a={a}, b={b}")


def basic_arithmetic():
    """Print sum, difference, product and division of two numbers."""
    a = 20
    b = 4
    print(f"Sum:        {a + b}")
    print(f"Difference: {a - b}")
    print(f"Product:    {a * b}")
    print(f"Division:   {a / b}")


show_data_types()
swap_numbers()
basic_arithmetic()