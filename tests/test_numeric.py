import numpy as np
import time
from git_template.numeric import fib, prime_factors


def fib_naive(n):
    if n < 1 or (not isinstance(n, int)):
        return None
    elif n == 1 or n == 2:
        return n - 1
    else:
        return fib_naive(n - 1) + fib_naive(n - 2)


def test_fib():
    inputs = [-1, 0, 1, 2, 5, 10]
    outputs = [None, None, 0, 1, 3, 34]
    for i in range(len(inputs)):
        assert fib(inputs[i]) == outputs[i]

    fib_time_input = 20
    start_time = time.time()
    fib(fib_time_input)
    time_fib = time.time() - start_time

    start_time = time.time()
    fib_naive(fib_time_input)
    time_fib_naive = time.time() - start_time

    assert time_fib_naive > time_fib

    return None


def test_prime_factors():
    inputs = [-1, 0, 1, 2, 5, 10, 60, 49]
    outputs = [None, None, "", "2", "5", "25", "2235", "77"]
    for i in range(len(inputs)):
        assert prime_factors(inputs[i]) == outputs[i]

    return None


if __name__ == "__main__":
    test_fib()
    test_prime_factors()
