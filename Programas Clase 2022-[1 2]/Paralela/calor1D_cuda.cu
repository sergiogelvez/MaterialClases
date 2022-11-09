#include <iostream>
#include <cmath>

using namespace std;

typedef struct celdas
{
    int filas;
    int columnas;
    double *elementos;
}celdas;

#define M2V(f, c, nf, mc) (f * mc + c)

double Uinicial(int );
double UinicialVel(int );

__global__ void KernelPrincipal(double *elem, double C, int t, int n, int m, int nGPU)
{
    // falta poner lo de multiGPU
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (( i >= 1 ) && ( i < m - 1 ))
    {
        // ecuación principal.
        elem[(t + 1) * m + i] = elem[t * m + i] + C * (elem[t * m + (i+1)] - 2*elem[t * m + i] + elem[t * m + (i - 1)]); 
    }
    if (i == 0 && t == 0) printf("Mugre t0: %lf ", elem[0]);
}

void imprimirMatriz(double *elem, int n, int m)
{
    for (int t = 0; t < n; t++)
    {
        for (int i = 0; i < m; i ++)
        {
            cout << elem[ t*m + i ] << ' '; // a ceros, para una prueba inicial
        }
    cout << endl;
    }
}

int main(int argc, char *argv[])
{
    int n = 64; // número de filas
    int m = 64; // número de columnas
    // lo escribo así porque después mejoraré el código
    if (n*m > 4194304)
    {
        cout << "Matriz demasiado grande." << endl;
        return 1;
    }
    celdas U, d_U, V;
    U.columnas = m;
    U.filas = n;
    size_t memSize = n*m*sizeof(double);
    U.elementos = (double*)malloc(memSize);
    d_U.columnas = m;
    d_U.filas = n;
    cudaMalloc(&d_U.elementos,  memSize);
    V.columnas = m;
    V.filas = n;
    V.elementos = (double*)malloc(memSize);
    // condiciones iniciales y de frontera
    const double UbordeInicial = 100.0;
    const double UbordeFinal = 0.0;
    // propiedades físicas de la barra, acero
    const double k = 1;
    const double deltaT = 0.01; // cada décima de segundo 
    const double deltaX = 1; // la barra es m veces este valor
    const double C = ( k * deltaT ) / deltaX;
    // i, j, k para las dimensiones espaciales, t para el tiempo
    //  en este caso, i va con las x.
    for (int t = 0; t < n; t++)
    {
        for (int i = 0; i < m; i ++)
        {
            U.elementos[ t * m + i ] = 0.0; // a ceros, para una prueba inicial
        }
    }
    // condiciones iniciales y de frontera
    for (int i = 0; i < m; i ++)
    {
        U.elementos[ 0 * m + i ] = Uinicial(i);
    }
    for (int t = 0; t < n; t++)
    {
        U.elementos[ t * m + 0 ] = UbordeInicial;
        U.elementos[ t * m + (m - 1) ] = UbordeFinal;
    }
    cout << endl;
    imprimirMatriz(U.elementos, n, m);
    // copia a GPU
    cudaMemcpy(d_U.elementos, U.elementos, memSize, cudaMemcpyHostToDevice);
    // ciclo principal en cpu
    cout << "CPU:" << endl;
    int t, i;
    for (t = 0; t < n - 1; t++)
    {
        for (i = 1; i < m - 1; i++)
        {
            // ecuación principal.
            U.elementos[(t + 1) * m + i] = U.elementos[t * m + i] + C * (U.elementos[t * m + (i+1)] - 2*U.elementos[t * m + i] + U.elementos[t * m + (i - 1)]); 
        }
        // cout << "Paso de tiempo " << t << endl;
        cout << ".";
        //imprimirMatriz(U.elementos, n, m);
    }
    cout << endl;
    //imprimirMatriz(U.elementos, n, m);
    // ciclo principal en GPU
    cout << "GPU:" << endl;
    for (t = 0; t < n - 1; t++)
    {
        //la implementación de streams acá aparecerá en la medida en que se intercalen copias, o se divida en multiple GPU
        KernelPrincipal<<< n / 64, 64>>>(d_U.elementos, C, t, n, m, 1);
        cudaDeviceSynchronize();
        // cout << "Paso de tiempo " << t << '\n';
        cout << ".";
        if ( t == 0 )
        {
            cudaMemcpy(V.elementos, d_U.elementos, memSize, cudaMemcpyDeviceToHost);
            cout << "paso t = 0 \n";
            imprimirMatriz(V.elementos, n, m);
        }
    }
    cudaMemcpy( V.elementos, d_U.elementos, memSize, cudaMemcpyDeviceToHost);
    //imprimirMatriz(V.elementos, n, m);
    for (i = 0; i < m; i++)
    {
        cout << U.elementos[ (n - 1) * m + i ] << " " << V.elementos[ (n - 1) * m + i ] << " ";
    }
}

double Uinicial(int i)
{
    // esto para facilitar cambiar las condiciones iniciales en el futuro
    return 0.0;
}

double UinicialVel(int i)
{
    // esto para facilitar cambiar las condiciones iniciales en el futuro
    return 0.0;
}