/* circuitSatifiability.c solves the Circuit Satisfiability
 *  Problem using a brute-force sequential solution.
 *
 *   The particular circuit being tested is "wired" into the
 *   logic of function 'checkCircuit'. All combinations of
 *   inputs that satisfy the circuit are printed.
 *
 *   16-bit version by Michael J. Quinn, Sept 2002.
 *   Extended to 32 bits by Joel C. Adams, Sept 2013.
 *   Adapted for HU-HPP by Huib Aldewereld, 2020.
 */

#include <stdio.h>     // printf()
#include <limits.h>    // UINT_MAX
#include <mpi.h>       // MPI
#include <math.h>      // ceil()

int checkCircuit (int, long);

int main (int argc, char *argv[]) {
   const long REPS = UINT_MAX;  // loop variable (64 bits)
   int global_count = 0;        // number of solutions (reduced over all processes)
   int local_count = 0;         // number of solutions (counted per process)
   int id, numProcesses;        // process id and amount of processes
   int start, stop;             // gets the first and last iteration int

   // start the timer
   double startTime = 0.0, totalTime = 0.0;
   startTime = MPI_Wtime();

   // initialize the MPI code
   MPI_Init(&argc, &argv);
   MPI_Comm_rank(MPI_COMM_WORLD, &id);
   MPI_Comm_size(MPI_COMM_WORLD, &numProcesses);

   printf ("\nProcess %d is checking the circuit...\n", id);

   // find chunk size for part of processes
   int chunkSize1 = (int)ceil(((double)REPS) / numProcesses);
   int remainder = REPS % numProcesses;

   // When remainder is 0, we have equal-sized chunks for all processes.
   // When remainder is not zero and the process id  is lower than remainder,
   // we use the higher chunk size.
   if (remainder == 0 || (remainder != 0 && id < remainder)) {
     start = id * chunkSize1;
     stop = start + chunkSize1;
   } else {
     // chunk size to spread among rest of processes
     int chunkSize2 = chunkSize1 - 1;
     // decrease chunk size by one to spread out across remaining
     // processes whose id is >= remainder
     start = (remainder * chunkSize1) + (chunkSize2 * (id - remainder));
     stop = start + chunkSize2;
   }

   for (int i = start; i < stop; i++) {     // iterate through our range
       local_count += checkCircuit (id, i);
   }

   printf ("Process %d finished, with count: %d\n", id, local_count);
   //fflush (stdout);
   MPI_Barrier(MPI_COMM_WORLD);

   // reduce all the local counts into the total count
   MPI_Reduce(&local_count, &global_count, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

   MPI_Finalize();

   // Print the result
   if (id == 0) {
     totalTime = MPI_Wtime() - startTime;
     printf("\nThe whole process took place in %f seconds\n", totalTime);
     printf("A total of %d solutions were found.\n\n", global_count);
   }
   return 0;
}

/* EXTRACT_BIT is a macro that extracts the ith bit of number n.
 *
 * parameters: n, a number;
 *             i, the position of the bit we want to know.
 *
 * return: 1 if 'i'th bit of 'n' is 1; 0 otherwise
 */

#define EXTRACT_BIT(n,i) ( (n & (1<<i) ) ? 1 : 0)


/* checkCircuit() checks the circuit for a given input.
 * parameters: id, the id of the process checking;
 *             bits, the (long) rep. of the input being checked.
 *
 * output: the binary rep. of bits if the circuit outputs 1
 * return: 1 if the circuit outputs 1; 0 otherwise.
 */

#define SIZE 32

int checkCircuit (int id, long bits) {
   int v[SIZE];        /* Each element is one of the 32 bits */
   int i;

   for (i = 0; i < SIZE; i++) {
     v[i] = EXTRACT_BIT(bits,i);
   }

   if ( ( (v[0] || v[1]) && (!v[1] || !v[3]) && (v[2] || v[3])
       && (!v[3] || !v[4]) && (v[4] || !v[5])
       && (v[5] || !v[6]) && (v[5] || v[6])
       && (v[6] || !v[15]) && (v[7] || !v[8])
       && (!v[7] || !v[13]) && (v[8] || v[9])
       && (v[8] || !v[9]) && (!v[9] || !v[10])
       && (v[9] || v[11]) && (v[10] || v[11])
       && (v[12] || v[13]) && (v[13] || !v[14])
       && (v[14] || v[15]) )
       &&
          ( (v[16] || v[17]) && (!v[17] || !v[19]) && (v[18] || v[19])
       && (!v[19] || !v[20]) && (v[20] || !v[21])
       && (v[21] || !v[22]) && (v[21] || v[22])
       && (v[22] || !v[31]) && (v[23] || !v[24])
       && (!v[23] || !v[29]) && (v[24] || v[25])
       && (v[24] || !v[25]) && (!v[25] || !v[26])
       && (v[25] || v[27]) && (v[26] || v[27])
       && (v[28] || v[29]) && (v[29] || !v[30])
       && (v[30] || v[31]) ) )
   {
      printf ("%d) %d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d \n", id,
         v[31],v[30],v[29],v[28],v[27],v[26],v[25],v[24],v[23],v[22],
         v[21],v[20],v[19],v[18],v[17],v[16],v[15],v[14],v[13],v[12],
         v[11],v[10],v[9],v[8],v[7],v[6],v[5],v[4],v[3],v[2],v[1],v[0]);
      fflush (stdout);
      return 1;
   } else {
      return 0;
   }
}
