import numpy as np
import time
import math

from mpi4py import MPI

# set all mpi related variables
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = 4
else:
    data = None

data = comm.bcast(data, root=0)
print(f"rank, {rank},{data}")
