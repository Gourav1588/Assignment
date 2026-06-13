# Q28, Q29, Q30, Q31 - Tuples and Sets


def tuple_demo() -> None:
    """Create a tuple and access its elements using index and slicing."""
    student = ("Gourav", 22, "Data Engineering", 9.1)

    print(f"Full tuple:    {student}")
    print(f"First element: {student[0]}")    # index from start
    print(f"Last element:  {student[-1]}")   # index from end
    print(f"Slice [1:3]:   {student[1:3]}")  # slicing


def tuple_to_list() -> None:
    """Convert a tuple to a list and modify an element."""
    coordinates = (10, 20, 30)
    print(f"Original tuple: {coordinates}")

    # Tuples are immutable, so convert to list to modify
    coords_list = list(coordinates)
    coords_list[1] = 99
    print(f"Modified list:  {coords_list}")


def set_operations() -> None:
    """Perform union, intersection and difference on two sets."""
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}

    print(f"Set A:        {set_a}")
    print(f"Set B:        {set_b}")
    print(f"Union:        {set_a | set_b}")  # all elements from both
    print(f"Intersection: {set_a & set_b}")  # only common elements
    print(f"Difference:   {set_a - set_b}")  # in A but not in B


def remove_duplicates() -> None:
    """Remove duplicate values from a list using a set."""
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    unique = sorted(set(numbers))  # set drops duplicates, sorted for clean output
    print(f"With duplicates:    {numbers}")
    print(f"Without duplicates: {unique}")

 
if __name__ == "__main__":
    tuple_demo()
    print()
    tuple_to_list()
    print()
    set_operations()
    print()
    remove_duplicates()