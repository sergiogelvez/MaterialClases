#include <iostream>
#include "mpi.h"

using namespace std;

int main(int argc, char **argv)
{ 

    int rank, size;
    srand(time(NULL));
    string message_s = "Il nome mio nessun sapra, nooo, nooo - "; 
    string message_r;

    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    string rango = to_string(rank);
    message_s = message_s + rango;



    if (rank == 0) {

        MPI_Probe(MPI_ANY_SOURCE, 10, MPI_COMM_WORLD, &status);
        cout << "Process " << rank << " obtained message status by probing it.\n";

        // Get the number of integers in the message probed
        int count;
        MPI_Get_count(&status, MPI_CHAR, &count);
        char buffdude[count];

        MPI_Recv(&buffdude, count, MPI_CHAR, MPI_ANY_SOURCE, 10, MPI_COMM_WORLD, &status);

        string gato(buffdude, count);

        std::cout << "Mensagge received is: " << gato << "\n"; 
    } else {
        MPI_Send(message_s.c_str(), message_s.size(), MPI_CHAR, 0, 10, MPI_COMM_WORLD); 
    } 
    MPI_Finalize(); 
    return 0;
    
}