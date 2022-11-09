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
    // algoritmo de ordenamiento por inserción
    i = 1;
    while (i < n)
    {
        t = A[i];
        j = i - 1;
        while (j >= 0 && A[j] > t)
        {
            cout << "(" << t << ") : ";
            A[j + 1] = A[j];
            j = j - 1;
            imprimirVec(A, n);
            cout << endl;
        }
        A[j + 1] = t;
        i = i + 1;
        cout << "(" << t << ") : ";
        imprimirVec(A, n);
        cout << endl;
    }
    cout << "Vector ordenado: \n";
    imprimirVec(A, n);


}



