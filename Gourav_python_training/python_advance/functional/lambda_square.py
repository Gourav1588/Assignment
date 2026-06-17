# Q1 - Write a lambda function to find the square of a number.

# Constants
SQUARE_INPUT = 6

# Lambda function for square
square_lambda = lambda number: number ** 2


if __name__ == "__main__":
    print(f"Square of {SQUARE_INPUT} = {square_lambda(SQUARE_INPUT)}")