import numpy as np
import time
import sys
import math

import pymp as omp
from mpi4py import MPI

# set all mpi related variables
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

local_sieve = list()
global_sieve = list()
local_primes = list()
n_begin, n_end = 0, 0

# use the master-worker pattern to distribute the workload
if rank == 0:

    # set the timer
    start_time = time.time()

    # get the amount of threads and N from the cmd
    N = int(sys.argv[1])

    # calculate all the ranges for which the algorithm still has to search for
    # primes
    ranges = list()
    n1 = 0
    delta = int(np.ceil(N / size))


    # get the ranges of the arrays to select
    for i in range(size):
        # correct for the exclusive range by adding 1 to n2
        n2 = min(n1 + delta, N)
        ranges.append((n1, n2))
        n1 = n2


    # let all the processes build their own initial local Sieves to eventually
    # filter out all the not primes
    for x in range(1, size):
        comm.send(("init", ranges[x]), dest=x)


    master_range = ranges[0]
    local_sieve = [True for i in range(master_range[0], master_range[1])]
    p = 2

    while (p * p <= N):

        # check if the current number is prime
        if local_sieve[p]:
            for x in range(1, size):
                comm.send(("filter", p), dest=x)

            # Update all multiples of p in own sieve
            for i in range(p * 2, len(local_sieve), p):
                local_sieve[i] = False

        p += 1


    # send the end signal to all processes to stop trying to receive a message
    # from the master and instead send their local sieve to the master
    for x in range(1, size):
        comm.send(("end", 1), dest=x)

    # set 0 and 1 to false
    local_sieve[0] = False
    local_sieve[1] = False

    #
    for k in range(len(local_sieve)):
        if local_sieve[k]:
            global_sieve.append(k)

    # collect all the other sieves
    for x in range(1, size):
        global_sieve += comm.recv(source=x)

    print(global_sieve)
    # print the time
    end_time = time.time()
    print("The function took {0} seconds".format(end_time - start_time))


else:
    # print("Thread {0} of {1} is waiting".format(rank, size))

    while True:
        data = comm.recv(source=0)

        if data[0] == "filter":
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
            print("Thread {0} is initialising".format(rank))
            n_begin = data[1][0]
            n_end = data[1][1]
            local_sieve = [True for i in range(n_begin, n_end + 1)]

        else:
            local_primes = list()
            for x in range(len(local_sieve)):
                if local_sieve[x]:
                    local_primes.append(x + n_begin)

            # send
            comm.send(local_primes, dest=0)
            break
