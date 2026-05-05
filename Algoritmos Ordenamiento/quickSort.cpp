#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

void imprimirVec(int vec[], int n)
{
    int i; 
    for (i = 0; i < n; i++)
    {
        cout << vec[i] << " ";
    }
}

int main()
{
    int i, j, t, n;
    cout << "Introduzca el número de elementos del vector: ";
    cin >> n;
    int A[n];
    srand(time(0));
    for (i = 0; i < n; i++)
    {
        A[i] = rand() % 100;
    }
    cout << "Vector original: \n"; 
    imprimirVec(A, n);
    cout << endl;
    // algoritmo quicksort

    
}