# Q3 - First module inside sample_package

NAME = "Gourav"


def greet_morning(name) -> str:
    """Return a morning greeting for the given name."""
    return f"Good morning, {name}!"


def greet_evening(name) -> str:
    """Return an evening greeting for the given name."""
    return f"Good evening, {name}!"


if __name__ == "__main__":
    print(greet_morning(NAME))
    print(greet_evening(NAME))