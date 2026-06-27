# Q2 - Write pytest test cases for a function that checks whether a number is prime.


def is_prime(number) -> bool:
    """Check whether a number is prime. (Function under test)"""
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def test_prime_number_returns_true() -> None:
    """A known prime number should return True."""
    assert is_prime(7) is True


def test_non_prime_number_returns_false() -> None:
    """A known non-prime number should return False."""
    assert is_prime(10) is False


def test_number_less_than_two_is_not_prime() -> None:
    """Numbers less than 2 should never be considered prime."""
    assert is_prime(1) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False


def test_two_is_prime() -> None:
    """The number 2 is the smallest prime number."""
    assert is_prime(2) is True


def test_large_prime_number() -> None:
    """A larger prime number should still be correctly identified."""
    assert is_prime(97) is True


def test_large_non_prime_number() -> None:
    """A larger non-prime number should still be correctly identified."""
    assert is_prime(100) is False