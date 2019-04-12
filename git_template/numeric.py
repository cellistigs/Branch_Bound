""" Licensing and authorship go here. """

import numpy as np

""" This file contains example source code, which can be unit tested
    in tests/ with pytest.  Unit tests for this code are automatically 
    run with each git commit (see .travis.yml). """


def fib(n):
    """Returns the nth number (1-indexing) of the Fibonacci sequence

		# Arguments 
            n (int): Index of the Fibonacci sequence to return.
    
        # Returns 
            (int): nth number of the Fibonacci sequence.
    
    """

    if n < 1 or (not isinstance(n, int)):
        return None

    fib_seq = [0, 1]

    for i in range(2, n):
        fib_seq.append(fib_seq[i - 1] + fib_seq[i - 2])

    return fib_seq[n - 1]


def prime_factors(n):
    """Finds the prime factorization of a positive integer.

		# Arguments 
            n (int): Number to prime factorize.
    
        # Returns 
            (string): Ordered prime factors with repetition.
    
    """

    if n < 1 or (not isinstance(n, int)):
        return None

    prime_str = ""

    # Count number of 2's.
    while np.mod(n, 2) == 0:
        prime_str += "2"
        n = n / 2

        # Skip even numbers.  It's okay to test non-prime odds.
    i = 3
    while n != 1:
        while np.mod(n, i) == 0:
            prime_str += "%d" % i
            n = n / i
        i += 2

    return prime_str
