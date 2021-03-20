import numpy as np
import time
import math

from mpi4py import MPI
from concurrent.futures import ThreadPoolExecutor

# set all mpi related variables
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = np.arange(1, 11)
else:
    data = None

data = comm.bcast(data, root=0)

data = data * (rank + 1)

def f(x):
    data[x] = 0

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(f, range(2, len(data), 2))


print(f"rank {rank}:  {data}")
