from __future__ import print_function

import time
import sys
from seq_sieve import norm_sieve, vect_sieve


def time_functions(N):
    s_time = time.time()
    prime_count = norm_sieve(N)
    print("Normal cython sieve\nPrimes: {0}\nThe function took {1} seconds\n".format(prime_count, time.time() - s_time))

    s_time = time.time()
    prime_count = vect_sieve(N)
    print("Vectorized cython sieve\nPrimes: {0}\nThe function took {1} seconds".format(prime_count, time.time() - s_time))


if __name__ == "__main__":
    N = int(sys.argv[1])
    time_functions(N)
