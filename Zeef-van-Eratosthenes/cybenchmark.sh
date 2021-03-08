#!/bin/bash

echo "Running Benchmarks"
echo

echo "Normal python parallel sieve"
mpirun.mpich -n 4 python3 ./versions/normal_parallel_sieve.py $1

echo

echo "Vectorized python parallel sieve"
mpirun.mpich -n 4 python3 ./versions/vec_parallel_sieve.py $1

echo

echo "Sequential python sieve (van casper)"
python3 ./versions/casper_sieve.py $1

echo

# running cython files
cd cython_sieve_sequential
python3 timings.py $1
echo

echo "done"
