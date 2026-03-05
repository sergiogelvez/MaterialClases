#include <iostream>
#include <cmath>
#include <omp.h>

using namespace std;

int main()
{
    int n = 100000;
    int i;
    double termino = 0.0;
    double suma = 0.0;

    int thread_num;

    thread_num = omp_get_max_threads ( );

    cout << "\n" ;
    cout << "  The number of processors available = " << omp_get_num_procs() << endl;
    cout << "  The number of threads available    = " << thread_num  << endl;

    #pragma omp parallel for reduction(+:suma)
    for (i = 0; i < n; i++)
    {
        termino = pow(-1.0,i) / ( 2*i + 1);
        // cout << termino << " ";
        suma = suma + termino;
    }
    cout << (suma * 4) << endl;
    cout << M_PI << endl;
}