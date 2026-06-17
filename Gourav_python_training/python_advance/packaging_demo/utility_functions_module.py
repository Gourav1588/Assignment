# Q1 - Create a module with two utility functions and import it into another Python file.
#
# This file IS the module. Import it from another file like this:
#   from python_advance.packaging_demo.utility_functions_module import convert_celsius_to_fahrenheit

CELSIUS_VALUE = 25
KILOMETERS_VALUE = 10


def convert_celsius_to_fahrenheit(celsius) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def convert_km_to_miles(kilometers) -> float:
    """Convert a distance from kilometers to miles."""
    return kilometers * 0.621371


if __name__ == "__main__":
    print(f"{CELSIUS_VALUE}°C in Fahrenheit: {convert_celsius_to_fahrenheit(CELSIUS_VALUE)}")
    print(f"{KILOMETERS_VALUE} km in miles: {convert_km_to_miles(KILOMETERS_VALUE)}")