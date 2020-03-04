/* ompArraySum.c uses an array to sum the values in parallel in an input file,
 *  whose name is specified on the command-line.
 * Stan Meyberg, HU, HPP, 2020
 * Based on the source code by:
 * Huib Aldewereld, HU, HPP, 2020
 */

#include <stdio.h>      /* I/O stuff */
#include <stdlib.h>     /* calloc, etc. */
#include <omp.h>     // OpenMP

void readArray(char * fileName, double ** a, int * n);
double sumArray(double * a, int numValues, int Threads) ;

int main(int argc, char * argv[])
{
  int howMany;
  double sum;
  double * a;
  double start, end;
  int numThreads;

  if (argc != 3) {
    fprintf(stderr, "\n*** Usage: arraySum <inputFile> <numthreads>\n\n");
    exit(1);
  }

  readArray(argv[1], &a, &howMany);

  start = omp_get_wtime();  // getting the start start time

  numThreads = atoi(argv[2]);
  sum = sumArray(a, howMany, numThreads);

  end = omp_get_wtime();    // getting the end time
  printf("Elapsed time = %f sec\n", end - start);

  printf("The sum of the values in the input file '%s' is %g\n",
           argv[1], sum);

  free(a);

  return 0;
}

/* readArray fills an array with values from a file.
 * Receive: fileName, a char*,
 *          a, the address of a pointer to an array,
 *          n, the address of an int.
 * PRE: fileName contains N, followed by N double values.
 * POST: a points to a dynamically allocated array
 *        containing the N values from fileName
 *        and n == N.
 */

void readArray(char * fileName, double ** a, int * n) {
  int count, howMany;
  double * tempA;
  FILE * fin;

  fin = fopen(fileName, "r");
  if (fin == NULL) {
    fprintf(stderr, "\n*** Unable to open input file '%s'\n\n",
                     fileName);
    exit(1);
  }

  fscanf(fin, "%d", &howMany);
  tempA = calloc(howMany, sizeof(double));
  if (tempA == NULL) {
    fprintf(stderr, "\n*** Unable to allocate %d-length array",
                     howMany);
    exit(1);
  }

  for (count = 0; count < howMany; count++)
   fscanf(fin, "%lf", &tempA[count]);

  fclose(fin);

  *n = howMany;
  *a = tempA;
}

/* sumArray sums the values in an array of doubles in parallel.
 * Receive: a, a pointer to the head of an array;
 *          numValues, the number of values in the array.
 * Return: the sum of the values in the array.
 */

double sumArray(double * a, int numValues, int threads) {
  int i;
  double result = 0.0;

  omp_set_num_threads(threads);

  #pragma omp parallel for reduction(+:result)
  for (i = 0; i < numValues; i++) {
    result += a[i];
  }

  return result;
}
