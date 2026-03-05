#include <iostream>
#include "mpi.h"

using namespace std;

int main(int argc, char **argv)
{ 
    int rangus;
	// Initialize MPI 
	MPI_Init(&argc, &argv); 	
	// pedir ranguito
    MPI_Comm_rank(MPI_COMM_WORLD, &rangus);
    if (rangus % 2 == 0)
    {
        cout << "Hallo Welt, von Rang :  " << rangus << endl; 
    }
    else
    {
        cout << "Bonjour le monde, du rang :  " << rangus << endl; 
    }
	// Finalise MPI 
	MPI_Finalize(); 
    // Finalise program
	return 0; 
}