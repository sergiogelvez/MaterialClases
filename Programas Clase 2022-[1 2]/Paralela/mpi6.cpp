#include "mpi.h" 
#include <iostream> 
#include <stdlib.h> 

using namespace std; 

int main(int argc, char **argv)
{ 
	int numtasks, rank, dest, source, rc, count; 
	char *inmsg; 
    string outmsg = "Testing";
	// char *outmsg =  

    cout << "Parametros " << argc << endl;

	MPI_Status Stat; 

    int size_out = outmsg.size();

	int bufsize = outmsg.size() * sizeof(char); 
	char *buf = (char *)malloc(bufsize); 
	inmsg = (char *) malloc(10 * sizeof(char)); 

	MPI_Init(&argc, &argv); 
	MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
    if (rank == 0)
    { 
        MPI_Buffer_attach( buf, bufsize ); 
        int time = MPI_Wtime(); 
        MPI_Bsend(outmsg.c_str(), outmsg.size(), MPI_CHAR, 1, 1, MPI_COMM_WORLD); 
        float etime = MPI_Wtime() - time; 
        cout << "Tarea " << rank << " : Envio con buffer (1), el proceso se bloqueará al desprenderse. Tiempo: " << etime << "\n"; 
        MPI_Buffer_detach( &buf, &bufsize ); 
        time = MPI_Wtime(); 
        MPI_Send(outmsg.c_str(), outmsg.size(), MPI_CHAR, 1, 1, MPI_COMM_WORLD); 
        etime = MPI_Wtime() - time; 
        cout << "Task " << rank << ": envío normal (2), process may will block here. Time: " << etime << "\n"; 
    } 
    else
    { 
        MPI_Recv(&inmsg, size_out, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &Stat); 
        rc = MPI_Get_count(&Stat, MPI_CHAR, &count); 
        cout << "Task " << rank << ": Received " << count << " char(s) from task " << Stat.MPI_SOURCE << " with tag " << Stat.MPI_TAG << "\n";
        MPI_Recv(&inmsg, size_out, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &Stat); 
        rc = MPI_Get_count(&Stat, MPI_CHAR, &count); 
        cout << "Task " << rank << ": Received " << count << " char(s) from task " << Stat.MPI_SOURCE << " with tag " << Stat.MPI_TAG << "\n";
    } 
	MPI_Finalize(); 
}