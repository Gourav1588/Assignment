# Q25, Q26, Q27 - Lists


def analyse_list():
    """Find sum, max, sorted order and unique values from a list of 10 numbers."""
    numbers = [4, 7, 2, 9, 1, 5, 3, 8, 6, 2]  # has one duplicate: 2

    print(f"Original list:  {numbers}")
    print(f"Sum:            {sum(numbers)}")
    print(f"Max:            {max(numbers)}")
    print(f"Sorted:         {sorted(numbers)}")
    print(f"No duplicates:  {sorted(set(numbers))}")  # set removes duplicates


def count_even_odd():
    """Count how many numbers in a list are even and how many are odd."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_count = 0
    odd_count = 0

    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    print(f"Even count: {even_count}")
    print(f"Odd count:  {odd_count}")


def reverse_list():
    """Reverseing  a list manually without using the built-in reverse() method."""
    numbers = [10, 20, 30, 40, 50]
    reversed_list = []

    # Loop from the last index down to 0
    for i in range(len(numbers) - 1, -1, -1):
        reversed_list.append(numbers[i])

    print(f"Original: {numbers}")
    print(f"Reversed: {reversed_list}")


analyse_list()
print()
count_even_odd()
print()
reverse_list()