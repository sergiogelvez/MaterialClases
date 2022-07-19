#include <iostream>
#include "mpi.h"

using namespace std;

int main(int argc, char **argv)
{ 
    int rangus, size;
	// Initialize MPI 
	MPI_Init(&argc, &argv); 	
	// pedir ranguito
    MPI_Comm_rank(MPI_COMM_WORLD, &rangus);
    // Pero necesitamos más que el rango, también el tamaño del comunicador
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if (rangus % 2 == 0)
    {
        cout << "Hallo Welt, von Rang :  " << rangus << ", Größe: " << size << endl; 
    }
    else
    {
        cout << "Bonjour le monde, du rang :  " << rangus << ", dimension: " << size << endl; 
    }
	// Finalise MPI 
	MPI_Finalize(); 
    // Finalise program
	return 0; 
}