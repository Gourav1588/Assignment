# Q1 - This file IMPORTS the module (utility_functions_module.py) and uses its functions.

from q1utility_functions_module import convert_celsius_to_fahrenheit,convert_km_to_miles

# Constants
SAMPLE_CELSIUS: float = 30
SAMPLE_KILOMETERS: float = 15


def use_imported_functions() -> None:
    """Use the two utility functions imported from utility_functions_module.py."""
    fahrenheit: float = convert_celsius_to_fahrenheit(SAMPLE_CELSIUS)
    miles: float = convert_km_to_miles(SAMPLE_KILOMETERS)

    print(f"{SAMPLE_CELSIUS}°C is {fahrenheit}°F")
    print(f"{SAMPLE_KILOMETERS} km is {miles} miles")


if __name__ == "__main__":
    use_imported_functions()