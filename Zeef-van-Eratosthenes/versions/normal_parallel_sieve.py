import numpy as np
import time
import sys
import math

from mpi4py import MPI

# set all mpi related variables
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

local_sieve = list()
n_begin, n_end = 0, 0

# use the master-worker pattern to distribute the workload
if rank == 0:

    # set the timer
    start_time = time.time()

    # get the amount of threads and N from the cmd
    N = int(sys.argv[1])

    # Calculate the chunk size every process gets to balance the workload
    # over all processes
    ranges = list()
    n1 = 0
    delta = int(np.ceil(N / size))

    # get the ranges of the arrays to select
    for i in range(size):
        n2 = min(n1 + delta, N)
        ranges.append((n1, n2))
        n1 = n2


    # let all the processes build their own initial local Sieves to eventually
    # filter out all the not primes
    for x in range(1, size):
        comm.send(("init", ranges[x]), dest=x)

    # Let the master build its own local Sieve for finding the primes
    master_range = ranges[0]
    local_sieve = [True for i in range(master_range[0], master_range[1])]
    p = 2

    while (p * p <= N):

        # check if the current number is prime
        if local_sieve[p]:
            # send the prime number the master has found to all the other processes
            # so they can filter out the multiples of this prime number
            for x in range(1, size):
                comm.send(("filter", p), dest=x)

            # Update all multiples of p in own sieve
            for i in range(p * 2, len(local_sieve), p):
                local_sieve[i] = False
        # update p
        p += 1


    # send the end signal to all processes to stop trying to receive a message
    # from the master and instead send their local sieve to the master
    for x in range(1, size):
        comm.send(("end", 1), dest=x)

    # set 0 and 1 to false
    local_sieve[0] = False
    local_sieve[1] = False

    # count the amount of primes
    prime_count = sum(local_sieve)

    # collect all the other sieves and concatenate them into 'global_sieve'
    for x in range(1, size):
        prime_count += comm.recv(source=x)

    end_time = time.time()

    # print all the info
    # print(global_sieve)
    print("Primes: {0}\nThe function took {1} seconds".format(prime_count, end_time - start_time))


else:
    # the process is a worker process

    while True:
        # every process waits for the master to send them a new prime so that
        # every process can filter all the multiples out of their own
        # 'local_sieve'
        data = comm.recv(source=0)

        if data[0] == "filter":
            # When a process gets the filter command the process will filter
            # out all the multiples of the given prime out of their own
            # 'local_sieve', after which it will restart listening for a new
            # command from the master process
            index = 0
            p = data[1]
            for x in local_sieve:
                if (n_begin + index) % p == 0:
                    for i in range(index, len(local_sieve), p):
                        local_sieve[i] = False
                    break
                else:
                    index += 1

        elif data[0] == "init":
            # let the process initialise their 'local_sieve' with True values
            print("Thread {0} is initialising".format(rank))
            n_begin = data[1][0]
            n_end = data[1][1]
            local_sieve = [True for i in range(n_begin, n_end + 1)]

        else:
            # the master has no more numbers to be filtered to pass on so every process
            # now collects the amount of primes and returns the number
            prime_cnt = sum(local_sieve)

            # The count is send back to the master process and the while True
            # loop is escaped so that all other processes can stop.
            comm.send(prime_cnt, dest=0)
            break
