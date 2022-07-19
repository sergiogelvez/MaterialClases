#include <iostream>
#include "mpi.h"

int main(int argc, char **argv) { 
    int rangus;
	// Initialize MPI 
	MPI_Init(&argc, &argv); 	
	// pedir ranguito
    MPI_Comm_rank(MPI_COMM_WORLD, &rangus);
	std::cout << "Hello World! from (parce que ich mag mezclar idiomas) rango:  " << rangus << std::endl; 
	
	// Finalize MPI 
	MPI_Finalize(); 
	
	return 0; 
}