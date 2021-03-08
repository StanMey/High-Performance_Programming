import time


def find_primes_sieve(N):
    """Finds all primes between 0 and N"""

    sieve = [True for i in range(N + 1)]
    p = 2
    primes = 0

    while (p * p <= N):

        # check if current number is prime
        if sieve[p]:

            # Update all multiples of p
            for i in range(p * 2, N + 1, p):
                sieve[i] = False
        p += 1

    # set 0 and 1 to false
    sieve[0] = False
    sieve[1] = False

    # iterate over the whole list and count all the primes
    for x in range(N + 1):
        if sieve[x]:
            primes += 1

    return primes


if __name__ == "__main__":
    start_time = time.time()

    # running the function with 10 million items
    n = 10000000
    find_primes_sieve(n)

    end_time = time.time()
    print("The algorithm took {0} seconds over {1} items".format(round(end_time - start_time, 3), n))
