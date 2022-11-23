#include <iostream>
#include <stdlib.h>
#include "mpi.h"


int main(int argc, char **argv)
{ 

    int rank, size;
    srand(time(NULL));
    int numberToSend = rand();
    int numberToReceive;

    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    if (rank == 0) {
        MPI_Recv(&numberToReceive, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        std::cout << "Number received is: " << numberToReceive << "\n"; 
    } else {
        MPI_Send(&numberToSend, 1, MPI_INT, 0, 10, MPI_COMM_WORLD); 
    } 
    MPI_Finalize(); 
    return 0;
    
}