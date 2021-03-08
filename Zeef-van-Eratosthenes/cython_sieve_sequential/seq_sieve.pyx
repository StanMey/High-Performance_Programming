cimport cython
import numpy as np
cimport numpy as np


def norm_sieve(int N) -> int:
    cdef int p, i, primes, x
    cdef np.ndarray sieve = np.full(N+1, 1, dtype=np.int8)

    p = 2
    primes = 0

    while (p * p <= N):

        # check if current number is prime
        if sieve[p]:

            # Update all multiples of p
            i = p * 2
            while i < N + 1:
                sieve[i] = 0
                i += p

        p += 1

    # set 0 and 1 to false
    sieve[0] = False
    sieve[1] = False

    # iterate over the whole list and count all the primes
    for x in range(N + 1):
        if sieve[x]:
            primes += 1

    return primes


def vect_sieve(int N) -> int:
    cdef int p, i, root_N, is_prime
    cdef np.ndarray sieve = np.full(N+1, 1, dtype=np.int8)
    p = 2

    root_N = int(N**0.5)
    for (i,), (is_prime) in np.ndenumerate(sieve[p:root_N+1]):
        p = i + 2
        if is_prime:
            sieve[p*2::p] = 0

    sieve[0:2] = 0
    return np.sum(sieve)
