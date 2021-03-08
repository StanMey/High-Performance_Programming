import time
from sys import argv

import numpy as np


def sieve(N):
    k = 2
    sieve = np.full(N, 1, dtype=np.int8) # 1 of 0
    root_N = int(N**0.5)
    for (i,), (is_prime) in np.ndenumerate(sieve[k:root_N+1]):
        k = i + 2
        if is_prime:
            sieve[k*2::k] = 0

    sieve[0:2] = 0
    return sieve.sum()


def main():
    # assert len(argv) > 1, "ERROR: Give me N"

    time0 = time.time()
    sieve(int(argv[1]))
    print(f"The function took {time.time() - time0} seconds")


if __name__ == "__main__":
    main()
